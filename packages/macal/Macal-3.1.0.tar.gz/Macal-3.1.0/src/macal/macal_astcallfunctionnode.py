# Filename:       | macal_astcallfunctionnode.py
# Author:         | Marco Caspers
# Version:        | 3.1.0
# Description:
#
# Macal 2.0 AST Node classes instantiated by the parser
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)
#
# 3.1.0 no changes here.
#

"""Implementation for AST Call Function node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodes import ast_function_Param_list
from .macal_parsernodetypes import CALL
from .macal_astvariablenode import ast_Variable

class ast_Call_function(AstNode):
    """AST Node: Call"""
    def __init__(self, tid: ast_Variable, params: ast_function_Param_list):
        """Initializes function call node type"""
        super().__init__(CALL, tid.token)
        self.ident = tid
        self.params = params

    def count(self):
        """returns the number of parameters in the list"""
        return self.params.count()

    def __str__(self):
        return f" CALL {self.token.token_value}{self.params}"