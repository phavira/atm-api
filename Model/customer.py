from datetime import datetime


class customer:
    def __init__(self, arg):
        self.id = arg[0]
        self.name = arg[1]
        self.account_no = arg[2]
        self.balance = arg[3]
        self.username = arg[4]
        self.role = arg[5]
        self.lang = arg[6]
        self.created_at = arg[7]

    def toMap(self):
        return {
            "id": self.id,
            "name": self.name,
            "account_no": self.account_no,
            "balance": str(self.balance),
            "username": self.username,
            "role": self.role,
            "lang": self.lang,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%I:%S")
        }
