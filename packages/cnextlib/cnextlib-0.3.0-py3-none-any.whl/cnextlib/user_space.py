from enum import Enum
import logging
from typing import Tuple, List

from cnextlib.df_updates import DataFrameOp, DataFrameUpdate
from cnextlib.libs.json_serializable import JsonSerializable
from .df_status_hook import DataFrameStatusHook

logging.basicConfig(filename='./cnextlib.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(funcName)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger(__name__)


class ExecutionMode(Enum):
    EVAL = 0
    EXEC = 1


class ModelInfoDict(JsonSerializable, dict):
    pass


class UserSpace:
    """
    Define the space where user code will be executed. 
    This is encapsulated in a python module so all the imports and variables are separated out from the rest.
    The code is executed on a kernel such as BaseKernel or IPythonKernel
    """

    def __init__(self, tracking_df_types: tuple = (), tracking_model_types: tuple = ()):
        """
        Args:
            df_types (list): a list of interested data frames types which can be either cycai.DataFrame or pandas.DataFrame
        """
        self.tracking_df_types = tracking_df_types
        self.tracking_model_types = tracking_model_types

    def globals(self):
        raise NotImplementedError('Abstract method not implemented.')

    @classmethod
    def fullname(cls, klass):
        module = klass.__module__
        if module == 'builtins':
            return klass.__qualname__
        return module + '.' + klass.__qualname__

    def get_active_dfs(self) -> List[Tuple[str, str, str]]:
        """
        Get a list of data frame with type in `df_types` from `user_space`

        Returns:
            list: list of data frame with the following information (name, id, type)
        """
        user_space = self.globals()
        names = list(user_space)
        df_list: List[Tuple[str, str, str]] = []

        if isinstance(names, list):
            for obj_name in names:
                obj_type = type(user_space[obj_name])
                if isinstance(user_space[obj_name], self.tracking_df_types):
                    # if obj_type in self.tracking_df_types:
                    df_list.append(
                        (obj_name, id(user_space[obj_name]), self.fullname(obj_type)))

        return df_list

    def get_active_models_info(self) -> ModelInfoDict:
        """
        Get a list of model with type in `model_types` from `user_space`

        Returns:
            list: list of data frame with the following information (name, id, type)
        """
        user_space = self.globals()
        names = list(user_space)
        model_dict = ModelInfoDict()  # List[Tuple[str, str, str]] = []
        if isinstance(names, list):
            for obj_name in names:
                obj_type = type(user_space[obj_name])
                for model_type in self.tracking_model_types:
                    if isinstance(user_space[obj_name], model_type):
                        # if obj_type in self.tracking_model_types or type(obj_type).__base__ in self.tracking_model_types:
                        model_dict[obj_name] = {'name': obj_name, 'id': id(
                            user_space[obj_name]), 'obj_class': self.fullname(obj_type), 'base_class': self.fullname(model_type)}

        return model_dict

    # @classmethod
    def update_working_df_status(self, df, df_update: DataFrameUpdate, df_op: DataFrameOp):
        DataFrameStatusHook.update_working_df_status(
            df, df_update, df_op, self.get_active_dfs())

    # @classmethod
    def get_active_dfs_status(self) -> dict:
        return DataFrameStatusHook.get_active_dfs_status(self.get_active_dfs())

    # @classmethod
    def reset_active_dfs_status(self):
        DataFrameStatusHook.reset_active_dfs_status()

    def execute(self, code, exec_mode: ExecutionMode = ExecutionMode.EVAL):
        raise NotImplementedError('Abstract method not implemented.')
