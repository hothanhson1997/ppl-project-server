#
# Description: The lexer class.
#
# change history:
# date            defect#        person            comments
# --------------------------------------------------------------------------------------------------------------------
# 2019-05-20      ********       Huy.Nguyen        create file
#
# @author: Huy.Nguyen
# @date: 2019-05-20 18:51
# @copyright: 2019, Mr.Tomatoes. All Rights Reserved.
#

from rply import LexerGenerator
import re
from src.common.tokenEnum import TokenEnum
from src.common.constants import AppConstant


class Lexer:

    def __init__(self):
        self.lg = LexerGenerator()
        self._build_lex_rules()

    def _build_lex_rules(self):
        for enum in TokenEnum:
            self.lg.add(enum.name, enum.value)
        # Parenthesis
        self.lg.ignore(AppConstant.SPACE_REGEX)

    def build_lexer(self):
        return self.lg.build()

    def clean_source(self, source_code):
        comment = re.search(AppConstant.COMMENT_REGEX, source_code)
        while comment is not None:
            start, end = comment.span(1)
            assert start >= 0 and end >= 0
            source_code = source_code[0:start] + source_code[end:]
            comment = re.search(AppConstant.COMMENT_REGEX, source_code)

        empty_line = re.search(AppConstant.EMPTY_LINE_REGEX, source_code)
        while empty_line is not None:
            start, end = empty_line.span(1)
            assert start >= 0 and end >= 0
            source_code = source_code[0:start] + source_code[end:]
            empty_line = re.search(AppConstant.EMPTY_LINE_REGEX, source_code)

        return source_code




