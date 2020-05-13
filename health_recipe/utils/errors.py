from rest_framework.exceptions import APIException


class ParameterException(APIException):  # 自定义异常类
    def __init__(self, msg):
        self.detail = msg