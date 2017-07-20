# -*- coding: utf-8 -*-

import urllib
from urllib.request import urlopen

from lxml import html
from urllib import error
import os
import re
import subprocess
from git import local_git
from go_director.main import GoDirector
import requests

from services.init.init_service import InitService


class HTMLCrawler:
    __css_files = []

    __base_url = ""

    def __init__(self, url):
        self.__base_url = url

    def __get_css_files(self):

        return self.__css_files

    def __clear_css_files(self):

        self.__css_files = []

    def __add_css_files(self, file):

        self.__css_files.append(file)

    @property
    def __get_base_url__(self):

        return self.__base_url

    def __get_url(self, environment):

        return self.__get_base_url__ + "/preview?environment=" + environment

    def get_dir_path(self):

        return GoDirector.get_build_config('SourcePath')

    def __file_path(self):

        return self.get_dir_path() + '/index.html'

    def __page(self, file):

        with open(file, 'r', encoding="utf-8") as target_file:
            return html.fromstring(target_file.read())

    def __is_external_url(self, url):

        return url[0] == 'h'

    def __is_relative_path(self, url):

        return url[0] == '/'

    def __clean_dir(self):

        print("clean")

        subprocess.check_output(
            'cd ' + self.get_dir_path() + ' && find . -maxdepth 1 -not -name .git -not -name . -exec rm -r {} +',
            shell=True)

    def __get_new_version(self, environment):

        last_prod_version = local_git.get_last_version('prod').split('v')[1]

        mayor_version = int(GoDirector.get_build_config('MayorVersion'))

        minor_version = int(GoDirector.get_build_config('MinorVersion'))

        patch_version = 1

        if int(last_prod_version.split('.')[0]) == mayor_version and int(last_prod_version.split('.')[1]) == minor_version:

            patch_version = 1 + int(last_prod_version.split('.')[-1])

        prod_version = "%s.%s.%s" % (mayor_version, minor_version, patch_version)

        print(prod_version)

        if environment == "prod":

            return prod_version

        else:

            last_env_version = local_git.get_last_version(environment).split('v')[1]

            env_counter = 1

            if prod_version == last_env_version.split('-')[0]:
                env_counter = 1 + int(last_env_version.split('-')[1].split('_')[1])

            return "%s-%s_%s" % (prod_version, environment, env_counter)

    def __create_tag(self, environment, new_version):

        branch = GoDirector.get_conf_ftp(environment)['Branch']

        if new_version != "0.0.1":

            subprocess.call(
                'cd ' + self.get_dir_path() + ''
                                              ' && git add  ' + self.get_dir_path() + ''
                                              ' && pwd'
                                              ' && git commit -m "' + new_version + '" ' +
                                              ' && git tag v' + new_version + ''
                                              ' && git push origin ' + branch + ' --tags',
                shell=True
            )

        else:

            subprocess.call(
                'cd ' + self.get_dir_path() + ''
                                              ' && git add  ' + self.get_dir_path() + ''
                                              ' && pwd'
                                              ' && git commit -m "' + new_version + '" ' +
                                              ' && git tag v' + new_version + ''
                                              ' && git push -u origin ' + branch + ' --tags',
                shell=True
            )

    def __change_branch(self, environment):

        branch = GoDirector.get_conf_ftp(environment)['Branch']

        output = subprocess.check_output(
            'cd ' + InitService.get_dir_path() + ' && git branch',
            shell=True
        )

        new_branch = ''

        if output.decode("utf-8").find(branch) < 0:
            new_branch = '-b'

        subprocess.call(
            'cd ' + self.get_dir_path() + '&& git checkout ' + new_branch + ' ' + branch,
            shell=True
        )

    def _get_produts_type_to_craw(self):

        r = requests.get(self.__base_url + '/preview/product_types.json')

        return r.json()

    def run(self, environment):

        self.__clear_css_files()

        new_version = self.__get_new_version(environment)

        self.__change_branch(environment)

        self.__clean_dir()

        print("Descargando HTML")

        self.__get_index(environment)

        print("Descargando CSS Index")

        self.__get_css(self.__file_path())

        print("Descargando JS Index")

        self.__get_js(self.__file_path())

        print("Descargando IMG Index")

        self.__get_img(self.__file_path())

        print("Descargando favicon Index")

        self.__get_favicon(self.__file_path())

        for p_t in self._get_produts_type_to_craw()['data']:

            file = self.get_dir_path() + p_t['filename']

            self.__get_index_product_type(p_t, environment)

            print("Descargando CSS %s" % p_t['name'])

            self.__get_css(file)

            print("Descargando JS %s" % p_t['name'])

            self.__get_js(file)

            print("Descargando IMG %s" % p_t['name'])

            self.__get_img(file)

            print("Descargando favicon %s" % p_t['name'])

            self.__get_favicon(file)

            self.__get_product_json(p_t['products'])

        print("Descargando IMG desde CSS")

        self.__get_img_in_css()

        self.__create_tag(environment, new_version)

    def __get_index(self, environment):

        print(self.__get_url(environment))

        response = urllib.request.urlopen(self.__get_url(environment))

        data = response.read()

        text = data.decode('utf-8')

        os.makedirs(self.get_dir_path(), exist_ok=True)

        f = open(self.__file_path(), 'w')

        f.write(text)

        f.close()

    def __get_css(self, file):

        for s in self.__page(file).cssselect("link[rel='stylesheet']"):

            href = s.get("href")

            if not self.__is_external_url(href):

                path = self.get_dir_path()

                for d in href.split('/')[:-1]:

                    if len(d) > 0:
                        path += '/' + d

                        os.makedirs(path, exist_ok=True)

                response = urllib.request.urlopen(self.__get_base_url__ + href)

                data = response.read()

                text = data.decode('utf-8')

                f = open(self.get_dir_path() + href, 'w')

                f.write(text)

                f.close()

                self.__add_css_files({
                    'path': self.get_dir_path() + href,
                    'url': href
                })

                print(self.get_dir_path() + href)

    def __get_js(self, file):

        for s in self.__page(file).cssselect("script"):

            src = s.get("src")

            if src:

                path = self.get_dir_path()

                for d in src.split('/')[:-1]:

                    if len(d) > 0:
                        path += '/' + d

                        os.makedirs(path, exist_ok=True)

                response = urllib.request.urlopen(self.__get_base_url__ + src)

                data = response.read()

                text = data.decode('utf-8')

                f = open(self.get_dir_path() + src, 'w')

                f.write(text)

                f.close()

                print(self.get_dir_path() + src)

    def __download_local_img(self, src):

        try:

            path = self.get_dir_path()

            for d in src.split('/')[:-1]:

                if len(d) > 0:
                    path += '/' + d

                    os.makedirs(path, exist_ok=True)

            url_img = ''.join([self.__get_base_url__, src])

            print(url_img)

            response = urllib.request.urlopen(url_img)

            data = response.read()

            f = open(self.get_dir_path() + src, 'wb')

            f.write(data)

            f.close()

        except UnicodeEncodeError as e:

            print(e)

        except urllib.error.HTTPError as e:

            print(e)

    def __get_img(self, file):

        imgs = []

        for s in self.__page(file).cssselect("img"):

            src = s.get("src")

            if not (src in imgs):

                imgs.append(src)

                try:

                    if not self.__is_external_url(src) and self.__is_relative_path(src):
                        self.__download_local_img(src)

                except:
                    print("Error to download img <%s>" % str(src))

    def __get_img_in_css(self):

        imgs = []

        for css in self.__get_css_files():

            my_list = []

            with open(css['path'], 'r') as f:

                for line in f:
                    my_list += re.findall('((url\([^)]*)\))+', line)

            for i in my_list:

                for j in i:

                    src = j[4:]

                    if not self.__is_external_url(src):

                        if src[-1] == ")":
                            src = src[:-1]

                        if not (src in imgs):

                            imgs.append(src)

                            if self.__is_relative_path(src):

                                self.__download_local_img(src.split('?')[0])

                            else:

                                print(src)

                                if src[0] == '.':
                                    print(css['url'].split('/'))

                                    print(src.split('/'))

    def __get_index_product_type(self, product_type, environment):

        print(product_type)

        print(self.__get_base_url__ + product_type['crawler_url'])

        response = urllib.request.urlopen(self.__get_base_url__ + product_type['crawler_url'] + "?environment=" + environment)

        data = response.read()

        text = data.decode('utf-8')

        os.makedirs(self.get_dir_path() + product_type['filename'].split('/index')[0], exist_ok=True)

        f = open(self.get_dir_path() + product_type['filename'], 'w')

        f.write(text)

        f.close()

    def __get_favicon(self, file):

        for f in self.__page(file).cssselect("link[rel='icon']"):

            src = f.get("href")

            if self.__is_relative_path(src):

                self.__download_local_img(src)

    def __get_product_json(self, products):

        for p in products:
            response = urllib.request.urlopen(
                self.__get_base_url__ + p['url'])

            data = response.read()

            text = data.decode('utf-8')

            os.makedirs(self.get_dir_path() + '/info/products', exist_ok=True)

            f = open(self.get_dir_path() + '/info/products' + str(p['id']) + '.json', 'w')

            f.write(text)

            f.close()
