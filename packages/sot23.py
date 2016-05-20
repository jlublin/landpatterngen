from tollen import TolLen

import ipc7351
import packages.double_row

def get_package(part, design, process):
	return SOT23(part, design, process)

class SOT23:

	# part contains T, W, S, L, A, B, E
	# design contais 'IPC7351-x' where x in {A,B,C}
	# process contains F and P
	def __init__(self, part, design, process):

		pins = part['npin']

		part['npin'] = 6

		if(pins == 3):
			part['deleted'] = [2, 4, 6]

		elif(pins == 5):
			part['deleted'] = [2]

		elif(pins == 6):
			part['deleted'] = None

		elif(pins == 8):
			part['deleted'] = None
			part['npin'] = 8

		else:
			print('Cannot handle SOT23 with {} pins'.format(pins))
			return

		part['mark'] = None

		# IPC7351 density level A, B or C
		if(design[0:8] == 'IPC7351-'):
			density = design[8]
			if(part['E'] > 0.625):
				design = ipc7351.IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)'][density]
			else:
				design = ipc7351.IPC7351['Flat Ribbon L and Gull-Wing Leads (<= 0.625mm pitch)'][density]

		else:
			print('Cannot handle design {}'.format(design))
			return

		self.generator = packages.double_row.DoubleRow(part, design, process)

		# C,E,G,X,Y,Z
	def gen(self, target):

		self.generator.gen(target)
