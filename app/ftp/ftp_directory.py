# -*- coding: utf-8 -*-
import ftplib
import os


class FtpDirectory:

    @staticmethod
    def __get_file_name(file):
        return file.split(' ')[-1]

    @staticmethod
    def __get_dir_name(dir):
        return dir.split(' ')[-1]

    @staticmethod
    def __is_dir(line):
        return line[0] == 'd'

    @staticmethod
    def __print_dir(ftp):

        data = []

        ftp.dir(data.append)

        for line in data:
            print("->", line)

    @staticmethod
    def clean_directory(ftp, rm_path):

        print("Eliminando: " + rm_path)

        ftp.cwd(rm_path)

        FtpDirectory.__print_dir(ftp)

        data = []

        ftp.dir(data.append)

        for f in data:

            if FtpDirectory.__is_dir(f):

                print(f)

                if f != "./":

                    FtpDirectory.clean_directory(ftp, rm_path + '/' + FtpDirectory.__get_dir_name(f))

                    ftp.sendcmd("RMD " + (FtpDirectory.__get_dir_name(f)))

            else:

                try:

                    ftp.delete(FtpDirectory.__get_file_name(f))

                except ftplib.error_perm as e:

                    print(f)

                    print(e)

        ftp.cwd('..')
        
    @staticmethod
    def upload_folder(ftp, local_path, remote_path):

        files = os.listdir(local_path)

        os.chdir(local_path)

        for f in files:

            print(f)

            if os.path.isfile(f):

                fh = open(f, 'rb')

                ftp.storbinary('STOR %s' % f, fh)

                fh.close()

            elif os.path.isdir(f):

                if f != '.git':

                    try:

                        ftp.mkd(f)

                    except ftplib.error_perm:

                        print("Folder exists")

                    ftp.cwd(f)

                    FtpDirectory.upload_folder(ftp, local_path + r'/{}'.format(f), remote_path + r'/{}'.format(f))

        ftp.cwd('..')

        os.chdir('..')
