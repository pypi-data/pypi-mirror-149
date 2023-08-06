# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 07/03/2019
# Project Name: Toolkit Sanction

'''
Module Summary: This module is used for implementing the variator functions for all of the variators.
**All of the variator functions have the same structure and interface** so that all of them can be called by same reflector function.
Before doing the variation, each variator function checks the values and parameters for applicability.

All functions returns 2 values: First is name value after variation and the second is title value after variation.
Functions return None, None if the function is not applicable for the values or parameters.

Parameters for all functions:

    - value: This is the input value for the name field to be variated for name variations that can be applied on name field.
    - title: This is the input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    - entitytype: This is the entity type for the record to be variated. It can be one of the E/I E: Entity, I:Individual
    - position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    - location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    - runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

'''


import pandas as pd
import random
import re as reg
import math
# import phonetics
import inflect
inflect_engine = inflect.engine()

import numpy as np

from config import constants, params

from sanction_utility import SanctionUtility


def insert_a_letter(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a random letter into the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    new_letter = SanctionUtility.get_random_letter()

    # RUNTYPE_RANDOM always called with position = 0 and location = LOCATION_NA

    if runtype == constants.RUNTYPE_RANDOM:

        insert_location = random.choice(range(0, len(value) + 1))
        value = SanctionUtility.insert_string(value, new_letter, insert_location)
        return value, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        if location == constants.LOCATION_BEGIN:
            insert_location = 0
        elif location == constants.LOCATION_END:
            insert_location = len(tokens[position-1])
        elif location == constants.LOCATION_MIDDLE:

            if len(tokens[position-1]) < 2:
                return None, None

            insert_location = random.choice(range(1, len(tokens[position-1])))

        elif location == constants.LOCATION_NA:
            return None, None


        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], new_letter, insert_location)
        return ' '.join(tokens), title

    return None, None


def insert_a_number(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a random number into the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if entitytype == constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    selected_number = SanctionUtility.get_random_number()
    insert_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        insert_location = random.choice(range(0, len(value) + 1))
        value = SanctionUtility.insert_string(value, selected_number, insert_location)
        return value, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        if location == constants.LOCATION_BEGIN:
            insert_location = 0

        elif location == constants.LOCATION_END:
            insert_location = -1

        elif location == constants.LOCATION_MIDDLE:

            if len(tokens[position-1]) < 2:
                return None, None

            insert_location = random.choice(range(1, len(tokens[position-1])))

        elif location == constants.LOCATION_NA:
            return None, None

        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], selected_number, insert_location)
        return ' '.join(tokens), title

    return None, None


def change_a_letter(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random letter at the position and location decided by the parameters with another random letter.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    letters = (constants.LETTERS)
    change_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        letter_indexes = [pos for pos, c in enumerate(value) if c in constants.LETTERS and c.isupper() == True]

        if len(letter_indexes) == 0:
            return None, None

        change_location = random.choice(letter_indexes)

        s[change_location] = SanctionUtility.change_letter(s[change_location])
        return ''.join(s), title


    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')
        s = list(tokens[position-1])

        if position > len(tokens):
            return None, None

        if location == constants.LOCATION_BEGIN:

            change_location = 0

            if s[change_location] not in letters:
                return None, None

        elif location == constants.LOCATION_END:

            change_location = -1

            if s[change_location] not in letters:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            letter_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in constants.LETTERS and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(letter_indexes) == 0:
                return None, None

            change_location = random.choice(letter_indexes)

        elif location == constants.LOCATION_NA:
            return None, None


        s[change_location] = SanctionUtility.change_letter(s[change_location])
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title


    return None, None


def change_a_vowel(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random vowel at the position and location decided by the parameters with another random vowel.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    vowels = (constants.VOWELS)

    if len(list(set(vowels) & set(value))) == 0: # no vowels
        return None, None

    change_location = -1


    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        vowel_indexes = [pos for pos, c in enumerate(value) if c in vowels]

        if len(vowel_indexes) == 0:
            return None, None

        change_location = random.choice(vowel_indexes)
        s[change_location] = SanctionUtility.change_vowel(s[change_location])
        return ''.join(s), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            change_location = 0

            if s[change_location] not in vowels:
                return None, None

        elif location == constants.LOCATION_END:

            change_location = -1

            if s[change_location] not in vowels:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            vowel_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in vowels and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(vowel_indexes) == 0:
                return None, None

            change_location = random.choice(vowel_indexes)

        elif location == constants.LOCATION_NA:
            return None, None


        s[change_location] = SanctionUtility.change_vowel(s[change_location])
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title


    return None, None


def change_a_letter_by_number(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random letter at the position and location decided by the parameters with a random number.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.


    '''

    if entitytype == constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    letters = (constants.LETTERS)
    change_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        letter_indexes = [pos for pos, c in enumerate(value) if c in constants.LETTERS]

        if len(letter_indexes) == 0:
            return None, None

        change_location = random.choice(letter_indexes)
        s[change_location] = SanctionUtility.change_letter_by_number((s[change_location]).upper())
        return ''.join(s), title


    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            change_location = 0

            if s[change_location] not in letters:
                return None, None

        elif location == constants.LOCATION_END:

            change_location = -1

            if s[change_location] not in letters:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            letter_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in constants.LETTERS and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(letter_indexes) == 0:
                return None, None

            change_location = random.choice(letter_indexes)

        elif location == constants.LOCATION_NA:
            return None, None


        s[change_location] = SanctionUtility.change_letter_by_number(s[change_location])
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title


    return None, None


def change_a_number(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random number at the position and location decided by the parameters with a random another number.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''


    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if location == constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    s = list(value)
    digit_indexes = [pos for pos, c in enumerate(value) if c.isdigit() == True]

    if len(digit_indexes) == 0:
        return None, None

    change_location = random.choice(digit_indexes)
    s[change_location] = SanctionUtility.change_number(s[change_location])
    return ''.join(s), title

def change_a_number_to_numberword(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random number at the position and location decided by the parameters with to its spelt name.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if location == constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    s = list(value)
    digit_indexes = [pos for pos, c in enumerate(value) if c.isdigit() == True]

    if len(digit_indexes) == 0:
        return None, None

    r = r"[0-9]+"
    nums = reg.findall(r, value)
    num_words = [inflect_engine.number_to_words(i) for i in nums]
    indices = [(m.start(0), m.end(0)) for m in reg.finditer(r, value)]
    indices_int = np.random.randint(len(indices))
    ind_start_end = indices[indices_int]
    start = ind_start_end[0]
    end = ind_start_end[1]
    value = value.replace(value[start:end], " "+num_words[indices_int]+" ").strip().replace("  ", " ")
    return value, title

def change_spaces_with_fullstop(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces all spaces with full stops.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if value.count(' ') < 2: # there should be at least 2 spaces
        return None, None

    return value.replace(' ', '.'), title


def change_a_number_by_letter(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random number at the position and location decided by the parameters with a random letter.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    s = list(value)
    digit_indexes = [pos for pos, c in enumerate(value) if c.isdigit() == True]

    if len(digit_indexes) == 0:
        return None, None

    change_location = random.choice(digit_indexes)
    s[change_location] = SanctionUtility.get_random_letter()
    return ''.join(s), title


def missing_word(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method randomly deletes one of the words from the value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 2:
        return None, None

    if runtype == constants.RUNTYPE_RANDOM:
        selected_position = random.choice(range(0, len(tokens)))
        del tokens[selected_position]
        return ' '.join(tokens), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:
        selected_position = position - 1
        del tokens[selected_position]
        return ' '.join(tokens), title

    return None, None


def added_word(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a random word at the position decided by the parameters. The inserted word is being selected from entity type related dictionary files.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    # TODO: We do not need to read dictionary files, just read int global variables once

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    if runtype == constants.RUNTYPE_RANDOM:

        if entitytype == constants.ENTITY_TYPE_INDIVIDUAL:

            arabic_word_list = [line.rstrip('\n') for line in open(constants.ARABIC_NAME_WORDS_PATH)]
            arabic_tokens = [t for t in tokens if t in arabic_word_list]

            if len(arabic_tokens) > 0:
                word_list = arabic_word_list.copy()
            else:
                with open(constants.DICTIONARY_FIRSTNAME_PATH) as f:
                    word_list = f.read().splitlines()
        else:
            with open(constants.DICTIONARY_COMPANYNAME_PATH) as f:
                word_list = f.read().splitlines()

        selected_word = random.choice(word_list)

        selected_position = random.choice(range(0, len(tokens) + 1))
        tokens.insert(selected_position, selected_word)
        return ' '.join(tokens), title
    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        if entitytype == constants.ENTITY_TYPE_INDIVIDUAL:

            arabic_word_list = [line.rstrip('\n') for line in open(constants.ARABIC_NAME_WORDS_PATH)]
            arabic_tokens = [t for t in tokens if t in arabic_word_list]

            if len(arabic_tokens) > 0:
                word_list = arabic_word_list.copy()
            else:
                with open(constants.DICTIONARY_FIRSTNAME_PATH) as f:
                    word_list = f.read().splitlines()
        else:
            with open(constants.DICTIONARY_COMPANYNAME_PATH) as f:
                word_list = f.read().splitlines()

        selected_word = random.choice(word_list)

        selected_position = position - 1
        tokens.insert(selected_position, selected_word)
        return ' '.join(tokens), title

    return None, None


def delete_a_space(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes one of the spaces between the value words randomly.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if ' ' not in value:
        return None, None


    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)
        space_indexes = [pos for pos, c in enumerate(value) if c == ' ']
        delete_location = random.choice(space_indexes)
        del s[delete_location]
        return ''.join(s), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        s = list(value)
        space_indexes = [pos for pos, c in enumerate(value) if c == ' ']
        delete_location = random.choice(space_indexes)

        tokens = value.split(' ')

        if position < 1 or position >= len(tokens):
            return None, None

        tokens[position -1] = str(tokens[position -1]) + str(tokens[position])
        del tokens[position]

        return ' '.join(tokens), title

    return None, None


def delete_all_spaces(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes all of the spaces between the value words.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if value.count(' ') < 2: # there should be at least 2 spaces
        return None, None

    return value.replace(' ', ''), title


def delete_a_number(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes a random number from the value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if len(value) < 3:
        return None, None

    s = list(value)

    number_indexes = [pos for pos, c in enumerate(value) if c.isdigit()]

    if len(number_indexes) == 0:
        return None, None

    delete_location = random.choice(number_indexes)
    del s[delete_location]
    return ''.join(s), title


def delete_a_letter(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes a random letter from the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    delete_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        if len(value) < 3:
            return None, None

        letter_indexes = [pos for pos, c in enumerate(value) if c in constants.LETTERS and c.isupper()]

        if len(letter_indexes) == 0:
            return None, None

        delete_location = random.choice(letter_indexes)
        value = SanctionUtility.delete_character(value, delete_location)
        return value, title


    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        if location == constants.LOCATION_BEGIN:
            delete_location = 0

            if value[delete_location] not in constants.LETTERS:
                return None, None

        elif location == constants.LOCATION_END:
            delete_location = len(tokens[position-1]) -1

            if value[delete_location] not in constants.LETTERS:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            if len(tokens[position-1]) < 3:
                return None, None

            letter_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in constants.LETTERS and c.isupper() and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(letter_indexes) == 0:
                return None, None

            delete_location = random.choice(letter_indexes)


        elif location == constants.LOCATION_NA:
            return None, None

        tokens[position-1] = SanctionUtility.delete_character(tokens[position-1], delete_location)
        return ' '.join(tokens), title

    return None, None


def delete_a_character(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes a random character at the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    delete_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        if len(value) < 3:
            return None, None

        delete_location = random.choice(range(0, len(value)))
        value = SanctionUtility.delete_character(value, delete_location)
        return value, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        if location == constants.LOCATION_BEGIN:
            delete_location = 0

        elif location == constants.LOCATION_END:
            delete_location = len(tokens[position-1]) -1

        elif location == constants.LOCATION_MIDDLE:

            if len(tokens[position-1]) < 3:
                return None, None

            delete_location = random.choice(range(1, len(tokens[position-1])-1))

        elif location == constants.LOCATION_NA:
            return None, None


        tokens[position-1] = SanctionUtility.delete_character(tokens[position-1], delete_location)
        return ' '.join(tokens), title


    return None, None


def change_hyphen_by_space(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes one of the hyphen characters with space.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location == constants.LOCATION_NA or position != 0 :
        return None, None

    if constants.HYPHEN not in value and constants.EN_DASH not in value and constants.EM_DASH not in value:
        return None, None


    s = list(value)
    hyphen_indexes = [pos for pos, c in enumerate(value) if (c == constants.HYPHEN or c == constants.EN_DASH or c == constants.EM_DASH)]
    change_location = random.choice(hyphen_indexes)
    s[change_location] = ' '
    return ''.join(s), title


def delete_hyphen(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes one of the hyphen characters randomly.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if constants.HYPHEN not in value and constants.EN_DASH not in value and constants.EM_DASH not in value:
        return None, None

    s = list(value)
    hyphen_indexes = [pos for pos, c in enumerate(value) if (c == constants.HYPHEN or c == constants.EN_DASH or c == constants.EM_DASH)]
    delete_location = random.choice(hyphen_indexes)
    del s[delete_location]
    return ''.join(s), title


def insert_hyphen(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a hyphen character into the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if runtype == constants.RUNTYPE_RANDOM:

        insert_location = random.choice(range(1, len(value) + 1))
        value = SanctionUtility.insert_string(value, constants.HYPHEN, insert_location)
        return value, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 and location == constants.LOCATION_NA:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        insert_location = random.choice(range(0, len(tokens[position-1])))
        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], constants.HYPHEN, insert_location)
        return ' '.join(tokens), title

    return None, None


def change_apostrophe_by_space(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random hyphen character at the position and location decided by the parameters with space character.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if "'" not in value:
        return None, None

    s = list(value)
    apostrophe_indexes = [pos for pos, c in enumerate(value) if c == '\'' and pos != 0]
    if len(apostrophe_indexes) > 0:
        change_location = random.choice(apostrophe_indexes)
        s[change_location] = ' '
        return ''.join(s), title

    return None, None

def change_ampersand_to_and(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random ampersand character at the position and location decided by the parameters with 'and'.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if "&" not in value:
        return None, None

    s = list(value)
    ampersand_indexes = [pos for pos, c in enumerate(value) if c == '&' and pos != 0]
    if len(ampersand_indexes) > 0:
        change_location = random.choice(ampersand_indexes)
        s[change_location] = 'AND'
        return ''.join(s), title

    return None, None

def change_and_to_ampersand(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes a random ampersand character at the position and location decided by the parameters with 'and'.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if " and " not in value or " AND ":
        return None, None

    s = value.split(' ')
    and_indexes = [pos for pos, c in enumerate(s) if (c == 'and' and pos != 0) or (c == 'AND' and pos != 0)]
    if len(and_indexes) > 0:
        change_location = random.choice(and_indexes)
        s[change_location] = '&'
        return ' '.join(s), title

    return None, None


def insert_apostrophe(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a random aposthrophe characater into the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if runtype == constants.RUNTYPE_RANDOM:
        insert_location = random.choice(range(0, len(value)))
        value = SanctionUtility.insert_string(value, "'", insert_location)
        return value, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        insert_location = random.choice(range(0, len(tokens[position-1])))
        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], "'", insert_location)
        return ' '.join(tokens), title

    return None, None


def delete_apostrophe(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes one of the aposthrophe characters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA or position != 0:
        return None, None

    if "'" not in value:
        return None, None

    s = list(value)
    apostrophe_indexes = [pos for pos, c in enumerate(value) if c == '\'']
    delete_location = random.choice(apostrophe_indexes)
    del s[delete_location]
    return ''.join(s), title


def initialize_a_word(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method initializes (just keep the first letter of the word and delete the other) one of the value words at the position decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA :
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 2:
        return None, None

    if runtype == constants.RUNTYPE_RANDOM:

        token_indexes = [pos for pos, t in enumerate(tokens) if len(t) > 1]

        if len(token_indexes) == 0:
            return None, None

        selected_token_index = random.choice(token_indexes)

        if tokens[selected_token_index][:1] not in constants.LETTERS:
            return None, None

        tokens[selected_token_index] = tokens[selected_token_index][:1]
        return ' '.join(tokens), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 :

        selected_token_index = position - 1

        if len(tokens[selected_token_index]) < 2:
            return None, None

        if tokens[selected_token_index][:1] not in constants.LETTERS:
            return None, None

        tokens[selected_token_index] = tokens[selected_token_index][:1]
        return ' '.join(tokens), title

    return None, None


def partial_word(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method truncates (just keep some first letter of the word and delete the other) one of the value words at the position decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    tokens = value.split(' ')

    if runtype == constants.RUNTYPE_RANDOM:

        token_indexes = [pos for pos, t in enumerate(tokens) if len(t) > 3]

        if len(token_indexes) == 0:
            return None, None

        selected_token_index = random.choice(token_indexes)
        new_length = math.ceil(len(tokens[selected_token_index]) / 2)
        tokens[selected_token_index] = tokens[selected_token_index][:new_length]
        return ' '.join(tokens), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 :

        selected_token_index = position - 1

        if len(tokens[selected_token_index]) < 4:
            return None, None

        new_length = math.ceil(len(tokens[selected_token_index]) / 2)
        tokens[selected_token_index] = tokens[selected_token_index][:new_length]
        return ' '.join(tokens), title

    return None, None


def insert_duplicated_character(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method duplicates one of the characters at the postion and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    duplicate_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        duplicate_loc_options = [pos for pos, c in enumerate(value) if (pos < len(value) and c != ' ')]

        if len(duplicate_loc_options) == 0:
            return None, None

        duplicate_location = random.choice(duplicate_loc_options)

        value = SanctionUtility.insert_string(value, value[duplicate_location], duplicate_location)
        return value, title


    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        if location == constants.LOCATION_BEGIN:
            duplicate_location = 0

        elif location == constants.LOCATION_END:

            duplicate_location = -1

            if len(tokens[position-1]) < 2:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            if len(tokens[position-1]) < 3:
                return None, None

            duplicate_location = random.choice(range(1, len(tokens[position-1] ) -1))

        elif location == constants.LOCATION_NA:
            return None, None

        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], tokens[position-1][duplicate_location], duplicate_location)
        return ' '.join(tokens), title

    return None, None


def delete_a_duplicate(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes one of the adjacent dublicate character pairs.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if runtype == constants.RUNTYPE_RANDOM:

        pattern = reg.compile(r"(.)\1{1,}",reg.DOTALL)
        value_new = pattern.sub(r"\1", value)

        if (value_new != value):
            return value_new, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 :

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        pattern = reg.compile(r"(.)\1{1,}",reg.DOTALL)
        value_new = pattern.sub(r"\1", tokens[position - 1])

        if value_new != tokens[position - 1]:
            tokens[position - 1] = value_new
            return ' '.join(tokens), title

    return None, None


def insert_space(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a space character at the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if len(value) < 2:
        return None, None

    if runtype == constants.RUNTYPE_RANDOM:

        insert_location = random.choice(range(1, len(value)))
        value = SanctionUtility.insert_string(value, ' ', insert_location)
        return value, title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 :

        tokens = value.split(' ')

        if len(tokens[position -1]) < 2:
            return None, None

        insert_location = random.choice(range(1, len(tokens[position-1])))
        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], ' ', insert_location)
        value = ' '.join(tokens)
        return value, title

    return None, None


def double_metaphone(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the value words with another word that has the same double-metaphone value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    # to do: this is one of the slowest variators. it must be reviewed as metaphone variations.

    if 1==1:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    if position == 0 and location == constants.LOCATION_NA:

        if entitytype == constants.ENTITY_TYPE_INDIVIDUAL:
            with open(constants.FIRSTNAMES_FILEPATH) as f:
                names = f.read().splitlines()
        else:
            with open(constants.COMPANYNAMES_FILEPATH) as f:
                names = f.read().splitlines()

        for i, t in enumerate(tokens):

            for name in names:
                print("hello")
                # TODO: Check this part as it is in Metaphone
                # metaphone1 = list(phonetics.dmetaphone(name))
                # metaphone2 = list(phonetics.dmetaphone(t))
                
                print(metaphone1)
                print(name)
                
                print(metaphone2)
                print(t)
                
                input()

                inters = list(set(metaphone1) & set(metaphone2))

                # CHECK
                #   if metaphone1 == metaphone2 and name != t and len(name) > 3 and len(t) > 3: # putted len > 3 to ignore short doublemetaphones
                if len(inters) > 1 and name != t :
                    tokens[i] = name
                    return ' '.join(tokens), title

    return None, None


def metaphone(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the value words with another word that has the same metaphone value.
    The metaphone similar word is being created randomly in compatible with the initial metaphone algorithm design.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    token_indexes = list(range(0, len(tokens)))
    random.shuffle(token_indexes) # to make a change on a radowm word, not always a change on the first words

    for i in token_indexes:

        token_metaphone = SanctionUtility.do_metaphone(tokens[i])
        if token_metaphone is not None:
            tokens[i] = token_metaphone
            return ' '.join(tokens), title

    return None, None


def swap_similar_sounds(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the value words with another word that has the same soundex code.
    The soundex similar word is being created randomly in compatible with the initial soundex algorithm design.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    token_indexes = list(range(0, len(tokens)))
    random.shuffle(token_indexes) # to make a change on a radowm word, not always a change on the first words

    for i in token_indexes:

        token_soundex = SanctionUtility.do_soundex(tokens[i])
        if token_soundex is not None:
            tokens[i] = token_soundex
            return ' '.join(tokens), title

    return None, None


def replace_special_pairs(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the special letters with one of the corresponding letters defined in the algorithm.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    pairs = {'B' : ['P'],
        'C' : ['S', 'K'],
        'D' : ['T'],
        'T' : ['D'],
        'G' : ['J'],
        'J' : ['G'],
        'M' : ['N'],
        'N' : ['M'],
        'S' : ['C', 'Z'],
        'I' : ['Y'],
        'Y' : ['I'],
        'K' : ['Q'],
        'Q' : ['K'],
        'V' : ['W'],
        'W' : ['V'] ,
        'Z' : ['S']
    }

    s = list(value)
    special_indexes = [pos for pos, c in enumerate(value) if c.upper() in pairs.keys()]

    if len(special_indexes) == 0:
        return None, None

    change_location = random.choice(special_indexes) # TODO: Check here, getting erro
    s[change_location] = random.choice(pairs.get(s[change_location].upper()))
    return ''.join(s), title


def change_visual_similar_characters(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the visual similar characters with one of the corresponding characters defined in the variation.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    pairs = {
        'A' : ['4'],
        'b' : ['6'],
        'B' : ['8'],
        'E' : ['3'],
        'g' : ['9'],
        'G' : ['6'],
        'I' : ['1', 'l'],
        'l' : ['1', 'I'],
        'O' : ['0'],
        'q' : ['9'],
        'S' : ['5'],
        'T' : ['7'],
        'Z' : ['2'],
        '0' : ['O'],
        '1' : ['l', 'I'],
        '2' : ['Z'],
        '3' : ['E'],
        '4' : ['A'],
        '5' : ['S'],
        '6' : ['G', 'b'],
        '8' : ['B'],
        '7' : ['T'],
        '9' : ['g', 'q']
    }

    s = list(value)
    special_indexes = [pos for pos, c in enumerate(value) if c.upper() in pairs.keys()]

    if len(special_indexes) == 0:
        return None, None

    change_location = random.choice(special_indexes)
    s[change_location] = random.choice(pairs.get(s[change_location].upper()))
    return ''.join(s), title


def keyboard_change_letter(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the letters with one of the neighbour letters from English QWERTY keyboard.
    The location and position of the change is being decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    letters = (constants.LETTERS)
    change_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        letter_indexes = [pos for pos, c in enumerate(value) if c in constants.LETTERS and c.isupper() == True]

        if len(letter_indexes) == 0:
            return None, None

        change_location = random.choice(letter_indexes)
        s[change_location] = SanctionUtility.get_random_neighbor(s[change_location])
        return ''.join(s), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            change_location = 0

            if s[change_location] not in letters:
                return None, None

        elif location == constants.LOCATION_END:

            change_location = -1

            if s[change_location] not in letters:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            letter_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in constants.LETTERS and c.isupper() == True and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(letter_indexes) == 0:
                return None, None

            change_location = random.choice(letter_indexes)

        elif location == constants.LOCATION_NA:
            return None, None


        s[change_location] = SanctionUtility.get_random_neighbor(s[change_location].upper())
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title


    return None, None


def keyboard_insert_letter(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts one of the neighbour letters from English QWERTY keyboard for the one of the letters in the value.
    The location and position of the change is being decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    letters = (constants.LETTERS)
    insert_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        letter_indexes = [pos for pos, c in enumerate(value) if c in constants.LETTERS and c.isupper() == True]

        if len(letter_indexes) == 0:
            return None, None

        insert_location = random.choice(letter_indexes)
        value = SanctionUtility.insert_string(value, SanctionUtility.get_random_neighbor(value[insert_location]), insert_location)
        return value, title


    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            insert_location = 0

            if s[insert_location] not in letters:
                return None, None

        elif location == constants.LOCATION_END:

            insert_location = -1

            if s[insert_location] not in letters:
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            if len(tokens[position-1]) < 2:
                return None, None

            letter_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in constants.LETTERS and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(letter_indexes) == 0:
                return None, None

            insert_location = random.choice(letter_indexes)

        elif location == constants.LOCATION_NA:
            return None, None


        tokens[position-1] = SanctionUtility.insert_string(tokens[position-1], SanctionUtility.get_random_neighbor(tokens[position-1][insert_location].upper()), insert_location)
        return ' '.join(tokens), title

    return None, None


def letter_lowercase(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes one of the letters to lowercase at the position and location decided by the parameters.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if 1==1:
        return None, None # it is closed because was getting  many errors about tle lookups and all of them must be checked for lowercase and uppercase as well

    letters = (constants.LETTERS)
    change_location = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        letter_indexes = [pos for pos, c in enumerate(value) if c in constants.LETTERS and c.isupper()]

        if len(letter_indexes) == 0:
            return None, None

        change_location = random.choice(letter_indexes)
        s[change_location] = s[change_location].lower()
        return ''.join(s), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            change_location = 0

            if s[change_location] not in letters or s[change_location].isupper():
                return None, None

        elif location == constants.LOCATION_END:

            change_location = -1

            if s[change_location] not in letters or s[change_location].isupper():
                return None, None

        elif location == constants.LOCATION_MIDDLE:

            letter_indexes = [pos for pos, c in enumerate(tokens[position-1]) if c in constants.LETTERS and c.isupper() and pos != len(tokens[position-1]) -1 and pos != 0]

            if len(letter_indexes) == 0:
                return None, None

            change_location = random.choice(letter_indexes)

        elif location == constants.LOCATION_NA:
            return None, None

        s[change_location] = s[change_location].lower()
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title

    return None, None


def swap_characters(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method swaps one of the characters with the following character in the value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    slocation1 = -1
    slocation2 = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        if len(s) < 2:
            return None, None

        swap_loc_options = [pos for pos, c in enumerate(s) if (pos > 0 and pos < len(s) -1 and s[pos] != s[pos+1])]

        if len(swap_loc_options) == 0:
            return None, None

        slocation1 = random.choice(swap_loc_options)
        slocation2 = slocation1 + 1

        s[slocation1], s[slocation2] = s[slocation2], s[slocation1]
        return ''.join(s), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            if len(s) < 2:
                return None, None

            slocation1 = 0
            slocation2 = 1

            if s[slocation1] == s[slocation2]:
                return None, None

        elif location == constants.LOCATION_END:
            return None, None # the self.location = middle covers this

        elif location == constants.LOCATION_MIDDLE:

            if len(s) < 3:
                return None, None

            swap_loc_options = [pos for pos, c in enumerate(s) if (pos > 0 and pos < len(s) -2 and s[pos] != s[pos+1])]

            if len(swap_loc_options) == 0:
                return None, None

            slocation1 = random.choice(swap_loc_options)
            slocation2 = slocation1 + 1

        elif location == constants.LOCATION_NA:
                return None, None

        s[slocation1], s[slocation2] = s[slocation2], s[slocation1]
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title

    return None, None

def swap_characters_2d(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method swaps one of the characters with the following second character in the value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    slocation1 = -1
    slocation2 = -1

    if runtype == constants.RUNTYPE_RANDOM:

        s = list(value)

        if len(s) < 3:
            return None, None

        swap_loc_options = [pos for pos, c in enumerate(s) if (pos < len(s) -2 and s[pos] != s[pos+2])]

        if len(swap_loc_options) == 0:
            return None, None

        slocation1 = random.choice(swap_loc_options)
        slocation2 = slocation1 + 2

        s[slocation1], s[slocation2] = s[slocation2], s[slocation1]
        return ''.join(s), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0:

        tokens = value.split(' ')

        if position > len(tokens):
            return None, None

        s = list(tokens[position-1])

        if location == constants.LOCATION_BEGIN:

            if len(s) < 3:
                return None, None

            slocation1 = 0
            slocation2 = 2

            if s[slocation1] == s[slocation2]: # if both of them are the same no need to swap and create an output
                return None, None

        elif location == constants.LOCATION_END:
            return None, None # there is no swap at the end so it must be return None

        elif location == constants.LOCATION_MIDDLE:

            if len(s) < 4:
                return None, None

            swap_loc_options = [pos for pos, c in enumerate(s) if (pos > 0 and pos < len(s) -3 and s[pos] != s[pos+2])]

            if len(swap_loc_options) == 0:
                return None, None

            slocation1 = random.choice(swap_loc_options)
            slocation2 = slocation1 + 2

        elif location == constants.LOCATION_NA:
            return None, None

        s[slocation1], s[slocation2] = s[slocation2], s[slocation1]
        tokens[position-1] = ''.join(s)
        return ' '.join(tokens), title

    return None, None

def swap_words(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method swaps one of the words with the following word in the value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

#    if location != constants.LOCATION_NA:
#        return None, None

    if runtype == constants.RUNTYPE_RANDOM:

        tokens = value.split(' ')

        if len(tokens) < 2:
            return None, None

        swap_location = random.choice(range(0, len(tokens) -1))
        tokens[swap_location], tokens[swap_location +1] = tokens[swap_location+1], tokens[swap_location]

        return ' '.join(tokens), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 and location == constants.LOCATION_NA:

        tokens = value.split(' ')

        if len(tokens) < 2:
            return None, None

        if position > len(tokens) - 1:
            return None, None

        swap_location = position - 1
        tokens[swap_location], tokens[swap_location +1] = tokens[swap_location+1], tokens[swap_location]

        return ' '.join(tokens), title

    return None, None


def swap_words_2d(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method swaps one of the words with the following second word in the value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if runtype == constants.RUNTYPE_RANDOM:

        tokens = value.split(' ')

        if len(tokens) < 3:
            return None, None

        swap_location = random.choice(range(0, len(tokens) -2))
        tokens[swap_location], tokens[swap_location +2] = tokens[swap_location+2], tokens[swap_location]

        return ' '.join(tokens), title

    elif runtype == constants.RUNTYPE_COMPREHENSIVE and position > 0 and location == constants.LOCATION_NA:

        tokens = value.split(' ')

        if len(tokens) < 3:
            return None, None

        if position > len(tokens) - 2:
            return None, None

        swap_location = position - 1
        tokens[swap_location], tokens[swap_location +2] = tokens[swap_location+2], tokens[swap_location]

        return ' '.join(tokens), title

    return None, None


def punctuation_change(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method deletes or replaces with space one of the comma or dot characters in the name value.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if '.' not in value and ',' not in value:
        return None, None

    s = list(value)
    punc_indexes = [pos for pos, c in enumerate(value) if (c == '.' or c == ',')]
    update_location = random.choice(punc_indexes)

    operation_select = random.choice(range(0,2)) # randomly chose one of either delete it or replace with space

    if operation_select == 0:
        del s[update_location] # delete it
    else:
        s[update_location] = ' '

    s = ''.join(s)
    s = reg.sub('[ ]{2,}', ' ', s)
    return s, title


def company_commonword_change(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes one of the company common words with another one from the related dictionary.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    if entitytype != constants.ENTITY_TYPE_ENTITY:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    with open(constants.COMPANY_COMMONWORDS_FILEPATH) as f:
        words = f.read().splitlines()

    common_word_indexes = [pos for pos, w in enumerate(tokens) if w in words]

    if len(common_word_indexes) == 0:
        return None, None

    selected_word_index = random.choice(common_word_indexes)
    wordstmp = words.copy()
    wordstmp.remove(tokens[selected_word_index])
    tokens[selected_word_index] = random.choice(wordstmp)
    return ' '.join(tokens), title


def company_auxword_change(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes one of the company auxilary words with another one from the related dictionary.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    if entitytype != constants.ENTITY_TYPE_ENTITY:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    with open(constants.COMPANY_AUXWORDS_FILEPATH) as f:
        words = f.read().splitlines()

    common_word_indexes = [pos for pos, w in enumerate(tokens) if w in words]

    if len(common_word_indexes) == 0:
        return None, None

    selected_word_index = random.choice(common_word_indexes)
    wordstmp = words.copy()
    wordstmp.remove(tokens[selected_word_index])
    tokens[selected_word_index] = random.choice(wordstmp)
    return ' '.join(tokens), title


def insert_title(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method inserts a random title from related title dictionary file.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if entitytype != constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    with open(constants.TITLES_FILEPATH) as f:
        titles = f.read().splitlines()

    if title is not None and title in titles:
        titles.remove(title)

    title = title.strip() + ' ' + random.choice(titles).strip()
    return value, title


def delete_title(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method removes the title words completely.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if entitytype != constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    if title is None:
        return None, None

    title = ''
    return value, title


def change_title(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method changes the title with another title from the related title dictionary file.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if position != 0:
        return None, None

    if location != constants.LOCATION_NA:
        return None, None

    if entitytype != constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    if title is None:
        return None, None

    with open(constants.TITLES_FILEPATH) as f:
        titles = f.read().splitlines()

        tokens = title.split()

        if len(tokens) == 0:
            return None, None

        for t in tokens:
            if t in titles:
                titles.remove(t)

        change_index = random.choice(range(0, len(tokens)))
        tokens[change_index] = random.choice(titles)
        title = ' '.join(tokens)

    return value, title.strip()


def word_to_nickname(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method replaces one of the firstnames with one of the corresponding synonym or nicknames from the related dictionary file.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    if entitytype != constants.ENTITY_TYPE_INDIVIDUAL:
        return None, None

    tokens = value.split(' ')

    if len(tokens) < 1:
        return None, None

    synonyms = pd.read_csv(constants.DICTIONARY_FIRSTNAME_SYNONYMS_PATH, engine='python', delimiter = '\t')

    synonyms.columns = ['Name', 'Synonyms']
    synonyms = synonyms.fillna('')

    name_indexes = [pos for pos, w in enumerate(tokens) if w in list(synonyms.Name.values)]

    if len(name_indexes) == 0:
        return None, None

    selected_name_index = random.choice(name_indexes)
    name_synonym = synonyms[synonyms['Name'] == tokens[selected_name_index]]
    tokens[selected_name_index] = random.choice(name_synonym.iloc[0][1].split(',')) # TODO: Check iloc

    return ' '.join(tokens), title


def No_change(value, title, entitytype=constants.ENTITY_TYPE_INDIVIDUAL, position=0, location=constants.LOCATION_RANDOM, runtype = constants.RUNTYPE_COMPREHENSIVE):

    '''
    This method returns the value and title as it is without doing any change to create a baseline for matching.

    :param value: Input value for the name field to be variated for name variations that can be applied on name field.
    :param title: Input value for the title field to be variated for the variations that can be applied on title field. Only valid for the Individuals.
    :param entitytype: Entity type for the record to be variated. It can be one of the E/I. (E: Entity, I:Individual)
    :param position: This is the parameter for word selection to variate. It can be Zero or positive numbers up to the total word count of the name field. It is not used for title variations.
    :param location: It is the location of the variation within the selected word. It can be one of the Begin/Middle/End/Whole.
    :param runtype: It is the parameter for Run Type Random or Comprehensive. It can be one of the R/C. For Random, the location and positon is being selected randomly.

    :rtype: it returns a tuple with two string elements in the format of *(ValueChanged, TitleChanged)*. The return elements either can be a string or *None* value.

    '''

    if location != constants.LOCATION_NA:
        return None, None

    if position != 0:
        return None, None

    return value, title
