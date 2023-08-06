# Filename:       | macal_parsernodetypes.py
# Author:         | Marco Caspers
# Version:        | 3.1.0
# Description:
#
# Macal 2.0 AST Node type names
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.1.0 04-05-2022: Include added.
#

"""AST Node type names"""

BLOCK    = "BLOCK"
ASSIGN   = "ASSIGN"
VARIABLE = "VARIABLE"
INDEX    = "INDEX"
PARAMS   = "PARAMS"
CALL     = "CALL"
IF       = "IF"
ELIF     = "ELIF"
ELSE     = "ELSE"
FOREACH  = "FOREACH"
HALT     = "HALT"
BREAK    = "BREAK"
RETURN   = "RETURN"
SELECT   = "SELECT"
INCLUDE  = "INCLUDE"