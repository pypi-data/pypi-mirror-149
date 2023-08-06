# -*- coding: utf-8 -*-


class RQFactorUserException(Exception):
    pass


class InvalidArgument(RQFactorUserException):
    pass


class RQFactorDataUnavailable(Exception):
    pass


class InvalidUserFactor(RQFactorUserException):
    pass
