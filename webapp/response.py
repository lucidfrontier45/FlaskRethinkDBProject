from flask import jsonify


def ok(ret=None):
    if ret is None:
        return jsonify({
            "code": 200,
            "msg": "OK"
        })

    else:
        return jsonify({
            "code": 200,
            "msg": "OK",
            "result": ret
        })


def not_found():
    return jsonify({
        "code": 404,
        "msg": "Not Found"
    })


def bad_request():
    return jsonify({
        "code": 400,
        "msg": "Bad Request"
    })
