#
# Description: The token enumeration class.
#
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 18:52
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from enum import Enum


class TokenEnum(Enum):
    # Constant
    FLOAT = r'-?\d+\.\d+'
    INTEGER = r'-?\d+'
    STRING = r'(""".*""")|(".*")|(\'.*\')'
    BOOLEAN = r'true(?!\w)|false(?!\w)|True(?!\w)|False(?!\w)|TRUE(?!\w)|FALSE(?!\w)'
    E = r'-?CONST\.E'
    PI = r'-?CONST\.PI'
    # Mathematical Operators
    SUM = r'\+'
    SUB = r'\-'
    MUL = r'\*'
    DIV = r'\/'
    # Binary Operator
    AND = r'and(?!\w)'
    OR = r'or(?!\w)'
    EQ = r'\=\='
    NEQ = r'\!\='
    GTEQ = r'\>\='
    LTEQ = r'\<\='
    GT = r'\>'
    LT = r'\<'
    ASSIGN = r'\='
    # Statement
    IF = r'if(?!\w)'
    ELSE = r'else(?!\w)'
    NOT = r'not!(?!\w)'
    # Semi Colon
    SEMI_COLON = r'\;'
    COMMA = r'\,'
    # Parenthesis
    LEFT_PARENT = r'\('
    RIGHT_PARENT = r'\)'
    LEFT_BRACKET = r'\{'
    RIGHT_BRACKET = r'\}'
    # Function
    INPUTTER = r'input'
    FUNCTION = r'func(?!\w)'
    PRINT = r'print'
    ABSOLUTE = r'abs'
    SIN = r'sin'
    COS = r'cos'
    TAN = r'tan'
    POWER = r'pow'
    # Assignment
    LET = r'let(?!\w)'
    IDENTIFIER = "[a-zA-Z_][a-zA-Z0-9_]*"


def get_all():
    tokens = []
    for token in TokenEnum:
        tokens.append([token.name, token.value])
    return tokens


def get_all_tokens_name():
    tokens = []
    for token in TokenEnum:
        tokens.append(token.name)
    return tokens

