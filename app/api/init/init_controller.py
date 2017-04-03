from flask import Blueprint, jsonify
from flask_api import status

from services.init.init_service import InitService

bp = Blueprint('init', __name__)
initBluePrint = Blueprint('init', __name__)


@initBluePrint.route('/api/init', methods=['POST'])
def init():

    content = jsonify({
        "data": InitService.init()
    })

    return content, status.HTTP_200_OK
