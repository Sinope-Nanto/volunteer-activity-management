from rest_framework.response import Response


class APIResponse:
    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def create_success(cls, data=None):
        response_data = {
            "code": 200,
            "msg": "",
            "data": {} if not data else data
        }
        print(response_data)
        return Response(data=response_data, content_type="application/json")

    @classmethod
    def create_fail(cls, code, msg=""):
        response_data = {
            "code": code,
            "msg": msg,
            "data": {}
        }
        print(response_data)
        return Response(data=response_data, content_type="application/json")

    def create(self):
        response_data = {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
        return Response(data=response_data, content_type="application/json")