# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
LOCATION_BEGIN = 'Begin' - test
'''


LOCATION_BEGIN = 'Begin'

LOCATION_END = 'End'
LOCATION_MIDDLE = 'Middle'
LOCATION_RANDOM = 'Random'
LOCATION_NA = 'Whole'



RUNTYPE_COMPREHENSIVE = 'C'
RUNTYPE_RANDOM = 'R'
RUNTYPE_FULL = 'F'


ENTITY_TYPE_INDIVIDUAL = 'I'
ENTITY_TYPE_ENTITY = 'E'

FIELD_NAME = 'Name'
FIELD_DOB = 'DOB'
FIELD_PASSPORTID = 'PassportId'
FIELD_NATIONALID = 'NationalId'
FIELD_ADDRESS = 'Address'

HMT_SANCTIONLIST_URL = 'https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.csv'
HMT_SANCTIONLIST_XML_URL = 'https://ofsistorage.blob.core.windows.net/publishlive/2022format/ConList.xml'

SANCTIONLIST_FILE_NAME = 'sanctionsconlist'
SANCTIONLIST_FILE_PATH = './SanctionToolkit/reflist/sanctionsconlist.csv' # sanctionslist csv file
SANCTIONLIST_XML_FILE_PATH = './SanctionToolkit/reflist/sanctionsconlist.xml' # sanctions list xml file
SANCTIONLIST_FILE_PATH_UNCHANGED = './SanctionToolkit/output/sanctionsconlist_initial_unchanged.txt'
INITIAL_LIST_FILE_PATH = './SanctionToolkit/output/sanctionsconlist_initial.txt' # initial sanctions file after preprocessing with initial_id
LIST_FILE_PATH_PROCESSED = './SanctionToolkit/output/sanctionsconlist_processed.txt' # processed santions list
LIST_FILE_PATH_PROFILED = './SanctionToolkit/output/sanctionsconlist_profiled.txt' # profiled processed sanctions list
PROFILED_LIST_FILE_PATH_L2 = './SanctionToolkit/output/sanctionsconlist_profiled_l2.txt' # ???
PROFILED_SAMPLED_FILE_PATH = './SanctionToolkit/output/sanctionsconlist_profiled_sampled.txt' #sampled version of the profiled data
SYNTHETIC_DATA_FILE_PATH = './SanctionToolkit/output/synthetic_sanction_data_depth1.txt' # generated synthetic data (ed1)
SYNTHETIC_DATA_FILE_PATH_PROFILED = './SanctionToolkit/output/synthetic_sanction_data_depth1_profiled.txt'# profiled generated synthetic data (ed1)
SYNTHETIC_DATA_FILE_PATH_D2 = './SanctionToolkit/output/synthetic_sanction_data_depth2.txt' # generated synthetic data (ed2)
SYNTHETIC_DATA_FILE_PATH_D2_PROFILED = './SanctionToolkit/output/synthetic_sanction_data_depth2_profiled.txt' # profiled generated synthetic data (ed2)
SYNTHETIC_DATA_FILE_PATH_D3 = './SanctionToolkit/output/synthetic_sanction_data_depth3.txt' # generated synthetic data (ed3)
SYNTHETIC_DATA_FILE_PATH_D3_PROFILED = './SanctionToolkit/output/synthetic_sanction_data_depth3_profiled.txt'# profiled generated synthetic data (ed3)
SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS = './SanctionToolkit/output/synthetic_sanction_data_alldepths.txt' # concatenated generated synthetic data (ed1, ed2, ed3)
METIS_OUTPUT = './SanctionToolkit/output/metis_output.csv'
VARIATION_BREAKDOWN = './SanctionToolkit/output/variation_types_breakdown.xlsx'

UNCHANGED_DATA_FILE_PATH_RESULTS = './SanctionToolkit/output/FromFirms/unchanged_query_results.txt' # query results recieved back from firms (fincom)
UNCHANGED_DATA_FILE_PATH_FULL_RESULTS = './SanctionToolkit/output/FullResults/UnchangedQueryFullResults.txt' 
FIRM_QUERY_FULL_RESULTS = './SanctionToolkit/output/FullResults/FirmQueryFullResults.txt'
SYNTHETIC_FAKE_FILE_PATH = './SanctionToolkit/output/synthetic_fake_results.txt'
SYNTHETIC_FAKE_FILE_PATH_D2 = './SanctionToolkit/output/synthetic_fake_results2.txt'
SYNTHETIC_FAKE_FILE_PATH_D3 = './SanctionToolkit/output/synthetic_fake_results3.txt'

#FIRM VISIT DATA
VISIT_DATA_FILE_PATH = './SanctionToolkit/output/ToFirms/FirmVisitData.txt'
VISIT_DATA_FILE_PATH_D2 = './SanctionToolkit/output/Firm Visit Data2.txt'
VISIT_DATA_FILE_PATH_D3 = './SanctionToolkit/output/Firm Visit Data3.txt'
UNCHANGED_DATA_FILE_PATH = './SanctionToolkit/output/synthetic_sanction_data_depth0.txt'
UNCHANGED_DATA_FILE_PATH_CHECK = './SanctionToolkit/output/synthetic_sanction_data_depth0_check.txt'

DICTIONARY_FIRSTNAME_PATH = './SanctionToolkit/resource/firstnames.txt'
DICTIONARY_COMPANYNAME_PATH = './SanctionToolkit/resource/company_names.txt'
DICTIONARY_FIRSTNAME_SYNONYMS_PATH = './SanctionToolkit/resource/firstname_synonyms.txt'
ARABIC_NAME_WORDS_PATH = './SanctionToolkit/resource/arabic_name_words.txt'
RUSSIAN_NAME_WORDS_PATH = './SanctionToolkit/resource/russian_name_words.txt'
CHINESE_NAME_WORDS_PATH = './SanctionToolkit/resource/chinese_name_words.txt'
NAME_EXCEPTIONS_PATH = './SanctionToolkit/resource/name_paranthesis.txt'
PARAMETER_FILE_PATH = './SanctionToolkit/config/run_params.txt'
PARAMETER_VARIATOR_FILE_PATH = './SanctionToolkit/params_variators.py'

SANCTION_RESULTS_FILE_PATH_OLD = './SanctionToolkit/output/sanction_results_old.txt'
SANCTION_RESULTS_FILE_PATH2_OLD = './SanctionToolkit/output/sanction_results_old2.txt'
SANCTION_RESULTS_FILE_PATH3_OLD = './SanctionToolkit/output/sanction_results_old2.txt'

SANCTION_RESULTS_FILE_PATH = './SanctionToolkit/output/sanction_results.txt'
SANCTION_RESULTS_FILE_PATH_D2 = './SanctionToolkit/output/sanction_results2.txt'
SANCTION_RESULTS_FILE_PATH_D3 = './SanctionToolkit/output/sanction_results3.txt'

#SANCTION_RESULTS_FILE_PATH_NEW = './SanctionToolkit/output/sanction_results_new.txt'
SANCTION_RESULTS_RAW_FILE_PATH = './SanctionToolkit/output/sanction_results_raw.txt'

#SANCTION_RESULTS_FILE_PATH_NEW_D2 = './SanctionToolkit/output/sanction_results_new2.txt'
SANCTION_RESULTS_RAW_FILE_PATH_D2 = './SanctionToolkit/output/sanction_results_raw2.txt'

#SANCTION_RESULTS_FILE_PATH_NEW_D3 = './SanctionToolkit/output/sanction_results_new3.txt'
SANCTION_RESULTS_RAW_FILE_PATH_D3 = './SanctionToolkit/output/sanction_results_raw3.txt'


COMPANY_COMMONWORDS_FILEPATH = './SanctionToolkit/resource/company_common_words.txt'
FIRSTNAMES_FILEPATH = './SanctionToolkit/resource/firstnames.txt'
COMPANYNAMES_FILEPATH = './SanctionToolkit/resource/company_names.txt'
COMPANY_AUXWORDS_FILEPATH = './SanctionToolkit/resource/company_aux_words.txt'
TITLES_FILEPATH = './SanctionToolkit/resource/titles.txt'

LOG_FILEPATH = './SanctionToolkit/output/logs/SanctionToolkit.log'


VISUALS_RUN_RESULTS_FILE_PATH = './SanctionToolkit/output/visuals/Run Results Error Depth1.png'
VISUALS_RESULTS_VNAME_NOHIT_PATH = './SanctionToolkit/output/visuals/Run Result VariationName-NoHit Depth1.png'
VISUALS_RESULTS_VNAME_HITTYPE_H_PATH = './SanctionToolkit/output/visuals/Run Result VariationName-Hittype Horizontal Error Depth1.png'
VISUALS_RESULTS_VNAME_HITTYPE_V_PATH = './SanctionToolkit/output/visuals/Run Result VariationName-Hittype Vertical Error Depth1.png'


VISUALS_RUN_RESULTS_FILE_PATH2 = './SanctionToolkit/output/visuals/Run Results Error Depth2.png'
VISUALS_RESULTS_VNAME_NOHIT_PATH2 = './SanctionToolkit/output/visuals/Run Result VariationName-NoHit Depth2.png'
VISUALS_RESULTS_VNAME_HITTYPE_H_PATH2 = './SanctionToolkit/output/visuals/Run Result VariationName-Hittype Horizontal Error Depth2.png'
VISUALS_RESULTS_VNAME_HITTYPE_V_PATH2 = './SanctionToolkit/output/visuals/Run Result VariationName-Hittype Vertical Error Depth2.png'


VISUALS_RUN_RESULTS_FILE_PATH3 = './SanctionToolkit/output/visuals/Run Results Error Depth3.png'
VISUALS_RESULTS_VNAME_NOHIT_PATH3 = './SanctionToolkit/output/visuals/Run Result VariationName-NoHit Depth3.png'
VISUALS_RESULTS_VNAME_HITTYPE_H_PATH3 = './SanctionToolkit/output/visuals/Run Result VariationName-Hittype Horizontal Error Depth3.png'
VISUALS_RESULTS_VNAME_HITTYPE_V_PATH3 = './SanctionToolkit/output/visuals/Run Result VariationName-Hittype Vertical Error Depth3.png'

all_entity_types = ['I', 'E']


CHARACTER_SET_ENGLISH = 'EN'

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'
CONSTONANTS = 'BCDFGHJKLMNPQRSTVWXYZ'
NUMBERS = '0123456789'

HYPHEN = '-'
EN_DASH = '–'
EM_DASH = '—'

SANCTION_MODE_GENERATE = 'GENERATE'
SANCTION_MODE_LOAD = 'LOAD'


KEYBOARD_NEIGHBORS = {
            'Q' : ['A', 'S', 'W'],
            'W' : ['Q', 'A', 'S', 'D', 'E'],
            'E' : ['W', 'S', 'D', 'F', 'R'],
            'R' : ['E', 'D', 'F', 'G', 'T'],
            'T' : ['R', 'F', 'G', 'H', 'Y'],
            'Y' : ['T', 'G', 'H', 'J', 'U'],
            'U' : ['Y', 'H', 'J', 'K', 'I'],
            'I' : ['U', 'J', 'K', 'L', 'O'],
            'O' : ['I', 'K', 'L', 'P'],
            'P' : ['O', 'L'],
            'A' : ['Q', 'W', 'S', 'Z'],
            'S' : ['A', 'Q', 'E', 'D', 'X', 'Z'],
            'D' : ['S', 'W', 'E', 'R', 'F', 'C', 'X'],
            'F' : ['D', 'E', 'R', 'T', 'G', 'V', 'C'],
            'G' : ['F', 'R', 'T', 'Y', 'H', 'B', 'V'],
            'H' : ['G', 'T', 'Y', 'U', 'J', 'N', 'B'],
            'J' : ['H', 'Y', 'U', 'I', 'K', 'M', 'N'],
            'K' : ['J', 'U', 'I', 'O', 'L', 'M'],
            'L' : ['K', 'I', 'O', 'P'],
            'Z' : ['A', 'S', 'D', 'X'],
            'X' : ['Z', 'S', 'D', 'C'],
            'C' : ['X', 'D', 'F', 'V'],
            'V' : ['C', 'F', 'G', 'B'],
            'B' : ['V', 'G', 'H', 'N'],
            'N' : ['B', 'H', 'J', 'M'],
            'M' : ['N', 'J', 'K']
        }


variators = ['insert_a_letter', 'delete_a_character', 'change_a_letter', 'change_a_vowel', 'change_a_letter_by_number', 'insert_a_number', 'change_a_number',
'change_a_number_by_letter', 'missing_word', 'added_word', 'delete_a_space', 'delete_all_spaces', 'delete_a_number','delete_a_letter', 'change_hyphen_by_space',
'delete_hyphen', 'insert_hyphen', 'change_apostrophe_by_space', 'insert_apostrophe', 'delete_apostrophe', 'initialize_a_word', 'partial_word', 'insert_duplicated_character',
'delete_a_duplicate', 'added_space', 'double_metaphone', 'swap_similar_sounds', 'replace_special_pairs', 'change_visual_similar_characters', 'keyboard_change_letter', 'keyboard_insert_letter',
'letter_lowercase', 'swap_characters', 'swap_characters_2d', 'swap_words', 'swap_words_2d', 'punctuation_change', 'company_commonword_change',
'company_auxword_change', 'insert_title', 'delete_title', 'change_title', 'word_to_nickname', 'metaphone' , 'No_change', 'change_ampersand_to_and',
'change_and_to_ampersand', 'change_a_number_to_numberword', 'change_spaces_with_fullstop']

variation_locations = ['Begin', 'End', 'Middle', 'Whole']
variation_locations_random = ['Whole']
variation_locations_comprehensive = ['Begin', 'End', 'Middle']

field_names = ['Name', 'DOB', 'Address', 'City', 'State', 'Country', 'VAT', 'NationalID', 'PassportID', 'CompanyNumber', 'PhoneNumber', 'Email']

entity_types = ['Individual', 'Entity', 'Vessel', 'Aircraft']
