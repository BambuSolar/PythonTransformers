import urllib

from flask import Blueprint, jsonify, request
from flask_api import status, exceptions
from crawler.main import HTMLCrawler
from git import local_git

bp = Blueprint('builds', __name__)
buildsBluePrint = Blueprint('builds', __name__)


@buildsBluePrint.route('/api/builds', methods=['POST'])
def create():

    try:

        body = request.json
        
    except Exception as e:
        content = {
            "message": str(e)
        }

        return content, status.HTTP_400_BAD_REQUEST

    if body:

        try:

            url = body['url']

            environment = body['environment']

            if environment not in ['prod', 'staging', 'beta']:

                raise exceptions.ParseError(
                    "Los environments aceptados son %s" % (str(['prod', 'staging', 'beta']))
                )

            before_deploy = local_git.get_last_version(environment)

            crawler = HTMLCrawler(url)

            crawler.run(environment)

            after_deploy = local_git.get_current_version()

            if before_deploy == after_deploy:
                content = jsonify({
                    "data": after_deploy
                })

                return content, status.HTTP_200_OK

            else:

                content = jsonify({
                    "data": after_deploy
                })

                return content, status.HTTP_201_CREATED

        except KeyError as e:

            raise exceptions.ParseError(
                "%s es un dato requerido" % (str(e)[1:-1].capitalize())
            )

        except urllib.error.URLError as e:

            raise exceptions.ParseError(
                "%s es un dato requerido" % (str(e)[1:-1].capitalize())
            )

    else:

        raise exceptions.ParseError(detail=None)


@buildsBluePrint.route('/api/builds', methods=['GET'])
def list_all():

    content = jsonify(local_git.get_all_versions('all'))

    return content, status.HTTP_200_OK


@buildsBluePrint.route('/api/builds/current', methods=['GET'])
def current():

    content = jsonify({
        "data": local_git.get_current_version()
    })

    return content, status.HTTP_200_OK


@buildsBluePrint.route('/api/builds/last', methods=['GET'])
def last():

    content = jsonify({
        "data": local_git.get_last_version('prod')
    })

    return content, status.HTTP_200_OK
