
import random
import json

import scipy
from scipy import optimize


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
		self.matching = sort_matching(self, get_matching(self))



def same_subfield(x, y):
	return x.subfield == y.subfield

def share_underrepresented_group(x, y):
	intersection = [value for value in x.underrepresented_groups if value in y.underrepresented_groups]
	return len(intersection) > 0

def same_university(x, y):
	return x.university == y.university

def elementwise_product(v1, v2):
	result = []
	for i in range(len(v1)):
		result.append(v1[i] * v2[i])
	return result

def negate_vector(v):
	result = []
	for el in v:
		result.append(-el)
	return result


def get_LP_inputs(db):
	A = []
	B = []
	C = []
	D = []
	X = []
	Y = []
	for x_key in db.mentors.keys():
		x = db.mentors[x_key]
		for y_key in db.mentees.keys():
			y = db.mentees[y_key]
			if same_subfield(x,y):
				A.append(1)
			else:
				A.append(0)
			if share_underrepresented_group(x, y):
				B.append(1)
			else:
				B.append(0)
			if len(x.underrepresented_groups) == 0:
				C.append(1)
			else:
				C.append(0)
			if same_university(x, y):
				D.append(1)
			else:
				D.append(0)

	for z_key in db.mentors.keys():
		X_z = []
		for x_key in db.mentors.keys():
			for y_key in db.mentees.keys():
				if x_key == z_key:
					X_z.append(1)
				else:
					X_z.append(0)
		X.append(X_z)

	for z_key in db.mentees.keys():
		Y_z = []
		for x_key in db.mentors.keys():
			for y_key in db.mentees.keys():
				if y_key == z_key:
					Y_z.append(1)
				else:
					Y_z.append(0)
		Y.append(Y_z)

	lp_ineq = []
	lp_eq = []
	b_ineq = []
	b_eq = []

	for row in Y:
		lp_eq.append(row)
		b_eq.append(2)
		lp_eq.append(elementwise_product(row, D))
		b_eq.append(0)

	for row in Y:
		lp_ineq.append(negate_vector(elementwise_product(A, row)))
		b_ineq.append(-1)
		lp_ineq.append(negate_vector(elementwise_product(B, row)))
		b_ineq.append(-1)
		lp_ineq.append(negate_vector(elementwise_product(C, row)))
		b_ineq.append(-1)

	bounds = []

	for x_key in db.mentors.keys():
		for y_key in db.mentees.keys():
			bound = [0, 1]
			bounds.append(bound)

	opt_direction = []

	for x_key in db.mentors.keys():
		for y_key in db.mentees.keys():
			opt_direction.append(-1)

	lp_inputs = []
	lp_inputs.append(opt_direction)
	lp_inputs.append(lp_ineq)
	lp_inputs.append(b_ineq)
	lp_inputs.append(lp_eq)
	lp_inputs.append(b_eq)
	lp_inputs.append(bounds)

	return lp_inputs
	

def get_matching(db):
	lp_inputs = get_LP_inputs(db)
	lp_output = optimize.linprog(lp_inputs[0], lp_inputs[1], lp_inputs[2], lp_inputs[3], lp_inputs[4], lp_inputs[5])
	if not lp_output.success:
		return []
	match_vector = lp_output.x
	matching = []
	index = 0
	for x_key in db.mentors.keys():
		x = db.mentors[x_key]
		for y_key in db.mentees.keys():
			y = db.mentees[y_key]
			if match_vector[index] == 1:
				new_match = [x_key, y_key]
				matching.append(new_match)
			index = index + 1
	return matching


def sort_matching(db, matching):
	if len(matching) <= 1:
		return matching
	pivot = matching[0]
	pivot_fn = db.mentees[pivot[1]].first_name
	pivot_ln = db.mentees[pivot[1]].last_name
	left = []
	middle = []
	right = []
	middle.append(pivot)
	for i in range(1, len(matching)):
		fn = db.mentees[matching[i][1]].first_name
		ln = db.mentees[matching[i][1]].last_name
		if ln < pivot_ln:
			left.append(matching[i])
		if ln > pivot_ln:
			right.append(matching[i])
		if ln == pivot_ln:
			if fn < pivot_fn:
				left.append(matching[i])
			if fn > pivot_fn:
				right.append(matching[i])
			if fn == pivot_fn:
				middle.append(matching[i])
	left = sort_matching(db, left)
	right = sort_matching(db, right)
	result = []
	for x in left:
		result.append(x)
	for x in middle:
		result.append(x)
	for x in right:
		result.append(x)
	return result
