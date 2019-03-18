import random
import string

import cherrypy

import server_helper

class MatchingServer(object):
	@cherrypy.expose
	def index(self):
		return server_helper.get_static_page('index')

	@cherrypy.expose
	def signup(self):
		return server_helper.signup_helper()

	@cherrypy.expose
	def mentor_signup_submit(self, first_name="", last_name="", university="", user_entered_university="", subfield="", woman = "", poc = "", health = ""):
		return server_helper.signup_submit('mentor', first_name, last_name, university, user_entered_university, subfield, woman, poc, health)

	@cherrypy.expose
	def mentee_signup_submit(self, first_name="", last_name="", university="", user_entered_university="", subfield="", woman = "", poc = "", health = ""):
		return server_helper.signup_submit('mentee', first_name, last_name, university, user_entered_university, subfield, woman, poc, health)

	@cherrypy.expose
	def admin(self):
		return server_helper.admin_helper()

	@cherrypy.expose
	def calculate_match(self):
		return server_helper.calculate_match_helper()



