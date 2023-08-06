# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 06/03/2019
# Project Name: Toolkit Sanction

''' Module Summary: This module is used for profiling the initial list after preprocess steps'''

import pandas as pd
import time
import math
import logging

from sanction_utility import SanctionUtility
# import constant
# import params

from config import constants, params


class RefListProfiler:

    '''
    This class is used for profiling the initial list after preprocess steps.

    The columns created after profiling will be used for 
        - Data sampling algorithm 
        - Creating reports, dashboards and analytics after running the data set on the Sanction Screening Software
    '''

    def __init__(self):

        '''
        This is the constructor method that initializes the Class level variables.
        '''

        self.filepath = ''
        self.entries = pd.DataFrame()
        self.level = 1

        self.logger = logging.getLogger('Sanctions')
        self.logger.info('Ref List profiling started.')


    def profile_list(self, filepath=constants.LIST_FILE_PATH_PROCESSED, outfilepath=constants.LIST_FILE_PATH_PROFILED, level=0):

        '''
        This method is the main method that does profiling on the pre-processed HMT List
        This method calls the other methods for the different steps of the profiling. 

        :param filepath: This is the parameter for the path of the Pre-processed file to be profiled. The default value is *constants.LIST_FILE_PATH_PROCESSED* value.
        :param outfilepath: This is the parameter for path of the output file to save the profiling data. The default value is *outfilepath = constants.LIST_FILE_PATH_PROFILED* value
        :param level: This is the parameter for level of profiling. The same method can be used for profiling initial file or the output files for ErroDepth1, ErroDepth2, ErrorDepth3

        :rtype: it has no return value

        '''

        print('-' * 80 + '\n')

        print('\nReflist profiling started...')
        start_time = time.time()

        self.filepath = filepath
        self.outfilepath = ''
        self.level = level

        self.import_list(filepath)
        self.calculate_word_pattern()
        self.calculate_word_count()
        self.calculate_contains_vowels()
        self.calculate_contains_hyphen()
        self.calculate_wordlength_count()        
        self.calculate_contains_dot()
        self.calculate_contains_comma()
        self.calculate_contains_duplicates()
        self.calculate_contains_number()
        self.calculate_contains_quote()
        self.calculate_contains_doublequote()
        self.calculate_contains_nonalpha()
        self.calculate_contains_multiplenonalpha()
        self.calculate_contains_titles()
        self.calculate_cultural_word_count()
        self.sample_data()
        self.write_profiles_to_file(outfilepath)

        elapsed_time = time.time() - start_time
        print('Reflist profiling completed in ' + str(math.ceil(elapsed_time)) + ' secs.')


    def import_list(self, filepath=constants.LIST_FILE_PATH_PROCESSED):

        '''
        This method imports the pre-processed file into pandas DataFrame.

        :param filepath: This is a parameter for the address of the Processed File. The default value is *constants.LIST_FILE_PATH_PROCESSED* value

        :rtype: it has no return value

        '''

        self.entries = pd.read_csv(filepath, engine='python', delimiter='\t', encoding="utf-8")

        # replacing NaN with ''
        self.entries = self.entries.fillna('')

        if 'Id' not in self.entries.columns:
            ids = [i for i in range(1, len(self.entries) + 1)]
            self.entries.insert(0, 'Id', ids)


    def calculate_cultural_word_count(self):

        '''
        This method creates 3 new columns and calculates the count of Arabic, Russian and Chinese name counts in Fullname field for each row.
        The Arabic, Russian and Chinese names are being checked against the dictionary files of the tool collected from public web resources.

        :param: it has no parameters

        :rtype: it has no return value

        '''

        # creating  new columns
        self.entries.insert(len(self.entries.columns), 'ArabicWordCount', 0)
        self.entries.insert(len(self.entries.columns), 'RussianWordCount', 0)
        self.entries.insert(len(self.entries.columns), 'ChineseWordCount', 0)

        arabicwords = [line.rstrip('\n') for line in open(constants.ARABIC_NAME_WORDS_PATH)]
        russianwords = [line.rstrip('\n') for line in open(constants.RUSSIAN_NAME_WORDS_PATH)]
        chinesewords = [line.rstrip('\n') for line in open(constants.CHINESE_NAME_WORDS_PATH)]

        def arabic_word_count(name):
            tokens = name.split()
            return len([value for value in tokens if value in arabicwords])

        def chinese_word_count(name):
            tokens = name.split()
            return len([value for value in tokens if value in chinesewords])

        def russian_word_count(name):
            tokens = name.split()
            return len([value for value in tokens if value in russianwords])

        self.entries['ArabicWordCount'] = self.entries.apply(lambda x: arabic_word_count(x['Fullname']), axis=1)
        self.entries['ChineseWordCount'] = self.entries.apply(lambda x: chinese_word_count(x['Fullname']), axis=1)
        self.entries['RussianWordCount'] = self.entries.apply(lambda x: russian_word_count(x['Fullname']), axis=1)


    def calculate_word_count(self):

        '''
        This method creates a new column contains the total word count of the Fullname field for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        self.entries.insert(len(self.entries.columns), 'WordCount', 0)
        self.entries['WordCount'] = self.entries['Fullname'].apply(SanctionUtility.get_word_count)


    def calculate_contains_duplicates(self):

        '''
        This method creates a new column contains the total adjacent duplicate character count for Fullname field for each row.

        :param: it has no parameters

        :rtype: it has no return value

        '''

        # creating a new column 
        self.entries.insert(len(self.entries.columns), 'DuplicateCount', 0)
        self.entries['DuplicateCount'] = self.entries['Fullname'].apply(SanctionUtility.get_duplicate_count)


    def calculate_wordlength_count(self):

        '''
        This method creates 4 new columns contains the total ShortWordCount, MediumWordCount, LongWordCount and InitialCount in the Fullname value for each row.
        ShortWord = Word 2-3 characters length
        MediumWord = Word 4-7 characters length
        LongWord = Word >=8 characters length
        Initial = Word 1 character length (just a letter)

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating  new columns 

        if 'ShortWordCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'ShortWordCount', 0)
            
        if 'MediumWordCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'MediumWordCount', 0)

        if 'LongWordCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'LongWordCount', 0)

        if 'InitialCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'InitialCount', 0)

        self.entries['ShortWordCount'] = self.entries['Fullname'].apply(SanctionUtility.get_short_word_count)
        self.entries['MediumWordCount'] = self.entries['Fullname'].apply(SanctionUtility.get_medium_word_count)
        self.entries['LongWordCount'] = self.entries['Fullname'].apply(SanctionUtility.get_long_word_count)
        self.entries['InitialCount'] = self.entries['Fullname'].apply(SanctionUtility.get_initial_count)


    def calculate_word_pattern(self):
        
        '''
        This method creates a new column and calculates the word patterns for Fullnames for each row. 
        Word pattern is the types of words in order. It is about the lenghts of the words in Fullname field.
        E.g. ShortWord I ShortWord LongWord

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        if 'WordPattern' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'WordPattern', '')

        self.entries['WordPattern'] = self.entries['Fullname'].apply(SanctionUtility.get_name_pattern)


    def calculate_contains_nonalpha(self):

        '''
        This method creates a new column that holds the Non-AlphaNumeric character count in the fullname for each row.
 
        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        
        if 'NonAlphaCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'NonAlphaCount', 0)
            
        self.entries['NonAlphaCount'] = self.entries['Fullname'].apply(SanctionUtility.get_nonalpha_count)


    def calculate_contains_multiplenonalpha(self):

        '''
        This method creates a new column that holds the number of words in the Fullnames that has non-alphanumeric characters more than 1. 
        This value is being calculated for each rows in the file. 

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 

        if 'NonAlphaMultipleCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'NonAlphaMultipleCount', 0)

        self.entries['NonAlphaMultipleCount'] = self.entries['Fullname'].apply(SanctionUtility.get_multiplenonalpha_count)


    def calculate_contains_number(self):

        '''
        This method creates a new column that holds the number of numeric characters in the Fullname value for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 

        if 'DigitCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'DigitCount', 0)

        self.entries['DigitCount'] = self.entries['Fullname'].apply(SanctionUtility.get_digit_count)


    def calculate_contains_vowels(self):

        '''
        This method creates a new column that holds the total number of vowel characters in Fullname for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 

        if 'VowelCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'VowelCount', 0)

        self.entries['VowelCount'] = self.entries['Fullname'].apply(SanctionUtility.get_vowel_count)


    def calculate_contains_hyphen(self):

        '''
        This method creates a new column that holds the total number of hyphen characters in Fullname for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        if 'HyphenCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'HyphenCount', 0)

        self.entries['HyphenCount'] = self.entries['Fullname'].apply(SanctionUtility.get_hyphen_count)


    def calculate_contains_dot(self):

        '''
        This method creates a new column that holds the total number of dot character in Fullname for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        if 'DotCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'DotCount', 0)

        self.entries['DotCount'] = self.entries['Fullname'].apply(SanctionUtility.get_dot_count)


    def calculate_contains_comma(self):

        '''
        This method creates a new column that holds the total number of comma character in Fullname for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''


        # creating a new column 

        if 'CommaCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'CommaCount', 0)

        self.entries['CommaCount'] = self.entries['Fullname'].apply(SanctionUtility.get_comma_count)


    def calculate_contains_quote(self):

        '''
        This method creates a new column that holds the total number of quote character in Fullname for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        if 'QuoteCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'QuoteCount', 0)

        self.entries['QuoteCount'] = self.entries['Fullname'].apply(SanctionUtility.get_quote_count)


    def calculate_contains_doublequote(self):

        '''
        This method creates a new column that holds the total number of double quote character in Fullname for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 

        if 'DoubleQuoteCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'DoubleQuoteCount', 0)

        self.entries['DoubleQuoteCount'] = self.entries['Fullname'].apply(SanctionUtility.get_double_quote_count)


    def calculate_contains_titles(self):

        '''
        This method creates a new column that holds the total word count in Title field for each row.

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        # creating a new column 
        if 'TitleWordCount' not in self.entries.columns:
            self.entries.insert(len(self.entries.columns), 'TitleWordCount', 0)

        self.entries['TitleWordCount'] = self.entries['Title'].apply(SanctionUtility.get_word_count)


    def write_profiles_to_file(self, outfilepath=constants.LIST_FILE_PATH_PROFILED):

        ''' 
        This method writes the output of the profiling dataset into the file.

        :param outfilepath: This parameter locates the path of the output file. The default value for the parameter is *constants.LIST_FILE_PATH_PROFILED* value 

        :rtype: it has no return value

        '''

        self.entries.to_csv(outfilepath, sep='\t', index=False)


    def sample_data(self):

        ''' 
        This method does a sampling on the dataset based on the data profiling dimensions calculated before. 
        An entropy value is being calculated for sampling for each of the rows in the list.

        1. step is to calculate total row count (GroupTotal) for the same entity type and put this value into each row. 
          This GroupTotal value will be used in the next steps for entropy calculation.

        2. step is to calculate frequencies for each of the profiling dimension columns within the same Entity_Type (FREQ columns).
          For example VOWELFREQ value for a particular row is the frequency of the same VOWELCOUNT accross the whole records with same EntityType.

        3. Step is to calculate Entropy value for each of the profiling dimension columns within the same Entity_Type (ENT columns).
          For example VOWELENT value for a particular row is calculated as : log10(GroupTotal/VowelFreq) for the values in the row.

        4. Step is to calculate a FinalEntropy value that is the sum of all individual entropy values for the profiling dimensions.  

        :param: it has no parameters         

        :rtype: it has no return value

        '''

        count_columns = [c for c in self.entries.columns if 'Count' in c and c not in ['WordCountAgg', 'WordCount']]
        self.entries['TotalPositives'] = self.entries.apply(lambda x: SanctionUtility.get_positives_count(x[count_columns]), axis=1)

        for col in count_columns:

            # frequency columns are being added
            aggregated = self.entries.groupby(['Entity_Type', col], as_index=False).count()
            aggregated = aggregated.loc[:, ['Entity_Type', col, 'Id']]
            aggregated.columns = ['Entity_Type', col, col.replace('Count', 'Freq')]
            self.entries = pd.merge(self.entries, aggregated, how='left', on=['Entity_Type', col])

            # min columns are being added
            aggregated2 = self.entries.groupby(['Entity_Type'], as_index=False)[col].min()
            aggregated2 = aggregated2.loc[:, ['Entity_Type', col]]
            aggregated2.columns = ['Entity_Type', col.replace('Count', 'Min')]
            self.entries = pd.merge(self.entries, aggregated2, how='left', on=['Entity_Type'])

            # max columns are being added
            aggregated3 = self.entries.groupby(['Entity_Type'], as_index=False)[col].max()
            aggregated3 = aggregated3.loc[:, ['Entity_Type', col]]
            aggregated3.columns = ['Entity_Type', col.replace('Count', 'Max')]
            self.entries = pd.merge(self.entries, aggregated3, how='left', on=['Entity_Type'])

        # group total entity count is being added
        aggregated4 = self.entries.groupby('Entity_Type', as_index=False).count()
        aggregated4 = aggregated4.loc[:, ['Entity_Type', 'Id']]
        aggregated4.columns = ['Entity_Type', 'GroupTotal']
        self.entries = pd.merge(self.entries, aggregated4, how='left', on=['Entity_Type'])

        # etropy value for each columns is being calculated
        for col in count_columns:
            freq_column = col.replace('Count', 'Freq')
            ent_column = col.replace('Count', 'Entropy')
            self.entries[ent_column] = self.entries['GroupTotal']/self.entries[freq_column]
            self.entries[ent_column] = self.entries[ent_column].apply(SanctionUtility.get_logarithm)

        entropy_columns = [c for c in self.entries.columns if 'Entropy' in c]
        self.entries['FinalEnt'] = round(self.entries[entropy_columns].sum(axis=1))

        # dropping the unnecessary columns
        min_columns = [c for c in self.entries.columns if 'Min' in c]
        max_columns = [c for c in self.entries.columns if 'Max' in c]
        freq_columns = [c for c in self.entries.columns if 'Freq' in c]

        self.entries = self.entries.drop(columns=entropy_columns)
        self.entries = self.entries.drop(columns=min_columns)
        self.entries = self.entries.drop(columns=max_columns)
        self.entries = self.entries.drop(columns=freq_columns)
        self.entries = self.entries.drop(columns=['GroupTotal'])
