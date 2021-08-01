class account:
    def __init__(self, args):
        self.id = args[0]
        self.username = args[1]
        self.active = args[3]
        self.lang = args[4]
        self.created_at = args[5]

    def toMap(self):
        return {
            "id": self.id,
            "username": self.username,
            "active": self.active,
            "lang": self.lang,
            "created_at": self.created_at,
        }
