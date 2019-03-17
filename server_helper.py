
import script
from script import DB, get_matching

def get_static_page(name):
	f = open('html/' + name + '.html')
	html = f.read()
	f.close()
	return html

def html_insert(s, key, replacement):
	s_split = s.split(key)
	result = ''
	result = result + s_split[0]
	result = result + replacement
	for i in range(1, len(s_split)):
		result = result + s_split[i]
	return result


def signup_helper():
	db = DB('people.db')
	db.load()
	html = get_static_page('signup')
	mentor_form = get_static_page('signup/mentor_form')
	mentee_form = get_static_page('signup/mentee_form')
	universities = db.get_universities()
	u_options = ""
	for u in universities:
		op = "<option value = \"" + u + "\">" + u + "</option>"
		u_options = u_options + op
	mentor_form = html_insert(mentor_form, 'UNIVERSITY_OPTIONS', u_options)
	mentee_form = html_insert(mentee_form, 'UNIVERSITY_OPTIONS', u_options)
	html = html_insert(html, 'MENTOR_SIGNUP_FORM', mentor_form)
	html = html_insert(html, 'MENTEE_SIGNUP_FORM', mentee_form)
	return html
	
	
