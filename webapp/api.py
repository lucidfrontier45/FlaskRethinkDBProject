from flask import request
from flask.ext.classy import FlaskView

from webapp.flask_rethinkdb import RethinkDBMixin
from webapp.response import ok


class MyAPI(FlaskView, RethinkDBMixin):
    _table_name = "test_log"

    def index(self):
        ret = self.get_table().run(self.get_conn())
        return ok(list(ret))

    def post(self):
        data = request.get_json()
        ret = self.get_table().insert(data).run(self.get_conn())
        return ok(ret)
