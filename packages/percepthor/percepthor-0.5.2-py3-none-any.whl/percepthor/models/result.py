import datetime
from pymongoose.mongo_types import Types, Schema

class Result (Schema):
	schema_name = "results"

	def __init__ (self, **kwargs):
		self.schema = {
			"image": {
				"type": Types.ObjectId,
				"ref": "images",
				"required": True
			},

			"epoch": {
				"type": Types.String,
				"default": None
			},
			"name": {
				"type": Types.String,
				"default": None
			},
			"filename": {
				"type": Types.String,
				"default": None
			},
			"url": {
				"type": Types.String,
				"default": None
			},

			"calidad_name": {
				"type": Types.String,
				"default": None
			},
			"calidad_proba": {
				"type": Types.Number,
				"default": 0
			},

			"n_elements": {
				"type": Types.Number,
				"default": 0
			},
			"elements": [{
				"clase": {
					"type": Types.String
				},
				"score": {
					"type": Types.Number
				},
				"area": {
					"type": Types.Number
				},
				"coords": {
					# we expect 4 values
				}
			}],

			"n_predictions": {
				"type": Types.Number,
				"default": 0
			},
			"predictions": [{
				"clase": {
					"type": Types.String
				},
				"score": {
					"type": Types.Number
				},
				"area": {
					"type": Types.Number
				},
				"coords": {
					# we expect 4 values
				}
			}],

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Result: {self.id}"
