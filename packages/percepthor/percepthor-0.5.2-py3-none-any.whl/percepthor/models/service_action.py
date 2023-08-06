import datetime
from pymongoose.mongo_types import Types, Schema

class ServiceAction (Schema):
	schema_name = "services.actions"

	def __init__ (self, **kwargs):
		self.schema = {
			"service": {
				"type": Types.ObjectId,
				"ref": "services",
				"required": True
			},
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"required": True
			},
			"value": {
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
		return f"ServiceAction: {self.id}"
