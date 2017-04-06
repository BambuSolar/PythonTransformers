# -*- coding: utf-8 -*-

import requests
import json


class GoDirector:

    @staticmethod
    def __get_base_url():

        return "http://45.55.23.251:3000"

    @staticmethod
    def get_conf_ftp(environment):

        token = "eyJUeXAiOiJKV1QiLCJBbGciOiJIUzI1NiIsIkN0eSI6IiJ9.eyJJUCI6IjM1LjE2Ni4yMy4xNjUiLCJOYW1lIjoiUHl0aG9uVHJhbnNmb3JtZXJzIiwiaWF0IjoxNDkxNDQxNzc4fQ.d01OUDNxT2dod09INzRlR2dQMFpJdFlvTUFNdTc1MzE2V3lLRm1JYUY0RQ"

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

        token = "eyJUeXAiOiJKV1QiLCJBbGciOiJIUzI1NiIsIkN0eSI6IiJ9.eyJJUCI6IjM1LjE2Ni4yMy4xNjUiLCJOYW1lIjoiUHl0aG9uVHJhbnNmb3JtZXJzIiwiaWF0IjoxNDkxNDQxNzc4fQ.d01OUDNxT2dod09INzRlR2dQMFpJdFlvTUFNdTc1MzE2V3lLRm1JYUY0RQ"

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

        token = "eyJUeXAiOiJKV1QiLCJBbGciOiJIUzI1NiIsIkN0eSI6IiJ9.eyJJUCI6IjM1LjE2Ni4yMy4xNjUiLCJOYW1lIjoiUHl0aG9uVHJhbnNmb3JtZXJzIiwiaWF0IjoxNDkxNDQxNzc4fQ.d01OUDNxT2dod09INzRlR2dQMFpJdFlvTUFNdTc1MzE2V3lLRm1JYUY0RQ"

        headers = {
            'cache-control': "no-cache",
            'Authorization': token
        }

        url = "%s/api/environments" % GoDirector.__get_base_url()

        response = requests.request("GET", url, headers=headers)

        data = response.text

        result = json.loads(data)

        return result['data']
