import random
import string

import cherrypy

import server_helper

import script
from script import DB, get_matching

class MatchingServer(object):
	@cherrypy.expose
	def index(self):
		return server_helper.get_static_page('index')

	@cherrypy.expose
	def signup(self):
		return server_helper.signup_helper()

	@cherrypy.expose
	def mentor_signup_submit(self, first_name="", last_name="", university="", user_entered_university="", subfield="", woman = "", poc = "", health = ""):
		return self.signup_submit('mentor', first_name, last_name, university, user_entered_university, subfield, woman, poc, health)

	@cherrypy.expose
	def mentee_signup_submit(self, first_name="", last_name="", university="", user_entered_university="", subfield="", woman = "", poc = "", health = ""):
		return self.signup_submit('mentee', first_name, last_name, university, user_entered_university, subfield, woman, poc, health)

	def signup_submit(self, role, first_name, last_name, university, user_entered_university, subfield, woman, poc, health):
		if university == 'not_listed':
			university = user_entered_university
		underrepresented_groups = []
		if woman == "on":
			underrepresented_groups.append("woman")
		if poc == "on":
			underrepresented_groups.append("poc")
		if health == "on":
			underrepresented_groups.append("health")
		db = DB('people.db')
		db.load()
		if role == 'mentor':
			db_id = db.add_mentor(first_name, last_name, university, underrepresented_groups, subfield)
		if role == 'mentee':
			db_id = db.add_mentee(first_name, last_name, university, underrepresented_groups, subfield)
		db.save()
		return "<html><body>Thank you for signing up! Your ID is " + str(db_id) + ".</body></html>"

	@cherrypy.expose
	def admin(self):
		db = DB('people.db')
		db.load()
		m = get_matching(db)
		html = "<html>"
		html = html + "<body>"
		for pair in m:
			html = html + db.mentors[pair[0]].first_name + " " + db.mentors[pair[0]].last_name + ", " + db.mentees[pair[1]].first_name + " " + db.mentees[pair[1]].last_name + "<br>"
		html = html + "</body>"
		html = html + "</html>"
		return html



