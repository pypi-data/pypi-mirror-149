#!/usr/bin/python3
#
# Filename:       | macal.py
# Author:         | Marco Caspers
# Version:        | 3.1.0
# Description:
#
# Macal 2.0 language Initialization
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)
#
# 3.1.0 04-05-2022: Added include to the language.
#

"""macal Main class implementation"""

from .macal_lexer import MacalTokenizer
from .macal_parser import MacalParser
from .macal_interpreter import MacalInterpreter
from .macal_library import MacalLibrary
from .macal_scope import MacalScope

from os.path import join

__version__ = "3.1.0"
__author__ = "Marco Caspers"
__credits__ = "Copyright (c) 2022 Westcon Security Netherlands"

class Macal:
    """macal Language"""
    def __init__(self):
        """Initializes macal Language class"""
        self.lexer       = MacalTokenizer()
        self.parser      = MacalParser()
        self.interpreter = MacalInterpreter()
        self.source      = None
        self.tokens      = None
        self.ast_tree    = None
        self.debug       = False
        self.print_tree  = False
        self.print_scope = False
        self.scope       = self.interpreter.scope
        self.Libraries:  list = []
        self.scope.Libraries = self.Libraries
        self.interpreter.IncludeRunner = self.run_include
        self.include_folder = ''

    def run_from_file(self, filename, **kwargs):
        """Runs the language using a file as input"""
        try:
            with open (filename, mode = 'r', encoding = 'utf-8') as text_file:
                source = text_file.read()
            return self.run_from_string(source, **kwargs)
        except FileNotFoundError:
            raise Exception("@Runtime error: File not found: {}".format(filename))

    def register_library(self, lib: MacalLibrary):
        self.Libraries.append(lib)

    def register_variable(self, name: str, value, vartype):
        var = self.interpreter.scope.add_new_variable(name)
        var.set_value(value)
        var.set_type(vartype)
        return var

    def set_include_folder(folder: str):
        self.include_folder = folder

    def run_from_string(self, source, **kwargs):
        """Runs the language using a string as input"""
        for name, value in kwargs.items():
        	self.register_variable(name, value, MacalScope.get_value_type(value))
        self.source = source
        self.tokens   = self.lexer.lex(self.source)
        self.ast_tree = self.parser.parse(self.tokens)
        if self.debug and self.print_tree:
            print(self.ast_tree)
            print()
        result = self.interpreter.interpret(self.ast_tree)
        if self.debug and self.print_scope:
            self.interpreter.scope.print(self.interpreter.scope)
            print()
        return result

    def versions(self):
        """Returns the versions of all individual modules that make up the language."""
        vstr = "Macal version:       {}\r\n".format(__version__)
        vstr = "{}Tokenizer version:   {}\r\n".format(vstr, self.lexer.version)
        vstr = "{}Parser version:      {}\r\n".format(vstr, self.parser.version)
        vstr = "{}interpreter version: {}\r\n\r\n".format(vstr, self.interpreter.version)
        vstr = "{}libraries:\n".format(vstr)
        for lib in self.Libraries:
        	vstr = "{}{:<10}           {}\r\n".format(vstr, lib.name, lib.version)
        return vstr


    def run_include(self, include: str):
        if self.scope.have_include(include) == False:
            lang = Macal()
            lang.scope.name = include
            lang.scope.Libraries = self.scope.Libraries
            filename = join(self.include_folder,"{}.mcl".format(include))
            self.scope.includes.append(lang.scope)
            kwargs = {}
            lang.run_from_file(filename, **kwargs)

