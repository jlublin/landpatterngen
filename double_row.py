import target_svg
import target_eagle

from ipc7351 import IPC7351
from tollen import TolLen

class DoubleRow:

	# part containts T, W, S, L, etc
	# design contaits J_H, J_T, J_S and CE
	# process contains F and P
	def __init__(self, part, design, process):

		for c in ['T', 'W']:
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

		if('S' not in part and 'L' not in part):
			print('Missing both "S" and "L"')
			return

		if('S' not in part):
			part['S'] = part['L'] - part['T'] - part['T']

		if('L' not in part):
			part['L'] = part['S'] + part['T'] + part['T']

		self.design = design
		self.process = process
		self.part = part
		self.land = {}

		self.calculate_pattern()


	def calculate_pattern(self):

		if('S' not in self.part):
			self.part['S'] = self.part['L'] - self.part['T'] - self.part['T']

		if('L' not in self.part):
			self.part['L'] = self.part['S'] + self.part['T'] + self.part['T']

		L = self.part['L']
		S = self.part['S']
		W = self.part['W']

		J_T = TolLen(self.design['J_T'], 0, 1)
		J_H = TolLen(self.design['J_H'], 0, 1)
		J_S = TolLen(self.design['J_S'], 0, 1)
		CE = self.design['CE']

		F = self.process['F']
		P = self.process['P']

		# Q = L + 2*JT + F + P
		# Zmax = Qmax + Qtol - Ltol

		Q = L + J_T + J_T + F + P
		Z =  Q.max + Q.tol - L.tol

		# Q = S - 2*JH + F + P
		# Gmin = Qmin - Qtol + Stol

		Q = S - J_H - J_H + F + P
		G =  Q.min - Q.tol + S.tol

		# Q = W + 2*JS + F + P
		# Xmax = Qmax + Qtol - Wtol

		Q = W + J_S + J_S + F + P
		X =  Q.max + Q.tol - W.tol

		Y = (Z - G) / 2
		C = G + Y

		# TODO: trimming

		self.land['C'] = round(C,1)
		self.land['G'] = round(G,1)
		self.land['X'] = round(X,1)
		self.land['Y'] = round(Y,1)
		self.land['Z'] = round(Z,1)


		# C,E,G,X,Y,Z
	def gen(self, target):

		A = self.part['A']
		B = self.part['B']
		E = self.part['E']
		L = self.part['L']

		C = self.land['C']
		X = self.land['X']
		Y = self.land['Y']
		Z = self.land['Z']
		npin = self.part['npin']

		CE = self.design['CE']

		CEx = max(L.max, Z)/2 + CE
		CEy = max(B.max, E*(npin//2 - 1) + X)/2 + CE

		y0 = (npin//2 - 1)/2 * E

		for i in range(npin//2):
			target.add_pac_pad(0, 0, (Y, X), (-C/2, y0 - i*E), i+1)
			target.add_pac_pad(0, 0, (Y, X), (C/2, y0 - i*E), npin-i)

		target.add_pac_line('Courtyard', 0.1, [(-CEx, -CEy), (CEx, -CEy), (CEx, CEy), (-CEx, CEy), ('end',0)])
		target.add_pac_line('Silk', 0.1, [(-A.max/2, -B.max/2), (A.max/2, -B.max/2), (A.max/2, B.max/2), (-A.max/2, B.max/2), ('end',0)])

		if(self.part['mark'] == 'circle'):
			d = 0.2
			target.add_pac_circle('Silk', d, (-A.nom/2 - 3*d, y0 + X/2 + 2*d))

		if(self.part['mark'] == 'diode'):
			target.add_pac_rectangle('Silk', (-A.max/2, B.max/2), (0, -B.max/2))

if(__name__ == '__main__'):

	soic8 = {	'A': TolLen(3.9, 4.4),
				'B': TolLen(4.9, 5.2),
				'E': 1.27,
				'L': TolLen(5.90, 6.10),
				'T': TolLen(0.40, 1.27),
				'W': TolLen(0.31, 0.51),
				'npin': 8,
				'mark': 'circle' }

	diode = {	'A': TolLen(1.85, 2.15),
				'B': TolLen(1.10, 1.40),
				'E': 0,
				'L': TolLen(1.85, 2.15),
				'S': TolLen(0.55, 1.32),
				'T': TolLen(0.15, 0.65),
				'W': TolLen(1.10, 1.40),
				'npin': 2,
				'mark': 'diode' }

	process = {	'F': TolLen(0, 0.05, 1),
				'P': TolLen(0, 0.05, 1) }

	soic8 = DoubleRow(soic8, IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)']['B'], process)
	diode = DoubleRow(diode, IPC7351['Rectangular or Square-End Components (Capacitors and Resistors) (>= 1608 (0603))']['C'], process)

	target = target_eagle.get_target()
	target.add_package('SOP127P6-8')
	soic8.gen(target)
	target.output('soic8.scr')

	target = target_eagle.get_target()
	target.add_package('DIOM2012')
	diode.gen(target)
	target.output('diode.scr')
