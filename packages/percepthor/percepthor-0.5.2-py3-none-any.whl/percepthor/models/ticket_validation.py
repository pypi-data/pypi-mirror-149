import datetime
from pymongoose.mongo_types import Types, Schema

TICKET_VALIDATION_RESULT_NONE = 0
TICKET_VALIDATION_RESULT_GOOD = 1
TICKET_VALIDATION_RESULT_BAD = 2

class TicketValidation (Schema):
	schema_name = "tickets.validations"

	def __init__ (self, **kwargs):
		self.schema = {
			"organization": {
				"type": Types.ObjectId,
				"ref": "organizations",
				"default": None
			},
			"project": {
				"type": Types.ObjectId,
				"ref": "projects",
				"required": True
			},

			"ticket": {
				"type": Types.ObjectId,
				"ref": "tickets",
				"required": True
			},

			"reviewer": {
				"type": Types.ObjectId,
				"ref": "users",
				"required": True
			},
			"staff": {
				"type": Types.ObjectId,
				"ref": "staffs",
				"default": None
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			},

			"result": {
				"type": Types.Number,
				"default": TICKET_VALIDATION_RESULT_NONE
			},

			"observations": {
				"type": Types.String,
				"default": None
			},
			"last": {
				"type": Types.Boolean,
				"default": True
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"TicketValidation: {self.id}"
