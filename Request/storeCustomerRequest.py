from functools import wraps

from flask import request, jsonify

from DBSource import DBsource
from validation import validation


class storeCustomer:
    @staticmethod
    def request(f):
        @wraps(f)
        def check(*args, **kwargs):
            if request.method == "POST":
                data = {}

                if request.args.get('name') is None:
                    data['name'] = "The name is required"
                else:
                    result = validation.statement(
                        f"select 1 from customers where name = '{request.args.get('name')}'")
                    if result:
                        data['name'] = "The name is already Exists"

                if request.args.get('account_no') is None:
                    data["account_no"] = "The account no is required"
                else:
                    # check unique account_no
                    result = validation.statement(
                        f"select 1 from customers where account_no = '{request.args.get('account_no')}'")
                    if result:
                        data['account_no'] = "The account_no is already Exists"

                if request.args.get('username') is None:
                    data["username"] = "The username is required"
                else:
                    result = validation.statement(
                        f"select 1 from users where username = '{request.args.get('username')}'")
                    if result:
                        data['username'] = "The username is already Exists"

                if request.args.get('password') is None:
                    data["password"] = "The password is required"

                if len(data) > 0:
                    return jsonify({"status": "error", "message": "The data was Invalid.", "data": data})
            return f(*args, **kwargs)

        return check
