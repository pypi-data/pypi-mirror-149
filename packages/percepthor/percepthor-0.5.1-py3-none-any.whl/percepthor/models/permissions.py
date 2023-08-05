import datetime
from pymongoose.mongo_types import Types, Schema

PERMISSIONS_TYPE_NONE = 0
PERMISSIONS_TYPE_SERVICE_NONE = 1
PERMISSIONS_TYPE_ORGANIZATION_NONE = 2
PERMISSIONS_TYPE_PROJECT_NONE = 3

def permissions_type_to_string (permissions_type: int):
	result = "Undefined"

	if (permissions_type == PERMISSIONS_TYPE_NONE):
		pass

	elif (permissions_type == PERMISSIONS_TYPE_SERVICE_NONE):
		result = "Service"

	elif (permissions_type == PERMISSIONS_TYPE_ORGANIZATION_NONE):
		result = "Organization"

	elif (permissions_type == PERMISSIONS_TYPE_PROJECT_NONE):
		result = "Project"

	return result

class Permissions (Schema):
	schema_name = "permissions"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None
			},
			"project": {
				"type": Types.ObjectId,
				"ref": "projects",
				"default": None
			},

			"permissions_type": {
				"type": Types.Number,
				"default": PERMISSIONS_TYPE_NONE
			},

			"user": {
				"type": Types.ObjectId,
				"ref": "users",
				"required": True
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},

			"actions": [{
				"type": Types.String
			}]
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Permissions: {self.id}"
