import datetime
from functools import wraps

from Exception import ErrorMessage
from Model.account import account
import Model.auth
from Model.customer import customer
from responseTemplate import responseTemplate
from flask import request, jsonify
import jwt
from dateutil.relativedelta import relativedelta

from Hash import Hash
from DBSource import DBsource


class Authentication:
    secretsKey = "atmAppKeyValidation$1"

    @staticmethod
    def roleCustomer(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                result = Authentication.tokenCheck()
                if result.get('role') != "customer":
                    raise ErrorMessage("Permission Denied.", 403)
                db = DBsource()
                result = db.select(
                    f'select * from customers join users on users.id = customers.user_id where users.id = "{result.get("id")}" limit 1')
                Model.auth.user = Model.auth.authrity(result[0])
            except ErrorMessage as e:
                return ErrorMessage.response(e)

            return f(*args, **kwargs)

        return check

    @staticmethod
    def tokenCheck():
        data = request.headers.get('Authorization')
        if data is None or len(data.split(" ")) < 2 or data.split(" ")[0] != "Bearer":
            raise ErrorMessage("Full authentication is required to access this resource.", 401)

        token = data.split(" ")[1]
        try:
            return jwt.decode(token, Authentication.secretsKey, algorithms=["HS256"])

        except:
            raise ErrorMessage("The Token is invalid.", 401)

    @staticmethod
    def roleAdmin(f):
        @wraps(f)
        def check(*args, **kwargs):
            try:
                result = Authentication.tokenCheck()
                if result.get('role') != "admin":
                    raise ErrorMessage("Permission Denied.", 403)
            except ErrorMessage as e:
                return ErrorMessage.response(e)

            return f(*args, **kwargs)

        return check

    @staticmethod
    def certificate(role, request: dict):
        db = DBsource()
        result = db.select(
            f"select * from users "
            f"where username = '{request.get('username')}' and role = '{role}' limit 1")

        if len(result) <= 0:
            return responseTemplate(message="The username or password was Incorrect.", status_code=403).json()
        print(result)
        data = account(result[0]).toMap()

        data['token'] = jwt.encode(
            {
             "role": role,
             "user": request.get('username'),
             "id": result[0][0],
             'exp': datetime.datetime.utcnow() + relativedelta(months=1)
             },
            Authentication.secretsKey, algorithm="HS256")

        return responseTemplate(message="Login Success", data=data).json()
