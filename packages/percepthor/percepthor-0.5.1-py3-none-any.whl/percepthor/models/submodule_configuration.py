import datetime
from pymongoose.mongo_types import Types, Schema

class SubmoduleConfiguration (Schema):
	schema_name = "submodules.configuration"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"props": [{
				"type": Types.ObjectId,
				"ref": "props",
				"required": True
			}],

			"screens": [{
				"type": Types.ObjectId,
				"ref": "screens",
				"required": True
			}],

			"on_submit": [{
				"type": Types.ObjectId,
				"ref": "components.actions",
				"required": False
			}],
			"on_next_screen": [{
				"type": Types.ObjectId,
				"ref": "components.actions",
				"required": False
			}],
			"when_completed": [{
				"type": Types.ObjectId,
				"ref": "components.actions",
				"required": False
			}],

			"version": {
				"type": Types.String,
				"required": True
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Submodule: {self.id} - {self.user}"
