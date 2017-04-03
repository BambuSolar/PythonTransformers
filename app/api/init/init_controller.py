from flask import Blueprint, jsonify
from flask_api import status

from services.init.init_service import InitService

bp = Blueprint('init', __name__)
initBluePrint = Blueprint('init', __name__)


@initBluePrint.route('/api/init', methods=['POST'])
def init():

    InitService.init()

    content = jsonify({
        "data": 'init successful'
    })

    return content, status.HTTP_200_OK
