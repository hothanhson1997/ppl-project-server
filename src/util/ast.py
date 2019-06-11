#
# Description: The ast class which represent the Abstract Syntax Tree.
# 
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 00:55
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from rply.token import BaseBox
from src.common.exceptions import *
from src.util.jsonParsedTree import *
from src.common.tokenEnum import *
from src.common.messageEnum import MessageEnum
from src.common.constants import AppConstant


class Program(BaseBox):
    def __init__(self, statement, program, state):
        self.state = state
        if type(program) is Program:
            self.statements = program.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, node):
        result = None
        for i, statement in enumerate(self.statements):
            left = Node(AppConstant.STATEMENT_FULL_NODE_NAME)
            right = Node(AppConstant.PROGRAM_NODE_NAME)
            if i == len(self.statements) - 1:
                node.children.extend([left])
            else:
                node.children.extend([left, right])
            node = right
            result = statement.eval(left)
        return result

    def rep(self):
        result = 'Program('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class Block(BaseBox):
    def __init__(self, statement, block, state):
        self.state = state
        if type(block) is Block:
            self.statements = block.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, node):
        result = None
        for i, statement in enumerate(self.statements):
            left = Node(AppConstant.STATEMENT_FULL_NODE_NAME)
            right = Node(AppConstant.BLOCK_NODE_NAME)
            if i == len(self.statements) - 1:
                node.children.extend([left])
            else:
                node.children.extend([left, right])
            node = right
            result = statement.eval(left)
        return result

    def rep(self):
        result = 'Block('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class If(BaseBox):
    def __init__(self, condition, body, else_body=None, state=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.state = state

    def eval(self, node):
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.IF_NODE_NAME), Node('('), expression,
                              Node(')')])
        condition = self.condition.eval(expression)
        block = Node(AppConstant.BLOCK_NODE_NAME)
        node.children.extend([Node('{'), block, Node('}')])
        else_block = Node(AppConstant.BLOCK_NODE_NAME)
        if self.else_body is not None:
            node.children.extend([Node(AppConstant.ELSE_NODE_NAME), Node('{'), else_block,
                                  Node('}')])
        if bool(condition) is True:
            return self.body.eval(block)
        else:
            if self.else_body is not None:
                return self.else_body.eval(else_block)
        return None

    def rep(self):
        return AppConstant.IF_ELSE_FUNC_REP % (self.condition.rep(), self.body.rep(), self.else_body.rep())


class Variable(BaseBox):
    def __init__(self, name, state):
        self.name = str(name)
        self.value = None
        self.state = state

    def get_name(self):
        return str(self.name)

    def eval(self, node):
        ident_node = Node(TokenEnum.IDENTIFIER.name)
        node.children.extend([ident_node])
        if dict(self.state.variables).get(self.name) is not None:
            self.value = self.state.variables[self.name]
            ident_node.children.extend([Node(self.name, [Node(self.value)])])
            return self.value
        ident_node.children.extend([Node(MessageEnum.EAST001.value % str(self.name))])
        raise LogicError(MessageEnum.EAST001.value % str(self.name))

    def to_string(self):
        return str(self.name)

    def rep(self):
        return AppConstant.VARIABLE_FUNC_REP % self.name


class FunctionDeclaration(BaseBox):
    def __init__(self, name, args, block, state):
        self.name = name
        self.args = args
        self.block = block
        state.functions[self.name] = self

    def eval(self, node):
        ident_node = Node(self.name)
        node.children.extend([Node(TokenEnum.FUNCTION.name), ident_node,
                              Node('{'), Node(AppConstant.BLOCK_NODE_NAME),
                              Node('}')])
        return self

    def to_string(self):
        return AppConstant.FUNC_DECLARE_REP % self.name


class CallFunction(BaseBox):
    def __init__(self, name, args, state):
        self.name = name
        self.args = args
        self.state = state

    def eval(self, node):
        ident_node = Node(self.name + " ( )")
        node.children.extend([ident_node])
        return self.state.functions[self.name].block.eval(ident_node)

    def to_string(self):
        return "<call '%s'>" % self.name


class BaseMathFunction(BaseBox):

    def __init__(self, expression, state):
        self.expression = expression
        self.value = None
        self.state = state
        self.max_length = 10

    def eval(self, node):
        raise NotImplementedError(MessageEnum.EAST006)

    def to_string(self):
        return str(self.value)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Absolute(BaseMathFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.MATH_ABS_NODE_NAME), Node('('), expression,
                              Node(')'), Node(AppConstant.SEMI_COLON_SIGN)])
        self.value = self.expression.eval(expression)
        if re.search(AppConstant.NUMERICAL_REGEX, str(self.value)):
            self.value = abs(self.value)
            return self.value
        else:
            raise ValueError(MessageEnum.EAST002.value % self.__class__.__name__.upper())

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Sin(BaseMathFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re
        import math
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.MATH_SIN_NODE_NAME), Node('('), expression,
                              Node(')')])
        self.value = self.expression.eval(expression)
        if re.search(AppConstant.NUMERICAL_REGEX, str(self.value)):
            self.value = round(math.sin(self.value), self.max_length)
            return self.value
        else:
            raise ValueError(MessageEnum.EAST002.value % self.__class__.__name__.upper())

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Cos(BaseMathFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.MATH_COS_NODE_NAME), Node('('), expression,
                              Node(')')])
        self.value = self.expression.eval(expression)
        if re.search(AppConstant.NUMERICAL_REGEX, str(self.value)):
            import math
            self.value = round(math.cos(self.value), self.max_length)
            return self.value
        else:
            raise ValueError(MessageEnum.EAST002.value % self.__class__.__name__.upper())

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Tan(BaseMathFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re
        import math
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.MATH_TAN_NODE_NAME), Node('('), expression,
                              Node(')')])
        self.value = self.expression.eval(expression)
        if re.search(AppConstant.NUMERICAL_REGEX, str(self.value)):
            self.value = round(math.tan(self.value), self.max_length)
            return self.value
        else:
            raise ValueError(MessageEnum.EAST002.value % self.__class__.__name__.upper())

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Pow(BaseMathFunction):
    def __init__(self, expression, sec_expression, state):
        super().__init__(expression, state)
        self.sec_expression = sec_expression
        self.sec_value = None

    def eval(self, node):
        import re
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        sec_expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.MATH_POW_NODE_NAME), Node('('), expression,
                              Node(AppConstant.COMMA_SIGN), sec_expression, Node(')')])
        self.value = self.expression.eval(expression)
        self.sec_value = self.sec_expression.eval(sec_expression)
        fst_matching = re.search(AppConstant.NUMERICAL_REGEX, str(self.value))
        sec_matching = re.search(AppConstant.NUMERICAL_REGEX, str(self.sec_value))
        if fst_matching and sec_matching:
            import math
            self.value = math.pow(self.value, self.sec_value)
            return self.value
        else:
            raise ValueError(MessageEnum.EAST002.value % self.__class__.__name__.upper())

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Constant(BaseBox):
    def __init__(self, state):
        self.value = None
        self.state = state

    def eval(self, node):
        value = Node(self.value)
        typed = Node(self.__class__.__name__.upper(), [value])
        constant = Node(AppConstant.CONSTANT_NODE_NAME, [typed])
        node.children.extend([constant])
        return self.value

    def to_string(self):
        return str(self.value)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Boolean(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        if AppConstant.BOOLEAN_VALUES_ACCEPTED.__contains__(value):
            if value.lower().__eq__(AppConstant.BOOLEAN_TRUE_LOWER):
                self.value = True
            if value.lower().__eq__(AppConstant.BOOLEAN_FALSE_LOWER):
                self.value = False
        else:
            raise TypeError(MessageEnum.EAST004)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Integer(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = int(value)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class Float(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = float(value)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class String(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = str(value)

    def to_string(self):
        return '"%s"' % str(self.value)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class MathConstPI(Constant):
    def __init__(self, name, state):
        super().__init__(state)
        import math
        self.name = str(name)
        if str(name).__contains__('-'):
            self.value = float(-math.pi)
        else:
            self.value = float(math.pi)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class MathConstE(Constant):
    def __init__(self, name, state):
        super().__init__(state)
        import math
        self.name = str(name)
        if str(name).__contains__(AppConstant.DASH_SIGN):
            self.value = float(-math.e)
        else:
            self.value = float(math.e)

    def rep(self):
        return AppConstant.COMMON_FUNCTION_REP % (self.__class__.__name__, self.value)


class BinaryOp(BaseBox):
    def __init__(self, left, right, state):
        self.left = left
        self.right = right
        self.state = state


class Assignment(BinaryOp):
    def eval(self, node):
        if isinstance(self.left, Variable):
            var_name = self.left.get_name()
            if dict(self.state.variables).get(var_name) is None:
                identifier = Node(AppConstant.IDENTIFIER_NODE_NAME, [Node(var_name)])
                expression = Node(AppConstant.EXPRESSION_NODE_NAME)
                node.children.extend([Node(AppConstant.LET_NODE_NAME), identifier,
                                      Node(AppConstant.ASSIGN_SIGN), expression])
                self.state.variables[var_name] = self.right.eval(expression)
                return self.state.variables

            # Otherwise raise error
            raise ImmutableError(var_name)

        else:
            raise LogicError(MessageEnum.EAST003 % self)

    def rep(self):
        return AppConstant.FUNCTION_REP_THREE_PARAMS % (self.__class__.__name__, self.left.rep(), self.right.rep())


class Sum(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.SUM_SIGN), right])
        return self.left.eval(left) + self.right.eval(right)


class Sub(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.SUB_SIGN), right])
        return self.left.eval(left) - self.right.eval(right)


class Mul(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.MUL_SIGN), right])
        return self.left.eval(left) * self.right.eval(right)


class Div(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.DIV_SIGN), right])
        return self.left.eval(left) / self.right.eval(right)


class Equal(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.EQUAL_SIGN), right])
        return self.left.eval(left) == self.right.eval(right)


class NotEqual(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.NOT_EQUAL_SIGN), right])
        return self.left.eval(left) != self.right.eval(right)


class GreaterThan(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.GREATER_THAN_SIGN), right])
        return self.left.eval(left) > self.right.eval(right)


class LessThan(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.LESS_THAN_SIGN), right])
        return self.left.eval(left) < self.right.eval(right)


class GreaterThanEqual(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.GREATER_THAN_EQUAL_SIGN), right])
        return self.left.eval(left) >= self.right.eval(right)


class LessThanEqual(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.LESS_THAN__EQUAL_SIGN), right])
        return self.left.eval(left) <= self.right.eval(right)


class And(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.AND_NODE_NAME), right])
        return self.left.eval(left) and self.right.eval(right)


class Or(BinaryOp):
    def eval(self, node):
        left = Node(AppConstant.EXPRESSION_NODE_NAME)
        right = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([left, Node(AppConstant.OR_NODE_NAME), right])
        return self.left.eval(left) or self.right.eval(right)


class Not(BaseBox):
    def __init__(self, expression, state):
        self.value = expression
        self.state = state

    def eval(self, node):
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node(AppConstant.NOT_NODE_NAME), expression])
        self.value = self.value.eval(expression)
        if isinstance(self.value, bool):
            return not bool(self.value)
        raise LogicError(MessageEnum.EAST005)


class Print(BaseBox):
    def __init__(self, first_expression=None, second_expression=None, state=None):
        self.first_expression = first_expression
        self.second_expression = second_expression
        self.state = state

    def eval(self, node):
        node.children.extend([Node(AppConstant.PRINT_NODE_NAME), Node('(')])
        if self.first_expression is None:
            print()
        elif self.second_expression is None:
            expression = Node(AppConstant.EXPRESSION_NODE_NAME)
            node.children.extend([expression])
            print(self.first_expression.eval(expression))
        else:
            fst_expression = Node(AppConstant.EXPRESSION_NODE_NAME)
            node.children.extend([fst_expression])
            node.children.extend([Node(AppConstant.COMMA_SIGN)])
            sec_expression = Node(AppConstant.EXPRESSION_NODE_NAME)
            node.children.extend([sec_expression])
            print(self.first_expression.eval(fst_expression), self.second_expression.eval(sec_expression))
        node.children.extend([Node(')')])


class Input(BaseBox):
    def __init__(self, expression=None, state=None):
        self.value = expression
        self.state = state

    def eval(self, node):
        node.children.extend([Node(AppConstant.INPUTTER_NODE_NAME), Node('(')])
        if self.value is None:
            result = input()
        else:
            expression = Node(AppConstant.EXPRESSION_NODE_NAME)
            node.children.extend([expression])
            result = input(self.value.eval(expression))
        node.children.extend([Node(')')])
        import re
        if re.search(AppConstant.NUMERICAL_REGEX, str(result)):
            return float(result)
        else:
            return str(result)


class Main(BaseBox):
    def __init__(self, program):
        self.program = program

    def eval(self, node):
        program = Node(AppConstant.PROGRAM_NODE_NAME)
        node.children.extend([program])
        return self.program.eval(program)


class ExpressParenthesis(BaseBox):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, node):
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([Node('('), expression, Node(')')])
        return self.expression.eval(expression)


class StatementFull(BaseBox):
    def __init__(self, statement):
        self.statement = statement

    def eval(self, node):
        statement = Node(AppConstant.STATEMENT_NODE_NAME)
        node.children.extend([statement, Node(AppConstant.SEMI_COLON_SIGN)])
        return self.statement.eval(statement)


class Statement(BaseBox):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, node):
        expression = Node(AppConstant.EXPRESSION_NODE_NAME)
        node.children.extend([expression])
        return self.expression.eval(expression)
