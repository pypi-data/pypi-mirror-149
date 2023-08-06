# Filename:       | macal_library_system.py                                                       
# Author:         | Marco Caspers                                                                 
# Version:        | 3.1.0
# Description:
#                                                                                                 
# Macal 2.0 Strings Library                                                                       
#                                                                                                 
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.1.0 22-04-2022: raising excption if null parameter value is passed in.
#
###################################################################################################

"""Strings library implementation"""

from .macal_library_external import *
from unidecode import unidecode
from .macal_exceptions import NilParameterValueError

class LibraryStrings(MacalLibrary):
    def __init__(self):
        super().__init__("strings")
        self.RegisterFunction("len",            [FuncArg("arg", ANY)], self.StrLen)
        self.RegisterFunction("left",           [FuncArg("arg", STRING),    FuncArg("length", INT)], self.StrLeft)
        self.RegisterFunction("mid",            [FuncArg("arg", STRING),    FuncArg("start", INT),   FuncArg("length", INT)], self.StrMid)
        self.RegisterFunction("tostring",       [FuncArg("arg", ANY)], self.ToString)
        self.RegisterFunction("format",         [FuncArg("format", STRING), FuncArg("arg", ANY)], self.StrFormat)
        self.RegisterFunction("replace",        [FuncArg("_var", STRING),  FuncArg("from", STRING), FuncArg("with", STRING)], self.StrReplace)
        self.RegisterFunction("startswith",     [FuncArg("haystack", STRING), FuncArg("needle", STRING)], self.StartsWith)
        self.RegisterFunction("removeNonAscii", [FuncArg("text", STRING)], self.RemoveNonAscii)
        self.RegisterFunction("replaceEx",      [FuncArg("_var", STRING),FuncArg("repl", STRING),FuncArg("by", STRING)], self.ReplaceEx)
        self.version = "3.0.7"

    def StrLen(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of console function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        arg = self.GetParamValue(params, "arg")
        if arg is None:
            raise NilParameterValueError(name, scope, "arg", name)
        result = len(self.GetParamValue(params, "arg"))
        scope.SetReturnValue(result, INT)
    
    def StrLeft(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of left function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        arg = self.GetParamValue(params, "arg")
        argl = self.GetParamValue(params, "length")
        if arg is None:
            raise NilParameterValueError(name, scope, "arg", name)
        if argl is None:
            raise NilParameterValueError(name, scope, "length", name)
        result = self.GetParamValue(params, "arg")[0:argl]
        scope.SetReturnValue(result, STRING)

    def StrMid(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of mid function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        arg = self.GetParamValue(params, "arg")
        args = self.GetParamValue(params, "start")
        argl = self.GetParamValue(params, "length")
        if arg is None:
            raise NilParameterValueError(name, scope, "arg", name)
        if arg2 is None:
            raise NilParameterValueError(name, scope, "start", name)
        if argl is None:
            raise NilParameterValueError(name, scope, "length", name)

        result = self.GetParamValue(params, "arg")[self.GetParamValue(params, "start"):self.GetParamValue(params, "length")]
        scope.SetReturnValue(result, STRING);

    def ToString(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of ToString function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        argvalue = self.GetParamValue(params, "arg")
        result = f"{argvalue}"
        scope.SetReturnValue(result, STRING);

    def StrFormat(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of StrFormat function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        result = self.GetParamValue(params, "format").format(self.GetParamValue(params, "arg"))
        scope.SetReturnValue(result, STRING);

    def StrReplace(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of StrReplace function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var = self.GetParamValue(params, "_var")
        if var is None:
           raise NilParameterValueError(name, scope, "_var", name) 
        frm = self.GetParamValue(params, "from")
        if frm is None:
           raise NilParameterValueError(name, scope, "from", name) 
        result = var.replace(frm, self.GetParamValue(params, "with"))
        scope.SetReturnValue(result, STRING);

    def StartsWith(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of StartsWith function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        haystack = self.GetParamValue(params, "haystack")
        needle = self.GetParamValue(params, "needle")
        if haystack is None:
           raise NilParameterValueError(name, scope, "haystack", name) 
        if needle is None:
           raise NilParameterValueError(name, scope, "needle", name) 
        scope.SetReturnValue(str.startswith(haystack, needle), BOOL)

    def RemoveNonAscii(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of RemoveNonAscii function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        txt = self.GetParamValue(params, "text")
        if txt is None:
           raise NilParameterValueError(name, scope, "text", name) 
        result = unidecode(txt)
        scope.SetReturnValue(result, STRING)

    def ReplaceEx(self, func: MacalFunction, name: str, params: list, scope: MacalScope):
        """Implementation of ReplaceEx function"""
        self.ValidateFunction(name, func, scope)
        self.ValidateParams(name, params, scope, func)
        var  = self.GetParamValue(params, "_var")
        repl = self.GetParamValue(params, "repl")
        by   = self.GetParamValue(params, "by")
        if var is None:
           raise NilParameterValueError(name, scope, "_var", name) 
        if repl is None:
           raise NilParameterValueError(name, scope, "repl", name) 
        result = var
        for ch in repl:
            result = result.replace(ch, by)
        scope.SetReturnValue(result, STRING)