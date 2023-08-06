# Filename:       | macal_keywords.py
# Author:         | Marco Caspers
# Version:        | 3.1.0
# Description:
#
# Macal 2.0 Language keywords names
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.1.0 04-05-2022: Include keyword added.


"""macal Keyword Names"""

KW_IF          = 'if'
KW_ELSE        = 'else'
KW_ELIF        = 'elif'

KW_SELECT      = 'select'
KW_DISTINCT    = 'distinct'
KW_AS          = 'as'
KW_FROM        = 'from'
KW_WHERE       = 'where'
KW_MERGE       = 'merge'
KW_INTO        = 'into'

KW_FOREACH     = 'foreach'

KW_BREAK       = 'break'
KW_HALT        = 'halt'
KW_RETURN      = 'return'

KW_INCLUDE     = 'include'

TRUE           = 'true'
FALSE          = 'false'
NIL            = 'nil'
AND            = 'and'
OR             = 'or'

KW_RECORD      = 'record'
KW_ARRAY       = 'array'

Keywords = [KW_IF, KW_ELSE, KW_ELIF, KW_SELECT, KW_DISTINCT, KW_AS, KW_FROM, KW_WHERE, KW_MERGE,
                KW_INTO, KW_FOREACH, KW_BREAK, KW_HALT, KW_RETURN, KW_RECORD, KW_ARRAY, KW_INCLUDE]
