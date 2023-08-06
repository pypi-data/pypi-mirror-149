# df['copy'] = df['Engine Speed']
# df.drop('copy', 1, inplace=True)
# df.iloc[10]

# df[:30]
# df.iloc[4]

import sys, os
sys.path.append(os.getcwd()+'/../')

import pandas as pd
import cnextlib.dataframe as cd

df = pd.read_csv('tests/data/housing_data/small-data.csv')
# df.drop('Alley', 1, inplace=True)
# df['CopyStreet'] = df['Street']
# df[['LotFrontage']] = df[['LotFrontage']].fillna(method="ffill")
# df[:30]
# px.scatter(df, x="LotConfig", y="LandSlope")

# import importlib
# import mime_types

# from pandas.api.extensions import register_extension_dtype
# from pandas.core.arrays.string_ import FilePathMimeDtype
# from pandas.core.dtypes.dtypes import PandasExtensionDtype, CategoricalDtype, PandasDtype
# import numpy as np
# # from pandas._typing import type_t

# from pandas.core.arrays import PandasArray
# from pandas.core.arrays.base import ExtensionArray

# class FilePathMimeDtype(type):
#     pass





# @register_extension_dtype
# class FilePathMimeDtype(PandasExtensionDtype):
#     type = FilePathMimeDtype
#     # kind = 'S'
#     # str = '|S100'
#     name = 'application/filepath'

#     # @classmethod
#     def construct_array_type(cls):# -> type_t[FilePathMimeDtype]:
#         """
#         Return the array type associated with this dtype.
#         Returns
#         -------
#         type
#         """
#         from pandas.core.arrays.string_ import FileMimeArray

#         return FileMimeArray

    #     return FilePathMimeDtype
    # @property
    # def name(self) -> str:
    #     """
    #     A bit-width name for this data-type.
    #     """
    #     return self._dtype.name

    # @property
    # def type(self): # -> type[np.generic]:
    #     """
    #     The type object used to instantiate a scalar of this NumPy data-type.
    #     """
    #     return self._dtype.type

# print(df.columns)
# print(df['MSZoning'])
# from pandas.core.dtypes.base import _registry as registry
# print(registry.dtypes)
# print(registry.find(FilePathMimeDtype).name)
# print(registry.find('application/filepath'))
df['MSZoning'] = df['MSZoning'].astype('application/filepath')
print(df['MSZoning'].dtype)
df2 = cd.DataFrame(df)
df2.df.describe(include='all')
df2.df['MSZoning'].unique().tolist()
print(df.dtypes)
# print(df.dtypes)
# print(df['MSZoning'].astype('string'))
# print(df['MSZoning'].dtype)