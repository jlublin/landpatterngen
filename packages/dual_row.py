import sys
import copy

from tollen import TolLen
#TODO version
'''
Arguments: (E1) (D) e (E) (S) (L) (b) npin mark (deleted) (holes) lead_type (C G X Y Z) (mount_pads) pin_order (row_offset1 row_offset2)
holes = (d, x, y)
If C X Y Z predefined, use them instead as custom device
Unused: (E2 D2 c r)
'''

def get_package(part, design, process):
	return DualRow(part, design, process)

def get_params():
	return ['E1:', 'D:', 'e', 'E:', 'S:', 'L:', 'b:', 'npin', 'mark', 'deleted*']

class DualRow:

	# part containts L, b, S, E, e, E1, D, npin, mark, deleted, holes
	# design contaits J_H, J_T, J_S and CE
	# process contains F and P
	def __init__(self, part, design, process):

		part = copy.deepcopy(part)

		if(isinstance(design, str) and design[0:8] == 'IPC7351-'):
			density = design[8]
			import ipc7351
			design = ipc7351.IPC7351[part['lead_type']]['B']

		for c in ['L', 'b', 'E1', 'e', 'D', 'npin']:
			if(c not in part):
				print('Missing "{}"'.format(c), file=sys.stderr)
				return

		for c in ['J_H', 'J_T', 'J_S', 'CE']:
			if(c not in design):
				print('Missing "{}"'.format(c), file=sys.stderr)
				return

		for c in ['F', 'P']:
			if(c not in process):
				print('Missing "{}"'.format(c), file=sys.stderr)
				return

		if('S' not in part and 'E' not in part):
			print('Missing both "S" and "E"', file=sys.stderr)
			return

		if('S' not in part):
			part['S'] = part['E'] - part['L'] - part['L']

		if('E' not in part):
			part['E'] = part['S'] + part['L'] + part['L']

		if('mount_pads' not in part):
			part['mount_pads'] = None

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
		deleted = self.part['deleted_pins']
		holes = self.part['holes']
		mount_pads = self.part['mount_pads']

		CE = self.design['CE']

		CEx = max(E.max, Z)/2 + CE
		CEy = max(D.max, e*(npin//2 - 1) + X)/2 + CE

		row1off = self.part.get('row_offset1') or 0
		row2off = self.part.get('row_offset2') or 0

		y0 = (npin//2 - 1)/2 * e

		# Generate pin mapping

		pin_map = {} # Pin position (always 1 in upper left and CCW) to pin name

		if('pin_order' in self.part and self.part['pin_order'] == 1):
			pin = 2
			# Deleted pins not implemented, not sure how it would work
			for i in range(npin//2):

				pin_map[i+1] = pin
				pin += 2

			pin = npin - 1
			for i in range(npin//2, npin):
				pin_map[i+1] = pin
				pin -= 2

		else:
			pin = 1
			for i in range(npin):
				if(deleted == None or (i+1) not in deleted):
					pin_map[i+1] = pin
					pin += 1

		# Add pads
		for i in range(npin):
			if(deleted == None or (i+1) not in deleted):
				if(i < npin//2):
					target.add_pac_pad(0, 0, (Y, X), (-C/2, y0 + row1off - i*e), pin_map[i+1])
				else:
					target.add_pac_pad(0, 0, (Y, X), (C/2, -y0 + row2off + (i-npin//2)*e), pin_map[i+1])

		# Add holes
		if(holes):
			for hole in holes:
				target.add_pac_hole(hole['d'], (hole['x'], hole['y']))

		# Add mount pad
		if(mount_pads):
			for pad in mount_pads:
				target.add_pac_mnt_pad((pad['w'], pad['h']), (pad['x'], pad['y']))

		# Add silk and courtyard
		target.add_pac_line('Courtyard', 0.1, [(-CEx, -CEy), (CEx, -CEy), (CEx, CEy), (-CEx, CEy), ('end',0)])
		target.add_pac_line('Silk', 0.1, [(-E1.max/2, -D.max/2), (E1.max/2, -D.max/2), (E1.max/2, D.max/2), (-E1.max/2, D.max/2), ('end',0)])

		if(self.part['mark'] == 'circle'):
			d = 0.2
			target.add_pac_circle('Silk', d, (-E1.nom/2 - 3*d, y0 + X/2 + 2*d))

		if(self.part['mark'] == 'diode'):
			target.add_pac_rectangle('Silk', (-E1.max/2, D.max/2), (0, -D.max/2))
