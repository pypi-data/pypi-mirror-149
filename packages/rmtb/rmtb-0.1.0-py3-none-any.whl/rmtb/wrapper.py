class converter:
	e2f = {
		"user joined": "user_joined",
		"user left": "user_left",
		"message": "message",
		"update users": "update_users",
		"user change nick": "user_change_nick",
		"get_voice_users": "get_voice_users",
		"getvoice": "get_voice",
		"typing": "typing",
		"reaction_add": "reaction_add",
		"reaction_remove": "reaction_remove",
		"reaction_update": "reaction_update",
		"lts_msgid": "lts_msgid"
	}
	def reverse(p):
		for k in converter.e2f:
			print("'"+converter.e2f[k]+"'"=="'update_users'")
			if "'"+converter.e2f[k]+"'" == p:
				print("SCIK")
				return p
		return False