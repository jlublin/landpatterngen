from tollen import TolLen

class DualRow:

	# part containts L, b, S, E, e, E1, D, npin, deleted, mark
	# design contaits J_H, J_T, J_S and CE
	# process contains F and P
	def __init__(self, part, design, process):

		for c in ['L', 'b']:
			if(c not in part):
				print('Missing "{}"'.format(c))
				return

		for c in ['J_H', 'J_T', 'J_S', 'CE']:
			if(c not in design):
				print('Missing "{}"'.format(c))
				return

		for c in ['F', 'P']:
			if(c not in process):
				print('Missing "{}"'.format(c))
				return

		if('S' not in part and 'E' not in part):
			print('Missing both "S" and "E"')
			return

		if('S' not in part):
			part['S'] = part['E'] - part['L'] - part['L']

		if('E' not in part):
			part['E'] = part['S'] + part['L'] + part['L']

		self.design = design
		self.process = process
		self.part = part
		self.land = {}

		self.calculate_pattern()


	def calculate_pattern(self):

		if('S' not in self.part):
			self.part['S'] = self.part['E'] - self.part['L'] - self.part['L']

		if('E' not in self.part):
			self.part['E'] = self.part['S'] + self.part['L'] + self.part['L']

		E = self.part['E']
		S = self.part['S']
		b = self.part['b']

		J_T = TolLen(self.design['J_T'], 0, 1)
		J_H = TolLen(self.design['J_H'], 0, 1)
		J_S = TolLen(self.design['J_S'], 0, 1)
		CE = self.design['CE']

		F = self.process['F']
		P = self.process['P']

		# Q = E + 2*JT + F + P
		# Zmax = Qmax + Qtol - Etol

		Q = E + J_T + J_T + F + P
		Z =  Q.max + Q.tol - E.tol

		# Q = S - 2*JH + F + P
		# Gmin = Qmin - Qtol + Stol

		Q = S - J_H - J_H + F + P
		G =  Q.min - Q.tol + S.tol

		# Q = b + 2*JS + F + P
		# Xmax = Qmax + Qtol - btol

		Q = b + J_S + J_S + F + P
		X =  Q.max + Q.tol - b.tol

		Y = (Z - G) / 2
		C = G + Y

		# TODO: trimming

		self.land['C'] = round(C,1)
		self.land['G'] = round(G,1)
		self.land['X'] = round(X,1)
		self.land['Y'] = round(Y,1)
		self.land['Z'] = round(Z,1)


		# C,e,G,X,Y,Z
	def gen(self, target):

		E1 = self.part['E1']
		D = self.part['D']
		e = self.part['e']
		E = self.part['E']

		C = self.land['C']
		X = self.land['X']
		Y = self.land['Y']
		Z = self.land['Z']
		npin = self.part['npin']
		deleted = self.part['deleted']

		CE = self.design['CE']

		CEx = max(E.max, Z)/2 + CE
		CEy = max(D.max, e*(npin//2 - 1) + X)/2 + CE

		y0 = (npin//2 - 1)/2 * e

		# Add pads
		pin = 1
		for i in range(npin):
			if(deleted == None or (i+1) not in deleted):
				if(i < npin//2):
					target.add_pac_pad(0, 0, (Y, X), (-C/2, y0 - i*e), pin)
				else:
					target.add_pac_pad(0, 0, (Y, X), (C/2, -y0 + (i-npin//2)*e), pin)

				pin += 1

		# Add silk and courtyard
		target.add_pac_line('Courtyard', 0.1, [(-CEx, -CEy), (CEx, -CEy), (CEx, CEy), (-CEx, CEy), ('end',0)])
		target.add_pac_line('Silk', 0.1, [(-E1.max/2, -D.max/2), (E1.max/2, -D.max/2), (E1.max/2, D.max/2), (-E1.max/2, D.max/2), ('end',0)])

		if(self.part['mark'] == 'circle'):
			d = 0.2
			target.add_pac_circle('Silk', d, (-E1.nom/2 - 3*d, y0 + X/2 + 2*d))

		if(self.part['mark'] == 'diode'):
			target.add_pac_rectangle('Silk', (-E1.max/2, D.max/2), (0, -D.max/2))
