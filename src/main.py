#
# Description: The main class.
#
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 18:50
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from src.util.lexer import Lexer
from src.util.parser import *
from src.util.jsonParsedTree import Node, write
from rply.lexer import LexerStream
from copy import copy
from pprint import pprint
import traceback

with open('sample/FirstSample.lang', 'r') as file:
    file_content = file.read()

lexer = Lexer().build_lexer()  # Build the lexer using LexerGenerator
tokens: LexerStream
try:
    print("------- Lexical Analysis - START -------")
    tokens = lexer.lex(file_content)  # Stream the input to analysis the lexical syntax
    pprint(list(copy(tokens)))
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("------- Lexical Analysis - END -------s")

SymbolTable = ParserState()
syntaxRoot: Node
semanticRoot = Node("main")
try:
    print("------- Program Execution - START -------")
    syntaxRoot = Node("main", Parser(syntax=True).build().parse(copy(tokens), state=SymbolTable))  # Get syntax tree !
    Parser().build().parse(copy(tokens), state=SymbolTable).eval(semanticRoot)  # Get semantic tree !
    print("------- Program Execution - END -------")
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("------- Syntax Analysis  - START -------")
    write(syntaxRoot, "SyntaxAnalysis")
    print("------- Syntax Analysis  - END -------")

    print("------- Semantic Analysis  - START -------")
    write(semanticRoot, "SemanticAnalysis")
    print("------- Semantic Analysis  - END -------")

    print("------- Symbol Table - START -------")
    pprint(SymbolTable.variables)
    pprint(SymbolTable.functions)
    print("------- Symbol Table - END -------")

