class EmailException(Exception):
    pass

class EmailMissingParamException(EmailException):
    pass

class Email:
    def __init__(self, server, fromaddr, to, user, pw):
        self.server = server
        self.fromaddr = fromaddr
        self.to = to
        self.user = user
        self.pw = pw
        if not server and fromaddr and to and user and pw:
            raise EmailMissingParamException
