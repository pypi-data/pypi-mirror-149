import datetime
from pymongoose.mongo_types import Types, Schema

PROP_TYPE_NONE = 0
PROP_TYPE_STORE = 1
PROP_TYPE_LOCATION = 2
PROP_TYPE_USER = 3

def prop_type_to_string (prop_type: int):
	result = "Undefined"

	if (prop_type == PROP_TYPE_NONE):
		pass

	elif (prop_type == PROP_TYPE_STORE):
		result = "Store"

	elif (prop_type == PROP_TYPE_LOCATION):
		result = "Location"

	elif (prop_type == PROP_TYPE_USER):
		result = "User"

	return result

class Prop (Schema):
	schema_name = "modules.props"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"p_type": {
				"type": Types.Number,
				"default": PROP_TYPE_NONE
			},

			"select": [{
				"type": Types.String,
				"required": False
			}],

			"prefix": {
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
		return f"Prop: {self.id} - {self.user}"
