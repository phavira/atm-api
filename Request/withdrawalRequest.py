from decimal import Decimal
from functools import wraps
from flask import request
import Model.auth as auth
from Exception import ErrorMessage


class withdrawal:
    @staticmethod
    def request(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                data = {}
                balance = request.args.get('balance')
                if balance is None:
                    data["balance"] = "The balance is required."
                elif auth.user.balance < Decimal(balance):
                    data["balance"] = "The balance is not Enough to withdrawal."

                if len(data) > 0:
                    raise ErrorMessage("The data is Invalid", 403, data)
            except ErrorMessage as error:
                return ErrorMessage.response(error)
            return f(*args, **kwargs)

        return check
