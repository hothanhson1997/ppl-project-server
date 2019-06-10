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
    E001 = 'Logical error: %s'
    E002 = 'Unexpected end of statement'
    E003 = 'Unexpected token %s'
    E004 = 'Cannot assign to immutable variable %s'
