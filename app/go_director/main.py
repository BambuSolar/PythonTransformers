# -*- coding: utf-8 -*-

import requests
import json
import os


class GoDirector:

    @staticmethod
    def __get_base_url():

        return os.getenv('GoDirectorURL')

    @staticmethod
    def __get_token():

        return os.getenv('GoDirectorToken')

    @staticmethod
    def get_conf_ftp(environment):

        token = GoDirector.__get_token()

        headers = {
            'cache-control': "no-cache",
            'Authorization': token
        }

        url = "%s/api/environments?query=Name:%s" % (GoDirector.__get_base_url(), environment)

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data'][0]

    @staticmethod
    def get_build_config(attribute):

        token = GoDirector.__get_token()

        headers = {
            'cache-control': "no-cache",
            'Authorization': token
        }

        url = "%s/api/system_parameters?query=Key:%s" % (GoDirector.__get_base_url(), attribute)

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data'][0]['Value']

    @staticmethod
    def get_environments():

        token = GoDirector.__get_token()

        headers = {
            'cache-control': "no-cache",
            'Authorization': token
        }

        url = "%s/api/environments" % GoDirector.__get_base_url()

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data']
