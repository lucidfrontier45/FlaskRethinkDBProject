import rethinkdb as r
from flask import Flask

from .api import MyAPI
from .default_config import DefaultConfig
from .flask_rethinkdb import RethinkDB


def init_db(app: Flask):
    db_name = app.config.get("RETHINKDB_DB")

    conn = app.rethinkdb.conn
    try:
        r.db_create(db_name).run(conn)
    except r.errors.ReqlOpFailedError as e:
        pass


def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)
    try:
        app.config.from_pyfile(config_filename)
    except:
        pass
    app.rethinkdb = RethinkDB(app)

    MyAPI.register(app, "my_api")

    with app.app_context():
        init_db(app)
        MyAPI.create_table()

    return app
