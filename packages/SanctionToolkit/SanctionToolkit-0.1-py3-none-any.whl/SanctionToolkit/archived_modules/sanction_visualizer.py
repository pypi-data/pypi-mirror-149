# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 15/04/2019
# Project Name: Toolkit Sanction 

''' Module Summary: This module is used for visualizing the synthetic data.'''

# import re
import pandas as pd
import time
import math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from pandas import DataFrame
import logging

from sanction_utility import SanctionUtility
from config import constants, params


class SanctionVisualizer:
    
    '''
    This class is used for visualizing the synthetic data.
    '''

    def __init__(self):
        
        '''
        This is the constructor method of the class.
        '''

        print('-' * 80 + '\n')
        self.logger = logging.getLogger('Sanctions')
        self.logger.info('Data visualisations started.\n\n')


    
    def visualize_data(self, infilepath = constants.SANCTIONLIST_FILE_PATH, error_depth = 1):
        
        '''
        This method creates the dashboards and visuals based on initial reference list, stsnthetic data generated aand the fake test run results from pseudo-Sanction Screening Module of the tool.
        
        :param infilepath: This is the path for the reference list - sanction list from the web.
        
        :rtype: it has no return value

        '''        
        
        print('\nVisualisations for ErrorDepth' + str(error_depth) + ' started.')
        start_time = time.time()

        if params.skip_visualisations == True:
            print('\nThe sanction list visualisations will be skipped as parameter selected.')
            # return
        
        if error_depth ==1:
            datafilepath = constants.SYNTHETIC_DATA_FILE_PATH
            resultsfilepath = constants.SANCTION_RESULTS_FILE_PATH
            results_visuals_save_path = constants.VISUALS_RUN_RESULTS_FILE_PATH
            results_vname_nohit_path = constants.VISUALS_RESULTS_VNAME_NOHIT_PATH
            results_vname_hittype_path_h = constants.VISUALS_RESULTS_VNAME_HITTYPE_H_PATH
            results_vname_hittype_path_v = constants.VISUALS_RESULTS_VNAME_HITTYPE_V_PATH
        elif error_depth ==2:     
            datafilepath = constants.SYNTHETIC_DATA_FILE_PATH_D2
            resultsfilepath = constants.SANCTION_RESULTS_FILE_PATH_D2
            results_visuals_save_path = constants.VISUALS_RUN_RESULTS_FILE_PATH2
            results_vname_nohit_path = constants.VISUALS_RESULTS_VNAME_NOHIT_PATH2
            results_vname_hittype_path_h = constants.VISUALS_RESULTS_VNAME_HITTYPE_H_PATH2
            results_vname_hittype_path_v = constants.VISUALS_RESULTS_VNAME_HITTYPE_V_PATH2
        elif error_depth ==3:     
            datafilepath = constants.SYNTHETIC_DATA_FILE_PATH_D3
            resultsfilepath = constants.SANCTION_RESULTS_FILE_PATH_D3
            results_visuals_save_path = constants.VISUALS_RUN_RESULTS_FILE_PATH3
            results_vname_nohit_path = constants.VISUALS_RESULTS_VNAME_NOHIT_PATH3
            results_vname_hittype_path_h = constants.VISUALS_RESULTS_VNAME_HITTYPE_H_PATH3
            results_vname_hittype_path_v = constants.VISUALS_RESULTS_VNAME_HITTYPE_V_PATH3


        # graph1: initial list size, pre-processed entries count, pre-processed unique initial id count
        
        dfdata = pd.read_csv(datafilepath, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True) 
        dfvariation = SanctionUtility.get_variation_list_group()
        dfresult = pd.read_csv(resultsfilepath, engine='python', delimiter = '\t') 
        dfsanction = pd.read_csv(infilepath, skiprows=[0], engine='python', encoding = 'cp1252')

        dfresultHit = dfresult[dfresult['Hitted'] == 'Y']
        dfresultNoHit = dfresult[dfresult['Hitted'] == 'N']

        dfresultHitSame = dfresultHit[dfresultHit['HitType'] == 'TP']             
        dfresultHitNotSame = dfresultHit[dfresultHit['HitType'] == 'FP']             

        dfsanction.rename(columns=lambda x: x.replace(' ', ''), inplace=True)
        dfsanction.rename(columns=lambda x: x.replace('GroupType', 'Entity_Type'), inplace=True)

        sanction_list_size = len(dfsanction)
        
        dfprocessed = pd.read_csv(constants.LIST_FILE_PATH_PROCESSED, engine='python', delimiter = '\t')
        processed_list_size = dfprocessed['InitialId'].count()
        processed_list_unique_size = dfprocessed['InitialId'].nunique()

        dfsampled = pd.read_csv(constants.PROFILED_SAMPLED_FILE_PATH, engine='python', delimiter = '\t')
        sampled_list_size = dfsampled['Id'].count()
        sampled_list_unique_size = dfsampled['InitialId'].nunique()

        total_data_generated = len(dfdata) 

        self.logger.info('-' * 80 + '\n')

        self.logger.info('DATA GENERATION STATISTICS:')
        self.logger.info('HMT Sanctions List (Reference List) size = {0}'.format(sanction_list_size))
        self.logger.info('Reference List size after pre-process(cleansing) = {0}'.format(processed_list_size))
        self.logger.info('Sampled List size = {0}'.format(sampled_list_size))
        self.logger.info('Total Data Generated by Variations (Error Depth1) = {0}'.format(total_data_generated))
        

        x = ['HMT List', 'HMT Cleansed', 'Sampled List', 'Synthetic Data']
        y = [sanction_list_size, processed_list_size, sampled_list_size, total_data_generated]
        
        Data = {'ListName': x, 'EntityCount': y}
        df = DataFrame(Data,columns=['ListName','EntityCount'])            
        sns.set(style="whitegrid")
        
        fig, axes = plt.subplots(ncols = 2, nrows = 2)            
        

        colors = ['indianred', 'coral', 'olive', 'steelblue'] 
        ax = df.plot(x='ListName', y='EntityCount', kind='bar', color = colors, figsize= (12,10), fontsize = 10, title = 'Total List Sizes', ax=axes[0, 0], legend = False)
        ax.set(xlabel='List Name', ylabel = 'Entity Count')

        for p in ax.patches:
            ax.annotate('{0}'.format(str(p.get_height())), (p.get_x(), p.get_height()))

        plt.tight_layout()


        # graph2: synthetic data error depth1, hit count, no-hit count
        
        total_data_generated = len(dfdata) 
        nohitted_data_count = dfresultNoHit['SyntheticDataId'].nunique()
        hitted_data_count = total_data_generated - nohitted_data_count
        total_hit_count = dfresultHit['ResultId'].count()
        
        hitted_same = len(dfresultHitSame)
        hitted_different = len(dfresultHitNotSame)    

        self.logger.info('No-hitted record count = {0}'.format(nohitted_data_count))
        self.logger.info('Hitted record count = {0}'.format(hitted_data_count))
        self.logger.info('Total hit count = {0}'.format(total_hit_count))
        self.logger.info('Hitted the same reference entry count = {0}'.format(hitted_same))
        self.logger.info('Hitted different reference entry count = {0}'.format(hitted_different))
        
        x = ['Not Hitted (FN) ', 'Hitted Data', 'Total Hits', 'Hit Same (TP)', 'Hit Different (FP)']
        y = [nohitted_data_count, hitted_data_count, total_hit_count, hitted_same, hitted_different]

        Data = {'Data': x, 'Count': y}
        df = DataFrame(Data,columns=['Data', 'Count'])            

        colors = ['maroon', 'olive', 'mediumorchid', 'green', 'orangered']

        ax = df.plot(x='Data', y='Count', kind='bar', color = colors, figsize= (12,10), fontsize = 10, title = 'Data Hit/NoHit Counts', ax=axes[0, 1], legend=False)
        ax.set(xlabel='Data Name', ylabel = 'Count')

        for p in ax.patches:
            ax.annotate('{0}'.format(str(int(p.get_height()))), (p.get_x(), p.get_height()))

        plt.tight_layout()


        # graph3: synthetic data error depth1, variation group, no-hit count

        dfall = pd.merge(dfdata, dfresult, how='left', left_on=['Id'], right_on = 'SyntheticDataId')   
        dfallgrouped = pd.merge(dfall, dfvariation, how='left', left_on=['Variation_Name'], right_on = 'Variation_Name')   
        df = dfallgrouped.groupby(['Variation_Group', 'HitType'], as_index=False).count()
        df = df[['Variation_Group', 'HitType', 'Hitted']]
        df.rename(columns=lambda x: x.replace('Hitted', 'Count'), inplace=True)
        df.sort_values(['HitType'], axis = 0, ascending = False, inplace = True, na_position ='last') 

        colors = ['maroon', 'orangered', 'steelblue', 'green']
        ax = pd.pivot_table(df, index= 'Variation_Group', columns= 'HitType', values= "Count").plot(kind='bar', color = colors, figsize = (12,10), ax=axes[1,0], title = 'HitType Counts by Variation Group', rot = 0)
        ax.set(xlabel='Variation Group', ylabel = 'Count')

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2)            

        for p in ax.patches:
            ax.annotate('{0}'.format(str(int(p.get_height()))), (p.get_x(), p.get_height()))
        
        plt.tight_layout()

        self.logger.info('\n\n')
        self.logger.info('-' * 80 + '\n')
        self.logger.info('HIT DISTRUBUTIONS BY VARIATION GROUP:')
        s = str(df.pivot(index = 'Variation_Group', columns = 'HitType', values = 'Count' ))
        self.logger.info(s)            


        dfall = pd.merge(dfdata, dfresultNoHit, how='left', left_on=['Id'], right_on = 'SyntheticDataId')   
        dfallgrouped = pd.merge(dfall, dfvariation, how='left', left_on=['Variation_Name'], right_on = 'Variation_Name')   

        df = dfallgrouped.groupby(['Variation_Group'], as_index=False).count()
        df = df[['Variation_Group', 'Hitted']]
        df.rename(columns=lambda x: x.replace('Hitted', 'Count'), inplace=True)
        df.sort_values(['Count'], axis = 0, ascending = False, inplace = True, na_position ='last') 

        ax = df.plot(x='Variation_Group', y='Count', kind='bar', color = 'maroon', figsize= (12,10), fontsize = 10, title = 'NoHit Counts by Variation Group', ax=axes[1,1], legend=False, rot = 0 )
        ax.set(xlabel='Variation Group', ylabel = 'NoHit Count')

        for p in ax.patches:
            ax.annotate('{0}'.format(str(p.get_height())), (p.get_x(), p.get_height()))

        plt.tight_layout()
        plt.savefig(results_visuals_save_path)   

        self.logger.info('\n\n')
        self.logger.info( '-' * 80 + '\n')
        self.logger.info('\n\nNOHIT (FN) COUNTS BY VARIATION GROUP:')
        s = str(df.to_string(index=False))
        self.logger.info(s)
        

        # graph4: synthetic data error depth1, variation name, no-hit count

        dfall = pd.merge(dfdata, dfresultNoHit, how='left', left_on=['Id'], right_on = 'SyntheticDataId')   

        df = dfall.groupby(['Variation_Name'], as_index=False).count()
        df = df[['Variation_Name', 'Hitted']]

        df.rename(columns=lambda x: x.replace('Hitted', 'Count'), inplace=True)
        df = df[df['Count'] > 0]
        
        df.sort_values(['Count'], axis = 0, ascending = False, inplace = True, na_position ='last') 
        
        from matplotlib import cm
        colors = cm.plasma_r(np.linspace(.6,.9, 40))
        ax = df.plot(x='Variation_Name', y='Count', kind='bar', color = colors, figsize= (14,5), fontsize = 10, title = 'NoHit (FN) Counts by Variation Name' , legend = False)
        # plt.axhline(df['Count'].mean(), color='red', linestyle='dashed', linewidth=0.8)
        ax.set(xlabel='Variation Name', ylabel = 'Count')

        for p in ax.patches:
            ax.annotate('{0}'.format(str(p.get_height())), (p.get_x(), p.get_height()))

        plt.tight_layout()
        plt.savefig(results_vname_nohit_path)   

        self.logger.info('\n\n')
        self.logger.info('-' * 80 + '\n')
        
        self.logger.info('NOHIT (FN) COUNTS BY VARIATION NAME:')
        s = str(df.to_string(index=False))
        self.logger.info(s)


        # graph5: synthetic data error depth1, variation name, hittype, hit count

        dfall = pd.merge(dfdata, dfresult, how='left', left_on=['Id'], right_on = 'SyntheticDataId')   
        df = dfall.groupby(['Variation_Name', 'HitType'], as_index=False).count()
        df = df[['Variation_Name', 'HitType', 'Hitted']]
        df.rename(columns=lambda x: x.replace('Hitted', 'Count'), inplace=True)
        df.sort_values(['Count'], axis = 0, ascending = False, inplace = True, na_position ='last') 
        df['Count'] = pd.to_numeric(df['Count'], downcast='integer' )

        colors = ['maroon', 'orangered', 'steelblue', 'green']
        ax = pd.pivot_table(df, index= 'Variation_Name', columns= 'HitType', values= "Count").plot(kind= 'barh', fontsize = 10, figsize = (6,40), color= colors)
        ax.set(xlabel='Variation Name', ylabel = 'Count')

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2)            

        for p in ax.patches:
            ax.annotate('{0}'.format(str(int(p.get_width()))), (p.get_width(), p.get_y()))
        
        plt.tight_layout()
        # plt.savefig(results_vname_hittype_path_h)   for now we do not need horizontal, if needed just open this line
        
        
        # this is th vertical versio of previous graph
        
        colors = ['maroon', 'orangered', 'steelblue', 'green']
        ax = pd.pivot_table(df, index= 'Variation_Name', columns= 'HitType', values= "Count").plot(kind= 'bar', fontsize = 10, figsize = (24,6), color = colors, title = 'Variation Name - Hit Type Details')
        ax.set(xlabel='Variation Name', ylabel = 'Count')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2)            

        for p in ax.patches:
            ax.annotate('{0}'.format(str(int(p.get_height()))), (p.get_x(), p.get_height()))
        
        plt.tight_layout()
        plt.savefig(results_vname_hittype_path_v)               
        
        self.logger.info('\n\n')
        self.logger.info('-' * 80 + '\n')
        self.logger.info('HIT DISTRUBUTIONS BY VARIATION NAME:')
        
        df = df.pivot(index= 'Variation_Name', columns = 'HitType', values = 'Count')
        df = df.fillna('0')
        df.TP = df.TP.astype(int)
        df.FP = df.FP.astype(int)
        df.FN = df.FN.astype(int)
        s = str(df.to_string())

        self.logger.info(s)             
        self.logger.info('\n\n')
        self.logger.info('-' * 80 + '\n')

        elapsed_time = time.time() - start_time
        print('Visualisations for ErrorDepth' + str(error_depth) + ' completed in ' + str(math.ceil(elapsed_time)) + ' secs.')
