from __future__ import annotations
from enum import Enum

from typing import (
    TYPE_CHECKING,
    Any,
)

import numpy as np

from pandas._config import get_option

from pandas._libs import (
    lib,
    missing as libmissing,
)
from pandas._libs.arrays import NDArrayBacked
from pandas._typing import (
    Dtype,
    Scalar,
)
from pandas.compat import pa_version_under1p0
from pandas.compat.numpy import function as nv

from pandas.core.dtypes.base import (
    ExtensionDtype,
    register_extension_dtype,
)
from pandas.core.dtypes.common import (
    is_array_like,
    is_bool_dtype,
    is_dtype_equal,
    is_integer_dtype,
    is_object_dtype,
    is_string_dtype,
    pandas_dtype,
)

from pandas.core import ops
from pandas.core.array_algos import masked_reductions
from pandas.core.arrays import (
    FloatingArray,
    IntegerArray,
    PandasArray,
)
from pandas.core.arrays.base import ExtensionArray
from pandas.core.arrays.floating import FloatingDtype
from pandas.core.arrays.integer import _IntegerDtype
from pandas.core.construction import extract_array
from pandas.core.indexers import check_array_indexer
from pandas.core.missing import isna

if TYPE_CHECKING:
    import pyarrow

from pandas.api.extensions import register_extension_dtype
from pandas.core.dtypes.dtypes import PandasExtensionDtype
from pandas.core.arrays import PandasArray
from pandas.core.arrays.base import ExtensionArray


class CnextMimeType(str, Enum):
    FILE_PNG = 'file/png'
    FILE_JPG = 'file/jpg'
    FILE_JPEG = 'file/jpeg'
    IMAGE_PNG = 'image/png'
    IMAGE_JPG = 'image/jpg'
    IMAGE_JPEG = 'image/jpeg'
    URL_PNG = 'url/png'
    URL_JPG = 'url/jpg'
    URL_JPEG = 'url/jpeg'

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

# Bach addeded this by copy from String type and remove the storage param in init#


class MimeDtypeType(type):
    pass


@register_extension_dtype
class FileMimeDtype(ExtensionDtype):
    type = MimeDtypeType
    name = CnextMimeType.FILE_PNG

    na_value = libmissing.NA
    _metadata = ("storage",)

    def __init__(self, storage=None):
        if storage is None:
            storage = get_option("mode.string_storage")
        if storage not in {"python", "pyarrow"}:
            raise ValueError(
                f"Storage must be 'python' or 'pyarrow'. Got {storage} instead."
            )
        if storage == "pyarrow" and pa_version_under1p0:
            raise ImportError(
                "pyarrow>=1.0.0 is required for PyArrow backed StringArray."
            )

        self.storage = storage

    # @classmethod
    def construct_array_type(cls):  # -> type_t[FilePathMimeDtype]:
        """
        Return the array type associated with this dtype.
        Returns
        -------
        type
        """
        # from pandas.core.arrays.string_ import FileMimeArray

        return FileMimeArray

    def __hash__(self) -> int:
        # custom __eq__ so have to override __hash__
        return super().__hash__()


class BaseFileMimeArray(ExtensionArray):
    pass


class FileMimeArray(BaseFileMimeArray, PandasArray):
    dtype_class = FileMimeDtype
    # undo the PandasArray hack
    _typ = "extension"

    def __init__(self, values, copy=False):
        values = extract_array(values)

        super().__init__(values, copy=copy)
        # error: Incompatible types in assignment (expression has type "FilePathMimeDtype",
        # variable has type "PandasDtype")
        NDArrayBacked.__init__(self, self._ndarray,
                               self.dtype_class(storage="python"))
        if not isinstance(values, type(self)):
            self._validate()

    def _validate(self):
        """Validate that we only store NA or strings."""
        if len(self._ndarray) and not lib.is_string_array(self._ndarray, skipna=True):
            raise ValueError(
                "FileMimeArray requires a sequence of strings or pandas.NA")
        if self._ndarray.dtype != "object":
            raise ValueError(
                "FileMimeArray requires a sequence of strings or pandas.NA. Got "
                f"'{self._ndarray.dtype}' dtype instead."
            )

    @classmethod
    def _from_sequence(cls, scalars, *, dtype: Dtype | None = None, copy=False):
        if dtype and not (isinstance(dtype, str) and dtype == "string"):
            dtype = pandas_dtype(dtype)
            # assert isinstance(dtype, FilePathMimeDtype) and dtype.storage == "python"

        from pandas.core.arrays.masked import BaseMaskedArray

        if isinstance(scalars, BaseMaskedArray):
            # avoid costly conversion to object dtype
            na_values = scalars._mask
            result = scalars._data
            result = lib.ensure_string_array(
                result, copy=copy, convert_na_value=False)
            result[na_values] = FileMimeDtype.na_value

        else:
            # convert non-na-likes to str, and nan-likes to FilePathMimeDtype.na_value
            result = lib.ensure_string_array(
                scalars, na_value=FileMimeDtype.na_value, copy=copy
            )

        # Manually creating new array avoids the validation step in the __init__, so is
        # faster. Refactor need for validation?
        new_string_array = cls.__new__(cls)
        NDArrayBacked.__init__(new_string_array, result, FileMimeDtype())

        return new_string_array

    @classmethod
    def _from_sequence_of_strings(
        cls, strings, *, dtype: Dtype | None = None, copy=False
    ):
        return cls._from_sequence(strings, dtype=dtype, copy=copy)

    @classmethod
    def _empty(cls, shape, dtype) -> FileMimeArray:
        values = np.empty(shape, dtype=object)
        values[:] = libmissing.NA
        return cls(values).astype(dtype, copy=False)

    def __arrow_array__(self, type=None):
        """
        Convert myself into a pyarrow Array.
        """
        import pyarrow as pa

        if type is None:
            type = pa.string()

        values = self._ndarray.copy()
        values[self.isna()] = None
        return pa.array(values, type=type, from_pandas=True)

    def _values_for_factorize(self):
        arr = self._ndarray.copy()
        mask = self.isna()
        arr[mask] = -1
        return arr, -1

    def __setitem__(self, key, value):
        value = extract_array(value, extract_numpy=True)
        if isinstance(value, type(self)):
            # extract_array doesn't extract PandasArray subclasses
            value = value._ndarray

        key = check_array_indexer(self, key)
        scalar_key = lib.is_scalar(key)
        scalar_value = lib.is_scalar(value)
        if scalar_key and not scalar_value:
            raise ValueError("setting an array element with a sequence.")

        # validate new items
        if scalar_value:
            if isna(value):
                value = FileMimeDtype.na_value
            elif not isinstance(value, str):
                raise ValueError(
                    f"Cannot set non-string value '{value}' into a FileMimeArray."
                )
        else:
            if not is_array_like(value):
                value = np.asarray(value, dtype=object)
            if len(value) and not lib.is_string_array(value, skipna=True):
                raise ValueError("Must provide strings.")

        super().__setitem__(key, value)

    def astype(self, dtype, copy=True):
        dtype = pandas_dtype(dtype)

        if is_dtype_equal(dtype, self.dtype):
            if copy:
                return self.copy()
            return self

        elif isinstance(dtype, _IntegerDtype):
            arr = self._ndarray.copy()
            mask = self.isna()
            arr[mask] = 0
            values = arr.astype(dtype.numpy_dtype)
            return IntegerArray(values, mask, copy=False)
        elif isinstance(dtype, FloatingDtype):
            arr = self.copy()
            mask = self.isna()
            arr[mask] = "0"
            values = arr.astype(dtype.numpy_dtype)
            return FloatingArray(values, mask, copy=False)
        elif isinstance(dtype, ExtensionDtype):
            cls = dtype.construct_array_type()
            return cls._from_sequence(self, dtype=dtype, copy=copy)
        elif np.issubdtype(dtype, np.floating):
            arr = self._ndarray.copy()
            mask = self.isna()
            arr[mask] = 0
            values = arr.astype(dtype)
            values[mask] = np.nan
            return values

        return super().astype(dtype, copy)

    def _reduce(self, name: str, *, skipna: bool = True, **kwargs):
        if name in ["min", "max"]:
            return getattr(self, name)(skipna=skipna)

        raise TypeError(f"Cannot perform reduction '{name}' with string dtype")

    def min(self, axis=None, skipna: bool = True, **kwargs) -> Scalar:
        nv.validate_min((), kwargs)
        result = masked_reductions.min(
            values=self.to_numpy(), mask=self.isna(), skipna=skipna
        )
        return self._wrap_reduction_result(axis, result)

    def max(self, axis=None, skipna: bool = True, **kwargs) -> Scalar:
        nv.validate_max((), kwargs)
        result = masked_reductions.max(
            values=self.to_numpy(), mask=self.isna(), skipna=skipna
        )
        return self._wrap_reduction_result(axis, result)

    def value_counts(self, dropna: bool = True):
        from pandas import value_counts

        return value_counts(self._ndarray, dropna=dropna).astype("Int64")

    def memory_usage(self, deep: bool = False) -> int:
        result = self._ndarray.nbytes
        if deep:
            return result + lib.memory_usage_of_objects(self._ndarray)
        return result

    def _cmp_method(self, other, op):
        from pandas.arrays import BooleanArray

        if isinstance(other, FileMimeArray):
            other = other._ndarray

        mask = isna(self) | isna(other)
        valid = ~mask

        if not lib.is_scalar(other):
            if len(other) != len(self):
                # prevent improper broadcasting when other is 2D
                raise ValueError(
                    f"Lengths of operands do not match: {len(self)} != {len(other)}"
                )

            other = np.asarray(other)
            other = other[valid]

        if op.__name__ in ops.ARITHMETIC_BINOPS:
            result = np.empty_like(self._ndarray, dtype="object")
            result[mask] = FileMimeDtype.na_value
            result[valid] = op(self._ndarray[valid], other)
            return self.dtype_class(result)
        else:
            # logical
            result = np.zeros(len(self._ndarray), dtype="bool")
            result[valid] = op(self._ndarray[valid], other)
            return BooleanArray(result, mask)

    _arith_method = _cmp_method

    # ------------------------------------------------------------------------
    # String methods interface
    _str_na_value = FileMimeDtype.na_value

    def _str_map(
        self, f, na_value=None, dtype: Dtype | None = None, convert: bool = True
    ):
        from pandas.arrays import BooleanArray

        if dtype is None:
            dtype = FileMimeDtype(storage="python")
        if na_value is None:
            na_value = self.dtype.na_value

        mask = isna(self)
        arr = np.asarray(self)

        if is_integer_dtype(dtype) or is_bool_dtype(dtype):
            constructor: type[IntegerArray] | type[BooleanArray]
            if is_integer_dtype(dtype):
                constructor = IntegerArray
            else:
                constructor = BooleanArray

            na_value_is_na = isna(na_value)
            if na_value_is_na:
                na_value = 1
            result = lib.map_infer_mask(
                arr,
                f,
                mask.view("uint8"),
                convert=False,
                na_value=na_value,
                # error: Value of type variable "_DTypeScalar" of "dtype" cannot be
                # "object"
                # error: Argument 1 to "dtype" has incompatible type
                # "Union[ExtensionDtype, str, dtype[Any], Type[object]]"; expected
                # "Type[object]"
                dtype=np.dtype(dtype),  # type: ignore[type-var,arg-type]
            )

            if not na_value_is_na:
                mask[:] = False

            return constructor(result, mask)

        elif is_string_dtype(dtype) and not is_object_dtype(dtype):
            # i.e. FilePathMimeDtype
            result = lib.map_infer_mask(
                arr, f, mask.view("uint8"), convert=False, na_value=na_value
            )
            return self.dtype_class(result)
        else:
            # This is when the result type is object. We reach this when
            # -> We know the result type is truly object (e.g. .encode returns bytes
            #    or .findall returns a list).
            # -> We don't know the result type. E.g. `.get` can return anything.
            return lib.map_infer_mask(arr, f, mask.view("uint8"))

    def tolist(self) -> list[Scalar]:
        """
        Return a list of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period)
        """
        return list(self)


@register_extension_dtype
class URLMimeDtype(FileMimeDtype):
    name = CnextMimeType.URL_PNG

    # @classmethod
    def construct_array_type(cls):
        """
        Return the array type associated with this dtype.
        Returns
        -------
        type
        """
        return URLMimeArray


class URLMimeArray(FileMimeArray):
    dtype_class = URLMimeDtype
