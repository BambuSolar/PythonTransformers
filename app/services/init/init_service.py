# -*- coding: utf-8 -*-
import subprocess

from go_director.main import GoDirector


class InitService:

    dir_path = ''

    @staticmethod
    def get_dir_path():

        if len(InitService.dir_path) == 0:

            InitService.dir_path = GoDirector.get_build_config('SourcePath')

        return InitService.dir_path

    @staticmethod
    def init():

        task = 'cd ' + InitService.get_dir_path() + ' && cd .. && rm -rf ' + InitService.get_dir_path()

        task += ' && mkdir ' + InitService.get_dir_path() + ' && cd ' + InitService.get_dir_path() + ' && git init'

        git_repo = "git@github.com:%s.git" % GoDirector.get_build_config('GitHubRepository')

        task += ' && git remote add origin ' + git_repo

        task += ' && git config --global user.name "Javier Caballero"'

        task += ' && git config --global user.email caballerojavier13@gmail.com'

        output = subprocess.check_output(
            task,
            shell=True
        )

        return output.decode("utf-8")[:-1]
