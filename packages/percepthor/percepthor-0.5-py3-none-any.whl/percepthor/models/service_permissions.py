import datetime
from pymongoose.mongo_types import Types, Schema

SERVICE_PERMISSIONS_TYPE_NONE = 0
SERVICE_PERMISSIONS_TYPE_ORGANIZATION = 1
SERVICE_PERMISSIONS_TYPE_USER = 2
SERVICE_PERMISSIONS_TYPE_TOKEN = 3

def service_permissions_type_to_string (status: int):
	result = "Undefined"

	if (status == SERVICE_PERMISSIONS_TYPE_NONE):
		pass

	elif (status == SERVICE_PERMISSIONS_TYPE_ORGANIZATION):
		result = "Organization"

	elif (status == SERVICE_PERMISSIONS_TYPE_USER):
		result = "User"

	elif (status == SERVICE_PERMISSIONS_TYPE_TOKEN):
		result = "Token"

	return result

class ServicePermissions (Schema):
	schema_name = "services.permissions"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"required": True
			},
			"user": {
				"type": Types.ObjectId,
				"ref": "users",
				"default": None
			},

			"permissions_type": {
				"type": Types.Number,
				"default": SERVICE_PERMISSIONS_TYPE_NONE
			},
			
			"token": {
				"type": Types.ObjectId,
				"ref": "tokens",
				"default": None
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"matches": [{
				"service": {
					"type": Types.ObjectId,
					"ref": "services",
					"required": True
				},
				"actions_mask": {
					"type": Types.Number,
					"default": 0
				}
			}]
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ServicePermissions: {self.id}"
