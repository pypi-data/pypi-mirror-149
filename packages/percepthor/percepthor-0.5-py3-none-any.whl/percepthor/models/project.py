import datetime
from pymongoose.mongo_types import Types, Schema

class Project (Schema):
	schema_name = "projects"

	def __init__ (self, **kwargs):
		self.schema = {
			"name": {
				"type": Types.String,
				"required": True
			},
			"description": {
				"type": Types.String,
				"required": True
			},
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"required": True
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Project: {self.id}"
