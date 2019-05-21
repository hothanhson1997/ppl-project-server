"""
    Description: The lexer generator class.
     
    change history:
    date            defect#        person            comments
    --------------------------------------------------------------------------------------------------------------------
    2019-05-20      ********       Huy.Nguyen       create file
     
    @author: Huy.Nguyen
    @date: 2019-05-20 12:01
"""

from rply import LexerGenerator

class Lexer():
  def __init__(self):
    self.lexer_generator = LexerGenerator()

  def __init__tokens(self):
    self.lexer_generator.('abstract', r'abstract')
    self.lexer_generator.('based', r'based')
    self.lexer_generator.('continue', r'continue')
    self.lexer_generator.('for', r'for')
    self.lexer_generator.('new', r'new')
    self.lexer_generator.('switch', r'switch')
    self.lexer_generator.('default', r'default')
    self.lexer_generator.('if', r'if')
    self.lexer_generator.('package', r'package')
    self.lexer_generator.('synchronized', r'synchronized')
    self.lexer_generator.('boolean', r'boolean')
    self.lexer_generator.('do', r'do')
    self.lexer_generator.('goto', r'goto')
    self.lexer_generator.('private', r'private')
    self.lexer_generator.('this', r'this')
    self.lexer_generator.('break', r'break')
    self.lexer_generator.('double', r'double')
    self.lexer_generator.('implements', r'implements')
    self.lexer_generator.('protected', r'protected')
    self.lexer_generator.('throw', r'throw')
    self.lexer_generator.('byte', r'byte')
    self.lexer_generator.('else', r'else')
    self.lexer_generator.('import', r'import')
    self.lexer_generator.('public', r'public')
    self.lexer_generator.('case', r'case')
    self.lexer_generator.('instanceof', r'instanceof')
    self.lexer_generator.('return', r'return')
    self.lexer_generator.('transient', r'transient')
    self.lexer_generator.('catch', r'catch')
    self.lexer_generator.('extends', r'extends')
    self.lexer_generator.('int', r'int')
    self.lexer_generator.('short', r'short')
    self.lexer_generator.('try', r'try')
    self.lexer_generator.('char', r'char')
    self.lexer_generator.('final', r'final')
    self.lexer_generator.('interface', r'interface')
    self.lexer_generator.('static', r'static')
    self.lexer_generator.('void', r'void')
    self.lexer_generator.('class', r'class')
    self.lexer_generator.('finally', r'finally')
    self.lexer_generator.('long', r'long')
    self.lexer_generator.('strictfp', r'strictfp')
    self.lexer_generator.('volatile', r'volatile')
    self.lexer_generator.('float', r'float')
    self.lexer_generator.('native', r'native')
    self.lexer_generator.('super', r'super')
    self.lexer_generator.('while', r'while')
    self.lexer_generator.('assert', r'assert')
    self.lexer_generator.('const', r'const')
    self.lexer_generator.('enum', r'enum')
    self.lexer_generator.('true', r'true')
    self.lexer_generator.('false', r'false')
    self.lexer_generator.('null', r'null')
    self.lexer_generator.('throws', r'throws')

