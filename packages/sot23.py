import copy
from tollen import TolLen

'''
Arguments: (E1) (D) e (E) (S) (L) (b) npin
'''

import ipc7351
import packages.dual_row

def get_package(part, design, process):
	return SOT23(part, design, process)

def get_params():
	return [
		('E1', 't'),
		('D', 't'),
		('e', 'f'),
		('E', 't'),
		('S', 't'),
		('L', 't'),
		('b', 't'),
		('npin', 'i')]

class SOT23:

	# part contains L, b, S, E, e, E1, D
	# design contais 'IPC7351-x' where x in {A,B,C}
	# process contains F and P
	def __init__(self, part, design, process):

		part = copy.deepcopy(part)
		self.generator = None

		pins = part['npin']

		if(pins == 3):
			part['deleted_pins'] = [2, 4, 6]
			part['npin'] = 6

		elif(pins == 5):
			part['deleted_pins'] = [2]
			part['npin'] = 6

		elif(pins == 6):
			part['deleted_pins'] = None

		elif(pins == 8):
			part['deleted_pins'] = None

		else:
			print('Cannot handle SOT23 with {} pins'.format(pins))
			return

		part['mark'] = None
		part['holes'] = None

		# IPC7351 density level A, B or C
		if(design[0:8] == 'IPC7351-'):
			density = design[8]
			if(part['e'] > 0.625):
				design = ipc7351.IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)'][density]
			else:
				design = ipc7351.IPC7351['Flat Ribbon L and Gull-Wing Leads (<= 0.625mm pitch)'][density]

		else:
			print('Cannot handle design {}'.format(design))
			return

		self.generator = packages.dual_row.DualRow(part, design, process)


	def gen(self, target):

		if(self.generator):
			self.generator.gen(target)
