from functools import wraps

from flask import request, jsonify

from Exception import ErrorMessage


class login:
    @staticmethod
    def request(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                data = {}
                if request.args.get('username') is None:
                    data["username"] = "The username is required."
                if request.args.get("password") is None:
                    data['password'] = "The password is required."
                if len(data) > 0:
                    raise ErrorMessage("The data is Invalid", 403, data)
            except ErrorMessage as error:
                return ErrorMessage.response(error)
            return f(*args, **kwargs)

        return check
