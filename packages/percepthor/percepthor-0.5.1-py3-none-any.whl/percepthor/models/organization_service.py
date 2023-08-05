import datetime
from pymongoose.mongo_types import Types, Schema

ORGANIZATION_SERVICE_STATUS_NONE = 0
ORGANIZATION_SERVICE_STATUS_AVAILABLE = 1
ORGANIZATION_SERVICE_STATUS_EXPIRED = 2
ORGANIZATION_SERVICE_STATUS_DISABLED = 3
ORGANIZATION_SERVICE_STATUS_REVOKED = 4

def organization_service_status_to_string (status: int):
	result = "Undefined"

	if (status == ORGANIZATION_SERVICE_STATUS_NONE):
		pass

	elif (status == ORGANIZATION_SERVICE_STATUS_AVAILABLE):
		result = "Available"

	elif (status == ORGANIZATION_SERVICE_STATUS_EXPIRED):
		result = "Expired"

	elif (status == ORGANIZATION_SERVICE_STATUS_DISABLED):
		result = "Disabled"

	elif (status == ORGANIZATION_SERVICE_STATUS_REVOKED):
		result = "Revoked"

	return result

class OrganizationService (Schema):
	schema_name = "organizations.services"

	def __init__ (self, **kwargs):
		self.schema = {
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"required": True
			},
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"required": True
			},
			"status": {
				"type": Types.Number,
				"default": ORGANIZATION_SERVICE_STATUS_NONE
			},
			"actions_mask": {
				"type": Types.Number,
				"default": 0
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"used": {
				"type": Types.Boolean,
				"default": False
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"OrganizationService: {self.id}"
