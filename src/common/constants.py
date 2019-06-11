#
# Description: The app constant class.
# 
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 19:35
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#


class AppConstant:
    # ------------ Common - START ------------
    LEFT = 'left'
    LEFT_PARENT_SIGN = r'('
    RIGHT_PARENT_SIGN = r')'
    LEFT_BRACKET_SIGN = r'{'
    RIGHT_BRACKET_SIGN = r'}'
    SEMI_COLON_SIGN = ';'
    COMMA_SIGN = ','
    DASH_SIGN = '-'
    ASSIGN_SIGN = '='
    SUM_SIGN = '+'
    SUB_SIGN = '-'
    MUL_SIGN = '*'
    DIV_SIGN = '/'
    EQUAL_SIGN = '=='
    NOT_EQUAL_SIGN = '!='
    GREATER_THAN_SIGN = '>'
    LESS_THAN_SIGN = '<'
    GREATER_THAN_EQUAL_SIGN = '>='
    LESS_THAN__EQUAL_SIGN = '<='
    # ------------ Common - END ------------

    # ------------ Regex - START ------------
    SPACE_REGEX = r'\s+'
    COMMENT_REGEX = r'(#.*)(?:\n|\Z)'
    EMPTY_LINE_REGEX = r'([\s]+)(?:\n)'
    NUMERICAL_REGEX = r'^-?\d+(\.\d+)?$'
    # ------------ Regex - END ------------

    # ------------ AST Constants - START ------------
    BOOLEAN_VALUES_ACCEPTED = ["true", "false", "True", "False", "TRUE", "FALSE"]
    BOOLEAN_TRUE_LOWER = 'true'
    BOOLEAN_FALSE_LOWER = 'false'
    COMMON_FUNCTION_REP = '%s(%s)'
    VARIABLE_FUNC_REP = 'Variable(%s)'
    FUNC_DECLARE_REP = "<function '%s'>"
    IF_ELSE_FUNC_REP = 'If(%s) Then(%s) Else(%s)'
    FUNCTION_REP_THREE_PARAMS = '%s(%s, %s)'
    MATH_ABS_NODE_NAME = 'ABSOLUTE'
    MATH_SIN_NODE_NAME = 'SIN'
    MATH_COS_NODE_NAME = 'COS'
    MATH_TAN_NODE_NAME = 'TAN'
    MATH_POW_NODE_NAME = 'POWER'
    BLOCK_NODE_NAME = 'block'
    CONSTANT_NODE_NAME = 'const'
    IDENTIFIER_NODE_NAME = 'IDENTIFIER'
    LET_NODE_NAME = 'LET'
    AND_NODE_NAME = 'AND'
    OR_NODE_NAME = 'OR'
    NOT_NODE_NAME = 'NOT'
    PRINT_NODE_NAME = 'PRINT'
    INPUTTER_NODE_NAME = 'INPUTTER'
    EXPRESSION_NODE_NAME = 'expression'
    STATEMENT_NODE_NAME = 'statement'
    PROGRAM_NODE_NAME = 'program'
    STATEMENT_FULL_NODE_NAME = 'statement_full'
    IF_NODE_NAME = 'IF'
    ELSE_NODE_NAME = 'ELSE'
    FUNCTION_NODE_NAME = 'FUNCTION_NODE_NAME'
    FLOAT_NODE_NAME = 'FLOAT'
    BOOLEAN_NODE_NAME = 'BOOLEAN'
    INTEGER_NODE_NAME = 'INTEGER'
    STRING_NODE_NAME = 'STRING'
    MATH_CONST_PI_NODE_NAME = 'CONST.PI'
    MATH_CONST_E_NODE_NAME = 'CONST.E'
    # ------------ AST Constants - END ------------
