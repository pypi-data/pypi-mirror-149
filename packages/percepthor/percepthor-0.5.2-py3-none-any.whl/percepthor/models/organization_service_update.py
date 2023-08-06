import datetime
from pymongoose.mongo_types import Types, Schema

class OrganizationServiceUpdate (Schema):
	schema_name = "organizations.services.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization_service": {
				"type": Types.ObjectId,
				"ref": "organizations.services",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": 0
			},
			"current_status": {
				"type": Types.Number,
				"default": 0
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"OrganizationService: {self.id}"
