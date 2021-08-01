class authrity:
    def __init__(self, arg=None):
        if arg is not None:
            self.id = arg[4]
            self.name = arg[1]
            self.username = arg[7]
            self.balance = arg[3]
            self.lang = arg[11]
            self.created_at = arg[12]
            self.customer_id = arg[0]
            self.password = arg[8]


user: authrity = authrity()
