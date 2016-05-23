from tollen import TolLen

class BGA:

	# part contains D, E, d, e, b, npin1, npin2, deleted, mark
	# design contains ?? and CE
	# process contains F and P
	def __init__(self, part, design, process):

		for c in ['D', 'E', 'd', 'e', 'b', 'npin1', 'npin2', 'deleted', 'mark']:
			if(c not in part):
				print('Missing "{}"'.format(c))
				return

#		for c in ['J_H', 'J_T', 'J_S', 'CE']:
#			if(c not in design):
#				print('Missing "{}"'.format(c))
#				return

		for c in ['F', 'P']:
			if(c not in process):
				print('Missing "{}"'.format(c))
				return

		self.design = design
		self.process = process
		self.part = part
		self.land = {}

		self.calculate_pattern()


	def calculate_pattern(self):

		D = self.part['D']
		E = self.part['E']
		d = self.part['d']
		e = self.part['e']
		b = self.part['b']

		CE = self.design['CE']

		F = self.process['F']
		P = self.process['P']

		# TODO: trimming?
		# TODO: rounding?


	def gen(self, target):

		D = self.part['D']
		E = self.part['E']
		d = self.part['d']
		e = self.part['e']
		b = self.part['b']

		X = self.design[b.nom]

		CE = self.design['CE']

		npin1 = self.part['npin1']
		npin2 = self.part['npin2']
		deleted = self.part['deleted']

		CE = self.design['CE']

		CEx = E.nom/2 + CE
		CEy = D.nom/2 + CE

		y0 = (npin1 - 1)/2 * e
		x0 = (npin2 - 1)/2 * d

		# Add pads
		for i in range(npin1): # A, B, C, ...
			for j in range(npin2): # 1, 2, 3...
				pin = chr(b'A'[0] + i) + chr(b'0'[0] + j + 1)
				if(deleted == None or pin not in deleted):
					target.add_pac_pad(1, 0, (X, X), (-x0 + j*e , y0 - i*e), pin)

		# Add silk and courtyard
		target.add_pac_line('Courtyard', 0.1, [(-CEx, -CEy), (CEx, -CEy), (CEx, CEy), (-CEx, CEy), ('end',0)])
		target.add_pac_line('Silk', 0.1, [(-E.max/2, -D.max/2), (E.max/2, -D.max/2), (E.max/2, D.max/2), (-E.max/2, D.max/2), ('end',0)])

		if(self.part['mark'] == 'circle'):
			d = 0.2
			target.add_pac_circle('Silk', d, (-E.nom/2 - 3*d, y0 + X/2 + 2*d))
