from ctypes import c_void_p, c_char_p, c_int, c_uint, c_bool

from .lib import lib

PERCEPTHOR_AUTH_TYPE_NONE = 1
PERCEPTHOR_AUTH_TYPE_ACTION = 2
PERCEPTHOR_AUTH_TYPE_ROLE = 3
PERCEPTHOR_AUTH_TYPE_SERVICE = 4
PERCEPTHOR_AUTH_TYPE_PERMISSIONS = 5
PERCEPTHOR_AUTH_TYPE_MULTIPLE = 6
PERCEPTHOR_AUTH_TYPE_COMPLETE = 7

PERCEPTHOR_AUTH_SCOPE_NONE = 1
PERCEPTHOR_AUTH_SCOPE_SINGLE = 2
PERCEPTHOR_AUTH_SCOPE_MANAGEMENT = 3

percepthor_auth_type_to_string = lib.percepthor_auth_type_to_string
percepthor_auth_type_to_string.argtypes = [c_int]
percepthor_auth_type_to_string.restype = c_char_p

percepthor_auth_scope_to_string = lib.percepthor_auth_scope_to_string
percepthor_auth_scope_to_string.argtypes = [c_int]
percepthor_auth_scope_to_string.restype = c_char_p

percepthor_auth_delete = lib.percepthor_auth_delete
percepthor_auth_delete.argtypes = [c_void_p]

percepthor_auth_get_type = lib.percepthor_auth_get_type
percepthor_auth_get_type.argtypes = [c_void_p]
percepthor_auth_get_type.restype = c_int

percepthor_auth_get_scope = lib.percepthor_auth_get_scope
percepthor_auth_get_scope.argtypes = [c_void_p]
percepthor_auth_get_scope.restype = c_int

percepthor_auth_get_resource = lib.percepthor_auth_get_resource
percepthor_auth_get_resource.argtypes = [c_void_p]
percepthor_auth_get_resource.restype = c_char_p

percepthor_auth_get_action = lib.percepthor_auth_get_action
percepthor_auth_get_action.argtypes = [c_void_p]
percepthor_auth_get_action.restype = c_char_p

percepthor_auth_get_admin = lib.percepthor_auth_get_admin
percepthor_auth_get_admin.argtypes = [c_void_p]
percepthor_auth_get_admin.restype = c_bool

percepthor_auth_get_permissions = lib.percepthor_auth_get_permissions
percepthor_auth_get_permissions.argtypes = [c_void_p]
percepthor_auth_get_permissions.restype = c_void_p

percepthor_auth_permissions_iter_start = lib.percepthor_auth_permissions_iter_start
percepthor_auth_permissions_iter_start.argtypes = [c_void_p]
percepthor_auth_permissions_iter_start.restype = c_bool

percepthor_auth_permissions_iter_get_next = lib.percepthor_auth_permissions_iter_get_next
percepthor_auth_permissions_iter_get_next.argtypes = [c_void_p]
percepthor_auth_permissions_iter_get_next.restype = c_void_p

percepthor_auth_create = lib.percepthor_auth_create
percepthor_auth_create.argtypes = [c_int]
percepthor_auth_create.restype = c_void_p

percepthor_single_authentication = lib.percepthor_single_authentication
percepthor_single_authentication.argtypes = [c_void_p, c_void_p, c_int, c_char_p, c_char_p]
percepthor_single_authentication.restype = c_uint

percepthor_custom_authentication_handler = lib.percepthor_custom_authentication_handler
percepthor_custom_authentication_handler.argtypes = [c_void_p, c_void_p]
percepthor_custom_authentication_handler.restype = c_uint
