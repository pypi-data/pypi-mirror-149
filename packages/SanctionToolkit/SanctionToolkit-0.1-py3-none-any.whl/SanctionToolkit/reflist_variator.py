# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 08/03/2019
# Project Name: Toolkit Sanction

''' Project Summary: This is a module that variates the given reference list with all of the variation functions and possible parameters '''

import pandas as pd
import time
import math
import traceback
import re
import random
import numpy as np
import logging
import time
from fuzzywuzzy import fuzz

from data_variators import *
from sanction_utility import SanctionUtility
import data_variators

from config import constants, params


class RefListVariator:

    '''This class variates the given reference list with all of the variation functions and all possible parameters.'''


    def __init__(self, sampling = False, max_word_count = 0, word_count_exact = False, entity_types_include = constants.all_entity_types, exclude_short_single_words = params.exclude_short_single_words):

        '''
        This is a constructor method that initializes Class level variables.

        :param sampling: If it is false whole list will be variated. If it is false only the output records of the sampling algorithm will be variated.
        :param max_word_count: It is a parameter for filtering the rows according to the total word count in the Fullname.
         If it is zero, the filtering for word cound will be ignored.
         If it is a positive number, the rows that has wordcount bigger than this parameter will be ignored.

        :param word_count_exact: If this parameter is True: only the rows that has the row count equals to max_word_count parameter will be variated. If it is False: All the rows that has the row count either equals to max_word_count or less than it will be variated.

        :param entity_types_include: This is the parameter defines which entity types will be included for variation. The default value is the list at params.entity_types value.

        :rtype: it has no return value

        '''

        print('-' * 80 + '\n')

        self.sampling = sampling
        self.max_word_count = max_word_count
        self.word_count_exact = word_count_exact
        self.variators = []
        self.entries = pd.DataFrame()
        self.entriessample = pd.DataFrame()
        self.word_counts = []
        self.variation_locations = []
        self.entity_types_include = entity_types_include
        self.exclude_short_single_words = exclude_short_single_words

        self.logger = logging.getLogger('Sanctions')
        self.logger.info('Ref List variation started.')


    def import_list(self, filepath = constants.LIST_FILE_PATH_PROFILED):

        '''
        This method imports the profiled list and do some filtering around word count(if required) and do a sampling.
        Some of these operations is being executed if the corresponding parameter is enabled in the class constructor.

        :param filepath: This is the path of the profiled file to import. Default value of the parameter is *constants.LIST_FILE_PATH_PROFILED* value

        :rtype: it has no return value

        '''

        self.entries = pd.read_csv(filepath, engine='python', delimiter = '\t')
        self.entries = self.entries.fillna('') # replacing NaN with ''

        if self.entity_types_include is not None:
            self.entries = self.entries[self.entries['Entity_Type'].isin(self.entity_types_include)]

        if self.max_word_count > 0: # applying the max word count parameter
            if self.word_count_exact == False:
                self.entries = self.entries[self.entries['WordCount'] <= self.max_word_count]
            else:
                self.entries = self.entries[self.entries['WordCount'] == self.max_word_count]


        self.entries = self.entries.sort_values(by=['WordCount'], ascending=False)

        #exclude short words
        if self.exclude_short_single_words == True:
            self.entries = self.entries[self.entries['WordPattern'] != 'Short']

        # sampling list
        self.do_sampling()


    def do_sampling(self):

        '''
        This method do the sampling on the list based on the Entity_Type, TotalPositives, FinalEnt values in each row.
        The sampling algorithm takes 1 random row for each of the aggregation group of Entity_Type, TotalPositives, FinalEnt columns.

        This method also writes the sampled data into a file for further analysis.

        :param: it has no parameters

        :rtype: it has no return value

        '''


        if self.sampling:
            self.entries = self.entries.groupby(['Entity_Type', 'TotalPositives', 'FinalEnt']).apply(lambda x: x.sample(1)).reset_index(drop=True)

        # if sampling True or not always write records to the file
        self.entries.to_csv(path_or_buf = constants.PROFILED_SAMPLED_FILE_PATH, index=False, sep = '\t')


    def variate_list(self, filepath = constants.LIST_FILE_PATH_PROFILED, outfilepath = constants.SYNTHETIC_DATA_FILE_PATH, runtype = constants.RUNTYPE_COMPREHENSIVE):
        '''
        This method applies ErrorDepth-1 variations on the profiled list (on whole list or sampled list). And it writes the synthetic data generated to the output file.
        It applies all variations to all of the rows in the file in a comprehensive way for all of the different parameter options.
        It calls the variation functions dynamically(reflection)

        :param filepath: This is the file path for profiled list data to variate. Default value is *constants.LIST_FILE_PATH_PROFILED* value
        :param outfilepath: This is the output file path to write down the Synthetic Data generated at the end of the step. Default value is *constants.SYNTHETIC_DATA_FILE_PATH* value
        :param runtype: This parameter defines if the function will will run by comprehensive(call the function for all locations and positions separetely) or run just for a random location and position

        :rtype: it has no return value

        '''

        start_time = time.time()
        print('\nVariations Error Depth 1 is started...')

        self.import_list()

        self.variators, var_id_map = SanctionUtility.get_variation_list(error_depth = 1)

        print('len of variations: ' + str(len(self.variators)))

        keys = list(self.variators)
        values = [0] * len(self.variators)
        times = dict(zip(keys, values))

        outfile = open(outfilepath, "w+")
        outfile.write('\t'.join(['Id', 'fca_uid', 'GroupID', 'InitialId', 'ErrorDepth', 'ParentId', 'Variation_Id', 'Original', 'Fullname_Previous', 'Fullname', 'Title', 'Derived', 'Entity_Type', 'Variation_Type', 'Variation_Location', 'Variation_Position', 'Total_Word_Count', 'NamePath', 'VariationPath', 'TitlePath', "regime"]) + '\n')

        visitfile = open(constants.VISIT_DATA_FILE_PATH, "w+")
        visitfile.write('\t'.join(['Id', 'InitialId', 'Fullname', 'Title']) + '\n')


        if runtype == constants.RUNTYPE_RANDOM:
            self.variation_locations = constants.variation_locations_random
        else:
            self.variation_locations = constants.variation_locations

        rowid = 1 + params.unchanged_sample
        a = 1
        total_line_count = len(self.entries)

        for _, row in self.entries.iterrows():

            if a % 10 == 0:
                print (str(math.ceil(a/total_line_count * 100)) + '% (' + str(a) + ' / ' + str(total_line_count) + ')')

            r_group_id = row['GroupID']
            r_fca_uid = row['fca_uid']
            r_name_previous	= row['Fullname']
            r_entity_type = row['Entity_Type']
            r_error_depth = 1
            r_parentid	= row['Id']
            r_initial_id = row['InitialId']
            r_derived = row['Derived']
            r_regime = row["regime"]

            old_value = row['Fullname']
            old_title = row['Title']

            a += 1
            variation_pos = row['WordCount']

            for v in self.variators:
                
                if runtype == constants.RUNTYPE_RANDOM:
                    variation_pos = 0
                else:
                    variation_pos = row['WordCount']

                for loc in self.variation_locations:
                    for pos in range(0, variation_pos + 1 ):

                        try:

                            start_time2 = time.time()

                            fun = globals()[v]
                            results = fun(value = row['Fullname'] , title = row['Title'], entitytype = row['Entity_Type'], position = pos, location = loc, runtype = runtype)

                            elapsed_time2 = time.time() - start_time2
                            times[v] = times[v] + elapsed_time2

                            if results[0] is not None and results[1] is not None:

                                variated_name = re.sub('[ ]{2,}', ' ', results[0])
                                variated_title = results[1]

                                if variated_name is None and variated_title is None:
                                    continue

                                variated_name = variated_name.strip()
                                variated_title = variated_title.strip()

                                r_id = rowid
                                r_variation_id	= var_id_map[v]
                                r_name_changed = variated_name 
                                r_title	= variated_title
                                r_variation_type = v
                                r_variation_location = loc
                                r_variation_position = pos
                                r_total_word_count	= len(variated_name.split(' '))
                                r_namepath = old_value + '->' + variated_name
                                r_variationpath	= v + '(' + str(pos) + ', ' + str(loc) + ')'
                                r_titlepath = old_title + '->' + variated_title
                                r_name_original = r_namepath.split('->')[0]

                                if (variated_name is not None or variated_title is not None):

                                    new_record = [r_id, r_fca_uid, r_group_id, r_initial_id, r_error_depth, r_parentid, r_variation_id, r_name_original, r_name_previous, r_name_changed, r_title, r_derived, r_entity_type, r_variation_type, r_variation_location, r_variation_position, r_total_word_count, r_namepath, r_variationpath, r_titlepath, r_regime]

                                    outfile.write('\t'.join(map(str, new_record)) + '\n')  # open it again
                                    visitfile.write('\t'.join(map(str, [r_id, r_initial_id, r_name_changed, r_title])) + '\n')  # open it again

                                    rowid += 1

                                    # print( 'Similarity (' + old_value + ', ' + str(variated_name).strip() + ') = ' + str(distance.get_jaro_distance(old_value, str(variated_name).strip(), winkler=True, scaling=0.1) ))

                        except:
                            print('Error at: ' + re.sub('[ ]{2,}', ' ', row['Fullname']) + '->' + str(pos) + '->' + str(loc) + '->' + v )
                            print(traceback.format_exc())
                            pass


        # print(times) total time by variation type

        print ('100% (' + str(total_line_count) + ' / ' + str(total_line_count) + ')')

        outfile.close()
        visitfile.close()
        elapsed_time = time.time() - start_time
        print('\n' + str(rowid) + ' rows created ')
        print('Variations Error Depth 1 completed in ' + str(math.ceil(elapsed_time)) + ' secs.' )


    def variate_list_additional_level(self, infilepath = constants.SYNTHETIC_DATA_FILE_PATH, outfilepath = constants.SYNTHETIC_DATA_FILE_PATH_D2, runtype = constants.RUNTYPE_RANDOM, error_depth = params.max_error_depth):


        '''
        This method applies ErrorDepth-2 and ErrorDepth-3 variations on the given list. And it writes the level2/3 synthetic data generated to the output file.
        For ErrorDepth2 and ErrorDepth3 this function must be called twice and with different parameters.
        It applies all variations to all of the rows in the file in a comprehensive way for all of the different parameter options.
        It calls the variation functions dynamically(reflection)

        :param infilepath: This is the file path for profiled list data to variate. Default value is *constants.SYNTHETIC_DATA_FILE_PATH* value
        :param outfilepath: This is the output file path to write down the Synthetic Data generated at the end of the step. Default value is *constants.SYNTHETIC_DATA_FILE_PATH_D2* value
        :param runtype: This parameter defines if the function will will run by comprehensive(call the function for all locations and positions separetely) or run just for a random location and position
        :param variationlist: This is a list that gives the function list will be applied on the rows. This list is being edited in params file. It is possible to give different variation list for different runs.

        :rtype: it has no return value

        '''

        print('\n' + '*' * 20)
        print('\n\nVariations Error Depth ' + str(error_depth) + ' is started...')

        rowid = 1

        start_time = time.time()
        column_names = []
        cols = {}

        total_line_count = 1
        with open(infilepath) as ft:
            for i, l in enumerate(ft):
                total_line_count += 1

        self.variators, var_id_map = SanctionUtility.get_variation_list(error_depth)

        if runtype == constants.RUNTYPE_RANDOM:
            self.variation_locations = constants.variation_locations_random
        else:
            self.variation_locations = constants.variation_locations


        infile = open(infilepath, "r")
        i = 1
        outfile = open(outfilepath, "w+")

        visitfile = open(constants.VISIT_DATA_FILE_PATH, "a")

        for line in infile:

            linetokens = line.rstrip('\n').split('\t')

            if i == 1:
                i += 1
                column_names = line.rstrip('\n').split('\t')
                cols = {k: v for v, k in enumerate(column_names)}
                outfile.write('\t'.join(map(str, column_names)) + '\n')
                continue

            if error_depth == 2 and i % 100 == 0:
                print (str(math.ceil(i/total_line_count * 100)) + '% (' + str(i) + ' / ' + str(total_line_count) + ')')

            elif error_depth > 2 and i % 1000 == 0:
                print (str(math.ceil(i/total_line_count * 100)) + '% (' + str(i) + ' / ' + str(total_line_count) + ')')


            if linetokens[cols.get('Fullname')] is None:
                continue

            if runtype == constants.RUNTYPE_RANDOM:
                variation_pos = 0
            else:
                variation_pos = int(linetokens[cols.get('Total_Word_Count')])

            r_fca_uid = linetokens[cols.get('fca_uid')]
            r_group_id = linetokens[cols.get('GroupID')]
            r_name_previous	= linetokens[cols.get('Fullname')]
            r_initial_id	= linetokens[cols.get('InitialId')]
            r_derived = linetokens[cols.get('Derived')]
            r_name_original = linetokens[cols.get('NamePath')].split('->')[0]
            r_regime = linetokens[cols.get('regime')]

            r_entity_type = linetokens[cols.get('Entity_Type')]
            r_parentid = linetokens[cols.get('Id')]
            r_error_depth = int(linetokens[cols.get('ErrorDepth')]) + 1

            old_value = linetokens[cols.get('Fullname')]
            old_title = linetokens[cols.get('Title')]

            for v in self.variators:
                variation_id = var_id_map[v]
                for loc in self.variation_locations:
                    for pos in range(0, variation_pos + 1 ):

                        try:

                            tokens = linetokens.copy()

                            fun = globals()[v]
                            results = fun(value = tokens[cols.get('Fullname')] , title = tokens[cols.get('Title')], entitytype = tokens[cols.get('Entity_Type')], position = pos, location = loc, runtype = runtype)
                            if results[0] is not None and results[1] is not None:

                                variated_name = results[0]
                                variated_title = results[1]

                                if variated_name is None and variated_title is None:
                                    continue

                                variated_name = variated_name.strip()
                                allname_variants = tokens[cols.get('NamePath')].split('->')

                                if variated_name in allname_variants:
                                    continue # if it is already in the list it means repretitive

                                variated_name = variated_name.strip()
                                variated_title = variated_title.strip()

                                if (variated_name is not None or variated_title is not None):

                                    variation_id += 1
                                    r_id = rowid
                                    r_fca_uid = r_fca_uid
                                    r_variation_id	= variation_id
                                    r_name_changed = variated_name
                                    r_title	= variated_title
                                    r_variation_type = v
                                    r_variation_location = loc
                                    r_variation_position = pos
                                    r_total_word_count	= len(re.sub('[ ]{2,}', ' ', variated_name).split(' '))
                                    r_namepath	= tokens[cols.get('NamePath')] + '->' + variated_name
                                    r_variationpath	= tokens[cols.get('VariationPath')] + '->' +  v + '(' + str(pos) + ', ' + str(loc) + ')'
                                    r_titlepath = tokens[cols.get('TitlePath')]  + '->' + variated_title

                                    new_record = [r_id, r_fca_uid, r_group_id, r_initial_id, r_error_depth, r_parentid, r_variation_id, r_name_original, r_name_previous, r_name_changed, r_title, r_derived, r_entity_type, r_variation_type, r_variation_location, r_variation_position, r_total_word_count, r_namepath, r_variationpath, r_titlepath, r_regime]
                                    visitfile.write('\t'.join(map(str, [r_id, r_initial_id, r_name_changed, r_title])) + '\n')  # open it again
                                    rowid += 1
                                    outfile.write('\t'.join(map(str, new_record)) + '\n')

                        except Exception:

                            print('Error at: ' + v + ' = ' + re.sub('[ ]{2,}', ' ', tokens[cols.get('Fullname')]) + '->' + str(pos) + '->' + str(loc) + '->' + v )
                            print(traceback.format_exc())
                            pass



            i += 1

        print ('100% (' + str(total_line_count) + ' / ' + str(total_line_count) + ')')

        outfile.close()
        infile.close()

        # #add 'RefId' to FirmVisit.txt
        # firmvisit = pd.read_csv(constants.VISIT_DATA_FILE_PATH, sep='\t', encoding='latin-1')
        # if 'RefId' in firmvisit.columns:
        #     firmvisit = firmvisit.drop('RefId', axis = 1)
        # ids = [i for i in range(1, len(firmvisit) + 1)]
        # firmvisit.insert(0, 'RefId', ids)
        # firmvisit.to_csv(constants.VISIT_DATA_FILE_PATH, index=False, sep = '\t')

        print('\n' + str(rowid) + ' rows created ' )
        elapsed_time = time.time() - start_time
        print('\n' + 'Variations Error Depth ' + str(error_depth) + ' is finished in ' + str(math.ceil(elapsed_time)) + ' secs.' )
        return

    def combine_synthetic_data(self, russia_only=True, sd1 = constants.SYNTHETIC_DATA_FILE_PATH, sd2 = constants.SYNTHETIC_DATA_FILE_PATH_D2, sd3 = constants.SYNTHETIC_DATA_FILE_PATH_D3, error_depth = params.max_error_depth):
        """
        This method combines the synthetic data for each of the error depths into one dataframe and returns a combined file.
        param: Files to be combined
        param: Error depth
        rtype: Combined list of variations
        rtype: Visit list for firms
        """
        if error_depth >= 1:
            all_depths = pd.read_csv(sd1, sep='\t', encoding='utf-8')
            ed1_len = len(all_depths[all_depths['ErrorDepth'] == 1]) #gets number of ed1
        if error_depth >= 2:
            sd2_df = pd.read_csv(sd2, sep='\t', encoding='utf-8')
            sd2_df = sd2_df.sample(n=ed1_len)
            all_depths = pd.concat([all_depths, sd2_df])
        if error_depth > 2:
            sd3_df = pd.read_csv(sd3, sep='\t', encoding='utf-8')
            sd3_df = sd3_df.sample(n=ed1_len)
            all_depths = pd.concat([all_depths, sd3_df])

        #add unchanged entities (error depth 0)
        unchanged = pd.read_csv(constants.UNCHANGED_DATA_FILE_PATH, sep='\t', encoding='utf-8')
        cols = all_depths.columns
        u_df = pd.DataFrame([], columns=all_depths.columns)
        u_df["fca_uid"] = unchanged["fca_uid"]
        u_df["GroupID"] = unchanged["GroupId"]
        u_df["Id"] = unchanged["Id"]
        u_df["Original"] = unchanged["Original"]
        u_df["regime"] = unchanged["regime"]
        u_df["Fullname"] = unchanged["Original"]
        u_df["Fullname_Previous"] = unchanged["Original"]
        u_df["ErrorDepth"] = 0
        u_df["Variation_Type"] = "baseline_nochange"
        u_df["VariationPath"] = "baseline_nochange"
        u_df["Total_Word_Count"] = [len(x.split(" ")) for x in unchanged["Original"].values]
        u_df["NamePath"] = [x+"->"+x for x in unchanged["Original"].values]
        u_df["Similarity_Score"] = 100
        u_df["Variation_Position"] = 0
        u_df["Variation_Location"] = "Whole"
        u_df["TitlePath"] = ""
        u_df["Variation_Id"] = max(all_depths["Variation_Id"])+1
        
        if russia_only:
            all_depths = all_depths[all_depths["regime"] == "Russia"]
        all_depths = pd.concat([u_df, all_depths], axis=0)
        all_depths = all_depths[cols]
        
        ids = [i for i in range(1, len(all_depths) + 1)]
        all_depths.insert(0, 'RefId', ids)

        all_depths.to_csv(constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, index=None, sep = '\t')

        firm_visit_data = all_depths[['RefId', 'Id', 'Fullname', 'Title']]
        firm_visit_data.to_csv(constants.VISIT_DATA_FILE_PATH, index=None, sep = '\t')

        return

    def similarity_metric(self, infile = constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, outfile = constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS):
        """
        This method calculates the similarity, using levenshtein distance, between the original name and the final variated name.
        The score is between 0-1, with 1 being exactly the same.
        It also adds a label based on the score.
        param: Combined synthetic data file.
        rtype: Combined synthetic data file wirh similait score and labelled bins.
        """
        results_df = pd.read_csv(infile, sep='\t', encoding='utf-8')
        results_df['Original'] = results_df['Original'].astype(str)
        results_df['Fullname'] = results_df['Fullname'].astype(str)
        results_df['Similarity_Score'] = results_df.apply(lambda x: fuzz.ratio(x.Original, x.Fullname), axis=1)
        results_df['Similarity_Labels'] = pd.cut(results_df['Similarity_Score'], bins=5, labels=['Most Change', 'Moderate Change', 'Some Change', 'Little Change', 'Least Change'])
        results_df.to_csv(outfile, index=False, sep = '\t')

        return


    def variation_profiler(self, infile = constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, outfile = constants.VARIATION_BREAKDOWN, error_depth = params.max_error_depth):
        """
        This method generates a breakdown of the number of variations for each error depth.
        This method also generates a summary of the number of different variations contained in the variated lists sent to firms.
        param: Combined synthetic data file.
        rtype: csv file with breakdown of variations.
        """
        all_depths = pd.read_csv(infile, sep='\t', encoding='utf-8')
        print(all_depths)

        #save high level breakdown to excel tab
        error_depth_breakdown = all_depths['ErrorDepth'].value_counts().rename_axis('ErrorDepth').to_frame('Count')
        with pd.ExcelWriter(outfile) as writer:
            error_depth_breakdown.to_excel(writer, sheet_name='Summary')
            writer.save()
            writer.close()

        #save profile variations to excel tabs
        #error depth 1
        if error_depth >= 1:
            ed_1 = all_depths[all_depths['ErrorDepth'] == 1].copy()
            ed_1_variations = ed_1['Variation_Type'].value_counts().rename_axis('Variation').to_frame('Count').reset_index()
            ed_1_variations['Variation_Group'] = ed_1_variations['Variation'].apply(lambda x: params.variators[x]['Variation_Group'])
            ed_1_variations = ed_1_variations[['Variation', 'Variation_Group','Count']]
            with pd.ExcelWriter(outfile) as writer:
                error_depth_breakdown.to_excel(writer, sheet_name='Summary')
                ed_1_variations.to_excel(writer, sheet_name='ErrorDepth1')
                writer.save()
                writer.close()
        #error depth 2
        if error_depth >= 2:
            ed_2 = all_depths[all_depths['ErrorDepth'] == 2].copy()
            ed_2['variations'] = ed_2['VariationPath'].apply(lambda x: re.sub(r'\([^)]*\)', '', str(x)))
            ed_2['variations'] = ed_2['variations'].apply(lambda x: x.split('->'))
            ed_2_vars = ed_2['variations'].apply(pd.Series).stack().reset_index(drop=True)
            ed_2_variations = ed_2_vars.value_counts().rename_axis('Variation').to_frame('Count').reset_index()
            ed_2_variations['Variation_Group'] = ed_2_variations['Variation'].apply(lambda x: params.variators[x]['Variation_Group'])
            ed_2_variations = ed_2_variations[['Variation', 'Variation_Group','Count']]
            with pd.ExcelWriter(outfile) as writer:
                error_depth_breakdown.to_excel(writer, sheet_name='Summary')
                ed_1_variations.to_excel(writer, sheet_name='ErrorDepth1')
                ed_2_variations.to_excel(writer, sheet_name='ErrorDepth2')
                writer.save()
                writer.close()
            time.sleep(5)
        #error depth 3
        if error_depth >= 3:
            ed_3 = all_depths[all_depths['ErrorDepth'] == 3].copy()
            ed_3['variations'] = ed_3['VariationPath'].apply(lambda x: re.sub(r'\([^)]*\)', '', str(x)))
            ed_3['variations'] = ed_3['variations'].apply(lambda x: x.split('->'))
            ed_3_vars = ed_3['variations'].apply(pd.Series).stack().reset_index(drop=True)
            ed_3_variations = ed_3_vars.value_counts().rename_axis('Variation').to_frame('Count').reset_index()
            ed_3_variations['Variation_Group'] = ed_3_variations['Variation'].apply(lambda x: params.variators[x]['Variation_Group'])
            ed_3_variations = ed_3_variations[['Variation', 'Variation_Group','Count']]
            ed_3_variations.to_excel(writer, sheet_name='ErrorDepth3')
            with pd.ExcelWriter(outfile) as writer:
                error_depth_breakdown.to_excel(writer, sheet_name='Summary')
                ed_1_variations.to_excel(writer, sheet_name='ErrorDepth1')
                ed_2_variations.to_excel(writer, sheet_name='ErrorDepth2')
                ed_3_variations.to_excel(writer, sheet_name='ErrorDepth3')
                writer.save()
                writer.close()
            time.sleep(5)