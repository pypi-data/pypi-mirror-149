import datetime
from pymongoose.mongo_types import Types, Schema

RESTRICTION_TYPE_NONE = 0
RESTRICTION_TYPE_NOT_NULL = 1
RESTRICTION_TYPE_NOT_EMPTY = 2
RESTRICTION_TYPE_IS_NUMBER = 3
RESTRICTION_TYPE_IS_LIST = 4
RESTRICTION_TYPE_EQUALS = 5
RESTRICTION_TYPE_BIGGER_THAN = 6
RESTRICTION_TYPE_EQUALS_OR_BIGGER_THAN = 7
RESTRICTION_TYPE_LESS_THAN = 8
RESTRICTION_TYPE_EQUALS_OR_LESS_THAN = 9
RESTRICTION_TYPE_LENGTH_EQUALS = 10
RESTRICTION_TYPE_LENGTH_BIGGER_THAN = 11
RESTRICTION_TYPE_LENGTH_EQUALS_OR_BIGGER_THAN = 12
RESTRICTION_TYPE_LENGTH_LESS_THAN = 13
RESTRICTION_TYPE_LENGTH_EQUALS_OR_LESS_THAN = 14
RESTRICTION_TYPE_LIST_CONTAINS = 15
RESTRICTION_TYPE_LIST_NOT_CONTAINS = 16

def restriction_type_to_string (restriction_type: int):
	result = "Undefined"

	if (restriction_type == RESTRICTION_TYPE_NONE):
		pass

	elif (restriction_type == RESTRICTION_TYPE_NOT_NULL):
		result = "Not Null"

	elif (restriction_type == RESTRICTION_TYPE_NOT_EMPTY):
		result = "Not Empty"

	elif (restriction_type == RESTRICTION_TYPE_IS_NUMBER):
		result = "Is Number"

	elif (restriction_type == RESTRICTION_TYPE_IS_LIST):
		result = "Is List"

	elif (restriction_type == RESTRICTION_TYPE_EQUALS):
		result = "Equals"

	elif (restriction_type == RESTRICTION_TYPE_BIGGER_THAN):
		result = "Bigger Than"

	elif (restriction_type == RESTRICTION_TYPE_EQUALS_OR_BIGGER_THAN):
		result = "Equals Or Bigger Than"

	elif (restriction_type == RESTRICTION_TYPE_LESS_THAN):
		result = "Less Than"

	elif (restriction_type == RESTRICTION_TYPE_EQUALS_OR_LESS_THAN):
		result = "Equals Or Less Than"

	elif (restriction_type == RESTRICTION_TYPE_LENGTH_EQUALS):
		result = "Length Equals"

	elif (restriction_type == RESTRICTION_TYPE_LENGTH_BIGGER_THAN):
		result = "Length Bigger Than"

	elif (restriction_type == RESTRICTION_TYPE_LENGTH_EQUALS_OR_BIGGER_THAN):
		result = "Length Equals Or Bigger Than"

	elif (restriction_type == RESTRICTION_TYPE_LENGTH_LESS_THAN):
		result = "Length Less Than"

	elif (restriction_type == RESTRICTION_TYPE_LENGTH_EQUALS_OR_LESS_THAN):
		result = "Lenght Equals Or Less Than"

	elif (restriction_type == RESTRICTION_TYPE_LIST_CONTAINS):
		result = "List Contains"

	elif (restriction_type == RESTRICTION_TYPE_LIST_NOT_CONTAINS):
		result = "List Not Contains"

	return result

class Restriction (Schema):
	schema_name = "modules.restrictions"

	def __init__ (self, **kwargs):
		self.schema = {
			"submodule": {
				"type": Types.ObjectId,
				"ref": "submodules",
				"required": True
			},

			"component": {
				"type": Types.ObjectId,
				"ref": "modules.components",
				"default": None
			},

			"condition": {
				"type": Types.ObjectId,
				"ref": "modules.conditions",
				"default": None
			},

			"restriction_type": {
				"type": Types.Number,
				"default": RESTRICTION_TYPE_NONE
			},
			"check_value": {
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Restriction: {self.id} - {self.user}"
