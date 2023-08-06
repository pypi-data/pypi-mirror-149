import pandas as pd 
import numpy as np
import aes
import string

def decrypt_key(arr):
    key = b"zelenskyymetis22"
    iv = b"zelenskyymetis22"
    
    decrypted = []
    for encr in arr:
        byte_encr = bytes.fromhex(encr)
        decr = aes.AES(key).decrypt_pcbc(byte_encr, iv)
        decrypted.append(decr.decode("utf-8"))
    return decrypted
    
def extract_info(arr, var_map):
    is_fake = []
    variations = []
    ed = []
    for key in arr:
        if len(key) == 5 and key[0] in string.digits:
            list_id = ""
            is_fake.append("T")
            ed.append("")
            variations.append("")
        elif len(key) == 4 and key[0] in string.ascii_letters:
            list_id = key
            is_fake.append("F")
            ed.append(0)
            variations.append("")
        else:
            list_id = key[:4]
            var = [var_map[int(x)] for x in key[4:].split("V") if x!=""]
            is_fake.append("F")
            ed.append(0)
            variations.append("->".join(var))
    
    
    return pd.DataFrame({"error_depth": ed, "is_fake": is_fake, "variations": variations})
             
    

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

var_map = {}
for key in variators:
    var_map[variators[key]["id"]] = key


REF_FILENAME = "output/metis_output.csv"

df =  pd.read_csv(REF_FILENAME, encoding="utf-8")


#below will be done by a sql query
# df = ref.merge(firm, how="left", left_on="encr_id", right_on="ID")

#if null
# hit = ["F" if pd.isna(x) else "T" for x in df["FRN-like"].values]
# df["Hit"] = hit

decrypted = decrypt_key(df["encr_id"].values)
info = extract_info(decrypted, var_map)
df = pd.concat([df, info], axis=1)
