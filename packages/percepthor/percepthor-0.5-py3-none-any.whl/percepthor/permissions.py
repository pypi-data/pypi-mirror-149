from ctypes import c_void_p, c_char_p, c_int, c_bool

from .lib import lib

PERMISSIONS_TYPE_NONE = 1
PERMISSIONS_TYPE_SERVICE = 2
PERMISSIONS_TYPE_ORGANIZATION = 3
PERMISSIONS_TYPE_PROJECT = 4

permissions_type_to_string = lib.permissions_type_to_string
permissions_type_to_string.argtypes = [c_int]
permissions_type_to_string.restype = c_char_p

permissions_get_resource = lib.permissions_get_resource
permissions_get_resource.argtypes = [c_void_p]
permissions_get_resource.restype = c_char_p

permissions_print = lib.permissions_print
permissions_print.argtypes = [c_void_p]

permissions_has_action = lib.permissions_has_action
permissions_has_action.argtypes = [c_void_p, c_char_p]
permissions_has_action.restype = c_bool
