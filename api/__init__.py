import os
from flask import Flask
from . import facedetect_api
from . import mtcnn_api


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.ProductionConfig')
    app.register_blueprint(facedetect_api.bp)
    app.register_blueprint(mtcnn_api.bp)
    return app
