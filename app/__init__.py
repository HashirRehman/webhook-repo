from flask import Flask
from .extensions import init_mongo
from app.webhook.routes import webhook
from app.webhook.views import views

def create_app():

    app = Flask(__name__)

    init_mongo(app)

    app.register_blueprint(webhook)
    app.register_blueprint(views)

    return app
