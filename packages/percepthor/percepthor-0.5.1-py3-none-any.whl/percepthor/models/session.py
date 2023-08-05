import datetime
from pymongoose.mongo_types import Types, Schema

SESSION_TYPE_NONE = 0
SESSION_TYPE_MOBILE = 1
SESSION_TYPE_WEB = 2
SESSION_TYPE_TEMP = 3

def session_type_to_string (session_type: int):
	result = "Undefined"

	if (session_type == SESSION_TYPE_NONE):
		pass

	elif (session_type == SESSION_TYPE_MOBILE):
		result = "Mobile"

	elif (session_type == SESSION_TYPE_WEB):
		result = "Web"

	elif (session_type == SESSION_TYPE_TEMP):
		result = "Temp"

	return result

SESSION_STATUS_NONE = 0
SESSION_STATUS_ACTIVE = 1
SESSION_STATUS_INACTIVE = 2

def session_status_to_string (status: int):
	result = "Undefined"

	if (status == SESSION_STATUS_NONE):
		pass

	elif (status == SESSION_STATUS_ACTIVE):
		result = "Active"

	elif (status == SESSION_STATUS_INACTIVE):
		result = "Inactive"

	return result

SESSION_REASON_NONE = 0
SESSION_REASON_REGISTER = 1
SESSION_REASON_LOGIN = 2
SESSION_REASON_REGISTRATION = 3

def session_reason_to_string (reason: int):
	result = "Undefined"

	if (reason == SESSION_STATUS_NONE):
		pass

	elif (reason == SESSION_REASON_REGISTER):
		result = "Register"

	elif (reason == SESSION_REASON_LOGIN):
		result = "Login"

	elif (reason == SESSION_REASON_REGISTRATION):
		result = "Registration"

	return result

class UserSession (Schema):
	schema_name = "users.sessions"

	user = None
	s_type = SESSION_TYPE_NONE
	status = SESSION_STATUS_NONE

	def __init__ (self, **kwargs):
		self.schema = {
			"user": {
				"type": Types.ObjectId,
				"ref": "users",
				"required": True
			},

			"s_type": {
				"type": Types.Number,
				"default": SESSION_TYPE_NONE
			},
			"status": {
				"type": Types.Number,
				"default": SESSION_STATUS_NONE
			},
			"reason": {
				"type": Types.Number,
				"default": SESSION_REASON_NONE
			},

			"date": {
				"type": Types.Date,
				"default": datetime.datetime.utcnow ()
			}
		}

		super ().__init__ (self.schema_name, self.schema, kwargs)

	def __str__ (self):
		return f"UserSession: {self.id} - {self.user}"
