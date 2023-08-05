import datetime
from pymongoose.mongo_types import Types, Schema

class User (Schema):
	schema_name = "users"

	def __init__ (self, **kwargs):
		self.schema = {
			"name": {
				"type": Types.String,
				"required": True
			},
			"email": {
				"type": Types.String,
				"default": None
			},

			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None
			},
			"username": {
				"type": Types.String,
				"required": True
			},

			"password": {
				"type": Types.String,
				"required": True
			},
			"password_changed": {
				"type": Types.Date,
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},
			"first_time": {
				"type": Types.Boolean,
				"default": False
			},

			"role": {
				"type": Types.ObjectId,
				"ref": "roles",
				"required": True
			},

			"firebase": {
				"type": Types.String,
				"default": None
			},

			"logged_out": {
				"type": Types.Date,
				"default": None
			},

			"recover_code": {
				"type": Types.String,
				"default": None
			},
			"recover_created": {
				"type": Types.Date,
				"default": None
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"User: {self.id}"
