# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



class PythonToolException(Exception):
    def __init__(self, message):
        super(PythonToolException, self).__init__(message)

class KeystoneAuthenticatorError(Exception):
    def __init__(self):
        super().__init__(self)


class KeystoneNotReachableError(KeystoneAuthenticatorError):
    def __init__(self, authority, ex):
        self.message = "Cannot contact Cegal Keystone ({}).  Please check your network configuration and firewall settings".format(authority.fqdn())
        self.ex = ex

    def __str__(self):
        return "{} [{}]".format(self.message, self.ex)


class KeystoneNotRespondingError(KeystoneAuthenticatorError):
    def __init__(self, authority, response):
        self.message = "Cegal Keystone ({}) did not respond succcesfully".format(authority.fqdn())
        self.response = response

    def __str__(self):
        return "{} [{}: {}]".format(self.message, self.response.code, self.response.read())


class KeystoneUnexpectedResponseError(KeystoneAuthenticatorError):
    def __init__(self, authority, ex):
        self.message = "Cegal Keystone ({}) gave an unexpected reponse".format(authority.fqdn())
        self.ex = ex

    def __str__(self):
        return "{} [{}]".format(self.message, self.ex)


class UserErrorException(Exception):
    def __init__(self, message, stack_trace=None):
        super(UserErrorException, self).__init__(message)
        self.petrel_stack_trace = stack_trace


class UnexpectedErrorException(Exception):
    def __init__(self, message, stack_trace=None):
        super(UnexpectedErrorException, self).__init__(message)
        self.petrel_stack_trace = stack_trace
