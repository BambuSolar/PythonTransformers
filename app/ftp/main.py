# -*- coding: utf-8 -*-

from .ftp_directory import FtpDirectory
from go_director.main import GoDirector
import ftplib


class FtpDriver:
    __general_conf = None

    __directory = ""

    __connection = None

    def __init__(self, environment):

        source_folder = GoDirector.get_build_config('SourcePath')

        print(source_folder)

        self.__set_source_folder(source_folder)

        self.__set_general_conf(self.__get_configuration_file(environment))

        self.__set_connection(self.__connect(self.__get_general_conf()))

    def clean(self):

        print("Eliminando archivos")

        FtpDirectory.clean_directory(self.__connect(self.__get_general_conf()), self.__get_general_conf()['FTPRootPath'])

    def upload(self):

        print("Subiendo archivos")

        FtpDirectory.upload_folder(self.__connect(self.__get_general_conf()),
                                   self.__get_source_folder(),
                                   self.__get_general_conf()['FTPRootPath'])

    @staticmethod
    def __connect(configuration):

        server = configuration['ServerUrl']

        print(server)

        try:

            ftp = ftplib.FTP_TLS(timeout=10)
            
            ftp.connect(server, 21)
            
            # enable TLS
            ftp.auth()
            
            ftp.prot_p()

            ftp.login(configuration['UserFTP'], configuration['PasswordFTP'])

            ftp.cwd(configuration['FTPRootPath'])

            data = []

            ftp.dir(data.append)

            print(4)

            for line in data:
                print("->", line)

            return ftp

        except:

            print("Error")

            return None

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

        return GoDirector.get_conf_ftp(environment)
