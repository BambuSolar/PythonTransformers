# -*- coding: utf-8 -*-
from .ftp_directory import FtpDirectory
import ftplib
import json


class FtpDriver:
    __general_conf = None

    __directory = ""

    __connection = None

    def __init__(self, environment):

        with open('./config/build_config.json') as data_file:
            self.__set_source_folder(json.load(data_file)['path'])

        self.__set_general_conf(self.__get_configuration_file(environment))

        self.__set_connection(self.__connect(self.__get_general_conf()))

    def clean(self):

        print("Eliminando archivos")

        FtpDirectory.clean_directory(self.__connect(self.__get_general_conf()), self.__get_general_conf()['path'])

    def upload(self):

        print("Subiendo archivos")
        FtpDirectory.upload_folder(self.__connect(self.__get_general_conf()),
                                   self.__get_source_folder(),
                                   self.__get_general_conf()['path'])


    @staticmethod
    def __connect(configuration):

        server = configuration['server']

        ftp = ftplib.FTP(server)

        ftp.login(configuration['user'], configuration['password'])

        ftp.cwd(configuration['path'])

        data = []

        ftp.dir(data.append)

        for line in data:
            print("->", line)

        return ftp

    @staticmethod
    def __get_connection():
        global connection

        return connection

    @staticmethod
    def __set_connection(ftp):
        global connection

        connection = ftp

    @staticmethod
    def __set_general_conf(conf):
        global general_conf
        general_conf = conf

    @staticmethod
    def __get_general_conf():
        global general_conf
        return general_conf

    @staticmethod
    def __set_source_folder(folder):
        global directory
        directory = folder

    @staticmethod
    def __get_source_folder():
        global directory
        return directory

    @staticmethod
    def __get_configuration_file(environment):

        with open('./config/conf_ftp.json') as data_file:

            data = json.load(data_file)

            return data[environment]
