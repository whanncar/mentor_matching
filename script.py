
import scipy
from scipy import optimize





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
