from DBSource import DBsource


class validation:
    @staticmethod
    def statement(sql):
        db = DBsource()
        result = db.select(sql)
        return len(result) > 0