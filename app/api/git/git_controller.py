from flask import Blueprint, jsonify, request
from flask_api import status, exceptions
from git import local_git

bp = Blueprint('git', __name__)
gitBluePrint = Blueprint('git', __name__)


@gitBluePrint.route('/api/git/update', methods=['POST'])
def update():

    body = request.json

    if body:

        try:
            environment = body['environment']

            if environment not in ['prod', 'staging', 'beta']:

                raise exceptions.ParseError(
                    "Los environments aceptados son %s" % (str(['prod', 'staging', 'beta']))
                )

            if local_git.update_branch(environment):

                content = jsonify({
                    "data": 'update successful'
                })

                return content, status.HTTP_200_OK

            else:

                content = jsonify({
                    "data": 'fail to update'
                })

                return content, status.HTTP_417_EXPECTATION_FAILED

        except KeyError as e:

            raise exceptions.ParseError(
                "%s es un dato requerido" % (str(e)[1:-1].capitalize())
            )

    else:

        raise exceptions.ParseError(detail=None)

