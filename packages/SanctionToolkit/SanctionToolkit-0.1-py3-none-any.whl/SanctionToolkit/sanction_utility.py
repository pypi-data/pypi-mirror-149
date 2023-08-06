# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 20/03/2019
# Project Name: Toolkit Sanction 

''' Module Summary: This module is used for keeping the project level utility functions.'''

import random
import re as reg
import math
import pandas as pd
import math
import importlib
from config import constants, params


class SanctionUtility:

    '''This class holds the static methods for project level utility functions.'''


    @staticmethod
    def change_letter(letter):
        
        ''' 
        This method changes the given *'letter'* with random another letter.
        
        :param letter: letter character to change
        
        :rtype str: it returns a letter (string length of 1) or None

        '''
        
        if letter.upper() not in constants.LETTERS:
            return None
        
        return random.choice(constants.LETTERS.replace(letter, ''))
        

    @staticmethod
    def change_letter_from_list(letter, list):

        ''' 
        This method changes the given *'letter'* with one of the letters in the *'list'* given as a parameter.
        
        :param letter: letter character to change
        :param list: list of letter characters to chose a random letter among the entries of it 
        
        :rtype str: it returns a letter (string length of 1) or None

        '''

        
        return random.choice(list)
        


    @staticmethod
    def change_character_at(value, index, str_to_insert):
        
        '''
        This method changes the character at given *'index'* of the *'value'* with the value of the *'str_to_insert'* parameter.
        
        :param value: the value to be inserted
        :param index: the index of the location within the value to be changed 
        :param str_to_insert: the value that will be replaced at the index location of value

        :rtype str: it returns a string value derived from the *'value'* parameter

        '''            
        
        if index < 0 or index > len(value):
            return value
            
        return value[:index] + str_to_insert + value[index+1:]


    @staticmethod
    def change_vowel(letter):

        '''
        This method changes the given vowel with a random another vowel letter.
        
        :param letter: vowel letter character to change
        :rtype str: it returns a letter (string length of 1) or None

        '''
        
        if letter.upper() not in constants.VOWELS:
            return None
        
        return random.choice(constants.VOWELS.replace(letter, ''))



    @staticmethod
    def change_number(number):

        '''
        This method changes the given number with a random another number.

        :param number: number character to change
        :rtype str: it returns a number (1 digit) or None

        '''

        if number not in constants.NUMBERS:
            return None
        
        return random.choice(constants.NUMBERS.replace(number, ''))        
        


    @staticmethod
    def get_random_letter():

        '''
        This method returns a random letter.

        :param: it has no parameters
        :rtype str: it returns a letter (string length of 1) or None

        '''
        
        return random.choice(constants.LETTERS)
        
        
    @staticmethod
    def get_random_number():
        
        '''
        This method return a random number.

        :param: is has no parameters

        :rtype str: it returns a number (1 digit)

        '''
        
        return random.choice(constants.NUMBERS)


    @staticmethod
    def insert_string(value, str_to_insert, index):
        
        '''
        This method inserts the str_to_insert value into the index location of the value.
        
        :param value: the value to be inserted
        :param index: the index of the location within the value to be inserted 
        :param str_to_insert: the value that will be inserted to the index location of value

        :rtype str: it returns a string value derived from the *'value'* parameter

        '''
        
        if value is None or str_to_insert is None:
            return None
            
        return value[:index] + str_to_insert + value[index:]    




    @staticmethod
    def delete_character(value, index):

        '''
        This method deletes the character at the *'index'* location from *'value'*.
        
        :param value: value to be changed
        :param index: index of the delete location within the value

        :rtype str: it returns a string value derived from the *'value'* parameter

        '''        
        
        if index < 0 or index > len(value):
            return value
            
        return value[:index] + value[index+1:]



    @staticmethod
    def change_letter_by_number(letter):
        
        '''
        This method changes the given letter with a random number.
        
        :param letter: letter character to be changed
        
        :rtype str: it returns a letter (string length of 1) or None
        
        '''
        
        if letter.upper() not in constants.LETTERS:
            return None
        
        return str(random.choice(constants.NUMBERS))



    @staticmethod
    def change_number_by_letter(number):
        
        '''
        This method changes the given number with a random letter.
        
        :param number: number character to be changed
        
        :rtype str: it returns a letter (string length of 1) or None
        
        '''
        
        if number not in constants.NUMBERS:
            return None
        
        return str(random.choice(constants.LETTERS))
        


    @staticmethod
    def get_random_neighbor(character):
        
        '''
        This method gets one of the keyboard neighbour letters of the given letter.

        :param character: character to be changed

        :rtype str: it returns a letter (string length of 1) or None

        '''
        
        if len(character) == 0 or len(character) > 1:
            return None
            
        if character not in constants.LETTERS:
            return None
            
        neighbors = {}
        neighbors = constants.KEYBOARD_NEIGHBORS
        
        if neighbors.get(character.upper()) is None:
            print('no value: ' + str(character) + ' : ' + str(character.upper()))
            
        return random.choice(neighbors.get(character.upper()))



    @staticmethod
    def get_name_pattern(name):

        '''
        This method returns the word types(lengths of the words: Short/Medium/Long/Initial) of the value in order.

        :param name: the string value with one or multiple word to create the pattern for

        :rtype str: it returns a string

        '''
        
        tokens = name.split()
        pattern = ''

        for t in tokens:

            if len(t) ==1:
                pattern = pattern + 'Initial '
            elif len(t) > 0 and len(t) < 4:
                pattern = pattern + 'Short '
            elif len(t) >= 4 and len(t) < 8:     
                pattern = pattern + 'Medium '
            elif len(t) >= 8:     
                pattern = pattern + 'Long '
                
        return pattern.strip()



    @staticmethod
    def get_short_word_count(name):
        
        '''
        This method returns the count of short words in the value. Short word means the word has 2-3 characters.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''

        tokens = name.split()
        return len([c for c in tokens if len(c) >=1 and len(c) < 4])



    @staticmethod
    def get_medium_word_count(name):

        '''
        This method returns the count of medium length words in the value. Medium word means the word has 4-7 characters.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number

        '''

        tokens = name.split()
        return len([c for c in tokens if len(c) >= 4 and len(c) < 8])



    @staticmethod
    def get_long_word_count(name):
        
        '''
        This method returns the count of long words in the value. Long word means the word has more than 7 characters.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number

        '''

        tokens = name.split()
        return len([c for c in tokens if len(c) >= 8])



    @staticmethod
    def get_initial_count(name):

        '''
        This method returns the initial of short words in the value. Short word means the word has only 1 letter.
        
        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        tokens = name.split()
        return len([c for c in tokens if len(c) == 1]) # needs to check to be a letter only 



    @staticmethod
    def get_word_count(name):

        '''
        This method returns the total word count of the value.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return len(name.split())


    @staticmethod
    def get_hyphen_count(name):

        '''
        This method returns the total hyphen character count in the value.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return sum(map(name.count, [constants.HYPHEN, constants.EN_DASH, constants.EM_DASH]))        
        

    @staticmethod
    def get_vowel_count(name):

        '''
        This method returns the total vowel letter count in the value.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        if len(name.split()) == 0:
            return 0
            
        return math.ceil(sum(map(name.count, list(constants.VOWELS))) / len(name.split()))       
        

    @staticmethod
    def get_digit_count(name):

        '''
        This method returns the total numeric character count in the value.
        
        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return sum(map(name.count, list(constants.NUMBERS)))        
        

    @staticmethod
    def get_dot_count(name):

        '''
        This method returns the total dot character count in the value.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return name.count('.') 
        

    @staticmethod
    def get_double_quote_count(name):
        
        '''
        This method returns the total double quote character count in the value.
        
        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return name.count('"') 
                
    @staticmethod
    def get_quote_count(name):

        '''
        This method returns the total quote character count in the value.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''

        return name.count("'") 
                
        
    @staticmethod
    def get_comma_count(name):

        '''
        This method returns the total comma character count in the value.
        
        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return name.count(',') 
        

    @staticmethod
    def get_nonalpha_count(name):
        
        '''
        This method returns the total non-alphanumeric character count in the value.
        
        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        return len([c for c in name if c.isalnum() == False])
        

    @staticmethod
    def get_multiplenonalpha_count(name):

        '''
        This method returns the total count of the words that has more than 1 non-alphanumeric characters in it.

        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number
        
        '''
        
        count = 0
        for t in name.split(): 
            nonalphacount = len([c for c in t if c.isalnum() == False])
            if nonalphacount > 1:
                count += 1
        
        return count        
        


    @staticmethod
    def get_duplicate_count(name):
        
        '''
        This method returns the adjacent dublicate character count in the name value.
        
        :param name: the string value with one or multiple word to process 

        :rtype int: it returns a integer value zero or positive number

        '''

        length = len(name)
        lettersfirst = name[:length-1]
        lettersnext = name[1:]
        return len([pos for pos in range(0, length-1) if lettersfirst[pos] == lettersnext[pos]])


    @staticmethod
    def get_positives_count(list):
        
        '''
        This method returns the total number of items in the list that has positive value.

        :param list: the list that contains the numeric values 

        :rtype int: it returns a integer value zero or positive number

        '''
        
        return len([1 for c in list if c > 0])


    @staticmethod
    def get_logarithm(value):
        
        '''
        This method returns the logarithm value of the given parameter in base 10.

        :param value: the numeric value to be processed 

        :rtype float: it returns a float number
        
        
        '''
        
        return math.log10(value)



    @staticmethod
    def get_scaled_sum(list):
        
        '''
        This method returns the sum of the list items.
        
        :param list: list of numeric items

        :rtype float: it returns a float number

        '''
        
        return sum(list)


    @staticmethod
    def get_variation_list_group():
        
        '''
        This method returns the variation name and varition group.
        
        :param: it has no parameters
        
        :rtype Pandas.DataFrame: it returns a pandas dataframe
        
        '''

        allvariators = params.variators
        
        variation_name = []
        variation_group = []
        
        for key, value in allvariators.items():        
            variation_name.append(key)
            variation_group.append(value['Variation_Group'])

        df = pd.DataFrame()
        df['Variation_Name'] = variation_name
        df['Variation_Group'] = variation_group
        
        return df    
                

    @staticmethod
    def get_variation_list(error_depth):
        
        '''
        This method returns the enabled list for the given error depth.
        
        :param error_depth: this is the error_depth value

        :rtype list: it returns list of strings that contains the variation names
        
        '''

        allvariators = params.variators
        
        variators = []
        var_id_map = {}
        for key, value in allvariators.items():        
            var_id_map[key] = value["id"]
            if error_depth == 1 and value['ErrorDepth1'] == 'Y':
                variators.append(key)
            elif error_depth == 2 and value['ErrorDepth2'] == 'Y':
                variators.append(key)
            elif error_depth == 3 and value['ErrorDepth3'] == 'Y':
                variators.append(key)
                
        return variators, var_id_map        
                


    @staticmethod
    def do_soundex(value):
        
        '''
        This method calculates and returns a soundex synonym word for the given word.
        
        :param value: the string value to be processed
        
        :rtype str: it returns a string value or None
        
        '''
        
        change_count = 0
        
        if len(value) < 4:
            return None
            
        group1_letters = 'BPFV'
        group2_letters = 'CSKGJQXZ'
        group3_letters = 'DT'
        group4_letters = 'MN'
        disregard_letters = 'AEIOUWYH'
        
        # chose one of the letters from each group and replace with another in the same group
        s = list(value)

        indexes = [pos for pos, c in enumerate(value) if c in group1_letters and pos > 0]
        if len(indexes) > 0:
            rand_index = random.choice(indexes)
            s[rand_index] = SanctionUtility.change_letter_from_list(s[rand_index], group1_letters.replace(s[rand_index], ''))
            change_count += 1


        indexes = [pos for pos, c in enumerate(s) if c in group2_letters and pos > 0]
        if len(indexes) > 0:
            rand_index = random.choice(indexes)
            s[rand_index] = SanctionUtility.change_letter_from_list(s[rand_index], group2_letters.replace(s[rand_index], ''))
            change_count += 1

        if change_count < 2:
            indexes = [pos for pos, c in enumerate(s) if c in group3_letters and pos > 0] 
            if len(indexes) > 0:
                rand_index = random.choice(indexes)
                s[rand_index] = SanctionUtility.change_letter_from_list(s[rand_index], group3_letters.replace(s[rand_index], ''))
                change_count += 1
            

        if change_count < 2:
            indexes = [pos for pos, c in enumerate(s) if c in group4_letters and pos > 0]
            if len(indexes) > 0:
                rand_index = random.choice(indexes)
                s[rand_index] = SanctionUtility.change_letter_from_list(s[rand_index], group4_letters.replace(s[rand_index], ''))
                change_count += 1
            
            
        if change_count < 2:
            indexes = [pos for pos, c in enumerate(s) if c in disregard_letters and pos > 0]
            if len(indexes) > 0:
                rand_index = random.choice(indexes)
                del s[rand_index]
                change_count += 1
            
            
        if change_count < 2:
            indexes = [pos for pos, c in enumerate(s) if c in disregard_letters and pos > 0]
            if len(indexes) > 0:
                rand_index = random.choice(indexes)
                s[rand_index] = SanctionUtility.change_letter_from_list(s[rand_index], disregard_letters.replace(s[rand_index], ''))
                change_count += 1

        
        new_value = ''.join(s)
        
        if new_value == value:
            return None
        else:
            return new_value
        

    @staticmethod
    def do_metaphone(value):
        
        '''
        This method calculates and returns a metaphone similar word for the given word.

        :param value: the string value to be processed
        
        :rtype str: it returns a string value or None

        '''
        
        change_count = 0
        pat = ''
        
        if len(value) < 4:
            return None

         
        # rule 1
        # delete one of the duplicates except c
        
        tmpval = value
        value = value.replace('CC', '$')
        value_old = value         
        pattern = reg.compile(r"(.)\1{1,}",reg.DOTALL)
        value = pattern.sub(r"\1", value)

        if (value_old != value):
            pat = pat + '-' + '1'
            change_count += 1
        value = value.replace('$', 'CC')
            

        # rule 2
        if value[0:2] in ['KN', 'GN', 'PN', 'AE', 'WR']:
            value = value[1:]
            change_count += 1
            pat = pat + '-' + '2'
            
            
        # rule 3    
        if change_count < 2:
            if value[-2:-1] == 'MB':
                value = value[:-1]
                change_count += 1
                pat = pat + '-' + '3'
                
        
        # rule 4
        if change_count < 2:
            if 'SCH' in value:
                value = value.replace('SCH', 'K', 1)
                change_count += 1
                pat = pat + '-' + '4'
                

        if change_count < 2:
            if 'CIA' in value:
                value = value.replace('CIA', 'X', 1)
                change_count += 1
                pat = pat + '-' + '4'


        if change_count < 2:
            if 'CH' in value:
                value = value.replace('CH', 'X', 1)
                change_count += 1
                pat = pat + '-' + '4'

        if change_count < 2:
            if 'CI' in value:
                value = value.replace('CI', 'S', 1)
                change_count += 1
                pat = pat + '-' + '4'

        if change_count < 2:
            if 'CE' in value:
                value = value.replace('CE', 'S', 1)
                change_count += 1
                pat = pat + '-' + '4'

        if change_count < 2:
            if 'CY' in value:
                value = value.replace('CY', 'S', 1)
                change_count += 1
                pat = pat + '-' + '4'

        if change_count < 2:
            if 'CY' in value:
                value = value.replace('C', 'K', 1)
                change_count += 1
                pat = pat + '-' + '4'


        # rule 5
        if change_count < 2:
            if 'DGE' in value:
                value = value.replace('DGE', 'J', 1)
                change_count += 1
                pat = pat + '-' + '5'

        if change_count < 2:
            if 'DGY' in value:
                value = value.replace('DGY', 'J', 1)
                change_count += 1
                pat = pat + '-' + '5'
                

        if change_count < 2:
            if 'DGI' in value:
                value = value.replace('DGI', 'J', 1)
                change_count += 1
                pat = pat + '-' + '5'
                
                

        if change_count < 2:
            if 'D' in value:
                value = value.replace('D', 'T', 1)
                change_count += 1
                pat = pat + '-' + '5'
                

        # rule 6

        if change_count < 2:
            g_indexes =  [pos for pos, c in enumerate(value) if ((c == 'G' and pos < len(value) -2) and (value[pos+1] == 'H') and (value[pos+2] not in constants.VOWELS))]
            if len(g_indexes) > 0:
                delete_index = random.choice(g_indexes) 
                value = SanctionUtility.delete_character(value, delete_index)    
                change_count += 1
                pat = pat + '-' + '6'
                
            

        if change_count < 2:
            g_indexes =  [pos for pos, c in enumerate(value) if ((c == 'G' and pos == len(value) -2 and value[pos+1] == 'N') or (c == 'G' and pos == len(value) -4 and value[pos+1:] == 'NED'))]
            if len(g_indexes) > 0:
                delete_index = random.choice(g_indexes) 
                value = SanctionUtility.delete_character(value, delete_index)    
                change_count += 1
                pat = pat + '-' + '6'
                

        # rule 7
        
        
        if change_count < 2:
            if 'G' in value:
                g_indexes =  [pos for pos, c in enumerate(value) if (c == 'G' and pos < len(value) -1) and (value[pos+1] == 'I' or value[pos+1] == 'E' or value[pos+1] == 'Y')]
                if len(g_indexes) > 0:
                    change_index = random.choice(g_indexes) 
                    value = SanctionUtility.change_character_at(value, change_index, 'J')    
                    change_count += 1
                    pat = pat + '-' + '7'
                    

        if change_count < 2:
            if 'G' in value:
                value = value.replace('G', 'K')
                change_count += 1
                pat = pat + '-' + '7'
                

        # rule 8

        
        if change_count < 2:
            
            if 'H' in value:
                h_indexes =  [pos for pos, c in enumerate(value) if (pos > 0 and c == 'H' and value[pos-1] in constants.VOWELS and (pos == len(value) -1 or (pos < len(value) -1 and value[pos+1] not in constants.VOWELS)))]
                if len(g_indexes) > 0:
                    change_index = random.choice(g_indexes) 
                    value = SanctionUtility.change_character_at(value, change_index, 'J')    
                    change_count += 1
                    pat = pat + '-' + '8'
                    

        # rule 9

        if change_count < 2:
            if 'CK' in value:
                value = value.replace('CK', 'K', 1)
                change_count += 1
                pat = pat + '-' + '9'


        # rule 10

        if change_count < 2:
            if 'PH' in value:
                value = value.replace('PH', 'F', 1)
                change_count += 1
                pat = pat + '-' + '10'
                


        # rule 11
        if change_count < 2:
            if 'Q' in value:
                value = value.replace('Q', 'K', 1)
                change_count += 1
                pat = pat + '-' + '11'
                


        # rule 12

        if change_count < 2:
            if 'SH' in value:
                value = value.replace('SH', 'X', 1)
                change_count += 1
                pat = pat + '-' + '12'
                

        if change_count < 2:
            if 'SIO' in value:
                value = value.replace('SIO', 'X', 1)
                change_count += 1
                pat = pat + '-' + '12'
                

        if change_count < 2:
            if 'SIA' in value:
                value = value.replace('SIA', 'X', 1)
                change_count += 1
                pat = pat + '-' + '12'
                

        # rule 13

        if change_count < 2:
            if 'TIA' in value:
                value = value.replace('TIA', 'X', 1)
                change_count += 1
                pat = pat + '-' + '13'
                
        
        if change_count < 2:
            if 'TIO' in value:
                value = value.replace('TIO', 'X', 1)
                change_count += 1
                pat = pat + '-' + '13'
                
                
        if change_count < 2:
            tch_index = value.find('TCH')
            if tch_index >= 0:
                value = SanctionUtility.delete_character(value, tch_index)
                change_count += 1
                pat = pat + '-' + '13'
                

        # rule 14

        if change_count < 2:
            if 'V' in value:
                value = value.replace('V', 'F', 1)
                change_count += 1
                pat = pat + '-' + '14'
                
        
        
        # rule 15

        if change_count < 2:
            if value[0:2] == 'WH':
                value = SanctionUtility.delete_character(value, 1)
                change_count += 1
                pat = pat + '-' + '15'
                
    
            
        if change_count < 2:
            w_indexes =  [pos for pos, c in enumerate(value) if ((c == 'W' and pos == len(value) -1) or (c == 'W' and pos < len(value) -1 and value[pos+1] not in constants.VOWELS))]
            if len(w_indexes) > 0:
                delete_index = random.choice(w_indexes) 
                value = SanctionUtility.delete_character(value, delete_index)    
                change_count += 1
                pat = pat + '-' + '15'
                


        # rule 16
        
        if change_count < 2:
            if value[0] == 'X':
                value = SanctionUtility.change_character_at(value, 0, 'S')
                change_count += 1
                pat = pat + '-' + '16'
                


        if change_count < 2:
            x_indexes = [pos for pos, c in enumerate(value) if c == 'X']
            if len(x_indexes) > 0:
                change_index = random.choice(x_indexes)
                value = SanctionUtility.change_character_at(value, change_index, 'KS')                
                change_count += 1
                pat = pat + '-' + '16'
                


        # rule 17 - # Drop 'Y' if not followed by a vowel.
        if change_count < 2:
            if 'Y' in value:
                y_indexes = [pos for pos, c in enumerate(value) if ((c == 'Y' and pos == len(value) -1) or (c == 'Y' and pos < len(value) -1 and value[pos+1] not in constants.VOWELS))]
                if len(y_indexes) > 0: 
                    delete_index = random.choice(y_indexes) 
                    value = SanctionUtility.delete_character(value, delete_index)    
                    change_count += 1
                    pat = pat + '-' + '17'


        
        # rule 18

        if change_count < 2:
            if 'Z' in value:
                value = value.replace('Z', 'S', 1)
                change_count += 1
                pat = pat + '-' + '18'
                

        # rule 19 
        if change_count < 2:
            vowel_indexes = [pos for pos, c in enumerate(value) if c in constants.VOWELS and pos > 0]
            if len(vowel_indexes) > 0:
                delete_index = random.choice(vowel_indexes)
                value = SanctionUtility.delete_character(value, delete_index)    
                change_count += 1
                pat = pat + '-' + '19'
                

        
        if change_count > 1 and len(value) > 2:
            return value
        else:
            return None
        




    # this is the original metaphone algorithm not the double-metaphone
    # 1- Drop duplicate adjacent letters, except for C.
    # 2- If the word begins with 'KN', 'GN', 'PN', 'AE', 'WR', drop the first letter.
    # 3- Drop 'B' if after 'M' at the end of the word.
    # 4- 'C' transforms to 'X' if followed by 'IA' or 'H' (unless in latter case, it is part of '-SCH-', in which case it transforms to 'K'). 'C' transforms to 'S' if followed by 'I', 'E', or 'Y'. Otherwise, 'C' transforms to 'K'.
    # 5- 'D' transforms to 'J' if followed by 'GE', 'GY', or 'GI'. Otherwise, 'D' transforms to 'T'.
    # 6- Drop 'G' if followed by 'H' and 'H' is not at the end or before a vowel. Drop 'G' if followed by 'N' or 'NED' and is at the end.
    # 7- 'G' transforms to 'J' if before 'I', 'E', or 'Y', and it is not in 'GG'. Otherwise, 'G' transforms to 'K'.
    # 8 - Drop 'H' if after vowel and not before a vowel.
    # 9 - 'CK' transforms to 'K'.
    # 10- 'PH' transforms to 'F'.
    # 11 - 'Q' transforms to 'K'.
    # 12 - 'S' transforms to 'X' if followed by 'H', 'IO', or 'IA'.
    # 13 - 'T' transforms to 'X' if followed by 'IA' or 'IO'. 'TH' transforms to '0'. Drop 'T' if followed by 'CH'.
    # 14 - 'V' transforms to 'F'.
    # 15 - 'WH' transforms to 'W' if at the beginning. Drop 'W' if not followed by a vowel.
    # 16 - 'X' transforms to 'S' if at the beginning. Otherwise, 'X' transforms to 'KS'.
    # 17 - Drop 'Y' if not followed by a vowel.
    # 18 - 'Z' transforms to 'S'.
    # 19 - Drop all vowels unless it is the beginning. +

# this is an alternative variator for double-metaphone
# as double-metaphone rule set is much more complex, so we will use this one for the beginning
# and implement a soundex version of it
