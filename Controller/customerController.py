import math
from datetime import datetime

import bcrypt

from DBSource import DBsource
from flask import make_response, jsonify

from Exception import ErrorMessage
from Hash import Hash
from Model.customer import customer
from Model.paginate import paginate
from responseTemplate import responseTemplate
import Model.auth as auth


class customerController:
    db = ""

    def __init__(self):
        self.db = DBsource()

    def index(self, request: dict):
        data = []
        page = 1
        if request.get('page') is not None:
            page = int(request.get('page'))

        result = self.db.select("select count(*) from customers")
        _pagiante = paginate(total_item=result[0][0], page=page)

        stm = f"select cs.id,cs.name,cs.account_no,cs.balance,us.username,us.role,us.lang,us.created_at " \
              f"from customers cs " \
              f"join users us on us.id = cs.user_id " \
              f"where us.active=1 " \
              f"limit {_pagiante.limit} offset {_pagiante.offset} "

        result = self.db.select(stm)
        for item in result:
            print(item)
            data.append(customer(item).toMap())

        return responseTemplate(data=data, message="Get Data Success", paginate=_pagiante.toMap()).json()

    def store(self, request: dict):
        name = request.get('name')
        account_no = request.get('account_no')
        username = request.get("username")
        password = Hash.make(request.get('password'))

        try:
            sql = "insert into users (username,password,role,created_at) values (%s,%s,'customer',%s)"
            val = (username, password, datetime.now())
            userResut = self.db.insert(sql, val, commit=False)
            if not userResut:
                self.db.connector.rollback()
                raise ErrorMessage("Error Store User", 422)

            user_id = userResut
            sql = "insert into customers (name,account_no,user_id,created_at) values (%s,%s,%s,%s)"
            val = (name, account_no, user_id, datetime.now())
            result = self.db.insert(sql, val, commit=False)
            if not result:
                self.db.connector.rollback()
                raise ErrorMessage("Error Store Customer", 422)

            self.db.connector.commit()

            data = self.db.select(
                f"select cs.id,cs.name,cs.account_no,cs.balance,us.username,us.role,us.lang,us.created_at "
                f"from customers cs "
                f"join users us on us.id = cs.user_id "
                f"where cs.id='{result}' limit 1")

            return responseTemplate(data=customer(data[0]).toMap(), message="Store Data Success").json()
        except ErrorMessage as error:
            return ErrorMessage.response(error)

    def destroy(self, id):
        try:
            sql = f"update users set active = 0 where id in (select user_id from customers where id = {id})"
            result = self.db.update(sql)
            if not result:
                raise ErrorMessage("Error Disable Account", 422)
            return responseTemplate(message="Disable Account Success").json()
        except ErrorMessage as e:
            return ErrorMessage.response(e)

    def enable(self, id):
        try:
            sql = f"update users set active = 1 where id in (select user_id from customers where id = {id})"
            result = self.db.update(sql)
            if not result:
                raise ErrorMessage("Error Enable Account", 422)

            return responseTemplate(message="Enable Account Success").json()
        except ErrorMessage as e:
            return ErrorMessage.response(e)

    def changePassword(self, id, request: dict):
        try:
            password = Hash.make(request.get('password'))
            sql = "update users set password = %s where id in (select user_id from customers where id = %s)"
            val = (password, id)
            result = self.db.update(sql, val=val)
            if not result:
                raise ErrorMessage("Change Password unsuccessful", 422)

            return responseTemplate(message="Change Password Successful").json()
        except ErrorMessage as e:
            return ErrorMessage.response(e)

    def changePasswordSelf(self, request: dict):
        return self.changePassword(auth.user.customer_id, {"password": request.get('new_password')})
