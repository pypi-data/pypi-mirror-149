import datetime
from pymongoose.mongo_types import Types, Schema

class Screen (Schema):
	schema_name = "modules.screens"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"name": {
				"type": Types.String,
				"required": True
			},
			"title": {
				"type": Types.String,
				"required": True
			},

			"components": [{
				"type": Types.ObjectId,
				"ref": "modules.components",
				"required": True
			}],

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Screen: {self.id} - {self.user}"
