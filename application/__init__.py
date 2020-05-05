import logging
from flask import Flask


def create_app(config, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    app.testing = testing
    if config_overrides:
        app.config.update(config_overrides)
    # Configure logging depth: ?NOTSET?, DEBUG, INFO, WARNING, ERROR, CRITICAL
    if not app.testing:
        log_level = logging.DEBUG if app.debug else logging.WARNING
        logging.basicConfig(level=log_level)

    # Setup the data model.
    with app.app_context():
        from . import routes  # noqa: F401
        from . import errors  # noqa: F401

    return app
