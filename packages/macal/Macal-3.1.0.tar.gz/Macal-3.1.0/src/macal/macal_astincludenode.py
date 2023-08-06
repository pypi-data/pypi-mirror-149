# Filename:       | macal_astincludenode.py
# Author:         | Marco Caspers
# Version:        | 3.1.0
# Description:
#
# Macal 3.x AST Node for include command.
#
# 3.1.0 04-05-2022: First implementation.
#

"""Implementation for AST Include command node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodetypes import INCLUDE

class ast_Include(AstNode):
    """AST Node: Include"""
    def __init__(self, lex_token, params: list):
        """Initializes function call node type"""
        super().__init__(INCLUDE, lex_token)
        self.params = params

    def __str__(self):
        result = " INCLUDE "
        first = True
        for token in self.params:
            if first:
                result = f"{result}{token.token_value}"
                first = False
            else:
                result = f"{result},{token.token_value}"
        return result