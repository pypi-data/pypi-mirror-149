import datetime
from pymongoose.mongo_types import Types, Schema

class PermissionsPreset (Schema):
	schema_name = "permissions.presets"

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
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"actions": [{
				"type": Types.ObjectId,
				"ref": "permissions.actions",
				"required": True
			}]
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"PermissionsPreset: {self.id} - {self.name}"
