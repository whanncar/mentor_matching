
import random
import json

import script



class Mentee:
	

	def __init__(self, data):
		self.db_id = data[0]
		self.first_name = data[1]
		self.last_name = data[2]
		self.university = data[3]
		self.underrepresented_groups = data[4]
		self.subfield = data[5]

	def get_data(self):
		data = []
		data.append(self.db_id)
		data.append(self.first_name)
		data.append(self.last_name)
		data.append(self.university)
		data.append(self.underrepresented_groups)
		data.append(self.subfield)
		return data

class Mentor:


	def __init__(self, data):
		self.db_id = data[0]
		self.first_name = data[1]
		self.last_name = data[2]
		self.university = data[3]
		self.underrepresented_groups = data[4]
		self.subfield = data[5]

	def get_data(self):
		data = []
		data.append(self.db_id)
		data.append(self.first_name)
		data.append(self.last_name)
		data.append(self.university)
		data.append(self.underrepresented_groups)
		data.append(self.subfield)
		return data


class DB:

	def __init__(self, path):
		self.mentees = {}
		self.mentors = {}
		self.matching = []
		self.filepath = path

	def add_mentee(self, f, l, uni, gps, subf):
		new_id = random.randint(10000000, 99999999)
		while new_id in self.mentees.keys() or new_id in self.mentors.keys():
			new_id = random.randint(10000000, 99999999)
		new_mentee_data = [new_id, f, l, uni, gps, subf]
		new_mentee = Mentee(new_mentee_data)
		self.mentees[new_id] = new_mentee
		return new_id

	def add_mentor(self, f, l, uni, gps, subf):
		new_id = random.randint(10000000, 99999999)
		while new_id in self.mentees.keys() or new_id in self.mentors.keys():
			new_id = random.randint(10000000, 99999999)
		new_mentor_data = [new_id, f, l, uni, gps, subf]
		new_mentor = Mentor(new_mentor_data)
		self.mentors[new_id] = new_mentor
		return new_id

	def get_universities(self):
		universities = []
		for k in self.mentees.keys():
			u = self.mentees[k].university
			if u not in universities:
				universities.append(u)
		for k in self.mentors.keys():
			u = self.mentors[k].university
			if u not in universities:
				universities.append(u)
		return universities
	

	def save(self):
		f = open(self.filepath, 'w')
		mentee_data = []
		mentor_data = []
		for m_key in self.mentees.keys():
			mentee_data.append(self.mentees[m_key].get_data())
		for m_key in self.mentors.keys():
			mentor_data.append(self.mentors[m_key].get_data())
		data = []
		data.append(mentee_data)
		data.append(mentor_data)
		data.append(self.matching)
		f.write(json.dumps(data))
		f.close()

	def load(self):
		f = open(self.filepath, 'r')
		raw = f.read()
		f.close()
		data = json.loads(raw)
		mentee_data = data[0]
		mentor_data = data[1]
		for entry in mentee_data:
			new_mentee = Mentee(entry)
			self.mentees[new_mentee.db_id] = new_mentee
		for entry in mentor_data:
			new_mentor = Mentor(entry)
			self.mentors[new_mentor.db_id] = new_mentor
		self.matching = data[2]

	def match(self):
		self.matching = script.sort_matching(self, script.get_matching(self))

