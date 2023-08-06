import datetime
from pymongoose.mongo_types import Types, Schema

class Image (Schema):
	schema_name = "images"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None,
			},

			"filename": {
				"type": Types.String,
				"required": True
			},
			
			"status": {
				"type": Types.Number,
				"default": 0
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Image: {self.id}"
