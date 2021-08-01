import mysql.connector


class DBsource:
    connector = ""

    def __init__(self):
        self.connector = mysql.connector.connect(
            host="plusmalls.com",
            user="vira_db",
            password="1562572D3431F56F",
            database="atm")

    def select(self, statement):
        mycursor = self.connector.cursor()
        mycursor.execute(statement)
        return mycursor.fetchall()

    def insert(self, statement, val, commit=True):
        mycursor = self.connector.cursor()
        mycursor.execute(statement, val)
        if commit:
            self.connector.commit()
        if mycursor.rowcount > 0:
            return mycursor.lastrowid
        else:
            return False

    def update(self, statement, commit=True, val=None):
        mycursor = self.connector.cursor()
        if val is not None:
            mycursor.execute(statement, val)
        else:
            mycursor.execute(statement)

        if commit:
            self.connector.commit()
        print(mycursor.rowcount)
        return mycursor.rowcount > 0

    def delete(self, statement):
        return self.update(statement)
