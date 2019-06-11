#
# Description: The Parser class.
# 
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 19:03
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from rply import ParserGenerator
from src.common.tokenEnum import *
from src.util.ast import *
from src.common.constants import AppConstant


# State instance which gets passed to parser !
class ParserState(object):
    def __init__(self):
        # We want to hold a dict of global-declared variables & functions.
        self.variables = {}
        self.functions = {}
        pass  # End ParserState's constructor !


class Parser:
    def __init__(self, syntax=False):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            get_all_tokens_name(),
            # A list of precedence rules with ascending precedence, to
            # disambiguate ambiguous production rules.
            precedence=(
                (AppConstant.LEFT, [TokenEnum.FUNCTION.name]),
                (AppConstant.LEFT, [TokenEnum.LET.name]),
                (AppConstant.LEFT, [TokenEnum.ASSIGN.name]),
                (AppConstant.LEFT, [TokenEnum.IF.name, TokenEnum.ELSE.name, TokenEnum.SEMI_COLON.name]),
                (AppConstant.LEFT, [TokenEnum.AND.name, TokenEnum.OR.name]),
                (AppConstant.LEFT, [TokenEnum.NOT.name]),
                (AppConstant.LEFT, [TokenEnum.EQ.name, TokenEnum.NEQ.name, TokenEnum.GTEQ.name,
                                    TokenEnum.GT.name, TokenEnum.LT.name, TokenEnum.LTEQ.name]),
                (AppConstant.LEFT, [TokenEnum.SUM.name, TokenEnum.SUB.name]),
                (AppConstant.LEFT, [TokenEnum.MUL.name, TokenEnum.DIV.name]),
                (AppConstant.LEFT, [TokenEnum.STRING.name, TokenEnum.INTEGER.name, TokenEnum.FLOAT.name,
                                    TokenEnum.BOOLEAN.name, TokenEnum.PI.name, TokenEnum.E.name])
            )
        )
        self.syntax = syntax
        self.parse()
        pass  # End Parser's constructor !

    def parse(self):
        @self.pg.production("main : program")
        def main_program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.PROGRAM_NODE_NAME, p[0])]
            return Main(p[0])

        @self.pg.production('program : statement_full')
        def program_statement(state, p):
            if self.syntax is True:
                return [Node(AppConstant.STATEMENT_FULL_NODE_NAME, p[0])]
            return Program(p[0], None, state)

        @self.pg.production('program : statement_full program')
        def program_statement_program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.STATEMENT_FULL_NODE_NAME, p[0]), Node(AppConstant.PROGRAM_NODE_NAME, p[1])]
            return Program(p[0], p[1], state)

        @self.pg.production('expression : LEFT_PARENT expression RIGHT_PARENT')
        def expression_parenthesis(state, p):
            if self.syntax is True:
                return [Node('{'), Node(AppConstant.EXPRESSION_NODE_NAME, p[1]),
                        Node('}')]
            return ExpressParenthesis(p[1])

        @self.pg.production('statement_full : IF LEFT_PARENT expression RIGHT_PARENT LEFT_BRACKET block RIGHT_BRACKET')
        def expression_if(state, p):
            if self.syntax is True:
                return [Node(AppConstant.IF_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}'),
                        Node('{'), Node(AppConstant.BLOCK_NODE_NAME, p[5]),
                        Node('}')]
            return If(condition=p[2], body=p[5], state=state)

        @self.pg.production('statement_full : IF LEFT_PARENT expression RIGHT_PARENT LEFT_BRACKET'
                            ' block '
                            'RIGHT_BRACKET ELSE LEFT_BRACKET'
                            ' block '
                            'RIGHT_BRACKET')
        def expression_if_else(state, p):
            if self.syntax is True:
                return [Node(AppConstant.IF_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}'),
                        Node('{'), Node(AppConstant.BLOCK_NODE_NAME, p[5]),
                        Node('}'), Node(AppConstant.ELSE_NODE_NAME),
                        Node('{'), Node(AppConstant.BLOCK_NODE_NAME, p[9]),
                        Node('}')]
            return If(condition=p[2], body=p[5], else_body=p[9], state=state)

        @self.pg.production('block : statement_full')
        def block_expr(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0])]
            return Block(p[0], None, state)

        @self.pg.production('block : statement_full block')
        def block_expr_block(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0]), Node(AppConstant.BLOCK_NODE_NAME, p[1])]
            return Block(p[0], p[1], state)

        @self.pg.production('statement_full : statement ' + TokenEnum.SEMI_COLON.name)
        def statement_full(state, p):
            if self.syntax is True:
                return [Node(AppConstant.STATEMENT_NODE_NAME, p[0]), Node(AppConstant.SEMI_COLON_SIGN)]
            return StatementFull(p[0])

        @self.pg.production('statement : expression')
        def statement_expr(state, p):
            if self.syntax is True:
                return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0])]
            return Statement(p[0])

        @self.pg.production('statement : LET IDENTIFIER ASSIGN expression')
        def statement_assignment(state, p):
            if self.syntax is True:
                return [Node(AppConstant.LET_NODE_NAME), Node(AppConstant.IDENTIFIER_NODE_NAME, p[1]),
                        Node(AppConstant.EQUAL_SIGN), Node(AppConstant.EXPRESSION_NODE_NAME, p[3])]
            return Assignment(Variable(p[1].getstr(), state), p[3], state)

        @self.pg.production('statement_full : FUNCTION IDENTIFIER LEFT_PARENT RIGHT_PARENT LEFT_BRACKET block RIGHT_BRACKET')
        def statement_func_noargs(state, p):
            if self.syntax is True:
                return [Node(AppConstant.FUNCTION_NODE_NAME), Node(AppConstant.IDENTIFIER_NODE_NAME, p[1]),
                        Node('{'), Node('}'),
                        Node('{'), Node(AppConstant.BLOCK_NODE_NAME, p[5]),
                        Node('}')]
            return FunctionDeclaration(name=p[1].getstr(), args=None, block=p[5], state=state)

        @self.pg.production('expression : NOT expression')
        def expression_not(state, p):
            if self.syntax is True:
                return [Node(AppConstant.NOT_NODE_NAME), Node(AppConstant.EXPRESSION_NODE_NAME, p[1])]
            return Not(p[1], state)

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_binary_operator(state, p):
            if p[1].gettokentype() == TokenEnum.SUM.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.SUM_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return Sum(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.SUB.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.SUM_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return Sub(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.MUL.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.MUL_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return Mul(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.DIV.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.DIV_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return Div(p[0], p[2], state)
            else:
                raise LogicError('Oops, this should not be possible!')

        @self.pg.production('expression : expression NEQ expression')
        @self.pg.production('expression : expression EQ expression')
        @self.pg.production('expression : expression GTEQ expression')
        @self.pg.production('expression : expression LTEQ expression')
        @self.pg.production('expression : expression GT expression')
        @self.pg.production('expression : expression LT expression')
        @self.pg.production('expression : expression AND expression')
        @self.pg.production('expression : expression OR expression')
        def expression_equality(state, p):
            if p[1].gettokentype() == TokenEnum.EQ.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.EQUAL_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return Equal(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.NEQ.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.NOT_EQUAL_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return NotEqual(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.GTEQ.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.GREATER_THAN_EQUAL_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return GreaterThanEqual(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.LTEQ.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.LESS_THAN__EQUAL_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return LessThanEqual(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.GT.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.GREATER_THAN_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return GreaterThan(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.LT.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.LESS_THAN_SIGN),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return LessThan(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.AND.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.AND_NODE_NAME),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return And(p[0], p[2], state)
            elif p[1].gettokentype() == TokenEnum.OR.name:
                if self.syntax is True:
                    return [Node(AppConstant.EXPRESSION_NODE_NAME, p[0]), Node(AppConstant.OR_NODE_NAME),
                            Node(AppConstant.EXPRESSION_NODE_NAME, p[2])]
                return Or(p[0], p[2], state)
            else:
                raise LogicError("Shouldn't be possible")

        @self.pg.production('expression : INPUTTER LEFT_PARENT RIGHT_PARENT')
        def program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.INPUTTER_NODE_NAME), Node('{'),
                        Node('}')]
            return Input()

        @self.pg.production('expression : INPUTTER LEFT_PARENT expression RIGHT_PARENT')
        def program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.INPUTTER_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Input(expression=p[2], state=state)

        @self.pg.production('statement : PRINT LEFT_PARENT RIGHT_PARENT')
        def program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.PRINT_NODE_NAME), Node('{'),
                        Node('}')]
            return Print()

        @self.pg.production('statement : PRINT LEFT_PARENT expression RIGHT_PARENT')
        def program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.PRINT_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Print(first_expression=p[2], state=state)

        @self.pg.production('statement : PRINT LEFT_PARENT expression COMMA expression RIGHT_PARENT')
        def program(state, p):
            if self.syntax is True:
                return [Node(AppConstant.PRINT_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Print(first_expression=p[2], second_expression=p[4], state=state)

        @self.pg.production('expression : ABSOLUTE LEFT_PARENT expression RIGHT_PARENT')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_ABS_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Absolute(p[2], state)

        @self.pg.production('expression : SIN LEFT_PARENT expression RIGHT_PARENT')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_SIN_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Sin(p[2], state)

        @self.pg.production('expression : COS LEFT_PARENT expression RIGHT_PARENT')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_COS_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Cos(p[2], state)

        @self.pg.production('expression : TAN LEFT_PARENT expression RIGHT_PARENT')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_TAN_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node('}')]
            return Tan(p[2], state)

        @self.pg.production('expression : POWER LEFT_PARENT expression COMMA expression RIGHT_PARENT')
        def expression_absolute(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_POW_NODE_NAME), Node('{'),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[2]), Node(AppConstant.COMMA_SIGN),
                        Node(AppConstant.EXPRESSION_NODE_NAME, p[4]), Node('}')]
            return Pow(p[2], p[4], state)

        @self.pg.production('expression : IDENTIFIER')
        def expression_variable(state, p):
            # Cannot return the value of a variable if it isn't yet defined
            if self.syntax is True:
                return [Node(AppConstant.IDENTIFIER_NODE_NAME, p[0])]
            return Variable(p[0].getstr(), state)

        @self.pg.production('expression : IDENTIFIER LEFT_PARENT RIGHT_PARENT')
        def expression_call_noargs(state, p):
            # Cannot return the value of a function if it isn't yet defined
            if self.syntax is True:
                return [Node(AppConstant.IDENTIFIER_NODE_NAME, p[0]),
                        Node('{'), Node('}')]
            return CallFunction(name=p[0].getstr(), args=None, state=state)

        @self.pg.production('expression : const')
        def expression_const(state, p):
            if self.syntax is True:
                return [Node(AppConstant.CONSTANT_NODE_NAME, p[0])]
            return p[0]

        @self.pg.production('const : FLOAT')
        def constant_float(state, p):
            if self.syntax is True:
                return [Node(AppConstant.FLOAT_NODE_NAME, p[0])]
            return Float(p[0].getstr(), state)

        @self.pg.production('const : BOOLEAN')
        def constant_boolean(state, p):
            if self.syntax is True:
                return [Node(AppConstant.BOOLEAN_NODE_NAME, p[0])]
            return Boolean(p[0].getstr(), state)

        @self.pg.production('const : INTEGER')
        def constant_integer(state, p):
            if self.syntax is True:
                return [Node(AppConstant.INTEGER_NODE_NAME, p[0])]
            return Integer(p[0].getstr(), state)

        @self.pg.production('const : STRING')
        def constant_string(state, p):
            if self.syntax is True:
                return [Node(AppConstant.STRING_NODE_NAME, p[0])]
            return String(p[0].getstr().strip('"\''), state)

        @self.pg.production('const : PI')
        def constant_pi(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_CONST_PI_NODE_NAME, p[0])]
            return MathConstPI(p[0].getstr(), state)

        @self.pg.production('const : E')
        def constant_e(state, p):
            if self.syntax is True:
                return [Node(AppConstant.MATH_CONST_E_NODE_NAME, p[0])]
            return MathConstE(p[0].getstr(), state)

        @self.pg.error
        def error_handle(state, token):
            raise ValueError(token)

    def build(self):
        return self.pg.build()
