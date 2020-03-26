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

    # TODO: For production, the output of the error should be disabled.
    @app.errorhandler(500)
    def server_error(e):
        app.logger.error('================== Error Handler =====================')
        app.logger.error(e)
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
