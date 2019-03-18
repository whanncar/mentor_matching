
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


def signup_submit(role, first_name, last_name, university, user_entered_university, subfield, woman, poc, health):
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


def admin_helper():
	db = DB('people.db')
	db.load()
	html = get_static_page('admin')
	dbeditor = get_static_page('admin/dbeditor')
	matchprogram = get_static_page('admin/matchprogram')
	mentor_table_entries = ""
	for k in db.mentors.keys():
		m = db.mentors[k]
		mentor_table_entries = mentor_table_entries + "<tr>"
		mentor_table_entries = mentor_table_entries + "<td>" + str(m.db_id) + "</td>"
		mentor_table_entries = mentor_table_entries + "<td>" + m.first_name + "</td>"
		mentor_table_entries = mentor_table_entries + "<td>" + m.last_name + "</td>"
		mentor_table_entries = mentor_table_entries + "<td>" + m.university + "</td>"
		mentor_table_entries = mentor_table_entries + "<td>"
		for g in m.underrepresented_groups:
			mentor_table_entries = mentor_table_entries + g + "<br>"
		mentor_table_entries = mentor_table_entries + "</td>"
		mentor_table_entries = mentor_table_entries + "<td>" + m.subfield + "</td>"
		mentor_table_entries = mentor_table_entries + "</tr>"
	dbeditor = html_insert(dbeditor, 'MENTORDBTABLE', mentor_table_entries)
	mentee_table_entries = ""
	for k in db.mentees.keys():
		m = db.mentees[k]
		mentee_table_entries = mentee_table_entries + "<tr>"
		mentee_table_entries = mentee_table_entries + "<td>" + str(m.db_id) + "</td>"
		mentee_table_entries = mentee_table_entries + "<td>" + m.first_name + "</td>"
		mentee_table_entries = mentee_table_entries + "<td>" + m.last_name + "</td>"
		mentee_table_entries = mentee_table_entries + "<td>" + m.university + "</td>"
		mentee_table_entries = mentee_table_entries + "<td>"
		for g in m.underrepresented_groups:
			mentee_table_entries = mentee_table_entries + g + "<br>"
		mentee_table_entries = mentee_table_entries + "</td>"
		mentee_table_entries = mentee_table_entries + "<td>" + m.subfield + "</td>"
		mentee_table_entries = mentee_table_entries + "</tr>"
	dbeditor = html_insert(dbeditor, 'MENTEEDBTABLE', mentee_table_entries)
	the_matching = db.matching
	the_matching_with_names = []
	for p in the_matching:
		the_mentor = db.mentors[p[0]].last_name + ", " + db.mentors[p[0]].first_name + " (" + str(p[0]) + ")"
		the_mentee = db.mentees[p[1]].last_name + ", " + db.mentees[p[1]].first_name + " (" + str(p[1]) + ")"
		new_p = []
		new_p.append(the_mentee)
		new_p.append(the_mentor)
		the_matching_with_names.append(new_p)
	for i in range(len(the_matching_with_names) - 1):
		if the_matching_with_names[i][0] == the_matching_with_names[i+1][0]:
			the_matching_with_names[i].append(the_matching_with_names[i+1][1])
			the_matching_with_names.pop(i+1)
		if i >= len(the_matching_with_names) - 2:
			break
	match_table_entries = ""
	for x in the_matching_with_names:
		match_table_entries = match_table_entries + "<tr><td>" + x[0] + "</td><td>" + x[1] + "</td><td>" + x[2] + "</td></tr>"
	matchprogram = html_insert(matchprogram, 'CURRENTMATCHTABLE', match_table_entries)
	html = html_insert(html, 'DBEDITOR', dbeditor)
	html = html_insert(html, 'MATCHPROGRAM', matchprogram)
	return html


def calculate_match_helper():
	db = DB('people.db')
	db.load()
	db.match()
	db.save()
	return admin_helper()







