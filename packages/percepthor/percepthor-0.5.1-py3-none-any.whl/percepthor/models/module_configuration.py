import datetime
from pymongoose.mongo_types import Types, Schema

class ModuleConfiguration (Schema):
	schema_name = "modules.configuration"

	def __init__ (self, **kwargs):
		self.schema = {
			"module": {
				"type": Types.ObjectId,
				"ref": "modules",
				"required": True
			},

			"image": {
				"type": Types.String,
				"required": True
			},
			"requires_map": {
				"type": Types.Boolean,
				"default": False
			},
			"primary_color": {
				"type": Types.String,
				"required": True
			},
			"secondary_color": {
				"type": Types.String,
				"required": True
			},

			"location_configuration": {
				"min_distance": {
					"type": Types.Number,
					"default": 0
				},
				"max_distance": {
					"type": Types.Number,
					"default": 0
				},
				"delta_distance": {
					"type": Types.Number,
					"default": 0
				},
				"update_distance": {
					"type": Types.Number,
					"default": 0
				},
				"can_update": {
					"type": Types.Boolean,
					"default": False
				}
			},

			"store_configuration": {
				"route": {
					"type": Types.String,
					"required": True
				},
				"data_to_show": [{
					"type": Types.String,
					"required": True
				}]
			},

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
		return f"Module: {self.id} - {self.user}"
