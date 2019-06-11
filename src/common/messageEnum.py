#
# Description: The message enumeration class.
# 
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 01:23
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from enum import Enum


class MessageEnum(Enum):

    # -------------- Exception Errors - START --------------
    E001 = "Logical Error: %s"
    E002 = "Unexpected end of statement"
    E003 = "Unexpected token %s"
    E004 = "Cannot assign to immutable variable %s"
    # -------------- Exception Errors - START --------------

    # -------------- AST Errors - START --------------
    EAST001 = "The variable [%s] is not defined yet."
    EAST002 = "Can not take the [%s] value of the non-digits character."
    EAST003 = "Cannot assign to [%s]."
    EAST004 = "Cannot cast boolean value while initiating Constant!"
    EAST005 = "Cannot 'not' that."
    EAST006 = "This is abstract method from abstract class BaseMathFunction(BaseBox){...}!"
    # -------------- AST Errors - START --------------
