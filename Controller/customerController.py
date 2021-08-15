import math
from datetime import datetime
from decimal import Decimal

import bcrypt

from DBSource import DBsource
from flask import make_response, jsonify

from Exception import ErrorMessage
from Hash import Hash
from Model.customer import customer, customerOnly
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

    def checkBalance(self):
        db = DBsource()
        result = db.select("select cs.id,cs.name,cs.account_no,cs.balance,us.username,us.role,us.lang,us.created_at "
                           "from customers cs "
                           "join users us on us.id = cs.user_id "
                           f"where us.active=1 and cs.id = {auth.user.customer_id}")
        cu = customer(result[0])
        print(cu.toMap())
        data = {
            'balance': str(auth.user.balance),
            'account_no': cu.account_no,
            "name": cu.name
        }
        return responseTemplate(message="Get Balance Success", data=data).json()

    def updateBalance(self, request: dict, type="in"):
        db = DBsource()
        balance = Decimal(request.get("balance"))
        if type == "in":
            reftxt = "self deposit with ATM"
        else:
            reftxt = "self withdrawal with ATM"
        val = (reftxt, datetime.now(), type, balance, auth.user.id)
        statment = 'insert into cash_transaction (ref_name,date,type,amount,user_id) values ("%s",%s,%s,%s, %s)'
        result = db.insert(statment, val, commit=False)
        if not result:
            db.connector.rollback()
            raise ErrorMessage(message="Store Balance unsuccessful", code=403)

        currentBalance = auth.user.balance
        if type == "in":
            currentBalance = auth.user.balance + balance
        elif type == "out":
            currentBalance = auth.user.balance - balance

        statment = f'update customers set balance = {currentBalance} where id = {auth.user.customer_id}'
        result = db.update(statment, commit=False)
        if not result:
            db.connector.rollback()
            raise ErrorMessage(message="set Balance unsuccessful", code=403)
        db.connector.commit()

        return True

    def deposit(self, request):
        try:
            result = self.updateBalance(request)
            if not result:
                return responseTemplate(message="Your Deposit Unsuccessful.", status_code=403).json()
            return responseTemplate(message="Your Deposit Successful.").json()
        except ErrorMessage as e:
            return ErrorMessage.response(e)

    def withdrawal(self, request):
        try:
            result = self.updateBalance(request, "out")
            if not result:
                return responseTemplate(message="Your withdrawal Unsuccessful.", status_code=403).json()
            return responseTemplate(message="Your withdrawal Successful.").json()
        except ErrorMessage as e:
            return ErrorMessage.response(e)

    def transfer(self, request):
        try:
            db = DBsource()
            balance = Decimal(request.get("balance"))
            account_no = request.get('account_no')
            user_transfer = db.select(f'select * from customers where account_no = {account_no} limit 1')
            cs = customerOnly(user_transfer[0])

            statment = 'insert into cash_transfer_transaction (ref_name,date,amount,reference_id,user_id) values ("transfer to %s",%s,%s,%s, %s)'
            val = (cs.name, datetime.now(), balance, cs.user_id, auth.user.id)
            result = db.insert(statment, val)
            if not result:
                raise ErrorMessage(message="Your Transfer Unsuccessful.", code=403)

            return responseTemplate(message="Your Transfer Successful.").json()
        except ErrorMessage as e:
            ErrorMessage.response(e)

    def billPayment(self, request):
        try:
            db = DBsource()
            billing_no = request.get("billing_no")
            billing_type = request.get('billing_type')
            amount = Decimal(request.get('balance'))

            statment = 'insert into bill_payment_transaction (ref_name,date,amount,billing_no,billing_type,user_id) values ("Pay bill to %s",%s,%s,%s,%s,%s)'
            val = (billing_type, datetime.now(), amount, billing_no, billing_type, auth.user.id)
            result = db.insert(statment, val)
            if not result:
                raise ErrorMessage(message="Your Pay Billing Unsuccessful.", code=403)

            return responseTemplate(message="Your Pay Billing Successful.").json()

        except ErrorMessage as e:
            ErrorMessage.response(e)
