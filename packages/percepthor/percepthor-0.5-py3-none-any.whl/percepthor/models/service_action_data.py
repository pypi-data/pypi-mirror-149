import datetime
from pymongoose.mongo_types import Types, Schema

SERVICE_ACTION_DATA_TYPE_NONE = 0
SERVICE_ACTION_DATA_TYPE_SERVICE = 1
SERVICE_ACTION_DATA_TYPE_ORGANIZATION = 2
SERVICE_ACTION_DATA_TYPE_TOKEN = 3

def service_action_data_type_to_string (status: int):
	result = "Undefined"

	if (status == SERVICE_ACTION_DATA_TYPE_NONE):
		pass

	elif (status == SERVICE_ACTION_DATA_TYPE_SERVICE):
		result = "Service"

	elif (status == SERVICE_ACTION_DATA_TYPE_ORGANIZATION):
		result = "Organization"

	elif (status == SERVICE_ACTION_DATA_TYPE_TOKEN):
		result = "Token"

	return result

class ServiceActionData (Schema):
	schema_name = "services.actions.data"

	def __init__ (self, **kwargs):
		self.schema = {
			"data_type": {
				"type": Types.Number,
				"default": SERVICE_ACTION_DATA_TYPE_NONE
			},
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"default": None
			},
			"action": {
				"type": Types.ObjectId,
				"ref": "services.actions",
				"default": None
			},
			"organization_service": {
				"type": Types.ObjectId,
				"ref": "organizations.services",
				"default": None
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
			"used": {
				"type": Types.Boolean,
				"default": False
			},
			"n_times_used": {
				"type": Types.Number,
				"default": 0
			},
			"last_time": {
				"type": Types.Date,
				"default": None
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"ServiceActionData: {self.id}"
