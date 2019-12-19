class _ResponseBase:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def __repr__(self):
        response = {'code': self.code, 'message': self.message}
        if self.data is not None:
            response['data'] = self.data
        return str(response)

    def to_json(self):
        response = {'code': self.code, 'message': self.message}
        if self.data is not None:
            response['data'] = self.data
        return response


class ResponseSuccess(_ResponseBase):
    def __init__(self, code=200, message='successful', data=None):
        super().__init__(code, message, data)


class ResponseFailed(_ResponseBase):
    def __init__(self, code=500, message='failed', data=None):
        super().__init__(code, message, data)
