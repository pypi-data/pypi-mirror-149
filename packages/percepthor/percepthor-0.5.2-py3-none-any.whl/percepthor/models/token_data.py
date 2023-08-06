import datetime
from pymongoose.mongo_types import Types, Schema

class TokenData (Schema):
	schema_name = "tokens.data"

	def __init__ (self, **kwargs):
		self.schema = {
			"token": {
				"type": Types.ObjectId,
				"ref": "tokens",
				"required": True
			},
			"used": {
				"type": Types.Boolean,
				"default": False
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"n_times_used": {
				"type": Types.Number,
				"default": 0
			},
			"last_time": {
				"type": Types.Date,
				"default": None
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"TokenData: {self.id}"
