#
# Description: The exceptions class which is a container of all customize exceptions.
#
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 00:54
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from src.common.messageEnum import MessageEnum


class LogicError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return MessageEnum.E001.value % self.message


class UnexpectedEndError(Exception):
    def __str__(self):
        return MessageEnum.E002.value


class UnexpectedTokenError(Exception):

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return MessageEnum.E003.value % self.token


class ImmutableError(Exception):

    def __init__(self, var_name):
        self.var_name = var_name

    def __str__(self):
        return MessageEnum.E004.value % self.var_name
