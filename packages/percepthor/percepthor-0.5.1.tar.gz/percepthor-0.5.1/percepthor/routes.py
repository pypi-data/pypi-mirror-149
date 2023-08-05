from ctypes import c_void_p, c_char_p, c_int

from .lib import lib

auth_route_delete = lib.auth_route_delete
auth_route_delete.argtypes = [c_void_p]

auth_route_create = lib.auth_route_create
auth_route_create.restype = c_void_p

auth_route_create_action = lib.auth_route_create_action
auth_route_create_action.argtypes = [c_char_p]
auth_route_create_action.restype = c_void_p

auth_route_create_role = lib.auth_route_create_role
auth_route_create_role.argtypes = [c_char_p, c_char_p]
auth_route_create_role.restype = c_void_p

auth_route_create_service = lib.auth_route_create_service
auth_route_create_service.restype = c_void_p

auth_route_create_permissions = lib.auth_route_create_permissions
auth_route_create_permissions.argtypes = [c_int, c_int, c_char_p]
auth_route_create_permissions.restype = c_void_p

auth_route_print = lib.auth_route_print
auth_route_print.argtypes = [c_void_p]
