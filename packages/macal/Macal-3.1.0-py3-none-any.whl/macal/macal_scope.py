# Filename:       | macal_scope.py
# Author:         | Marco Caspers
# Description:
#
# Macal 3.0 Expression node class
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)
#
# 3.1.0 04-05-2022: Added root() function to get to the root scope.
#                   Added includes to allow adding scopes from included libraries. Only to be used in the root scope.
#                   Updated search for variables and functions to include the includes.
#

"""Scope class implementation, this class is used by the interpreter."""

from .macal_variable_types import ARRAY, BOOL, FLOAT, INT, STRING, RECORD
from .macal_keywords import NIL
from .macal_variable import MacalVariable
from .macal_function import MacalFunction

VARIABLE_COLUMN_WIDTH = 40
TYPE_COLUMN_WIDTH     = 12
VALUE_COLUMN_WIDTH    = 36

class MacalScope:
    """Scope class implements execution branch scope"""
    def __init__(self, name: str, parent):
        self.name = name
        self.variables:   list = []
        self.functions:   list = []
        self.children:    list = []
        self.includes:    list = []
        self.break_flag:  bool            = False
        self.x_halt_flag: bool            = False
        self.is_loop:     bool            = False
        self.is_function: bool            = False
        self.parent:      MacalScope      = parent
        self.Libraries:   list            = []
        self.can_search:  bool            = True

    def create_child(self, name: str, prop_loop: bool = True):
        child = MacalScope("{}->{}".format(self.name, name), self)
        if prop_loop:
            child.is_loop = self.is_loop
        child.is_function = self.is_function;
        self.children.append(child)
        return child

    def remove_child(self, child):
        self.children.remove(child)
    
    def set_halt(self):
        self.x_halt_flag = True

    def get_halt(self):
        return self.x_halt_flag

    def add_new_variable(self, name: str):
        """Adds a new PVariable to the scope and returns it."""
        variable = MacalVariable(name)
        self.variables.append(variable)
        return variable

    def add_new_function(self, name: str, parameters, block):
        """Adds a new PFunction to the scope and returns it."""
        func = MacalFunction(name, parameters, block)
        self.functions.append(func)
        return func
    
    @staticmethod
    def _obj_first_or_default(lst: list, name: str):
        """Returns the first object in the list that has name, or None if not found."""
        return next((x for x in lst if x.name == name), None)
    
    def _get_variable(self, name: str):
        """Find variable by name in the current scope"""
        return next((x for x in self.variables if x.name == name), None)

    def _get_function(self, name: str):
        """Find function by name in the current scope"""
        return next((x for x in self.functions if x.name == name), None)

    def _get_scope_exitvar(self):
        for var in self.variables:
            if var.name[:8] == "?return_":
                return var
        return None

    def SetReturnValue(self, value, valuetype):
        var = self._get_scope_exitvar()
        if var is None:
            raise Exception(f"This scope has no exitvar! {self}")
        #print(f"scope set returnvalue: {var.name} -> {value} ({valuetype})")
        var.set_value(value)
        var.set_type(valuetype)

    def _find_variable(self, name: str, scope):
        """Find variable by name in the current scope. If not found, calls parent scope to do so, if parent is not None"""
        var = scope._get_variable(name)
        if var is not None:
            return var

        if not self.can_search:
            return None

        if len(scope.Libraries) > 0:
            for lib in scope.Libraries:
                var = lib.variable_by_name(name)
                if var  is not None:
                    return var

        if len(scope.includes) > 0:
            for incl in scope.includes:
                var = incl.find_variable(name)
                if var  is not None:
                    return var

        if scope.parent is not None:
            return scope._find_variable(name, scope.parent)
        return None

    def _find_function(self, name: str, scope):
        """Find function by name in the current scope. If not found, calls parent scope to do so, if parent is not None"""
        func = scope._get_function(name)
        if func is not None:
            return func

        if len(scope.Libraries) > 0:
            for lib in scope.Libraries:
                func = lib.GetFunction(name)
                if func is not None:
                    return func

        if len(scope.includes) > 0:
            for incl in scope.includes:
                func = incl.find_function(name)
                if func is not None:
                    return func

        if scope.parent is not None:
            return scope._find_function(name, scope.parent)

        return None

    def _have_include(self, name: str, scope):
        if len(scope.includes) > 0:
            for incl in scope.includes:
                if incl.name == name:
                    return True
                if incl.has_includes():
                    result = incl.have_include(name)
                    if result:
                        return result
        if scope.parent is not None:
            return scope.have_include(name)
        return False

    def find_variable(self, name: str):
        return self._find_variable(name, self)
    
    def find_function(self, name: str):
        return self._find_function(name, self)
    
    def have_include(self, name: str):
        return self._have_include(name, self)

    def has_children(self):
        return len(self.children) > 0

    def has_variables(self):
        return len(self.variables) > 0

    def has_functions(self):
        return len(self.functions) > 0

    def has_includes(self):
        return len(self.includes) > 0

    def print_variables(self):
        """Displays a table showing all variables in this scope."""
        # define the column width
        variable_size = VARIABLE_COLUMN_WIDTH
        type_size     = TYPE_COLUMN_WIDTH
        value_size    = VALUE_COLUMN_WIDTH
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))
        print("|{}|{}|{}|".format(
            "Variable".ljust(variable_size),
            "Type".ljust(type_size),
            "Value".ljust(value_size)))
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))
        for var in self.variables:
            vt = var.get_type()
            vts = '{}'.format(vt)
            vv = repr(var.get_value())
            if isinstance(vv, MacalFunction):
                vv = vv.name
            print("|{}|{}|{}|".format(var.name.ljust(variable_size), vts.ljust(type_size), '{}'.format(vv).ljust(value_size)))
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))

    def print_functions(self):
        """Displays a table showing all functions in this scope."""
        variable_size = VARIABLE_COLUMN_WIDTH
        print(''.ljust(variable_size + 2,'_'))
        print("|{}|".format("Function".ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))
        for fun in self.functions:
            fn = fun.name
            print("|{}|".format(fn.ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))

    def print_includes(self):
        """Displays a table showing all includes in this scope."""
        variable_size = VARIABLE_COLUMN_WIDTH
        print(''.ljust(variable_size + 2,'_'))
        print("|{}|".format("Include".ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))
        for fun in self.includes:
            fn = fun.name
            print("|{}|".format(fn.ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))

    @staticmethod
    def get_value_type(obj):
        """returns a string representing the given object type"""
        result = "unknown"
        if obj is None:
            result = NIL
        elif isinstance(obj, bool):
            result = BOOL
        elif isinstance(obj, int):
            result = INT
        elif isinstance(obj, float):
            result = FLOAT
        elif isinstance(obj, str):
            result = STRING
        elif isinstance(obj, list):
            result = ARRAY
        # ToDo: Add dictionaries to the language.
        elif isinstance(obj, dict):
            result = RECORD
        # the following types should never happen, but i added them in to be complete.
        elif isinstance(obj, complex):
            result = "complex"
        elif isinstance(obj, tuple):
            result = "tuple"
        elif isinstance(obj, bytes):
            result = "bytes"
        elif isinstance(obj, bytearray):
            result = "bytearray"
        elif isinstance(obj, set):
            result = "set"
        elif isinstance(obj, frozenset):
            result = "frozenset"
        else:
            raise Exception("Unknown type: {}".format(type(obj)))
        return result

    def root(self, scope):
        if scope.parent is not None:
            return self.root(scope.parent)
        else:
            return scope
    
    def print(self, scope):
        print(f"\nScope: {scope.name}, break: {scope.break_flag}, halt: {scope.x_halt_flag}, isLoop: {scope.is_loop}, Libraries: {len(scope.Libraries)}")
        if scope.has_variables():
            scope.print_variables()
        if scope.has_functions():
            scope.print_functions()
        if scope.has_includes():
            scope.print_includes()
        if scope.has_children():
            for child in scope.children:
                self.print(child)

    def __str__(self):
        result = f"\nScope: {self.name}, break: {self.break_flag}, halt: {self.x_halt_flag}, isLoop: {self.is_loop}, Libraries: {len(self.Libraries)}, Includes: {len(self.includes)}\n"
        if self.has_variables():
            result = f"{result}\nVariables:\n"
            for variable in self.variables:
                result = f"{result}{variable}\n"
        if self.has_functions():
            result = f"{result}\nFunctions:\n"
            for function in self.functions:
                result = f"{result}{function.name}\n"
        if self.has_includes():
            result = f"{result}\nIncludes:\n"
            for incl in self.includes:
                result = f"{result}{incl.name}\n"
        if self.has_children():
            result = f"{result}\nChildren:\n"
            for child in self.children:
                result = f"{result}{child}\n"
        return result