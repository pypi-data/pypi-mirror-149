# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Bunyamin Dursun
# Date: 14/02/2019
# Project Name: Toolkit Sanction

'''This is the main module that calls the other modules for different steps of the synthetic data generation.'''

import time
import math
import random
import logging
from datetime import datetime
import numpy as np
import pandas as pd
import re
import string

from reflist_preprocessor_consolidated import RefListPreprocessor
from reflist_profiler import RefListProfiler
from reflist_variator import RefListVariator
from sanction_utility import SanctionUtility
from faker import Faker

import aes
#from sanction_run_faker import SanctionRunFaker
#from sanction_visualizer import SanctionVisualizer

from config import constants, params
import os

# import constant
# import params

class SyntheticDataCreator:

    '''
    This class is the main class that calls the other classed or modules for different steps of the synthetic data generation.
    Basically most of the running parameters come from the params file.
    '''

    def create_data(self):


        '''
        This method calls the other classes or methods step by step to create the Synthetic Sanction Data required.

        - Step 1: Calling download_hmt_list method of the RefListDownloader class to download the HMT List from web url.
        - Step 2: Calling preprocess_list method of the RefListPreprocessor class to run pre-process on the downloaded HMT List.
        - Step 3: Calling profile_list method of the RefListProfiler class to run profiling on the downloaded HMT List.
        - Step 4: Calling variate_list method of the RefListVariator class to run the variations on ErrorDepth1 (ErrorDepth2 and ErrorDepth3)
        - Step 5: Queries synthetic names against a vendor api.
        # removed after phase 1 of project...
        - Step 6: Creating fake run results - This will be changed with loading real run results.
        - Step 7: Interpreting the test run results.
        - Step 8: Visualisations.

        :param: it has no parameters
        :rtype: it has no return value

        '''

        with open(constants.LOG_FILEPATH, 'w'):   # it overwrites the log file otherwise it appends to the current file
            pass

        logging.basicConfig(format='- %(message)s', filename = constants.LOG_FILEPATH, level=logging.INFO)
        self.logger = logging.getLogger("Sanctions")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('Date: ' + str(dt_string))
        self.logger.info('Date: ' + str(dt_string))
        self.logger.info('Synthetic sanctions screening data generation started.')

        #overwrite parameters without editing the params.py file
        self.parameter_overwrite(overwrite = False)
        self.parameter_information()

        # initial reference list is being preprocessed and cleansed
        processor = RefListPreprocessor()
        processor.unchanged_firmvisit()
        processor.preprocess_list()

        # profiling is being done on pre-processed list
        profiler = RefListProfiler()
        profiler.profile_list(filepath = constants.LIST_FILE_PATH_PROCESSED, outfilepath = constants.LIST_FILE_PATH_PROFILED, level = 0)
        
        synth_names, fake_ids = self.generate_synthetic_data()
        
        self.variate_data()
        
        self.add_encrypted_uid()
        
        output_df = self.output_ref_table()
        
        return output_df
        #self.create_fake_results()
        #self.visualize_data()
    
    def output_ref_table(self):
        entries = pd.read_csv(constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, encoding="utf-8", engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True)

        output = entries[["Fullname", "encr_id"]]
        
        synth_df = self.generate_synthetic_data()
        
        print(synth_df)
        
        full_df = pd.concat([output,synth_df])
        
        full_df = full_df.sample(frac=1).reset_index(drop=True)
        now = datetime.now()
        full_df["date"] = now.strftime("%Y%m%d")
        
        full_df.to_csv(constants.METIS_OUTPUT, encoding="utf-8", index=False)
        return full_df
    

    def parameter_information(self):

        '''
        This method was created in order to print/log key information on parameters when running the toolkit.
        
        :param: it has no parameters

        :rtype: it has no return value
        '''
        print('Error Depth: {}'.format(str(params.max_error_depth)))
        self.logger.info('Error Depth: {}'.format(str(params.max_error_depth)))

        print('Unchanged Name Sampling: {}'.format(str(params.unchanged_sample)))
        self.logger.info('Unchanged Name Sampling: {}'.format(str(params.unchanged_sample)))
        
        print('Error Depth Sampling: {}'.format(str(params.sampling)))
        self.logger.info('Error Depth Sampling: {}'.format(str(params.sampling)))



    # def load_sanction_result_data(self):

    #     '''
    #     This method loads the sanction screening result data.
    #     For consistency the initial reference list, and interim files should be kept as it is until the result file be loaded.

    #     :param: it has no parameters

    #     :rtype: it has no return value

    #     '''

    #     # this method must be called 2 or 3 times with suitable parameters for error dept2 and error dept2
    #     faker = SanctionRunFaker()
    #     faker.load_external_screen_results(filepath=constants.SYNTHETIC_DATA_FILE_PATH, reflist_path=constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path=constants.SANCTION_RESULTS_FILE_PATH, error_depth=1)

    #     if params.max_error_depth >= 2:
    #         faker.load_external_screen_results(filepath=constants.SYNTHETIC_DATA_FILE_PATH_D2, reflist_path=constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path=constants.SANCTION_RESULTS_FILE_PATH_D2, error_depth=2)

    #     if params.max_error_depth == 3:
    #         faker.load_external_screen_results(filepath=constants.SYNTHETIC_DATA_FILE_PATH_D3, reflist_path=constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path=constants.SANCTION_RESULTS_FILE_PATH_D3, error_depth=3)

    #     self.visualize_data()


    def parameter_overwrite(self, overwrite):

        '''
        This method was created for testing the toolkit with different parameters. In the industrialisation phase these parameters will be selected via a selection screen GUI.

        :param: it has no parameters

        :rtype: it has no return value

        '''

        if overwrite == False:
            return

        params.max_error_depth = 1 # can be one of the 1/2/3
        params.runtype_error_depth1 = 'R' # can be one of the R/C
        params.runtype_error_depth2 = 'R' # can be one of the R/C
        params.runtype_error_depth3 = 'R' # can be one of the R/C

        params.match_max_count = 2


    def variate_data(self):

        '''
        This method variates the reference list.

        :param: it has no parameters

        :rtype: it has no return value

        '''

        # ErrorDepth1: variations is being created on the preprocessed list
        listvariator = RefListVariator(sampling = params.sampling, max_word_count = params.max_word_count, word_count_exact = params.word_count_exact, entity_types_include = params.entity_types_include)
        listvariator.variate_list(filepath = constants.LIST_FILE_PATH_PROFILED, outfilepath = constants.SYNTHETIC_DATA_FILE_PATH, runtype = params.runtype_error_depth1)


        # ErrorDepth2
        if params.max_error_depth >= 2:
            listvariator.variate_list_additional_level(runtype = params.runtype_error_depth2, infilepath = constants.SYNTHETIC_DATA_FILE_PATH, outfilepath = constants.SYNTHETIC_DATA_FILE_PATH_D2, error_depth = 2)


        # ErrorDepth3
        if params.max_error_depth == 3:
            listvariator.variate_list_additional_level(runtype = params.runtype_error_depth3, infilepath = constants.SYNTHETIC_DATA_FILE_PATH_D2, outfilepath = constants.SYNTHETIC_DATA_FILE_PATH_D3, error_depth = 3)

        listvariator.combine_synthetic_data(russia_only=True)
        listvariator.similarity_metric()
        #listvariator.variation_profiler()
    
    def add_encrypted_uid(self, filepath=constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS):
        t0 = time.time()
        entries = pd.read_csv(filepath, encoding="utf-8", engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True)
        _, var_id_map = SanctionUtility.get_variation_list(1) #argument doesn't matter here
        key = b"zelenskyymetis22"
        iv = b"zelenskyymetis22"
        encr_keys = []
        for i, row in entries.iterrows():
            fca_key = row["fca_uid"]
            
            if row["ErrorDepth"] == 0:
                encrypted = aes.AES(key).encrypt_pcbc(fca_key.encode("utf-8"), iv)
                encrypted_hex = encrypted.hex()
            elif row["ErrorDepth"] == 1:
                v_id = row["Variation_Id"]
                pre_enc_str = "{0}V{1}".format(fca_key, str(v_id))
                encrypted = aes.AES(key).encrypt_pcbc(pre_enc_str.encode("utf-8"), iv)
                encrypted_hex = encrypted.hex()
            else:
                var_path = row["VariationPath"]
                var1 = var_id_map[var_path[:var_path.index("(")]]
                #will return the final variations but not the first. This can be improved with better regex to return all variations.
                remaining = "+".join(["V"+str(var_id_map[x]) for x in re.findall("(?<=>).*?(?=\()", var_path)])
                pre_enc_str = fca_key+"V"+str(var1)+remaining
                encrypted = aes.AES(key).encrypt_pcbc(pre_enc_str.encode("utf-8"), iv)
                encrypted_hex = encrypted.hex()
                
                
            encr_keys.append(encrypted_hex)
            
            
        entries["encr_id"] = encr_keys
        entries.to_csv(filepath, sep='\t', encoding="utf-8")
        t1 = time.time()
        print("Time taken for encrypting keys: {}".format(t1-t0))
    
    def generate_synthetic_data(self, n=20000):
        from russian_names import RussianNames
        from korean_romanizer.romanizer import Romanizer
        
        print("starting russian names")
        
        ru_names = []
        n_russians = int(n/3)
        
        ru_names.extend(RussianNames(count=int(n_russians*0.45), uppercase=True, name_max_len=20, patronymic_max_len=20, surname_max_len=20, transliterate=True, rare=False).get_batch())
        ru_names.extend(RussianNames(count=int(n_russians*0.05), uppercase=True, name_max_len=20, patronymic_max_len=20, surname_max_len=20, transliterate=True, rare=True).get_batch())
        ru_names.extend(RussianNames(count=int(n_russians*0.45), uppercase=True, name_max_len=20, patronymic_max_len=20, surname_max_len=20, transliterate=False, rare=False).get_batch())
        ru_names.extend(RussianNames(count=int(n_russians*0.05), uppercase=True, name_max_len=20, patronymic_max_len=20, surname_max_len=20, transliterate=False, rare=True).get_batch())
        
        print("starting arabic names")
        #arabic
        ar_generic = Faker("ar_AA")
        ar_palestine = Faker("ar_PS")
        ar_saudi = Faker("ar_SA")
        
        ar_names = []
        ar_names.extend([ar_saudi.name() for x in range(int(n/9))])
        ar_names.extend([ar_generic.name() for x in range(int(n/9))])
        ar_names.extend([ar_saudi.name() for x in range(int(n/9))])
        
        #korean
        print("starting korean names")
        ko_fake = Faker("ko_KR")
        ko_names_hangul = [ko_fake.name() for x in range(int(n/3))]
        
        ko_names = []
        for hname in ko_names_hangul:
            split_name = " ".join(list(hname))
            r = Romanizer(split_name)
            ko_names.append(r.romanize().upper())
            
        all_names = ru_names + ar_names + ko_names
        
        #Insert Unique ID
        done = False
        uids = set()
        while not done:
            uids.add("".join(np.random.choice(list(string.digits), size=5)))
            if len(uids) == len(all_names):
                done = True
        uids = list(uids)
        
        key = b"zelenskyymetis22"
        iv = b"zelenskyymetis22"
        encr_uids = []
        for uid in uids:
            encrypted = aes.AES(key).encrypt_pcbc(uid.encode("utf-8"), iv)
            encrypted_hex = encrypted.hex()
            encr_uids.append(encrypted_hex)
        
        return pd.DataFrame({"Fullname": all_names, "encr_id": encr_uids})
        
    
    # def query_names(self):
        
    #     '''
    #     This method queries the synthetic names and unchanged names, if selected, against a vendor api.

    #     :param: it has no parameters

    #     :rtype: it has no return value

    #     '''

    #     api_query = Fincom_API_Query()

    #     if params.unchanged_names == True:
    #         api_query.unchanged_query_loop()
    #         api_query.join_results_check(check_data = constants.UNCHANGED_DATA_FILE_PATH_CHECK, query_data = constants.UNCHANGED_DATA_FILE_PATH_RESULTS, outfilepath = constants.UNCHANGED_DATA_FILE_PATH_FULL_RESULTS, lefton = 'RefId', righton = 'RefId')

    #     api_query.query_loop()
    #     api_query.join_results_check(check_data = constants.FINCOM_QUERY_RESULTS_PATH, query_data = constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, outfilepath = constants.FIRM_QUERY_FULL_RESULTS, lefton = 'RefId', righton = 'RefId')

    # def create_fake_results(self):

    #     '''
    #     This method instantiates the class that creates fake sanction screening results for the initial reference list and the synthetic data created by the tool at the previous steps.
    #     Depending on the error_depth value it can create fake result data for ErrorDepth1 or ErrorDepth2 and ErrorDepth3 as well.

    #     :param: it has no parameters

    #     :rtype: it has no return value

    #     '''


    #     # creating fake test run results.
    #     # To check: getting error for the name values contains double quotes in it

    #     if params.skip_fake_results == True:
    #         print('\nCreating fake run results will be skipped as parameter selected...')
    #         return

    #     faker = SanctionRunFaker()
    #     faker.sanction_screen_fake(filepath=constants.SYNTHETIC_DATA_FILE_PATH, reflist_path=constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path=constants.SANCTION_RESULTS_FILE_PATH, error_depth=1, sanction_mode=constants.SANCTION_MODE_GENERATE)

    #     if params.max_error_depth >= 2 and params.fake_depth2:
    #         faker.sanction_screen_fake(filepath=constants.SYNTHETIC_DATA_FILE_PATH_D2, reflist_path=constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path=constants.SANCTION_RESULTS_FILE_PATH_D2, error_depth=2, sanction_mode=constants.SANCTION_MODE_GENERATE)

    #     if params.max_error_depth == 3 and params.fake_depth3:
    #         faker.sanction_screen_fake(filepath=constants.SYNTHETIC_DATA_FILE_PATH_D3, reflist_path=constants.LIST_FILE_PATH_PROCESSED, sanctionresults_path=constants.SANCTION_RESULTS_FILE_PATH_D3, error_depth=3, sanction_mode=constants.SANCTION_MODE_GENERATE)



    # def visualize_data(self):

    #     '''
    #     This method instantiates the class that creates visualisations and analytics for the initial reference list and the synthetic data created by the tool at the previous steps.
    #     Depending on the error_depth value it can create fake result data for ErrorDepth1 or ErrorDepth2 and ErrorDepth3 as well.

    #     :param: it has no parameters

    #     :rtype: it has no return value

    #     '''

    #     visualizer = SanctionVisualizer()
    #     visualizer.visualize_data(error_depth = 1)

    #     if params.max_error_depth >= 2 and params.visualize_depth2:
    #         visualizer.visualize_data(error_depth = 2)

    #     if params.max_error_depth == 3 and params.visualize_depth3:
    #         visualizer.visualize_data(error_depth = 3)
    
    def transform_to_vmuk(self, filepath=constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, vmuk_in="./SanctionToolkit/reflist/vmuk_sample.txt", vmuk_out="./SanctionToolkit/output/vmuk_output.txt"):
        entries = pd.read_csv(filepath, engine='python', delimiter = '\t', error_bad_lines=False, warn_bad_lines = True) 
        
        sample_cols = ['RUN_TIMESTAMP', 'CUSTOMER_SOURCE_UNIQUE_ID', 'ORGUNIT_CODE', 'CUSTOMER_SOURCE_REF_ID', 'PERSON_TITLE', 'FIRST_NAME', 'MIDDLE_NAMES', 'LAST_NAME', 'SUFFIX', 'CUSTOMER_NAME', 'COMPANY_NAME', 'COMPANY_FORM', 'REGISTERED_NUMBER', 'INCORPORATION_DATE', 'INCORPORATION_COUNTRY_CODE', 'BUSINESS_TYPE', 'BUSINESS_SEGMENT_1', 'BUSINESS_SEGMENT_2', 'INITIALS', 'DATE_OF_BIRTH', 'NAME_OF_BIRTH', 'ADDRESS', 'ZONE', 'CITY', 'POSTAL_CODE', 'COUNTRY_OF_RESIDENCE', 'COUNTRY_OF_ORIGIN', 'NATIONALITY_CODE', 'PLACE_OF_BIRTH', 'GENDER_CODE', 'PRIME_BRANCH_ID', 'RELATIONSHIP_MGR_ID', 'EMPLOYEE_FLAG', 'EMPLOYEE_NUMBER', 'MARITAL_STATUS', 'OCCUPATION', 'EMPLOYMENT_STATUS', 'ACQUISITION_DATE', 'CANCELLED_DATE', 'CUSTOMER_TYPE_CODE', 'CUSTOMER_STATUS_CODE', 'CUSTOMER_SEGMENT_1', 'CUSTOMER_SEGMENT_2', 'CUSTOMER_SEGMENT_3', 'RESIDENCE_FLAG', 'SPECIAL_ATTENTION_FLAG', 'DECEASED_FLAG', 'DORMANT_FLAG', 'DORMANT_OVERRIDE_DATE', 'RISK_SCORE', 'BANKRUPT_FLAG', 'COMPENSATION_REQD_FLAG', 'CUSTOMER_COMPLAINT_FLAG', 'END_RELATIONSHIP_FLAG', 'MERCHANT_NUMBER', 'FACE_TO_FACE_FLAG', 'CHANNEL', 'AGE', 'NEAR_BORDER_FLAG', 'INTENDED_PRODUCT_USE', 'SOURCE_OF_FUNDS', 'COMPLEX_STRUCTURE', 'EXPECTED_ANNUAL_TURNOVER', 'TRADING_DURATION', 'BALANCE_SHEET_TOTAL', 'VAT_NUMBER', 'BROKER_CODE', 'BLACK_LISTED_FLAG', 'DOMAIN_CODE', 'COMMENTS', 'CUSTOMER_RISK', 'PEP_FLAG', 'WIRE_IN_NUMBER', 'WIRE_OUT_NUMBER', 'WIRE_IN_VOLUME', 'WIRE_OUT_VOLUME', 'CASH_IN_VOLUME', 'CASH_OUT_VOLUME', 'CHECK_IN_VOLUME', 'CHECK_OUT_VOLUME', 'OVERALL_SCORE_ADJUSTMENT', 'TAX_NUMBER', 'EMAIL_ADDRESS', 'ADDRESS_TYPE', 'NCA_ADDRESS_LINE_1', 'NCA_ADDRESS_LINE_2', 'NCA_ADDRESS_LINE_3', 'NCA_ADDRESS_LINE_4', 'NCA_ADDRESS_LINE_5', 'NCA_POST_CODE']
        sample = pd.read_csv(vmuk_in, sep="|", names=sample_cols)
        
        output = pd.DataFrame([], columns=sample_cols)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        orgunit = "TST"
        resident = "GB"
        origin = "ZZ"
        customer_type = ["P", "C"]
        customer_status = ["NOVAL", "A"]
        postcode = "AA2 FCA"
        d_flag = "N"
        
        
        
        output["RUN_TIMESTAMP"] = [timestamp for i in range(len(entries))]
        output['CUSTOMER_SOURCE_UNIQUE_ID'] = entries["RefId"]
        output['CUSTOMER_SOURCE_REF_ID'] = entries["RefId"]
        output['ORGUNIT_CODE'] = [orgunit for i in range(len(entries))]
        output['DECEASED_FLAG'] = [d_flag for i in range(len(entries))]
        output["CUSTOMER_NAME"] = entries["Fullname"]
        output['COUNTRY_OF_RESIDENCE'] = [resident for i in range(len(entries))]
        output['COUNTRY_OF_ORIGIN'] = [origin for i in range(len(entries))]
        output['NATIONALITY_CODE'] = [origin for i in range(len(entries))]
        output["NCA_POST_CODE"] = [postcode for i in range(len(entries))]
        output['CUSTOMER_TYPE_CODE'] = [np.random.choice(customer_type) for i in range(len(entries))]
        output['CUSTOMER_STATUS_CODE'] = [np.random.choice(customer_status) for i in range(len(entries))]
        
        output.to_csv(vmuk_out, sep="|", encoding="utf-8", index=False, header=None)


def main():

    '''
    This is the entry point to run the toolkit. This method must be called for running it.

    :param: it has no parameters
    :rtype: it has no return value

    '''

    start_time = time.time()
    sdc = SyntheticDataCreator()

    if params.sanction_mode == constants.SANCTION_MODE_GENERATE:
        print('\nSynthetic Data Generation started...\n')
        df = sdc.create_data()
        elapsed_time = time.time() - start_time
        print('-' * 80 + '\n\n')
        print('Synthetic Data Generation finished in ' + str(math.ceil(elapsed_time)) + ' secs.')

    else:
        print('\nSanction Results Loading started...\n')
        sdc.load_sanction_result_data()
        elapsed_time = time.time() - start_time
        print('-' * 80 + '\n\n')
        print('Sanction Results Loading finished in ' + str(math.ceil(elapsed_time)) + ' secs.')
    return df


if __name__ == '__main__':
    main()

    # run script
    # sudo /home/ec2-user/.local/share/virtualenvs/SanctionToolkit-P6aO8do-/bin/python3.6m SanctionToolkit/synthetic_data_creator.py
