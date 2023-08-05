from ctypes import c_void_p, c_char_p, c_int, c_uint, c_int64, c_bool

from .lib import lib

PERCEPTHOR_AUTH_TYPE_NONE = 0
PERCEPTHOR_AUTH_TYPE_TOKEN = 1
PERCEPTHOR_AUTH_TYPE_ACTION = 2
PERCEPTHOR_AUTH_TYPE_ROLE = 3
PERCEPTHOR_AUTH_TYPE_SERVICE = 4
PERCEPTHOR_AUTH_TYPE_PERMISSIONS = 5
PERCEPTHOR_AUTH_TYPE_MULTIPLE = 6
PERCEPTHOR_AUTH_TYPE_COMPLETE = 7

PERCEPTHOR_AUTH_SCOPE_NONE = 0
PERCEPTHOR_AUTH_SCOPE_SINGLE = 1
PERCEPTHOR_AUTH_SCOPE_MANAGEMENT = 2

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

percepthor_auth_get_token_id = lib.percepthor_auth_get_token_id
percepthor_auth_get_token_id.argtypes = [c_void_p]
percepthor_auth_get_token_id.restype = c_char_p

percepthor_auth_get_token_type = lib.percepthor_auth_get_token_type
percepthor_auth_get_token_type.argtypes = [c_void_p]
percepthor_auth_get_token_type.restype = c_int

percepthor_auth_get_token_organization = lib.percepthor_auth_get_token_organization
percepthor_auth_get_token_organization.argtypes = [c_void_p]
percepthor_auth_get_token_organization.restype = c_char_p

percepthor_auth_get_token_permissions = lib.percepthor_auth_get_token_permissions
percepthor_auth_get_token_permissions.argtypes = [c_void_p]
percepthor_auth_get_token_permissions.restype = c_char_p

percepthor_auth_get_token_role = lib.percepthor_auth_get_token_role
percepthor_auth_get_token_role.argtypes = [c_void_p]
percepthor_auth_get_token_role.restype = c_char_p

percepthor_auth_get_token_user = lib.percepthor_auth_get_token_user
percepthor_auth_get_token_user.argtypes = [c_void_p]
percepthor_auth_get_token_user.restype = c_char_p

percepthor_auth_get_token_username = lib.percepthor_auth_get_token_username
percepthor_auth_get_token_username.argtypes = [c_void_p]
percepthor_auth_get_token_username.restype = c_char_p

percepthor_auth_get_mask = lib.percepthor_auth_get_mask
percepthor_auth_get_mask.argtypes = [c_void_p]
percepthor_auth_get_mask.restype = c_int64

percepthor_auth_create = lib.percepthor_auth_create
percepthor_auth_create.argtypes = [c_int]
percepthor_auth_create.restype = c_void_p

percepthor_auth_print_token = lib.percepthor_auth_print_token
percepthor_auth_print_token.argtypes = [c_void_p]

percepthor_single_authentication = lib.percepthor_single_authentication
percepthor_single_authentication.argtypes = [c_void_p, c_void_p, c_int, c_char_p, c_char_p]
percepthor_single_authentication.restype = c_uint

percepthor_custom_authentication_handler = lib.percepthor_custom_authentication_handler
percepthor_custom_authentication_handler.argtypes = [c_void_p, c_void_p]
percepthor_custom_authentication_handler.restype = c_uint
