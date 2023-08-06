from shioaji.base import BaseModel

class BaseError(Exception):
    def __init__(self, code, message):
        formated_mes = "StatusCode: {}, Detail: {}".format(code, message)
        super().__init__(formated_mes)
        self.code = code
        self.message = message


class TokenError(BaseError):
    """Raise when token error."""


class SystemMaintenance(BaseError):
    """Raise when system maintenance an error."""

class TimeoutError(BaseError):
    """Timeout Error"""
    def __init__(self, topic: str, extra_info: dict):
        formated_mes = "Timeout 408 Topic: {}, ExtraInfo: {}".format(topic, extra_info)
        super().__init__("408", formated_mes)
        self.topic = topic
        self.extra_info = extra_info
