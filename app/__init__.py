from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and initialize the routes
    from . import routes
    routes.init_app(app)

    return app
