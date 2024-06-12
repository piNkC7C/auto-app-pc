# 自定义错误
# 当错误发生时，我们捕获到发生的错误，然后抛出我们自定义的错误
def format_response(code, message, data):
    # 在这里实现 formatResponse 函数的逻辑
    pass


# 业务处理错误基类
class ServiceException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

    # 格式化的返回错误信息
    def to_response_json(self):
        return format_response(self.code, self.args[0], None)


# 图片未找到错误
class ImageNotFoundException(ServiceException):
    def __init__(self, message):
        super().__init__(message, 101)


# 未知错误
class UnknownError(ServiceException):
    def __init__(self):
        super().__init__("server internal error", 500)
