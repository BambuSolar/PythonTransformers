# -*- coding: utf-8 -*-

import requests
import json


class GoDirector:

    @staticmethod
    def __get_base_url():

        return "http://45.55.23.251:3000"

    @staticmethod
    def get_conf_ftp(environment):

        headers = {
            'cache-control': "no-cache"
        }

        url = "%s/api/environments?query=Name:%s" % (GoDirector.__get_base_url(), environment)

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data'][0]

    @staticmethod
    def get_build_config(attribute):

        headers = {
            'cache-control': "no-cache"
        }

        url = "%s/api/system_parameters?query=Key:%s" % (GoDirector.__get_base_url(), attribute)

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data'][0]['Value']

    @staticmethod
    def get_environments():
        headers = {
            'cache-control': "no-cache"
        }

        url = "%s/api/environments" % GoDirector.__get_base_url()

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data']
