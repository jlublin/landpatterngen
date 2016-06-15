from tollen import TolLen

'''
Arguments: (D) (E) e (L) (b) npin

TODO: Thermal tab
'''

import ipc7351
import packages.quad_row

def get_package(part, design, process):
	return SOT23(part, design, process)

class SOT23:

	# part contains D, E, e, L, b, npin
	# design contais 'IPC7351-x' where x in {A,B,C}
	# process contains F and P
	def __init__(self, part, design, process):

		if(isinstance(part, list)):
			p = part
			part = {	'D': TolLen(float(p[0][0]), float(p[0][1])),
						'E': TolLen(float(p[1][0]), float(p[1][1])),
						'e': float(p[2]),
						'L': TolLen(float(p[3][0]), float(p[3][1])),
						'b': TolLen(float(p[4][0]), float(p[4][1])),
						'npin': int(p[5])}

		part['D1'] = part['D']
		part['E1'] = part['E']
		part['npin1'] = part['npin'] // 4
		part['npin2'] = part['npin'] // 4
		part['mark'] = 'circle'
		part['deleted'] = None

		# IPC7351 density level A, B or C
		if(design[0:8] == 'IPC7351-'):
			density = design[8]
			design = ipc7351.IPC7351['Flat, No Lead'][density]

		else:
			print('Cannot handle design {}'.format(design))
			return

		self.generator = packages.quad_row.QuadRow(part, design, process)


	def gen(self, target):

		self.generator.gen(target)
