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
    LEFT = 'left'
    LEFT_BRACKET = '('
    SPACE_REGEX = r'\s+'
    COMMENT_REGEX = r'(#.*)(?:\n|\Z)'
    EMPTY_LINE_REGEX = r'([\s]+)(?:\n)'
    EXPRESSION_NAME = 'expression'
