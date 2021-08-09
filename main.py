from functools import wraps

from flask import Flask, make_response, request, jsonify, url_for

from Controller.customerController import customerController
from Middleware.Authentication import Authentication
from Request.ChangePasswordCustomerRequest import ChangePasswordCustomer
from Request.PayBillingRequest import PayBilling
from Request.TransferRequest import Transfer
from Request.depositRequest import deposit
from Request.loginRequest import login
from Request.storeCustomerRequest import storeCustomer
from Request.withdrawalRequest import withdrawal

app = Flask(__name__)
prefix = "/api"


@app.route('/')
def root():
    return "welcome to Python API"


@app.route(f'{prefix}/admin/sign-in', methods=["POST"])
@login.request
def LoginAdmin():
    return Authentication.certificate(role="admin", request=request.args.to_dict())


@app.route(f'{prefix}/sign-in', methods=["POST"])
@login.request
def LoginCustomer():
    return Authentication.certificate(role="customer", request=request.args.to_dict())


@app.route(f'{prefix}/customers', methods=["POST"])
@storeCustomer.request
def customersCreate():
    return customerController().store(request=request.args.to_dict())


@app.route(f'{prefix}/customers', methods=["GET"])
@Authentication.roleAdmin
@storeCustomer.request
def customers():
    return customerController().index(request=request.args.to_dict())


csPrefix = "customers"


@app.route(f'{prefix}/{csPrefix}/enable/<id>', methods=["PUT"])
@Authentication.roleAdmin
def enableAccount(id):
    return customerController().enable(id)


@app.route(f'{prefix}/{csPrefix}/change-password/<id>', methods=["PUT"])
@Authentication.roleAdmin
def changePasswordAccount(id):
    return customerController().changePassword(id, request.args.to_dict())


@app.route(f'{prefix}/{csPrefix}/<id>', methods=["PUT", "DELETE"])
@Authentication.roleAdmin
def UpdateCustomer(id):
    if request.method == "PUT":
        return customerController().store(request=request.args.to_dict())
    else:
        return customerController().destroy(id)


@app.route(f'{prefix}/change-password', methods=["PUT"])
@Authentication.roleCustomer
@ChangePasswordCustomer.request
def changePasswordself():
    return customerController().changePasswordSelf(request.args.to_dict())


@app.route(f'{prefix}/check-balance', methods=['GET'])
@Authentication.roleCustomer
def checkBalance():
    return customerController().checkBalance()


@app.route(f'{prefix}/deposit', methods=['POST'])
@Authentication.roleCustomer
@deposit.request
def deposit():
    return customerController().deposit(request.args.to_dict())


@app.route(f'{prefix}/withdrawal', methods=['POST'])
@Authentication.roleCustomer
@withdrawal.request
def withdrawal():
    return customerController().withdrawal(request.args.to_dict())


@app.route(f'{prefix}/transfer', methods=['POST'])
@Authentication.roleCustomer
@Transfer.request
def transfer():
    return customerController().transfer(request.args.to_dict())


@app.route(f'{prefix}/pay-billing', methods=['POST'])
@Authentication.roleCustomer
@PayBilling.request
def billPayment():
    return customerController().billPayment(request.args.to_dict())


if (__name__ == '__main__'):
    app.run(debug=True, port=83, host="0.0.0.0")
