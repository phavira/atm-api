from decimal import Decimal
from functools import wraps
from flask import request
import Model.auth as auth
from Exception import ErrorMessage

from validation import validation


class PayBilling:
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
                    data["balance"] = "The balance is not Enough to Pay Billing."

                if request.args.get('billing_no') is None:
                    data["billing_no"] = "The billing no is required."

                if request.args.get('billing_type') is None:
                    data["billing_type"] = "The billing type is required."
                elif request.args.get('billing_type') not in ['electric', 'water', 'phone']:
                    data["billing_type"] = "The billing type is not match."

                if len(data) > 0:
                    raise ErrorMessage("The data is Invalid", 403, data)
            except ErrorMessage as error:
                return ErrorMessage.response(error)
            return f(*args, **kwargs)

        return check
