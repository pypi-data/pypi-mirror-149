import datetime
from pymongoose.mongo_types import Types, Schema

CONDITION_TYPE_NONE = 0
CONDITION_TYPE_VALUE = 1
CONDITION_TYPE_SCREEN = 2
CONDITION_TYPE_SUBMODULE = 3

def condition_type_to_string (condition_type: int):
	result = "Undefined"

	if (condition_type == CONDITION_TYPE_NONE):
		pass

	elif (condition_type == CONDITION_TYPE_VALUE):
		result = "Value"

	elif (condition_type == CONDITION_TYPE_SCREEN):
		result = "Screen"

	elif (condition_type == CONDITION_TYPE_SUBMODULE):
		result = "Submodule"

	return result

class Condition (Schema):
	schema_name = "modules.conditions"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"condition_type": {
				"type": Types.Number,
				"default": CONDITION_TYPE_NONE
			},
			"condition_value": {
				"default": None
			},

			"restrictions": [{
				"type": Types.ObjectId,
				"ref": "modules.restrictions",
				"required": True
			}],

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Condition: {self.id} - {self.user}"
