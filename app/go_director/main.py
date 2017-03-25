# -*- coding: utf-8 -*-

import http.client
import json


class GoDirector:

    @staticmethod
    def __get_base_url():

        return "http://45.55.23.251:3000"

    @staticmethod
    def get_conf_ftp(environment):

        conn = http.client.HTTPConnection(GoDirector.__get_base_url())

        payload = {}

        headers = {
            'cache-control': "no-cache"
        }

        uri = "/api/environments?query=Name:%s" % environment

        conn.request("GET", uri, payload, headers)

        res = conn.getresponse()

        data = res.read()

        result = json.loads(data.decode("utf-8"))

        return result['data'][0]

    @staticmethod
    def get_build_config(attribute):

        conn = http.client.HTTPConnection(GoDirector.__get_base_url())

        payload = {}

        headers = {
            'cache-control': "no-cache"
        }

        uri = "/api/system_parameters?query=Key:%s" % attribute

        conn.request("GET", uri, payload, headers)

        res = conn.getresponse()

        data = res.read()

        result = json.loads(data.decode("utf-8"))

        return result['data'][0]['Value']
