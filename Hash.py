import bcrypt


class Hash:
    @staticmethod
    def make(password: str):
        salt = bcrypt.gensalt(rounds=4)
        return bcrypt.hashpw(password.encode(), salt).decode()

    @staticmethod
    def check(password: str, hashed: str):
        return bcrypt.checkpw(password.encode(), hashed.encode())
