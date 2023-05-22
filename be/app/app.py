from flask import Flask
from app.settings import settings


class App(Flask):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(__name__, *args, **kwargs)
        self.config.from_object(settings)


def create_app() -> App:
    from app.models import db
    from app.api.routes import bp

    app = App()
    db.init_app(app)
    app.register_blueprint(bp)

    return app
