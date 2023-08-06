import datetime
from pymongoose.mongo_types import Types, Schema

class Module (Schema):
	schema_name = "modules"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"required": True
			},

			"code": {
				"type": Types.String,
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

			"logo": {
				"type": Types.String,
				"required": True
			},

			"configuration": {
				"type": Types.ObjectId,
				"ref": "modules.configuration",
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Module: {self.id} - {self.user}"
