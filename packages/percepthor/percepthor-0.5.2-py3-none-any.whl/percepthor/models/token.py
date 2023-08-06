import datetime
from pymongoose.mongo_types import Types, Schema

TOKEN_TYPE_NONE = 0
TOKEN_TYPE_NORMAL = 1
TOKEN_TYPE_TEMPORARY = 2
TOKEN_TYPE_QUANTITY = 3
TOKEN_TYPE_USER = 4

def token_type_to_string (t_type: int):
	result = "Undefined"

	if (t_type == TOKEN_TYPE_NONE):
		pass

	elif (t_type == TOKEN_TYPE_NORMAL):
		result = "Normal"

	elif (t_type == TOKEN_TYPE_TEMPORARY):
		result = "Temporary"

	elif (t_type == TOKEN_TYPE_QUANTITY):
		result = "Quantity"

	elif (t_type == TOKEN_TYPE_USER):
		result = "User"

	return result

TOKEN_STATUS_NONE = 0
TOKEN_STATUS_AVAILABLE = 1
TOKEN_STATUS_EXPIRED = 2
TOKEN_STATUS_DISABLED = 3
TOKEN_STATUS_REVOKED = 4

def token_status_to_string (status: int):
	result = "Undefined"

	if (status == TOKEN_STATUS_NONE):
		pass

	elif (status == TOKEN_STATUS_AVAILABLE):
		result = "Available"

	elif (status == TOKEN_STATUS_EXPIRED):
		result = "Expired"

	elif (status == TOKEN_STATUS_DISABLED):
		result = "Disabled"

	elif (status == TOKEN_STATUS_REVOKED):
		result = "Revoked"

	return result

class Token (Schema):
	schema_name = "tokens"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None
			},
			"t_type": {
				"type": Types.Number,
				"default": TOKEN_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": TOKEN_STATUS_NONE
			},

			# owner
			"user": {
				"type": Types.ObjectId,
				"ref": "users",
				"required": True
			},

			# user values
			"role": {
				"type": Types.ObjectId,
				"ref": "roles",
				"default": None
			},
			"username": {
				"type": Types.String,
				"default": None
			},

			# api key
			"name": {
				"type": Types.String,
				"default": None
			},
			"description": {
				"type": Types.String,
				"default": None
			},

			# actual token values
			"iat": {
				"type": Types.Number,
				"default": 0
			},
			"value": {
				"type": Types.String,
				"required": True
			},

			# configuration
			"expiration": {
				"type": Types.Date,
				"default": None
			},
			"quantity": {
				"type": Types.Number,
				"default": 0
			},
			"permissions": {
				"type": Types.ObjectId,
				"ref": "permissions",
				"default": None
			},

			"created": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"expired": {
				"type": Types.Date,
				"default": None
			},
			"disabled": {
				"type": Types.Date,
				"default": None
			},
			"revoked": {
				"type": Types.Date,
				"default": None
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Token: {self.id}"
