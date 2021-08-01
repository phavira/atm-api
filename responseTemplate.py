from flask import jsonify, make_response


class responseTemplate:

    def __init__(self, **keyargs):
        self.status_code = keyargs.get("status_code", 200)
        self.data = keyargs.get("data", None)
        self.message = keyargs.get("message", None)
        self.paginate = keyargs.get("paginate", None)

    def json(self):
        if self.status_code == 200:
            status = "OK"
        else:
            status = "error"
        data = {"status": status, "message": self.message}

        if self.data is not None:
            data['data'] = self.data

        if self.paginate is not None:
            data['paginate'] = {
                "total_page": self.paginate['total_page'],
                "page": self.paginate['page'],
                "total_item": self.paginate['total_item'],
                "limit": self.paginate['limit']
            }
        return jsonify(data), self.status_code
