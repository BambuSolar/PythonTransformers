from flask_api import FlaskAPI
from api.deploy import deploysBluePrint
from api.build import buildsBluePrint


def create_app():

    app = FlaskAPI(__name__)

    app.register_blueprint(deploysBluePrint)

    app.register_blueprint(buildsBluePrint)

    return app
