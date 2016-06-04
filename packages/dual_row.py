from tollen import TolLen

'''
Arguments: (E1) (D) e (E) (S) (L) (b) (E2 D2 c r) npin mark (deleted) (holes) lead_type (C G X Y Z)
holes = (d, x, y)
If C X Y Z predefined, use them instead as custom device
'''

def get_package(part, design, process):
	return DualRow(part, design, process)

class DualRow:

	# part containts L, b, S, E, e, E1, D, npin, mark, deleted, holes
	# design contaits J_H, J_T, J_S and CE
	# process contains F and P
	def __init__(self, part, design, process):

		if(isinstance(part, list)):
			p = part
			part = {	'E1': TolLen(float(p[0][0]), float(p[0][1])),
						'D': TolLen(float(p[1][0]), float(p[1][1])),
						'e': float(p[2]),
						'E': TolLen(float(p[3][0]), float(p[3][1])),
						'S': TolLen(float(p[4][0]), float(p[4][1])),
						'L': TolLen(float(p[5][0]), float(p[5][1])),
						'b': TolLen(float(p[6][0]), float(p[6][1])),
						'npin': int(p[7]),
						'mark': p[8],
						'deleted': p[9],
						'holes': p[10],
						'C': p[12][0],
						'G': p[12][1],
						'X': p[12][2],
						'Y': p[12][3],
						'Z': p[12][4] }

			import ipc7351
			design = ipc7351.IPC7351[p[11]]['B']

		for c in ['L', 'b', 'E1', 'e', 'D', 'npin']:
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

		# Z
		if('Z' in self.part and self.part['Z']):
			Z = self.part['Z']
		else:
			# Q = E + 2*JT + F + P
			# Zmax = Qmax + Qtol - Etol

			Q = E + J_T + J_T + F + P
			Z =  Q.max + Q.tol - E.tol

		# G
		if('G' in self.part and self.part['G']):
			G = self.part['G']
		else:
			# Q = S - 2*JH + F + P
			# Gmin = Qmin - Qtol + Stol

			Q = S - J_H - J_H + F + P
			G =  Q.min - Q.tol + S.tol

		# X
		if('X' in self.part and self.part['X']):
			X = self.part['X']
		else:
			# Q = b + 2*JS + F + P
			# Xmax = Qmax + Qtol - btol

			Q = b + J_S + J_S + F + P
			X =  Q.max + Q.tol - b.tol

		# Y
		if('Y' in self.part and self.part['Y']):
			Y = self.part['Y']
		else:
			Y = (Z - G) / 2

		# C
		if('C' in self.part and self.part['C']):
			C = self.part['C']
		else:
			C = G + Y

		# TODO: trimming
		# TODO: rounding (eg 1.05, 1.10 1.15 (c=0.05) x = round(x0/c)*c
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
		holes = self.part['holes']

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

		# Add holes
		if(holes):
			for hole in holes:
				target.add_pac_hole(hole[0], (hole[1], hole[2]))

		# Add silk and courtyard
		target.add_pac_line('Courtyard', 0.1, [(-CEx, -CEy), (CEx, -CEy), (CEx, CEy), (-CEx, CEy), ('end',0)])
		target.add_pac_line('Silk', 0.1, [(-E1.max/2, -D.max/2), (E1.max/2, -D.max/2), (E1.max/2, D.max/2), (-E1.max/2, D.max/2), ('end',0)])

		if(self.part['mark'] == 'circle'):
			d = 0.2
			target.add_pac_circle('Silk', d, (-E1.nom/2 - 3*d, y0 + X/2 + 2*d))

		if(self.part['mark'] == 'diode'):
			target.add_pac_rectangle('Silk', (-E1.max/2, D.max/2), (0, -D.max/2))
