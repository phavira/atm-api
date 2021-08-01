from functools import wraps

import bcrypt
from flask import request, jsonify

from Exception import ErrorMessage
import Model.auth as auth


class ChangePasswordCustomer:
    @staticmethod
    def request(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                data = {}
                if request.args.get('current_password') is None:
                    data["current_password"] = "The current_password is required."
                if request.args.get("new_password") is None:
                    data['new_password'] = "The new password is required."
                if request.args.get("confirm_password") is None:
                    data['confirm_password'] = "The confirm_password is required."

                if (request.args.get('confirm_password') != request.args.get('new_password')):
                    data['confirm_password'] = "The confirm password and new password not match"
                check = bcrypt.checkpw(request.args.get('current_password').encode(), auth.user.password.encode())
                if not check:
                    data['current_password'] = "The confirm password and new password not match"

                if len(data) > 0:
                    raise ErrorMessage("The data is Invalid", 403, data)
            except ErrorMessage as error:
                return ErrorMessage.response(error)
            return f(*args, **kwargs)

        return check
