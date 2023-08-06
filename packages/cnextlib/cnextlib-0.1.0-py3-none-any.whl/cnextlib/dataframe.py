import pandas as pd
import logging
import traceback
import inspect
import sys
from functools import wraps
import glob
from multipledispatch import dispatch
import pandas as pd
# from .df_status_hook import DataFrameStatusHook
from .user_space import UserSpace
from .df_updates import DataFrameOp, UpdateType, DataFrameUpdate

logging.basicConfig(filename='./cnextlib.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(funcName)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger(__name__)


class DataFrameTracker:
    class_variables = ['df', 'cached_df', 'wrapped_obj', 'cdf']
    # status_hook = DataFrameStatusHook
    user_space: UserSpace

    @classmethod
    def set_user_space(cls, user_space: UserSpace):
        """ Setting up the space where the data frames are defined """
        cls.user_space = user_space

    def cache_df(self, method_name):
        if method_name in self.cache_required_funcs:
            self.cached_df = self.df.copy()

    def _handle_col_updates(self, old_cols: list, new_cols: list) -> DataFrameUpdate:
        update = None
        added_cols = [x for x in old_cols | new_cols if x not in old_cols]
        del_cols = [x for x in old_cols | new_cols if x not in new_cols]
        if len(added_cols) > 0 and len(del_cols) > 0:
            log.error('Expect cols to be either added or deleted not both, got added_cols %s, del_cols %s' % (
                added_cols, del_cols))
        if len(added_cols) > 0:
            log.info('Columns added %s' % (added_cols))
            update = DataFrameUpdate(UpdateType.add_cols, added_cols)
        if len(del_cols) > 0:
            log.info('Columns deleted %s' % (del_cols))
            update = DataFrameUpdate(UpdateType.del_cols, del_cols)

        return update if update != None else DataFrameUpdate(UpdateType.no_update)

    def _handle_row_updates(self, old_index: int, new_index: int) -> DataFrameUpdate:
        """ This is called when the df length changed. 
            Since compare table operation is heavy, it will be optional. 
            If new length is smaller, then report the number of deleted rows. 
            - TODO: think about how to have more comprehensive check. 
            If new length is bigger, then report the number of added rows 
            and the location where the added rows started. 
            Optionally, also do table compare because insert """

        update = None
        added_rows = [x for x in old_index | new_index if x not in old_index]
        del_rows = [x for x in old_index | new_index if x not in new_index]
        if len(added_rows) > 0 and len(del_rows) > 0:
            log.error('Expect rows to be either added or deleted not both, got added_rows %s, del_rows %s'
                      % (added_rows, del_rows))
        if len(added_rows) > 0:
            log.info('Rows added: %s' % (added_rows))
            update = DataFrameUpdate(UpdateType.add_rows, added_rows)
        if len(del_rows) > 0:
            log.info('Rows deleted: %s' % (del_rows))
            update = DataFrameUpdate(UpdateType.del_rows, del_rows)

        return update if update != None else DataFrameUpdate(UpdateType.no_update)

    def _handle_cell_updates(self, compare) -> DataFrameUpdate:
        update = None
        columns = compare.columns.levels[0]
        other = 'other'
        index = compare.index
        updates_dict = {}
        for col in columns:
            updates_dict[col] = []
            for idx in index:
                if (not pd.isna(compare[col][other][idx])) or (not pd.isna(compare[col]['self'][idx])):
                    updates_dict[col].append(idx)
        update = DataFrameUpdate(UpdateType.update_cells, updates_dict)

        return update if update != None else DataFrameUpdate(UpdateType.no_update)

    def _handle_dataframe_transform(self, method_name) -> DataFrameUpdate:
        # print(type(self), method_name, self.df, self.cached_df)
        update = None
        if method_name in self.df_transform_funcs:
            old_cols = set(self.cached_df.columns)
            new_cols = set(self.df.columns)
            old_index = self.cached_df.index
            new_index = self.df.index
            log.info('Handle transform ops df.shape: %s, cached_df.shape: %s',
                     self.df.shape, self.cached_df.shape)
            if old_cols != new_cols:
                log.info('cols updated new_cols %s, old_cols %s' %
                         (new_cols, old_cols))
                update = self._handle_col_updates(old_cols, new_cols)
            # only compare len not compare the index directly because
            # we are only interested in whether rows has been added or deleted
            # we will handle index update as cell update case #
            elif old_index.shape[0] != new_index.shape[0]:
                log.info('rows updated new_len %s, old_len %s' %
                         (new_index.shape, old_index.shape))
                update = self._handle_row_updates(old_index, new_index)
            else:
                compare = self.df.compare(self.cached_df)
                if not compare.empty:
                    # log.info('cell updated %s'%(compare))
                    log.info('cell updated: updated columns = %s' %
                             (compare.columns.levels[0]))
                    update = self._handle_cell_updates(compare)

        return update if update != None else DataFrameUpdate(UpdateType.no_update)

    ##
    # Build APIs
    ##

    def _apply_method(self, method_name, *args, **kwargs):
        log.info('Run function %s on %s %s' % (method_name, args, kwargs))
        # print(type(self), method_name)

        df_func = getattr(self.wrapped_obj, method_name)

        if callable(df_func):
            # print(method_name, " func")
            # This hacky solution is to make sure the assigned item will be pd.DataFrame instead of its wrapper cd.DataFrame
            # which will help avoid having to hack into "__setitem__"
            # TODO: test this and check the case where the assigned item is a series. need to review the design and cover
            # other funtions #
            if method_name == "__setitem__":
                if isinstance(args[1], DataFrame):
                    args = (args[0], args[1].df)

            # cache df before running function
            self.cache_df(method_name)

            res = df_func(*args, **kwargs)

            # handle situation when df is transformed
            update = self._handle_dataframe_transform(method_name)

            if method_name in self.df_transform_funcs:
                self.user_space.update_working_df_status(
                    self.cdf, update, DataFrameOp(method_name, *args, **kwargs))

            original_class_name = type(res)
            if original_class_name == pd.DataFrame:
                return DataFrame(res)
            elif original_class_name in [pd.core.indexing._LocIndexer, pd.core.indexing._iLocIndexer, pd.core.indexing._AtIndexer]:
                wrapper_class = getattr(
                    sys.modules[__name__], original_class_name.__name__)
                return wrapper_class(res, self.cdf)
            else:
                return res
        else:
            log.error("Method %s is not callable" % df_func)
            # self.status_hook.update_working_df_status(
            #     self.cdf, DataFrameUpdate(UpdateType.no_update), DataFrameOp(method_name, *args, **kwargs))

    def _apply_property(self, property_name, *args, **kwargs):
        # log.info('Run %s on %s %s'%(property_name, args, kwargs))
        log.info('Run property %s' % (property_name))
        # print(type(self), property_name)

        self.cache_df(property_name)

        res = getattr(self.wrapped_obj, property_name)

        update = self._handle_dataframe_transform(property_name)

        if property_name in self.df_transform_funcs:
            self.user_space.update_working_df_status(
                self.cdf, update, DataFrameOp(property_name))

        original_class_name = type(res)
        if original_class_name == pd.DataFrame:
            return DataFrame(res)
        elif original_class_name in [pd.core.indexing._LocIndexer, pd.core.indexing._iLocIndexer, pd.core.indexing._AtIndexer]:
            wrapper_class = getattr(
                sys.modules[__name__], original_class_name.__name__)
            return wrapper_class(res, self.cdf)
        else:
            return res

    @classmethod
    def build_api(cls, method_names):
        def _make_wrapper(method_name):
            # @wraps(getattr(pd.DataFrame, method_name))
            def _wrapper(self, *args, **kwargs):
                return self._apply_method(method_name, *args, **kwargs)
            return _wrapper

        # TODO: currently everything is wrapped as a function, let's find away to avoid calling function for method like 'columns' or 'index'
        for method_name in method_names:
            setattr(cls, method_name, _make_wrapper(method_name))

    @classmethod
    def build_property(cls, property_names):
        def _make_wrapper(property_name):
            try:
                @property
                # @wraps(getattr(pd.DataFrame, property_name))
                def _wrapper(self, *args, **kwargs):
                    return self._apply_property(property_name, *args, **kwargs)
                return _wrapper
            except TypeError as error:
                raise error  # TODO: raise function not found here

        for property_name in property_names:
            setattr(cls, property_name, _make_wrapper(property_name))
            # cls.property_name = property(_make_wrapper(property_name))
            # print(cls.property)

    @classmethod
    def build_vars(cls):
        for var in cls.class_variables:
            setattr(DataFrame, var, None)

    ##
    # Basic functions
    ##
    def __repr__(self):
        return self.df.__repr__()

    ##
    # This function has to be defined to avoid a recursive call because this class inherit pd.DataFrame
    # Because of this, we also have to define class_variables and initiate it
    ##
    def __getattr__(self, name: str):
        try:
            pass
        except Exception as error:
            log.error("%s: %s - %s" % (name, error, traceback.format_exc()))
            raise FuncNotImplemented(name)

    # def __setattr__(self, name: str, value) -> None:
    #     return setattr(name, value)


class DataFrame(DataFrameTracker, pd.DataFrame):
    @dispatch(str)
    def __init__(self, path):
        log.info('Create a dataframe from a file')
        if glob.glob(path) == []:
            log.info("No path named %s" % path)
            raise Exception("No path named %s" % path)

        self.df = pd.read_csv(path, index_col=False)
        self.cached_df: pd.DataFrame = None
        self.wrapped_obj = self.df
        self.cdf = self

    @dispatch(pd.DataFrame)
    def __init__(self, df: pd.DataFrame):
        log.info('Create a dataframe from a pd.dataframe')
        self.df = df
        self.cached_df: pd.DataFrame = None
        self.wrapped_obj = self.df
        self.cdf = self


class _LocIndexer(DataFrameTracker, pd.core.indexing._LocIndexer):
    def __init__(self, indexer: pd.core.indexing._LocIndexer, cdf: DataFrame):
        self.df = indexer.obj
        self.cached_df: pd.DataFrame = None
        self.wrapped_obj = indexer
        self.cdf = cdf


class _iLocIndexer(DataFrameTracker, pd.core.indexing._iLocIndexer):
    def __init__(self, indexer: pd.core.indexing._iLocIndexer, cdf: DataFrame):
        self.df = indexer.obj
        self.cached_df: pd.DataFrame = None
        self.wrapped_obj = indexer
        self.cdf = cdf


class _AtIndexer(DataFrameTracker, pd.core.indexing._AtIndexer):
    def __init__(self, indexer: pd.core.indexing._AtIndexer, cdf: DataFrame):
        self.df = indexer.obj
        self.cached_df: pd.DataFrame = None
        self.wrapped_obj = indexer
        self.cdf = cdf


class FuncNotImplemented(Exception):
    def __init__(self, func_name):
        self.message = "Function %s is not implemented." % func_name
        super().__init__(self.message)


def initialize_wrapper_class(wrapper_class, original_class, additional_all_funcs, additional_transform_funcs):
    wrapper_class.build_vars()

    ## Create a list of all public pandas functions #
    wrapper_class.all_funcs = [attr for attr in dir(original_class) if callable(getattr(original_class, attr))
                               and attr.startswith('__') == False and attr.startswith('_') == False
                               ] + additional_all_funcs

    ## Create a list of functions that should be tracked i.e. every function that has the keyword 'inplace' in it #
    wrapper_class.df_transform_funcs = [attr for attr in wrapper_class.all_funcs if 'inplace' in inspect.signature(
        getattr(original_class, attr)).parameters.keys()] + additional_transform_funcs

    # TODO: since caching is potentially expensive, this list needs to be improved
    wrapper_class.cache_required_funcs = wrapper_class.df_transform_funcs

    wrapper_class.all_properties = [attr for attr in dir(original_class) if not callable(getattr(original_class, attr))
                                    and attr.startswith('__') == False and attr.startswith('_') == False
                                    ]

    # Build DataFrame functions and properties from pd DataFrame's ones
    wrapper_class.build_api(wrapper_class.all_funcs)
    wrapper_class.build_property(wrapper_class.all_properties)


initialize_wrapper_class(_LocIndexer, pd.core.indexing._LocIndexer, [
                         '__getitem__', '__setitem__'], ['__setitem__'])

initialize_wrapper_class(_iLocIndexer, pd.core.indexing._iLocIndexer, [
                         '__getitem__', '__setitem__'], ['__setitem__'])

initialize_wrapper_class(_AtIndexer, pd.core.indexing._AtIndexer, [
                         '__getitem__', '__setitem__'], ['__setitem__'])

initialize_wrapper_class(DataFrame, pd.DataFrame, [
                         '__getitem__', '__setitem__'], ['__setitem__'])
