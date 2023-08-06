'''
This file is the parameter file for the SanctionToolkit.
The file contains default values for all run type parameters.
In case of need the values in the file must be changed properly for different data requirements.

Parameters:

    - max_error_depth: This parameter tells the maximum ErrorDepth for data generations. It can be one of the 1/2/3.

    - runtype_error_depth1 : The run types for ErrorDepth1. It can be one of the R/C. (R: Random, C: Comprehensive)
    - runtype_error_depth2 : The run types for ErrorDepth2. It can be one of the R/C. (R: Random, C: Comprehensive)
    - runtype_error_depth3 : The run types for ErrorDepth3. It can be one of the R/C. (R: Random, C: Comprehensive)

    - unchanged_names : True queries unchanged names through the vendor api in 'fincom_query.py'.

    - sampling: This is the parameter for RefListVariator that makes sampling enabled or diabled. It can be one of the True/False

    - max_word_count: This is one of the parameters for RefListVariator. It can be Zero or a positive number
    - word_count_exact: This is one the parameters for RefListVariator. It can be one of the True/False
    - entity_types_include: This is one of the parameter for RefListVariator. I can be one of the ['E', 'I'] / ['I'] / ['E']
    - overwrite_download_file: This is of the parameter for RefListDownloader. It ca ne of the True/False

    error_depth1_variators: This is the dictionary type parameter for RefListVariator for ErrorDepth1. All values can be one of the Y/N
                            The keys are copied from the content of the constant.variators list. If a new variator is added both the files should be updated.

    error_depth2_variators: This is the dictionary type parameter for RefListVariator for ErrorDepth2. All values can be one of the Y/N
                            The keys are copied from the content of the constant.variators list. If a new variator is added both the files should be updated.

    error_depth3_variators: This is the dictionary type parameter for RefListVariator for ErrorDepth3. All values can be one of the Y/N
                            The keys are copied from the content of the constant.variators list. If a new variator is added both the files should be updated.


    sanction_mode: This is a switching mode between generating the sanctions screening results with in the toolkit or
                   bringing results from an external firm visit or using results from a 3rd Party Sanction provider. GENERATE value means all steps of the
                   synthetic data generation and the screening happens within the toolkit. LOAD means, the aim is to load an external screening result set.
                   In the industrialisation phase these two must be seprated into 2 different process.

'''

max_error_depth = 1

runtype_error_depth1 = 'R'
runtype_error_depth2 = 'R'
runtype_error_depth3 = 'R'

unchanged_names = True
unchanged_sample = False #can be 'False' or any postive integer between (1 - number of rows in sanctions list)

sampling = False

#389392 with max word count
#434612 without

max_word_count = 15
exclude_short_single_words = False

word_count_exact = False

entity_types_include = ['I', 'E']

match_max_count = 2

skip_visualisations = True
skip_fake_results = True

fake_depth2 = True
visualize_depth2 = False

fake_depth3 = True
visualize_depth3 = False

sanction_mode = 'GENERATE'
#sanction_mode = 'LOAD'


variators = {'No_change'          : {'Variation_Group': 'Baseline', 'ErrorDepth1': 'N', 'ErrorDepth2': 'N', 'ErrorDepth3': 'N', "id": 0},
             'insert_a_letter'            : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 1},
             'delete_a_character'         : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 2},
             'change_a_letter'            : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 3},
             'change_a_vowel'             : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 4},
             'change_a_letter_by_number'  : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 5},
             'insert_a_number'            : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 6},
             'change_a_number'            : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 7},
             'change_a_number_by_letter'  : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 8},
             'missing_word'               : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 9},
             'added_word'                 : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 10},
             'delete_a_space'             : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 11},
             'delete_all_spaces'          : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 12},
             'delete_a_number'            : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 13},
             'delete_a_letter'            : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 14},
             'change_hyphen_by_space'     : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 15},
             'delete_hyphen'             : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 16},
             'insert_hyphen'               : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 17},
             'change_apostrophe_by_space' : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 18},
             'insert_apostrophe'           : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 19},
             'delete_apostrophe'         : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 20},
             'initialize_a_word'          : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 21},
             'partial_word'               : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 22},
             'insert_duplicated_character': {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 23},
             'delete_a_duplicate'         : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 24},
             'insert_space'                : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 25},
             'double_metaphone'           : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 26},
             'swap_similar_sounds'        : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 27},
             'replace_special_pairs'      : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 28},
             'change_visual_similar_characters' : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 29},
             'keyboard_change_letter'     : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 30},
             'keyboard_insert_letter'     : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 31},
             'letter_lowercase'           : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 32},
             'swap_characters'            : {'Variation_Group': 'Swap', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 33},
             'swap_characters_2d'         : {'Variation_Group': 'Swap', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 34},
             'swap_words'                 : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 35},
             'swap_words_2d'              : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 36},
             'punctuation_change'         : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 37},
             'company_commonword_change'  : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 38},
             'company_auxword_change'     : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 39},
             'insert_title'               : {'Variation_Group': 'Insert', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'N', 'ErrorDepth3': 'N', "id": 40},
             'delete_title'               : {'Variation_Group': 'Delete', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'N', 'ErrorDepth3': 'N', "id": 41},
             'change_title'               : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'N', 'ErrorDepth3': 'N', "id": 42},
             'word_to_nickname'           : {'Variation_Group': 'Word Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 43},
             'metaphone'                  : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 44},
             'change_ampersand_to_and'    : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 45},
             'change_and_to_ampersand'    : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 46},
             'change_a_number_to_numberword' : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 47},
             'change_spaces_with_fullstop' : {'Variation_Group': 'Change', 'ErrorDepth1': 'Y', 'ErrorDepth2': 'Y', 'ErrorDepth3': 'Y', "id": 48}
             }



#error_depth_runtypes = ['C', 'C', 'R']
