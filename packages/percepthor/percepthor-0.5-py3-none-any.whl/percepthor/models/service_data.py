import datetime
from pymongoose.mongo_types import Types, Schema

SERVICE_DATA_TYPE_NONE = 0
SERVICE_DATA_TYPE_SERVICE = 1
SERVICE_DATA_TYPE_ORGANIZATION = 2
SERVICE_DATA_TYPE_TOKEN = 3

def service_data_type_to_string (status: int):
	result = "Undefined"

	if (status == SERVICE_DATA_TYPE_NONE):
		pass

	elif (status == SERVICE_DATA_TYPE_SERVICE):
		result = "Service"

	elif (status == SERVICE_DATA_TYPE_ORGANIZATION):
		result = "Organization"

	elif (status == SERVICE_DATA_TYPE_TOKEN):
		result = "Token"

	return result

class ServiceData (Schema):
	schema_name = "services.data"

	def __init__ (self, **kwargs):
		self.schema = self.schema = {
			"service_data_type": {
				"type": Types.Number,
				"default": SERVICE_DATA_TYPE_NONE
			},
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
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
		return f"ServiceData: {self.id}"
