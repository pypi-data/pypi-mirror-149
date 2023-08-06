# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 08/03/2019
# Project Name: Toolkit Sanction 

''' Project Summary: This is a module that creates fake run results data data for the synthetic test data created '''

import pandas as pd
import random
import time
import math
import logging
from config import constants, params


class SanctionRunFaker:
    
    '''
    This class generates random fake run results for the synthetic data created before. 
    We need this functionality to create some dashboards based on the test data run results. 
    As we do not have a 3rd Party Sanction Screening Software ready currently, we created this simulation to generate test data run results.
    '''
    
    def __init__(self):
        
        '''
        This method is the constractor method that assignes the Class level variables.
        
        :param filepath: This is the path for the synthetic data file to create fake run results on it.
        :param outfilepath: This is the path for file to save the fake run results in it.
        :param error_depth: This is the parameter for ErrorDepth. It can be one of the 1/2/3
        
        :rtype: it has no return value

        '''
        
        print('-' * 80 + '\n')

        self.logger = logging.getLogger('Sanctions')
        self.logger.info('Fake sanction screening fake test results generation started.')



    def sanction_screen_fake(self, filepath = constants.SYNTHETIC_DATA_FILE_PATH, reflist_path = constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path = constants.SANCTION_RESULTS_FILE_PATH, error_depth = 0, sanction_mode = constants.SANCTION_MODE_GENERATE):


        '''
        This method creates the fake run results based on the selected fuzzy matching library.
        
        :param filepath: This is the path for the synthetic data file to create fake run results on it.
        :param reflist_path: This is the path for the reference list.
        :param sanctionresults_path: This is the path for the fake run results file.
        :param error_depth: This is the parameter for Error Depth

        :rtype: it has no return value

        '''

        print('\nSanction Screening for ErrorDepth' + str(error_depth) + ' started.')
        start_time = time.time()

        self.entries = pd.read_csv(filepath, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True) 
        
        if error_depth > 1:
            self.entries = self.entries.head(10000) ## just to eliminate the results, this must be removed in production

        self.reflist = pd.read_csv(reflist_path, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True) 


        self.entries = self.entries.fillna('')
        self.reflist = self.reflist.fillna('')

        self.entries['FullnameT'] = self.entries['Title'].astype(str) + ' ' + self.entries['Fullname'].astype(str) 
        self.reflist['FullnameT'] = self.reflist['Title'].astype(str) + ' ' + self.reflist['Fullname'].astype(str) 

        self.reflistkeys = self.reflist[['Id', 'GroupID', 'InitialId']]
        self.reflistkeys.columns = ['RefListId', 'RefListGroupID', 'RefListInitialId']

        df = link_table(self.entries, self.reflist, left_on = ['FullnameT'], right_on = ['FullnameT'], left_id_col = 'Id', right_id_col = 'Id' )
        df.columns = ['SyntheticDataId', 'HittedId', 'Match_Score', 'Match_Rank', 'Fullname_Original',	'Fullname_Variated']  
        df['HittedId'] = pd.to_numeric(df['HittedId'], downcast='integer' )
        df = df.round({'Match_Score': 3})        
    
        if error_depth == 1:
            df.to_csv(constants.SANCTION_RESULTS_RAW_FILE_PATH, sep='\t', index=False )
        elif error_depth == 2:
            df.to_csv(constants.SANCTION_RESULTS_RAW_FILE_PATH_D2, sep='\t', index=False )
        elif error_depth == 3:
            df.to_csv(constants.SANCTION_RESULTS_RAW_FILE_PATH_D3, sep='\t', index=False )

        dfresults = pd.merge(df, self.entries, how='left', left_on=['SyntheticDataId'], right_on = 'Id')   
        dfresults = dfresults[['SyntheticDataId', 'GroupID', 'InitialId', 'HittedId', 'Match_Score', 'Match_Rank', 'Fullname_Original', 'Fullname_Variated']]
        
        dfresults['HittedId'] = pd.to_numeric(dfresults['HittedId'], downcast='integer' )

        dfresults = pd.merge(dfresults, self.reflistkeys, how='left', left_on=['HittedId'], right_on = 'RefListId')   
        dfresults = dfresults.drop(['RefListId', 'Match_Rank'], axis=1)

        dfresults['SyntheticDataId'] = pd.to_numeric(dfresults['SyntheticDataId'], downcast='integer' )
        dfresults['InitialId'] = pd.to_numeric(dfresults['InitialId'], downcast='integer' )
        dfresults['HittedId'] = pd.to_numeric(dfresults['HittedId'], downcast='integer' )
        dfresults['RefListInitialId'] = pd.to_numeric(dfresults['RefListInitialId'], downcast='integer' )

        # dfresults = dfresults.drop_duplicates()

        dfresults.drop(dfresults[dfresults.Match_Score < 0].index, inplace=True)
        
        # these 2 lines is for eliminating the results
        dfresults.sort_values(['SyntheticDataId', 'Match_Score'], axis = 0, ascending = False, inplace = True, na_position ='last')
        dfresults = dfresults.groupby('SyntheticDataId').head(params.match_max_count).reset_index(drop=True)        


        dfresults['Hitted'] = 'N'        
        dfresults['HitType'] = ''        
        dfresults.loc[dfresults['HittedId'] > 0, 'Hitted'] = 'Y'        
        dfresults.loc[dfresults['Hitted'] == 'N', 'HitType'] = 'FN'        
        dfresults.loc[(dfresults.HittedId > 0) & (dfresults.GroupID == dfresults.RefListGroupID) , 'HitType'] = 'TP'        
        dfresults.loc[(dfresults.HittedId > 0) & ((dfresults.GroupID != dfresults.RefListGroupID) | (dfresults.Match_Score <= 0 )) , 'HitType'] = 'FP'        

        result_id = [i for i in range(1, len(dfresults) + 1 )]
        dfresults.insert(0, 'ResultId', result_id)

        dfresults.to_csv(sanctionresults_path, sep='\t', index=False )
        
        elapsed_time = time.time() - start_time
        print('Sanction Screening for ErrorDepth' + str(error_depth) + ' completed in ' + str(math.ceil(elapsed_time)) + ' secs.')


    def load_external_screen_results(self, filepath = constants.SYNTHETIC_DATA_FILE_PATH, reflist_path = constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path = constants.SANCTION_RESULTS_FILE_PATH, error_depth = 1):


        '''
        This method creates the fake run results based on the selected fuzzy matching library.
        
        :param filepath: This is the path for the synthetic data file to create fake run results on it.
        :param reflist_path: This is the path for the reference list.
        :param sanctionresults_path: This is the path for the fake run results file.
        :param error_depth: This is the parameter for Error Depth

        :rtype: it has no return value

        '''

        print('\nSanction Screening external result file loading started.')
        start_time = time.time()

        self.entries = pd.read_csv(filepath, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True) 
        self.reflist = pd.read_csv(reflist_path, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True) 

        self.entries = self.entries.fillna('')
        self.reflist = self.reflist.fillna('')

        self.entries['FullnameT'] = self.entries['Title'].astype(str) + ' ' + self.entries['Fullname'].astype(str) 
        self.reflist['FullnameT'] = self.reflist['Title'].astype(str) + ' ' + self.reflist['Fullname'].astype(str) 

        self.reflistkeys = self.reflist[['Id', 'GroupID', 'InitialId']]
        self.reflistkeys.columns = ['RefListId', 'RefListGroupID', 'RefListInitialId']

        if error_depth == 1:
            df = pd.read_csv(constants.SANCTION_RESULTS_RAW_FILE_PATH, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True)  
        elif error_depth == 2:
            df = pd.read_csv(constants.SANCTION_RESULTS_RAW_FILE_PATH_D2, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True)  
        elif error_depth == 3:
            df = pd.read_csv(constants.SANCTION_RESULTS_RAW_FILE_PATH_D3, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True)  

        df.columns = ['SyntheticDataId', 'HittedId', 'Match_Score', 'Match_Rank', 'Fullname_Original',	'Fullname_Variated']  
        df['HittedId'] = pd.to_numeric(df['HittedId'], downcast='integer' )
        df = df.round({'Match_Score': 3})        


        dfresults = pd.merge(df, self.entries, how='left', left_on=['SyntheticDataId'], right_on = 'Id')   
        dfresults = dfresults[['SyntheticDataId', 'GroupID', 'InitialId', 'HittedId', 'Match_Score', 'Match_Rank', 'Fullname_Original', 'Fullname_Variated']]
        
        dfresults['HittedId'] = pd.to_numeric(dfresults['HittedId'], downcast='integer' )

        dfresults = pd.merge(dfresults, self.reflistkeys, how='left', left_on=['HittedId'], right_on = 'RefListId')   
        dfresults = dfresults.drop(['RefListId', 'Match_Rank'], axis=1)

        dfresults['SyntheticDataId'] = pd.to_numeric(dfresults['SyntheticDataId'], downcast='integer' )
        dfresults['InitialId'] = pd.to_numeric(dfresults['InitialId'], downcast='integer' )
        dfresults['HittedId'] = pd.to_numeric(dfresults['HittedId'], downcast='integer' )
        dfresults['RefListInitialId'] = pd.to_numeric(dfresults['RefListInitialId'], downcast='integer' )

        # dfresults = dfresults.drop_duplicates()

        dfresults.drop(dfresults[dfresults.Match_Score < 0].index, inplace=True)
        
        # these 2 lines is for eliminating the results
        dfresults.sort_values(['SyntheticDataId', 'Match_Score'], axis = 0, ascending = False, inplace = True, na_position ='last')
        dfresults = dfresults.groupby('SyntheticDataId').head(params.match_max_count).reset_index(drop=True)        

        dfresults['Hitted'] = 'N'        
        dfresults['HitType'] = ''        
        dfresults.loc[dfresults['HittedId'] > 0, 'Hitted'] = 'Y'        
        dfresults.loc[dfresults['Hitted'] == 'N', 'HitType'] = 'FN'        
        dfresults.loc[(dfresults.HittedId > 0) & (dfresults.GroupID == dfresults.RefListGroupID) , 'HitType'] = 'TP'        
        dfresults.loc[(dfresults.HittedId > 0) & ((dfresults.GroupID != dfresults.RefListGroupID) | (dfresults.Match_Score <= 0 )) , 'HitType'] = 'FP'        
        # dfresults.loc[(dfresults.HittedId > 0) & (dfresults.HitType == 'TP') & (dfresults.InitialId != dfresults.RefListInitialId ) , 'HitType'] = 'T2P'        

        result_id = [i for i in range(1, len(dfresults) + 1 )]
        dfresults.insert(0, 'ResultId', result_id)

        dfresults.to_csv(sanctionresults_path, sep='\t', index=False )
        
        elapsed_time = time.time() - start_time
        print('Sanction Screening external result file loading completed in ' + str(math.ceil(elapsed_time)) + ' secs.')

        