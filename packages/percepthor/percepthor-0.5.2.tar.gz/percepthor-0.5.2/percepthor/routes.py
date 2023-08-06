from ctypes import c_void_p, c_char_p, c_int

from cerver.http import HTTP_ROUTE_AUTH_TYPE_CUSTOM
from cerver.http import RequestMethod
from cerver.http import HttpHandler
from cerver.http import http_route_create
from cerver.http import http_route_set_custom_data
from cerver.http import http_route_set_delete_custom_data
from cerver.http import http_route_set_auth
from cerver.http import http_route_set_authentication_handler

from .lib import lib

from .auth import PERCEPTHOR_AUTH_SCOPE_MANAGEMENT
from .auth import percepthor_custom_authentication_handler
from .permissions import PermissionsType

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

# create route with common values
def percepthor_route_create_internal (
	method: RequestMethod, path: str, handler: HttpHandler
) -> c_void_p:
	percepthor_route = http_route_create (method, path.encode ("utf-8"), handler)

	http_route_set_auth (percepthor_route, HTTP_ROUTE_AUTH_TYPE_CUSTOM)
	# http_route_set_delete_custom_data (percepthor_route, auth_route_delete)
	http_route_set_authentication_handler (percepthor_route, percepthor_custom_authentication_handler)

	return percepthor_route

def percepthor_route_create (
	method: RequestMethod, path: str, handler: HttpHandler
) -> c_void_p:
	percepthor_route = percepthor_route_create_internal (method, path, handler)

	http_route_set_custom_data (percepthor_route, auth_route_create ())

	return percepthor_route

def percepthor_action_route_create (
	method: RequestMethod, path: str, handler: HttpHandler, action: str
) -> c_void_p:
	action_route = percepthor_route_create_internal (method, path, handler)

	http_route_set_custom_data (
		action_route, auth_route_create_action (action.encode ("utf-8"))
	)

	return action_route

def percepthor_role_route_create (
	method: RequestMethod, path: str, handler: HttpHandler, role: str, action: str
) -> c_void_p:
	role_route = percepthor_route_create_internal (method, path, handler)

	http_route_set_custom_data (
		role_route, auth_route_create_role (
			action.encode ("utf-8"), role.encode ("utf-8")
		)
	)

	return role_route

def percepthor_service_route_create (
	method: RequestMethod, path: str, handler: HttpHandler
) -> c_void_p:
	service_route = percepthor_route_create_internal (method, path, handler)

	http_route_set_custom_data (service_route, auth_route_create_service ())

	return service_route

def percepthor_single_route_create (
	method: RequestMethod, path: str, handler: HttpHandler
) -> c_void_p:
	return http_route_create (method, path.encode ("utf-8"), handler)

def percepthor_management_route_create (
	method: RequestMethod, path: str, handler: HttpHandler,
	permissions: PermissionsType, action: str
) -> c_void_p:
	management_route = percepthor_route_create_internal (method, path, handler)

	http_route_set_custom_data (management_route, auth_route_create_permissions (
		PERCEPTHOR_AUTH_SCOPE_MANAGEMENT, permissions, action.encode ("utf-8")
	))

	return management_route
