import datetime
from pymongoose.mongo_types import Types, Schema

TICKET_TYPE_NONE = 0
TICKET_TYPE_REPORT = 1
TICKET_TYPE_DISCOVER = 2

def ticket_type_to_string (t_type: int):
	result = "Undefined"

	if (t_type == TICKET_TYPE_NONE):
		pass

	elif (t_type == TICKET_TYPE_REPORT):
		result = "Report"

	elif (t_type == TICKET_TYPE_DISCOVER):
		result = "Discover"

	return result

TICKET_STATUS_NONE = 0
TICKET_STATUS_CREATED = 1
TICKET_STATUS_WAITING = 2
TICKET_STATUS_IN_REVIEW = 3
TICKET_STATUS_GOOD = 4
TICKET_STATUS_BAD = 5
TICKET_STATUS_PASSED = 6
TICKET_STATUS_ERROR = 7

def ticket_status_to_string (status: int):
	result = "Undefined"

	if (status == TICKET_STATUS_NONE):
		pass

	elif (status == TICKET_STATUS_CREATED):
		result = "Created"

	elif (status == TICKET_STATUS_WAITING):
		result = "Waiting"

	elif (status == TICKET_STATUS_IN_REVIEW):
		result = "In Review"

	elif (status == TICKET_STATUS_GOOD):
		result = "Good"

	elif (status == TICKET_STATUS_BAD):
		result = "Bad"

	elif (status == TICKET_STATUS_PASSED):
		result = "Passed"

	elif (status == TICKET_STATUS_ERROR):
		result = "Error"

	return result

class Ticket (Schema):
	schema_name = "tickets"

	def __init__ (self, **kwargs):
		self.schema = {
			"project": {
				"type": Types.ObjectId,
				"ref": "projects",
				"required": True
			},
			"name": {
				"type": Types.String,
				"default": None
			},
			"description": {
				"type": Types.String,
				"default": None
			},
			"image": {
				"type": Types.ObjectId,
				"ref": "images",
				"required": True
			},
			"t_type": {
				"type": Types.Number,
				"default": TICKET_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": TICKET_STATUS_NONE
			},
			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"Ticket: {self.id}"
