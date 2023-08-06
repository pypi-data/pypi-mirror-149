# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Classification: FCA Restricted
# Author: Rory Hurley
# Date: 03/02/2020
# Project Name: Toolkit Sanction

''' Project Summary: This is a module that queries the fincom API '''

import http.client
import json
import pandas as pd
import os
import collections
import numpy as np
import time
from config import constants, params
import logging
import time
import math
from fuzzywuzzy import fuzz

class Fincom_API_Query:
    '''
    This class queries each synthetically created sanction name against the Fincom API
    '''

    def __init__(self, filepath=constants.SYNTHETIC_DATA_FILE_PATH, outfilepath=constants.FINCOM_QUERY_RESULTS_PATH):
        '''
        This method is the constractor method that assignes the Class level variables.

        :param filepath: This is the path for the synthetic data file to create fake run results on it.
        :param outfilepath: This is the path for file to save the Fincom query results in it.
        :param error_depth: This is the parameter for ErrorDepth. It can be one of the 1/2/3

        :rtype: it has no return value

        '''

        print('-' * 80 + '\n')

        self.logger = logging.getLogger('Sanctions')
        self.logger.info('Fincom API queries started.')

    def query_loop(self, filepath=constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, outfilepath=constants.FINCOM_QUERY_RESULTS_PATH, threshold = constants.FINCOM_THRESHOLD, ml_threshold = constants.FINCOM_ML_THRESHOLD):
        '''
        This method sets the proxies and tunnel to allow for HTTPS connection at the FCA. It then runs each of the synthetic names through the
        vendor api, saving the results to a file.

        :param filepath: synthetic data to be queried
        :param outfilepath: results of queried named
        :param thresholds: threshold specific to the vendor api
        '''

        print('\nSetting proxies and tunnel.')

        #proxies
        os.environ['http_proxy'] = 'http://localhost:3128'
        os.environ['https_proxy'] = 'http://localhost:3128'
        print('\nProxies Set.')

        #tunnel
        conn = http.client.HTTPSConnection("localhost", 3128)
        conn.set_tunnel("fca.explore.fincom.co")
        conn.request("GET", "/")
        r1 = conn.getresponse()
        data1 = r1.read()
        print('\nTunnel Set.')

        # authentication
        print("\nAuthenticating...")

        payload = {
            "username": "fca",
            "password": "fcafincom2020"
        }

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        conn.request("POST", "/api/v1/authentications/authenticate", json.dumps(payload), headers)

        r2 = conn.getresponse()

        data = r2.read()
        xaccesstoken =  json.loads(data)['resultData']['token']

        print("\nAuthentication Complete")

        print("\nLoading Synthetic Data...")
        #THIS WILL NEED TO BE CHANGED TO CONNECT TO NOT BE LOCAL. do this is def args
        synthetic_sanction_data = pd.read_csv(filepath, sep='\t', encoding='latin-1')
        print("\nSynthetic Data Loaded.\n")

        # Query Loop begins
        print("\n  Querying API.\n")
        query_no = 1
        data = synthetic_sanction_data
        max_data = len(data)
        results_df = pd.DataFrame()
        start_time = time.time()

        #query loop begins
        for _, val in data.iterrows():
            if (query_no == 1) or (query_no % 250 == 0):
                #current_time = time.time()
                print("Query {} of {}".format(query_no, max_data))
                print("Processing...")

            synthetic_variation = val['Fullname']
            Title = val['Title']
            Id = val['Id']
            InitialId = val['InitialId']
            RefId = val['RefId']

            payload = {'names': [synthetic_variation],
                        #'isIndividual': entity_bool, #can be True,False,None
                        'responseType': 'fullResults',#can be: fullResults, minimalResults
                        'selectedDataSources': ['fca_xml_list'],
                        'threshold': threshold, #default is 0.4
                        'mlThreshold': ml_threshold, #default is 0.7
                        'minimumWordsInName': 0,# usual default is 2 unless none individual search is done.
                        'explain': 'numeric'
                        }

            req = json.dumps(payload, indent=4)

            headers = {
                'Content-Type': "application/json",
                'x-access-token': xaccesstoken,
                'cache-control': "no-cache"
            }

            conn.request("POST", "/api/v1/queries/aml", req, headers)

            res = conn.getresponse()
            data = res.read()
            response = json.loads(data.decode("utf-8"))

            #if error occurs
            if 'message' in response.keys():
                name = "No Match"
                score = np.nan
                phonetic_score = np.nan
                matched_group_id = "No Match"
                #add to df
                result = collections.OrderedDict({'RefId':RefId, 'Id':Id, 'InitialId':InitialId, 'Variation':synthetic_variation, 'Title':Title, 'Match':name, 'Match_Group_ID': matched_group_id, 'Score':score, 'PhoneticScore':phonetic_score})
                results_df = results_df.append(result, ignore_index=True)

            # if no result back
            elif range(len(response['resultData']) == 0):
                name = "No Match"
                score = np.nan
                phonetic_score = np.nan
                matched_group_id = "No Match"
                #add to df
                result = collections.OrderedDict({'RefId':RefId, 'Id': Id, 'InitialId':InitialId, 'Variation':synthetic_variation, 'Title':Title, 'Match':name, 'Match_Group_ID': matched_group_id, 'Score':score, 'PhoneticScore':phonetic_score})
                results_df = results_df.append(result, ignore_index=True)
            #if 1 or more result
            elif range(len(response['resultData']) > 0):
                #for rach result returned
                for i in range(len(response['resultData'])):
                    name = response['resultData'][i]['foundNames'][0]['name']
                    score = response['resultData'][i]['foundNames'][0]['score']
                    phonetic_score = response['resultData'][i]['foundNames'][0]['phonetixScore']
                    general_info = response['resultData'][i]['information']['generalInfo']
                    for idx, val in enumerate(general_info):
                        if val['type'] == 'GroupID':
                            matched_group_id = general_info[idx]['value']
                    #add to df
                    result = collections.OrderedDict({'RefId':RefId, 'Id':Id, 'InitialId':InitialId, 'Variation':synthetic_variation, 'Title':Title, 'Match':name, 'Match_Group_ID': matched_group_id, 'Score':score, 'PhoneticScore':phonetic_score})
                    results_df = results_df.append(result, ignore_index=True)

            query_no += 1

        #time taken
        elapsed_time = time.time() - start_time
        print('Queries completed in ' + str(math.ceil(elapsed_time)) + ' secs.')

        results_df = results_df[['RefId', 'Id', 'InitialId', 'Variation', 'Title', 'Match','Match_Group_ID', 'Score', 'PhoneticScore']]

        results_df.to_csv(outfilepath, index=None, sep='\t')

    def unchanged_query_loop(self, unchanged_firmvisit_path = constants.UNCHANGED_DATA_FILE_PATH, unchanged_outfilepath=constants.UNCHANGED_DATA_FILE_PATH_RESULTS, threshold = constants.FINCOM_THRESHOLD, ml_threshold = constants.FINCOM_ML_THRESHOLD):
        '''
        This method sets the proxies and tunnel to allow for HTTPS connection at the FCA. It then runs each of the synthetic names through the
        vendor api, saving the results to a file.

        :param filepath: unchanged data to be queried
        :param outfilepath: results of queried names
        :param thresholds: threshold specific to the vendor api
        '''

        print('\nQuerying Unchanged List')
        print('\nSetting proxies and tunnel.')

        #proxies
        os.environ['http_proxy'] = 'http://localhost:3128'
        os.environ['https_proxy'] = 'http://localhost:3128'
        print('\nProxies Set.')

        #tunnel
        conn = http.client.HTTPSConnection("localhost", 3128)
        conn.set_tunnel("fca.explore.fincom.co")
        conn.request("GET", "/")
        r1 = conn.getresponse()
        data1 = r1.read()
        print('\nTunnel Set.')

        # authentication
        print("\nAuthenticating...")

        payload = {
            "username": "fca",
            "password": "fcafincom2020"
        }

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        conn.request("POST", "/api/v1/authentications/authenticate", json.dumps(payload), headers)

        r2 = conn.getresponse()

        data = r2.read()
        xaccesstoken =  json.loads(data)['resultData']['token']

        print("\nAuthentication Complete")

        print("\nLoading Unchanged Data...")
        #THIS WILL NEED TO BE CHANGED TO CONNECT TO NOT BE LOCAL. do this is def args
        unchanged_firmvisit = pd.read_csv(unchanged_firmvisit_path, sep='\t', encoding='latin-1')
        print("\nUnchanged Loaded.\n")

        # Query Loop begins
        print("\n  Querying API.\n")
        query_no = 1
        data = unchanged_firmvisit.sample(5000)
        max_data = len(data)
        results_df = pd.DataFrame()
        start_time = time.time()

        #query loop begins
        for _, val in data.iterrows():
            if (query_no == 1) or (query_no % 250 == 0):
                #current_time = time.time()
                print("Query {} of {}".format(query_no, max_data))
                print("Processing...")

            unchanged = val['Original']
            RefId = val['RefId']

            payload = {'names': [unchanged],
                        #'isIndividual': entity_bool, #can be True,False,None
                        'responseType': 'fullResults',#can be: fullResults, minimalResults
                        'selectedDataSources': ['fca_xml_list'],
                        'threshold': threshold, #default is 0.4
                        'mlThreshold': ml_threshold, #default is 0.7
                        'minimumWordsInName': 0,# usual default is 2 unless none individual search is done.
                        'explain': 'numeric'
                        }

            req = json.dumps(payload, indent=4)

            headers = {
                'Content-Type': "application/json",
                'x-access-token': xaccesstoken,
                'cache-control': "no-cache"
            }

            conn.request("POST", "/api/v1/queries/aml", req, headers)

            res = conn.getresponse()
            data = res.read()
            response = json.loads(data.decode("utf-8"))

            #if error occurs
            if 'message' in response.keys():
                name = "No Match"
                score = np.nan
                phonetic_score = np.nan
                matched_group_id = "No Match"
                #add to df
                result = collections.OrderedDict({'RefId':RefId, 'Original':unchanged, 'Match':name, 'Match_Group_ID': matched_group_id, 'Score':score, 'PhoneticScore':phonetic_score})
                results_df = results_df.append(result, ignore_index=True)

            # if no result back
            elif range(len(response['resultData']) == 0):
                name = "No Match"
                score = np.nan
                phonetic_score = np.nan
                matched_group_id = "No Match"
                #add to df
                result = collections.OrderedDict({'RefId':RefId, 'Original':unchanged, 'Match':name, 'Match_Group_ID': matched_group_id, 'Score':score, 'PhoneticScore':phonetic_score})
                results_df = results_df.append(result, ignore_index=True)
            #if 1 or more result
            elif range(len(response['resultData']) > 0):
                #for rach result returned
                for i in range(len(response['resultData'])):
                    name = response['resultData'][i]['foundNames'][0]['name']
                    score = response['resultData'][i]['foundNames'][0]['score']
                    phonetic_score = response['resultData'][i]['foundNames'][0]['phonetixScore']
                    general_info = response['resultData'][i]['information']['generalInfo']
                    for idx, val in enumerate(general_info):
                        if val['type'] == 'GroupID':
                            matched_group_id = general_info[idx]['value']
                    #add to df
                    result = collections.OrderedDict({'RefId':RefId, 'Original':unchanged, 'Match':name, 'Match_Group_ID': matched_group_id, 'Score':score, 'PhoneticScore':phonetic_score})
                    results_df = results_df.append(result, ignore_index=True)

            query_no += 1

        #time taken
        elapsed_time = time.time() - start_time
        print('Queries completed in ' + str(math.ceil(elapsed_time)) + ' secs.')

        results_df = results_df[['RefId', 'Original', 'Match','Match_Group_ID', 'Score', 'PhoneticScore']]

        results_df.to_csv(unchanged_outfilepath, index=None, sep='\t')

    def join_results_check(self, check_data = constants.FINCOM_QUERY_RESULTS_PATH, query_data = constants.SYNTHETIC_DATA_FILE_PATH_ALLDEPTHS, outfilepath = constants.FIRM_QUERY_FULL_RESULTS, lefton = 'Id', righton = 'Id'):
        '''
        This method joins the results from the firm queries to the variated list for detailed results output.

        :param check_data: the data to be joined to the results filepath
        :param query_data: the results from the vendo Queries
        :param outfilepath: the file where the joined results will be saved to.
        :param lefton, righton: the ids to join the datasets on
        '''
        query_data_df = pd.read_csv(query_data, sep='\t', encoding='latin-1')
        check_data_df = pd.read_csv(check_data, sep='\t', encoding='latin-1')
        merge = pd.merge(check_data_df, query_data_df, left_on=lefton, right_on=righton, suffixes=('_data', '_result'))
        merge.to_csv(outfilepath, index = None, sep='\t')
