import datetime
from pymongoose.mongo_types import Types, Schema

class PhotoTypes (Schema):
	schema_name = "modules.photo.types"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"question": {
				"type": Types.String,
				"required": True
			},
			"suffix": {
				"type": Types.String,
				"required": True
			},
			"options": {
				# we expect dynamic types
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"PhotoTypes: {self.id} - {self.user}"
