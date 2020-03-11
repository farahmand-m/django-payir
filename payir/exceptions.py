class GatewayError(RuntimeError):

    def __init__(self, error_code, error_message):
        super().__init__(error_message)
        self.error_code = error_code
        self.error_message = error_message
