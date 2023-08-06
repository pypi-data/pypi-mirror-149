# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 01/03/2019
# Project Name: Toolkit Sanction

''' Module Summary: This module is used for pre-processing, standardisation, row splitting and reformatting the sanction list'''

import pandas as pd
import random
import re
import time
import math
import logging

from sanction_utility import SanctionUtility

from config import constants, params

NEW_SOURCE_FILEPATH = "reflist/combined_sanction_lists_20220505_main.csv"


class RefListPreprocessor:

    '''
    This class is used for pre-processing, standardisation, cleansing, row splitting and reformatting the initial sanction list.
    '''

    def __init__(self):

        '''
        This is the constructor method of the class that sets the class level variables.
        '''

    def preprocess_list(self, filepath = constants.SANCTIONLIST_FILE_PATH):

        '''
        This method is the main method that does the pre-processing on the initial HMT List.
        This method calls the other methods for the different steps of the pre-processing.

        :param filepath: The path of the Sanction List Reference file. The default value for the filepath parameter is *constants.SANCTIONLIST_FILE_PATH* configuration value.
        :rtype: it has no return value

        '''

        self.logger = logging.getLogger('Sanctions')
        self.logger.info('Ref List pre-process started.')

        self.filepath = filepath

        self.entries = pd.DataFrame()
        self.processed = pd.DataFrame()

        self.unchanged = pd.DataFrame()
        self.unchanged_check = pd.DataFrame()

        print('-' * 80 + '\n')

        print('\nList pre-processing started...')
        start_time = time.time()

        self.load_list()
        self.unchanged_firmvisit()
        self.select_columns()
        self.deduplicate_rows()
        self.add_row_identifiers()
        self.write_initial_to_file()
        self.cleanse_standardise()
        self.calculate_word_count()
        self.split_rows()

        elapsed_time = time.time() - start_time
        print('List pre-processing completed in ' + str(math.ceil(elapsed_time)) + ' secs.')


    def load_list(self):

        '''
        This method loads the list entries from the Reference File into a pandas dataframe and rename the column names as required.

        :param: it has no parameters
        :rtype: it has no return value

        '''

        # reading the file into dataframe
        self.entries = pd.read_csv(NEW_SOURCE_FILEPATH, engine='python', encoding='utf-8')
        self.entries = self.entries[self.entries["sanction_list"].isin(["UK Cons", "UK Inv"])]
        
        #self.entries = pd.read_csv(self.filepath, skiprows=[0], engine='python', encoding = 'cp1252')

        # renaming columns, remove spaces from column names
        self.entries.rename(columns=lambda x: x.replace(' ', ''), inplace=True)
        self.entries.rename(columns=lambda x: x.replace('entity_type', 'Entity_Type'), inplace=True)
        self.entries.rename(columns=lambda x: x.replace('full_name', 'Fullname'), inplace=True)
        self.entries.rename(columns=lambda x: x.replace('title', 'Title'), inplace=True)
        self.entries.rename(columns=lambda x: x.replace('list_internal_id', 'GroupID'), inplace=True)

        # replacing NaN with ''
        self.entries = self.entries.fillna('')

    def unchanged_firmvisit(self, sanctions_list = constants.SANCTIONLIST_FILE_PATH, unchanged_path = constants.SANCTIONLIST_FILE_PATH_UNCHANGED, unchanged_firmvisit_path = constants.UNCHANGED_DATA_FILE_PATH, unchanged_firmvisit_path_check = constants.UNCHANGED_DATA_FILE_PATH_CHECK, sample_unchanged=params.unchanged_sample):

        '''
        This creates concatenates name field from the initial HMT list and exports to two new files; one for the firm to query, the other
        to join at a later date.

        :param: HMT sanctions list.
        :rtype: Unchanged list to send to firms
        :rtype: Check list to join to firms results file

        '''
        
        self.unchanged = pd.read_csv(NEW_SOURCE_FILEPATH, sep=',', encoding='utf-8')
        self.unchanged = self.unchanged.fillna('')
        self.unchanged = self.unchanged[self.unchanged["sanction_list"].isin(["UK Cons", "UK Inv"])]
        
        
        self.unchanged['Original'] = self.unchanged['title'].astype(str) + " " + self.unchanged['full_name'].astype(str)
        self.unchanged['Original'] = self.unchanged['Original'].apply(lambda x: re.sub('\s\s+', ' ', x).strip())
        self.unchanged['Derived'] = 0
        self.unchanged['Entity_Type'] = self.unchanged['entity_type']
        e_i_mapping = {"Entity": "E", "Individual": "I"}
        self.unchanged = self.unchanged.replace({"Entity_Type": e_i_mapping})
        self.unchanged['GroupId'] = self.unchanged['list_internal_id']
        ids = [i for i in range(1, len(self.unchanged) + 1)]
        self.unchanged.insert(0, 'RefId', ids)
        
        #CHNAGE TO ACCOUNT FOR NEW SOURCE LIST
        
        # self.unchanged['Original'] = self.unchanged['Title'].astype(str) + " " + self.unchanged['Name 1'].astype(str) + " " + self.unchanged['Name 2'].astype(str) + " " + self.unchanged['Name 3'].astype(str) + " " + self.unchanged['Name 4'].astype(str) + " " + self.unchanged['Name 5'].astype(str) + " " + self.unchanged['Name 6'].astype(str)
        # self.unchanged['Original'] = self.unchanged['Original'].apply(lambda x: re.sub('\s\s+', ' ', x).strip())
        # self.unchanged['Derived'] = 0
        # self.unchanged['Entity_Type'] = self.unchanged['Group Type']
        # e_i_mapping = {"Entity": "E", "Individual": "I"}
        # self.unchanged = self.unchanged.replace({"Entity_Type": e_i_mapping})
        # self.unchanged['GroupId'] = self.unchanged['Group ID']
        # #add id field
        # ids = [i for i in range(1, len(self.unchanged) + 1)]
        # self.unchanged.insert(0, 'RefId', ids)

        self.unchanged_check = self.unchanged[['RefId', 'fca_uid', 'GroupId', 'Original', 'Derived', 'Entity_Type', 'regime']]
        self.unchanged = self.unchanged[['GroupId', 'fca_uid', 'Original', "Entity_Type", 'regime']]

        #if no sampling of ed0
        if sample_unchanged == False:
            ed0_ids = [i for i in range(1, len(self.unchanged) + 1)]
            self.unchanged.insert(0, 'Id', ed0_ids)

        #if number for sampling, sample
        elif isinstance(sample_unchanged, int):
            rows = random.sample(range(0, len(self.unchanged)), sample_unchanged)
            self.unchanged_check = self.unchanged_check.iloc[rows, :]
            self.unchanged = self.unchanged.iloc[rows, :]
            ed0_ids = [i for i in range(1, sample_unchanged + 1)]
            self.unchanged.insert(0, 'Id', ed0_ids)

        self.unchanged_check.to_csv(unchanged_firmvisit_path_check, sep='\t', index=None)
        self.unchanged.to_csv(unchanged_firmvisit_path, sep='\t', index=None)

    def calculate_word_count(self):

        '''
        This method inserts a new column called *'Total_Word_Count'* calculates the total word count for Fullname value for each row.

        :param: it has no parameters
        :rtype: it has no return value

        '''

        self.entries.insert(len(self.entries.columns), 'Total_Word_Count', 0)
        self.entries['Total_Word_Count'] = self.entries['Fullname'].apply(SanctionUtility.get_word_count)


    def select_columns(self):

        '''
        This method takes the columns only required for the synthetic data generation.
        For the first phase of the project we need only name fields, title field and Entity Type field.
        In the future we might need the other fields like DateOfBirth, Country, Address etc.

        :param: it has no parameters
        :rtype: it has no return value

        '''

        # column selection is being done
        self.entries = self.entries[['Fullname', 'Title', 'Entity_Type', 'GroupID', "fca_uid", "regime"]]


    def deduplicate_rows(self):
        '''
        It makes de-duplication on the list. It only takes care the selected columns for de-duplication operation.

        :param: it has no parameters
        :rtype: it has no return value


        '''
        self.entries = self.entries.drop_duplicates()


    def add_row_identifiers(self):
        
        #SHOULD THIS BE WHERE WE DO THE CONSOLIDATED ID

        '''
        This methods introduces unique row identifiers to the list entries. Initially there is no identifiers for the entries in the initial file.

        :param: it has no parameters
        :rtype: it has no return value

        '''

        # inserting a new row identifier column at the beginning of each row
        initial_id = [i for i in range(1, len(self.entries) + 1)]
        self.entries.insert(0, 'InitialId', initial_id)


    def write_initial_to_file(self):

        '''
        It writes initial entries to the file given as parameter.
        Default path for the file is *constants.INITIAL_LIST_FILE_PATH* value.
        Before writing entries into the file it adds a calculated field that holds the total word count in the 6 Name fields.

        :param: it has no parameters
        :rtype: it has no return value

        '''

        self.entries.insert(len(self.entries.columns), 'WordCount', 0)
        # TODO: Do it at a time, not by calling for all name columns separately
        split_name = self.entries['Fullname'].str.split(" ")
        self.entries["WordCount"] = split_name.apply(len)
        
        self.entries.to_csv(constants.INITIAL_LIST_FILE_PATH, sep='\t', index=False)


    # def not_derived(self):

    #     '''
    #     This method adds a column called 'derived' to show if a column is derived or not.
    #     Initially these will be populated with 0s. These will be changed to 1 later if new rows are derived as part of the splitrows()
    #     '''
    #     self.entries['Derived'] = 0


    def cleanse_standardise(self):

        '''
        This method does data cleansing in 2 steps:
         1. Replace all sequential multiple spaces into single space (it is important for calculating the total word count)
         2. It converts Fullname and Title values to uppercase

        :param: it has no parameters
        :rtype: it has no return value

        '''

        # replacing multiple spaces with single space
        self.entries.replace(regex={'[ ]{2,}' : ' '})

        # convert title and Fullname to uppercase
        self.entries['Fullname'] = self.entries['Fullname'].str.upper()
        self.entries['Title'] = self.entries['Title'].str.upper()


    def split_rows(self):

        '''
        This method splits one row into multiple rows based on the Title and Fullname value.
        This is a 2 level nested splitting operation.
            - If there are multiple Titles delimited by '/' character at the Title column value, this method creates a new rocord for each title token.
            - If the Fullname contains some data between left and right paranthesis, this method creates 2 or 3 entries from the Fullname.
        Based on the Title and Fullname values this method might create multiple entries name and title values changing and all the other data remain same.

        :param: it has no parameters
        :rtype: it has no return value

        '''


        # 2 level nested splitting
        # split rows according to the paranthesis on the fullname column, one row will hold the whole name value, second row will hold the name value the string between paranthesis throwned away
        # split rows according to the / character in the title column: One row will hold one of the title, second row will hold the other titles

        exceptionwords = [line.rstrip('\n') for line in open(constants.NAME_EXCEPTIONS_PATH)]

        file = open(constants.LIST_FILE_PATH_PROCESSED, "w+")
        self.entries.insert(1, 'Derived', 0 )

        file.write('\t'.join(['Id', 'fca_uid', 'GroupID', 'InitialId', 'Fullname', 'Derived', 'Title', 'Entity_Type', 'Total_Word_Count', "regime"])  + '\n')

        id = 1

        for i, row in self.entries.iterrows():

            titles = row['Title'].split('/')
            names = []

            names.append(row['Fullname'].strip()) # adding the original version

            if '(' in row['Fullname'] and ')' in row['Fullname']:

                #***
                #names.append(row['Fullname'].strip()) # adding the original version for parenthases

                strparanthesis = row['Fullname'][row['Fullname'].find('(')+1:row['Fullname'].find(')')].strip()
                strparanthesisall = row['Fullname'][row['Fullname'].find('('):row['Fullname'].find(')') +1].strip()

                if strparanthesis in exceptionwords:
                    names.append(row['Fullname'].replace(strparanthesisall, '').strip())
                else:
                    names.append(strparanthesis.strip())
                    names.append(row['Fullname'].replace(strparanthesisall, '').strip())


            #names.append(row['Fullname'].strip()) # adding the original version
            #removed to get derived col

            #title_name_variant_id = 1
            derived_id = 0

            for name in names:
                for title in titles:

                    if name != '' or title != '':

                        new_row = row.copy()
                        new_row['Fullname'] = re.sub('[ ]{2,}', ' ', name.strip() )
                        new_row['Title'] = title
                        new_row['Derived'] = derived_id
                        derived_id = 1

                        file.write('\t'.join(list([str(id), str(new_row["fca_uid"]), str(new_row['GroupID']), str(new_row['InitialId']), new_row['Fullname'], str(new_row['Derived']), new_row['Title'], new_row['Entity_Type'][:1], str(new_row['Total_Word_Count']),str(new_row['regime'])])) + '\n')
                        id += 1

        file.close()
