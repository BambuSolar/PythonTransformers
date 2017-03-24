from flask import Blueprint, request
from ftp.main import FtpDriver
from flask_api import status, exceptions
from git import local_git

bp = Blueprint('deploys', __name__)
deploysBluePrint = Blueprint('deploys', __name__)


@deploysBluePrint.route('/api/deploys', methods=['POST'])
def create():

    body = request.json

    if body:

        print(body)

        version = body['version']

        environment = body['environment']

        if local_git.set_version(version):

            ftp_driver = FtpDriver(environment)

            try:

                ftp_driver.clean()

                ftp_driver.upload()

                content = {
                    "message": "Deploy success"
                }

                return content, status.HTTP_201_CREATED

            except Exception as e:

                content = {
                    "message": str(e)
                }

                return content, status.HTTP_417_EXPECTATION_FAILED

        else:

            raise exceptions.ParseError(
                "The version %s don't exist" % version
            )

    else:

        return 'nada'
