import rethinkdb as r
from flask import current_app
# Since no older versions than 0.9 are supported for Flask, this is safe
from flask import Flask, _app_ctx_stack as stack


class RethinkDB(object):
    def __init__(self, app: Flask = None, db=None):
        self.db = db
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        app.config.setdefault('RETHINKDB_HOST', 'localhost')
        app.config.setdefault('RETHINKDB_PORT', '28015')
        app.config.setdefault('RETHINKDB_AUTH', '')
        app.config.setdefault('RETHINKDB_DB', 'test')

        @app.teardown_appcontext
        def teardown(exception):
            ctx = stack.top
            if hasattr(ctx, 'rethinkdb'):
                ctx.rethinkdb.close()

    def connect(self):
        return r.connect(host=current_app.config['RETHINKDB_HOST'],
                         port=current_app.config['RETHINKDB_PORT'],
                         auth_key=current_app.config['RETHINKDB_AUTH'],
                         db=self.db or current_app.config['RETHINKDB_DB'])

    @property
    def conn(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'rethinkdb'):
                ctx.rethinkdb = self.connect()
            return ctx.rethinkdb


class RethinkDBMixin(object):
    _table_name = "logs"

    @classmethod
    def create_table(cls):
        r.table_create(cls._table_name).run(cls.get_conn())

    @classmethod
    def get_conn(cls):
        return current_app.rethinkdb.conn

    @classmethod
    def get_table(cls):
        return r.table(cls._table_name)
