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

		part['npin'] = 6
		part['deleted'] = [2, 4, 6]
		part['mark'] = None

		if(design[0:8] == 'IPC7351-'):
			density = design[8]
			design = ipc7351.IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)'][density]

		else:
			print('Cannot handle design {}'.format(design))
			return

		self.generator = packages.double_row.DoubleRow(part, design, process)

		# C,E,G,X,Y,Z
	def gen(self, target):

		self.generator.gen(target)
