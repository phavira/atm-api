from functools import wraps
from flask import request

from Exception import ErrorMessage


class deposit:
    @staticmethod
    def request(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                data = {}
                if request.args.get('balance') is None:
                    data["balance"] = "The balance is required."
                else:
                    if not request.args.get('balance').isdecimal():
                        data['balance'] = "The balance is not a number."

                if len(data) > 0:
                    raise ErrorMessage("The data is Invalid", 403, data)
            except ErrorMessage as error:
                return ErrorMessage.response(error)
            return f(*args, **kwargs)

        return check
