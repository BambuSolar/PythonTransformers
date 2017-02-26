from flask_api import FlaskAPI
from api.deploy.deploy_controller import deploysBluePrint
from api.build.build_controller import buildsBluePrint
from api.git.git_controller import gitBluePrint


def create_app():

    app = FlaskAPI(__name__)

    app.register_blueprint(deploysBluePrint)

    app.register_blueprint(buildsBluePrint)

    app.register_blueprint(gitBluePrint)

    return app
