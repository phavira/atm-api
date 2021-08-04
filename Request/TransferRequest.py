from decimal import Decimal
from functools import wraps
from flask import request
import Model.auth as auth
from Exception import ErrorMessage

from validation import validation


class Transfer:
    @staticmethod
    def request(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                data = {}
                balance = request.args.get('balance')
                account_no = request.args.get('account_no')
                if balance is None:
                    data["balance"] = "The balance is required."
                elif auth.user.balance < Decimal(balance):
                    data["balance"] = "The balance is not Enough to Transfer."
                if account_no is None:
                    data["account_no"] = "The account no is required."
                else:
                    result = validation.statement(
                        f"select 1 from customers where account_no = {account_no} and id not in ({auth.user.customer_id})")
                    if not result:
                        data["account_no"] = "The account no not Exists."

                if len(data) > 0:
                    raise ErrorMessage("The data is Invalid", 403, data)
            except ErrorMessage as error:
                return ErrorMessage.response(error)
            return f(*args, **kwargs)

        return check
