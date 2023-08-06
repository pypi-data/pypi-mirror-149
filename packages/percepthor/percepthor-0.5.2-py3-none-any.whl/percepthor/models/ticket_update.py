import datetime
from pymongoose.mongo_types import Types, Schema

class TicketUpdate (Schema):
	schema_name = "tickets.updates"

	def __init__ (self, **kwargs):
		self.schema = {
			"ticket": {
				"type": Types.ObjectId,
				"ref": "tickets",
				"required": True
			},

			"prev_status": {
				"type": Types.Number,
				"default": 0
			},
			"current_status": {
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
		return f"Ticket: {self.id}"
