import os
import sys
import logging
from typing import Tuple, List
from unittest import TestCase
# os.chdir('...')
# sys.path.append(os.getcwd());
import cnextlib.dataframe as cd
from ..df_updates import UpdateType
from ..user_space import UserSpace
import pandas as pd
from cnextlib.df_status_hook import DataFrameStatusHook


class MyUserSpace(UserSpace):
    def globals(self):
        return globals()


class TestDataFrame(TestCase):
    def setUp(self):
        DataFrameStatusHook.set_user_space(
            MyUserSpace([cd.DataFrame, pd.DataFrame]))
        DataFrameStatusHook.remove_inactive_dfs_status()
        DataFrameStatusHook.reset_active_dfs_status()

    def test_create_and_cleanup_df(self):
        data = [['tom', 10], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])
        global cdf
        cdf = cd.DataFrame(df)
        # print(cdf.status_hook)
        # print(MyUserSpace([cd.DataFrame]).get_globals())
        # print(globals())
        DataFrameStatusHook.update_new_dfs_status()
        # DataFrameStatusHook.update_potential_status()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # print("active dataframe: %s" % active_df_status)
        self.assertTrue('cdf' in active_df_status)
        last_status = active_df_status['cdf'].status_list[-1]
        self.assertTrue(last_status.name == 'cdf')
        self.assertTrue(last_status.id == id(cdf))
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.new_df)
        self.assertTrue(last_status.updates.update_content == [])
        DataFrameStatusHook.reset_active_dfs_status()
        # test clean up
        del cdf
        DataFrameStatusHook.remove_inactive_dfs_status()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # print("active dataframe: %s" % active_df_status)
        self.assertTrue(active_df_status == {})
        DataFrameStatusHook.reset_active_dfs_status()

    def test_is_updated(self):
        data = [['tom', 10], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])
        global cdf
        cdf = cd.DataFrame(df)
        # print()
        DataFrameStatusHook.update_new_dfs_status()
        self.assertTrue(DataFrameStatusHook.is_updated() == True)
        DataFrameStatusHook.reset_active_dfs_status()
        self.assertTrue(DataFrameStatusHook.is_updated() == False)

    def test_empty_df(self):
        DataFrameStatusHook.update_new_dfs_status()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # print("active dataframe: %s" % active_df_status)
        self.assertTrue(active_df_status == {})
        DataFrameStatusHook.reset_active_dfs_status()

    def test_get_new_df_status(self):
        data = [['tom', 10], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('cdf' not in globals())

        global cdf

        ## new data frame #
        df1 = cd.DataFrame(df)
        DataFrameStatusHook.update_new_dfs_status()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        last_status = active_df_status['cdf'].status_list[-1]
        self.assertTrue('df1' in active_df_status)
        self.assertTrue(last_status.name == 'cdf')
        self.assertTrue(last_status.id == id(cdf))
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.new_df)
        self.assertTrue(last_status.updates.update_content == [])
        DataFrameStatusHook.reset_active_dfs_status()

        ## exisitng data frame with new id #
        old_id = id(cdf)
        cdf = cd.DataFrame(df)
        DataFrameStatusHook.update_new_dfs_status()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # print("active dataframe: %s" % active_df_status)
        self.assertTrue('cdf' in active_df_status)
        self.assertTrue(last_status.name == 'cdf')
        self.assertTrue(last_status.id == id(cdf))
        self.assertTrue(last_status.id != old_id)
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.new_df)
        self.assertTrue(last_status.updates.update_content == [])
        DataFrameStatusHook.reset_active_dfs_status()

        # clean up
        del cdf
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_create_multiple_dfs(self):
        data = [['tom', 10], ['nick', 15], ['juli', 14]]
        df1 = pd.DataFrame(data, columns=['Name', 'Age'])
        df2 = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('cdf1' not in globals())
        self.assertTrue('cdf2' not in globals())

        global cdf1, cdf2

        ## create two data frames then update status #
        # cd.DataFrame(df1).loc[:, 'Name']
        cdf1 = cd.DataFrame(df1)
        cdf1 = cdf1.loc[:, ['Name']]
        # DataFrameStatusHook.get_new_dfs_status()
        # cdf2 = cdf1.loc[:,'Name']
        # cdf1 = cd.DataFrame(df1)
        # cdf2 = cd.DataFrame(df2)
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # print(active_df_status)
        # cdf1_last_status = active_df_status['cdf1'].last_status
        # cdf2_last_status = active_df_status['cdf2'].last_status
        # self.assertTrue(active_df_status['cdf1'].is_updated == True)
        # self.assertTrue(active_df_status['cdf2'].is_updated == True)
        # self.assertTrue(cdf1_last_status.df_updated == True)
        # self.assertTrue(cdf2_last_status.df_updated == True)
        # DataFrameStatusHook.reset_dfs_status()

        # ## create two data frames but update status in between #
        # cdf1 = cd.DataFrame(df1)
        # # DataFrameStatusHook.get_new_dfs_status()
        # DataFrameStatusHook.reset_dfs_status()
        # cdf2 = cd.DataFrame(df2)
        # # DataFrameStatusHook.get_new_dfs_status()
        # active_df_status = DataFrameStatusHook.get_active_df()
        # print(active_df_status)
        # self.assertTrue(active_df_status['cdf1'].is_updated == False)
        # self.assertTrue(active_df_status['cdf2'].is_updated == True)
        # self.assertTrue(cdf1_last_status.df_updated == True)
        # self.assertTrue(cdf2_last_status.df_updated == True)
        # DataFrameStatusHook.reset_dfs_status()

        # del cdf1, cdf2
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_drop_cols_df_status(self):
        data = [['tom', 10], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('cdf' not in globals())

        global cdf

        ## create a data frame then drop a columns#
        cdf = cd.DataFrame(df)
        cdf.drop('Age', axis=1, inplace=True)
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # print(active_df_status)
        last_status = active_df_status['cdf'].status_list[-1]
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.del_cols)
        self.assertTrue(
            last_status.updates.update_content == ["Age"])

        del cdf
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_fillna_df_status(self):
        data = [['tom', None], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('cdf' not in globals())

        global cdf

        ## create a data frame then drop a columns#
        cdf = cd.DataFrame(df)
        cdf[['Age']] = cdf[['Age']].fillna(method='bfill')
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()

        # print(cdf, active_df_status)
        last_status = active_df_status['cdf'].status_list[-1]
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.update_cells)
        self.assertTrue(
            last_status.updates.update_content == {"Age": [0]})

        del cdf
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_df_status_json(self):
        """
        Test two ways to create json string for active df status
        """
        data = [['tom', None], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('cdf' not in globals())

        global cdf

        ## create a data frame then drop a columns#
        cdf = cd.DataFrame(df)
        cdf[['Age']] = cdf[['Age']].fillna(method='bfill')
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()

        import simplejson as json

        json_str = json.dumps(
            active_df_status, default=lambda o: o.__dict__, ignore_nan=True)
        json_str = active_df_status.toJSON()
        
        del cdf
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_indexer_df_status(self):
        data = [['tom', None], [None, 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('cdf' not in globals())

        global cdf

        ## create a data frame then drop a columns#
        cdf = cd.DataFrame(df.copy())
        cdf.loc[:, ['Age']] = cdf.loc[:, ['Age']].fillna(method='bfill')
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        last_status = active_df_status['cdf'].status_list[-1]
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.update_cells)
        self.assertTrue(
            last_status.updates.update_content == {"Age": [0]})

        cdf = cd.DataFrame(df.copy())
        cdf.iloc[0:2, 0:2] = cdf.iloc[0:2, 0:2].fillna(
            value={'Name': 'Bach', 'Age': 100})
        # cdf.loc[df['Name'].isnull(), 'Name'] = 'Bach'
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        last_status = active_df_status['cdf'].status_list[-1]
        # print(cdf, active_df_status)
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.update_cells)
        self.assertTrue(
            last_status.updates.update_content == {"Name": [1], "Age": [0]})
        self.assertTrue(cdf.loc[1, 'Name'] == 'Bach')
        self.assertTrue(cdf.loc[0, 'Age'] == 100)

        cdf = cd.DataFrame(df.copy())
        cdf.at[1, 'Name'] = 'Bach'
        # cdf.loc[df['Name'].isnull(), 'Name'] = 'Bach'
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        last_status = active_df_status['cdf'].status_list[-1]
        # print(cdf, active_df_status)
        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.update_cells)
        self.assertTrue(
            last_status.updates.update_content == {"Name": [1]})
        self.assertTrue(cdf.at[1, 'Name'] == 'Bach')

        del cdf
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_pandas_df_status(self):
        data = [['tom', None], ['nick', 15], ['juli', 14]]
        global df
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        last_status = active_df_status['df'].status_list[-1]
        # print(active_df_status)

        self.assertTrue(last_status.df_updated == True)
        self.assertTrue(
            last_status.updates.update_type == UpdateType.new_df)
        self.assertTrue(
            last_status.type == str(pd.DataFrame))

        del df
        DataFrameStatusHook.remove_inactive_dfs_status()

    def test_df_lineage(self):
        script = """from inspect import getframeinfo, currentframe
DataFrameStatusHook.TRACK_LINEAGE = True                
data = [['tom', None], [None, 15], ['juli', 14]]
df = pd.DataFrame(data, columns=['Name', 'Age'])
global cdf
DataFrameStatusHook.preset(getframeinfo(currentframe()).lineno)
cdf = cd.DataFrame(df)
DataFrameStatusHook.preset(getframeinfo(currentframe()).lineno)
cdf.loc[:, ['Age']] = cdf.loc[:, ['Age']].fillna(method='bfill')
DataFrameStatusHook.preset(getframeinfo(currentframe()).lineno)
active_df_status = DataFrameStatusHook.get_active_df()
"""
        exec(script)
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        self.assertTrue(len(active_df_status['cdf'].status_list) == 2)
        df_status_list = active_df_status['cdf'].__dict__['_status_list']
        self.assertTrue(len(df_status_list) == 2)
        self.assertTrue(df_status_list[0].__dict__[
                        'updates'].__dict__['update_type'] == 'new_df')
        self.assertTrue(df_status_list[0].__dict__[
                        'op'].__dict__['name'] == '')
        self.assertTrue(df_status_list[1].__dict__[
                        'updates'].__dict__['update_type'] == 'update_cells')
        self.assertTrue(df_status_list[1].__dict__[
                        'op'].__dict__['name'] == '__setitem__')

    def test_playground(self):
        data = [['tom', None], ['nick', 15], ['juli', 14]]
        df = pd.DataFrame(data, columns=['Name', 'Age'])

        # check pre-condition
        self.assertTrue('df1' not in globals())

        global cdf, cdft

        ## create a data frame then drop a columns#
        cdf = cd.DataFrame(df)
        cdft = cdf.T
        # print(type(cdft))
        # cdf[['Age']] = cdf[['Age']].fillna(method='bfill')
        # cdf.loc[:,['Age']] = cdf.loc[:,['Age']].fillna(method='bfill')
        # cdf1 = cdf.loc[1:2,['Age']]
        # print(type(cdf1))
        # DataFrameStatusHook.review_potential_transform_df_status()
        DataFrameStatusHook.update_all()
        active_df_status = DataFrameStatusHook.get_active_dfs_status()
        # active_df_status = DataFrameStatusHook.get_active_df()
        # print(active_df_status)
        # self.assertTrue(last_status.df_updated==True)
        # self.assertTrue(last_status.updates.update_type==UpdateType.del_cols)
        # self.assertTrue(last_status.updates.update_content==["Age"])

        del cdf, cdft
        DataFrameStatusHook.remove_inactive_dfs_status()
