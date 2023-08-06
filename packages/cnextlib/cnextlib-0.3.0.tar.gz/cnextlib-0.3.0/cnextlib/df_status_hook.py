import logging
from typing import Tuple, List
import simplejson as json

from .df_updates import DataFrameOp, DataFrameUpdate, UpdateType
from .libs.json_serializable import JsonSerializable

logging.basicConfig(filename='./cnextlib.log', filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(funcName)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.DEBUG)
log = logging.getLogger(__name__)


class DataFrameStatusItem(JsonSerializable):
    """ 
    DataFrameStatusItem stores info about the status of a single operation
    `type`, `name`, `id`: store the correspoding information of the dataframe
    `update: DataFrameUpdate`: store info about the update if any
    `op`: 
    `df_updated`: [Deprecated]
     """

    def __init__(self, name, id, df_type, update: DataFrameUpdate, op: DataFrameOp, line_number: int) -> None:
        self.type = df_type
        self.name = name
        self.id = id
        # self.df_updated = df_updated
        # TODO: find better way to handle None
        self.updates = update
        self.op = op
        self.line_number = line_number

    # def reset_status(self):
    #     self.df_updated = False
    #     self.updates = {}


class DataFrameStatus(JsonSerializable):
    """ 
    DataFrameStatus keeps track of the status of a dataframe which identified by `name` (not `id`)
    `_status_list`: store status info of each operation applied to this dataframe and it's effects
    `is_updated`: indicate where this data frame has been changed in the last code execution
    """

    def __init__(self):
        self._status_list: List[DataFrameStatusItem] = []
        self.is_updated: bool = False

    @property
    def status_list(self):
        return self._status_list

    @property
    def has_status(self):
        return len(self._status_list) > 0

    @property
    def last_status(self):
        if self.has_status:
            return self._status_list[-1]
        else:
            return None

    def reset_status(self):
        self.is_updated = False

    def add_status(self, is_updated: bool, status: DataFrameStatusItem):
        self._status_list.append(status)
        self.is_updated = is_updated


class DataFrameStatusDict(JsonSerializable, dict):
    pass

class DataFrameStatusHook:
    active_dfs_status = DataFrameStatusDict()
    # user_space: UserSpace = None
    running_line_number: int = 1
    TRACK_LINEAGE = True

    @classmethod
    def preset(cls, line_number: int = None, active_dfs_list: list = []):
        cls.update_all(active_dfs_list)
        if cls.TRACK_LINEAGE:
            cls.running_line_number = line_number

    # @classmethod
    # def set_running_line_number(cls, line_number: int):
    #     cls.update_new_dfs_status()
    #     cls.running_line_number = line_number

    # @classmethod
    # def set_user_space(cls, user_space: UserSpace):
    #     """ Setting up the space where the data frames are defined """
    #     cls.user_space = user_space
    
    @classmethod
    def update_new_dfs_status(cls, active_dfs_list: list=[]):
        """
        This function will update the status of new data frames. New data frames are the one that satisfies one of the following
        conditions:
            1. name is not in the current list
            2. name is in the current list but has new id
        It is hard to detect a new dataframe because it might be created without envoking any dataframe function, for example:
        `df = df1.loc[:]`. To reliably detect new data frame we insert function `preset()` in front of every code line and call this function inside `preset()`. 
        """

        # if cls.user_space == None:
        #     raise ValueError('user_space is not set')
        user_space_dfs = active_dfs_list #cls.user_space.get_active_dfs()
        # print(user_space_dfs)
        for name, df_id, df_type in user_space_dfs:
            if not name.startswith('_') and cls.is_new_df(name, df_id):
                if name not in cls.active_dfs_status:
                    cls.active_dfs_status[name] = DataFrameStatus()
                cls.active_dfs_status[name].add_status(True, DataFrameStatusItem(
                    name, df_id, df_type, DataFrameUpdate(UpdateType.new_df), DataFrameOp(), cls.running_line_number))

    @classmethod
    def is_new_df(cls, name, df_id) -> bool:
        """
        Check if the dataframe with name and df_id is a new dataframe.
        A dataframe is new if name is not in the active list or name is in the active list but df_id is new

        Args:
            clsf (_type_): _description_
            name (_type_): _description_
            df_id (_type_): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if name not in cls.active_dfs_status:
            return True
        else:
            if cls.active_dfs_status[name].last_status == None:
                log.error(
                    'Error: the last status is None for dataframe %s' % name)
                return True  # return True to enfoce create a new one #
            else:
                if df_id != cls.active_dfs_status[name].last_status.id:
                    return True
        return False

    @classmethod
    def remove_inactive_dfs_status(cls, active_dfs_list: list = []):
        # if cls.user_space == None:
        #     raise ValueError('user_space is not set')
        user_space_dfs = active_dfs_list #cls.user_space.get_active_dfs()

        new_active_dfs = []
        cur_active_dfs = []
        for name, df_id, df_type in user_space_dfs:
            new_active_dfs.append(name)

        ## have to have two for loops to avoid `RuntimeError: dictionary changed size during iteration` #
        for name in cls.active_dfs_status.keys():
            cur_active_dfs.append(name)

        for name in cur_active_dfs:
            if name not in new_active_dfs:
                cls.active_dfs_status.pop(name)

    @classmethod
    def reset_active_dfs_status(cls):
        for _, status in cls.active_dfs_status.items():
            status.reset_status()

    @classmethod
    def update_working_df_status(cls, df, df_update: DataFrameUpdate, df_op: DataFrameOp, active_dfs_list: list = []):
        """ 
        This is called within DataFrame to inform about the updates of the dataframe 
        """
        # if cls.user_space == None:
        #     raise ValueError('user_space is not set')
        user_space_dfs = active_dfs_list #cls.user_space.get_active_dfs()
        # print(df_update, df_op, id(df))
        log.info("Got status changed id=%s, type=%s, updates=%s" %
                 (id(df), type(df), df_update))
        
        ## create new_df here to handle situation where the new df is created in the middle of the execution #
        cls.update_new_dfs_status(user_space_dfs)

        for name, df_id, df_type in user_space_dfs:
            log.info('df_status_hood: %s %s' % (name, df_id))
            ## only track dataframe with name does not have '_' prefix #
            if not name.startswith('_') and df_id == id(df):
                # if cls.is_new_df(name, df_id):
                #     ## create new_df here to handle situation where the new df is created in the middle of the execution #
                #     if name not in cls.active_dfs_status:
                #         print('create first time', name, df_id)
                #         cls.active_dfs_status[name] = DataFrameStatus()
                #     cls.active_dfs_status[name].add_status(True, DataFrameStatusItem(
                #         name, df_id, df_type, True, DataFrameUpdate(UpdateType.new_df), DataFrameOp()))
                # else:
                if df_update.update_type != UpdateType.no_update:
                    cls.active_dfs_status[name].add_status(True, DataFrameStatusItem(
                        name, df_id, df_type, df_update, df_op, cls.running_line_number))
                else:
                    cls.active_dfs_status[name].add_status(False, DataFrameStatusItem(
                        name, df_id, df_type, df_update, df_op, cls.running_line_number))

    @classmethod
    def is_updated(cls) -> bool:
        for _, status in cls.active_dfs_status.items():
            if status.is_updated == True:
                return True
        return False

    @classmethod
    def update_all(cls, active_dfs_list: list = []):
        cls.remove_inactive_dfs_status(active_dfs_list)
        cls.update_new_dfs_status(active_dfs_list)

    @classmethod
    def get_active_dfs_status(cls, active_dfs_list: list = []) -> dict:
        cls.update_all(active_dfs_list)
        return cls.active_dfs_status
