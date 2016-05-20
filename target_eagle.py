#!/usr/bin/env python3

def get_target():
	return Eagle()

sym_scale = 100
sym_wire_scale = 16

class Eagle:

	def __init__(self):

		self.symbols = []
		self.packages = []


	def add_symbol(self, name):

		self.current_symbol = { 'name': name, 'pins': [], 'lines': [], 'arcs': [], 'rings': [], 'texts': [] }
		self.symbols.append(self.current_symbol)


	def add_package(self, name):

		self.current_package = { 'name': name, 'pads': [], 'lines': [], 'circles': [], 'rectangles': [] , 'texts': []}
		self.packages.append(self.current_package)


	def output(self, path):

		scr = '''\
# Created by LandPatternGen

set wire_bend 2;

'''
		for symbol in self.symbols:
			scr += 'edit \'{name}.sym\';\n'.format(name=symbol['name'])
			scr += 'grid mil\n'

			scr += 'layer 94;\n'

			for pin in symbol['pins']:
				scr += self.gen_sym_pin(pin[0], pin[1])

			current_layer = -1

			for line in symbol['lines']:

				if(line[0] != current_layer):
					scr += 'layer {};\n'.format(line[0])

				scr += self.gen_sym_line(line[1], line[2])

			for arc in symbol['arcs']:

				if(arc[0] != current_layer):
					scr += 'layer {};\n'.format(arc[0])

				scr += self.gen_sym_arc(arc[1], arc[2], arc[3], arc[4])


			for ring in symbol['rings']:

				if(ring[0] != current_layer):
					scr += 'layer {};\n'.format(ring[0])

				scr += self.gen_sym_ring(ring[1], ring[2], ring[3])

			for text in symbol['texts']:

				if(text[0] != current_layer):
					scr += 'layer {};\n'.format(text[0])

				scr += self.gen_sym_text(text[1], text[2])

			scr += '\n'

		for package in self.packages:
			scr += 'edit \'{name}.pac\';\n'.format(name=package['name'])
			scr += 'grid mm\n'

			for pad in package['pads']:
				scr += self.gen_pac_pad(pad[2], pad[3], pad[4])

			current_layer = -1

			for line in package['lines']:

				if(line[0] != current_layer):
					scr += 'layer {};\n'.format(line[0])

				scr += self.gen_pac_line(line[1], line[2])

			for circle in package['circles']:

				if(circle[0] != current_layer):
					scr += 'layer {};\n'.format(circle[0])

				scr += self.gen_pac_circle(circle[1], circle[2])

			for rect in package['rectangles']:

				if(rect[0] != current_layer):
					scr += 'layer {};\n'.format(rect[0])

				scr += self.gen_pac_rectangle(rect[1], rect[2])

			for text in package['texts']:

				if(text[0] != current_layer):
					scr += 'layer {};\n'.format(text[0])

				scr += self.gen_pac_text(text[1], text[2])

			scr += '\n'

		f = open(path, 'w')
		f.write(scr)
		f.close


	def add_sym_pin(self, id, pos):

		self.current_symbol['pins'].append([id, pos])


	def gen_sym_pin(self, id, pos):
		return 'pin \'{id}\' I/O None Point R0 Both 0 ({x} {y});\n'.format(id=id, x=pos[0]*sym_scale, y=pos[1]*sym_scale);


	def add_pac_pad(self, type, angle, size, pos, number):

		self.current_package['pads'].append([type, angle, size, pos, number])


	def gen_pac_pad(self, size, pos, number):

		# TODO: Types and angle

		return 'smd \'{id}\' {w} {h} -0 R0 ({x} {y});\n'.format(id=number, w=size[0], h=size[1], x=pos[0], y=pos[1]);


	def add_sym_line(self, layer_name, width, vertices):

		if(layer_name == 'Symbols'):
			layer = 94
		else:
			layer = 97

		self.current_symbol['lines'].append([layer, width, vertices])


	def gen_sym_line(self, width, vertices):

		wires = ''

		for i in range(len(vertices)):
			if(i+1 < len(vertices)):

				if(vertices[i+1][0] == 'end'):
					vertices[i+1] = vertices[0];

				wires += 'wire {} ({} {}) ({} {});\n'.format(
							width * sym_wire_scale,
							vertices[i][0] * sym_scale,
							vertices[i][1] * sym_scale,
							vertices[i+1][0] * sym_scale,
							vertices[i+1][1] * sym_scale)

		return wires


	def add_pac_line(self, layer_name, width, vertices):

		if(layer_name == 'Courtyard'):
			layer = 41
		elif(layer_name == 'Silk'):
			layer = 21
		else:
			layer = 51

		self.current_package['lines'].append([layer, width, vertices])


	def gen_pac_line(self, width, vertices):

		wires = ''

		for i in range(len(vertices)):
			if(i+1 < len(vertices)):

				if(vertices[i+1][0] == 'end'):
					vertices[i+1] = vertices[0];

				wires += 'wire {} ({} {}) ({} {});\n'.format(
							width,
							vertices[i][0],
							vertices[i][1],
							vertices[i+1][0],
							vertices[i+1][1])

		return wires


	def add_sym_arc(self, layer_name, width, start, center, end):

		if(layer_name == 'Symbols'):
			layer = 94
		else:
			layer = 97

		self.current_symbol['arcs'].append([layer, width, start, center, end])


	def gen_sym_arc(self, width, start, center, end):

		diameter = (2*center[0] - start[0], 2*center[1] - start[1])

		return 'arc {:.3f} ({:.3f} {:.3f}) ({:.3f} {:.3f}) ({:.3f} {:.3f});\n'.format(
			width * sym_wire_scale,
			start[0] * sym_scale,
			start[1] * sym_scale,
			diameter[0] * sym_scale,
			diameter[1] * sym_scale,
			end[0] * sym_scale,
			end[1] * sym_scale)


	def add_sym_ring(self, layer_name, width, diameter, pos):

		if(layer_name == 'Symbols'):
			layer = 94
		else:
			layer = 97

		self.current_symbol['rings'].append([layer, width, diameter, pos])


	def gen_sym_ring(self, width, diameter, pos):

		return 'circle {:.3f} ({:.3f} {:.3f}) ({:.3f} {:.3f});\n'.format(
			width * sym_wire_scale,
			pos[0] * sym_scale,
			pos[1] * sym_scale,
			(pos[0] + diameter) * sym_scale,
			pos[1] * sym_scale)


	def add_pac_circle(self, layer_name, diameter, pos):

		if(layer_name == 'Courtyard'):
			layer = 41
		elif(layer_name == 'Silk'):
			layer = 21
		else:
			layer = 51

		self.current_package['circles'].append([layer, diameter, pos])


	def gen_pac_circle(self, diameter, pos):

		return 'circle 0 ({:.3f} {:.3f}) ({:.3f} {:.3f});\n'.format(pos[0], pos[1], pos[0] + diameter, pos[1])


	def  add_pac_rectangle(self, layer_name, pos1, pos2):

		if(layer_name == 'Courtyard'):
			layer = 41
		elif(layer_name == 'Silk'):
			layer = 21
		else:
			layer = 51


		self.current_package['rectangles'].append([layer, pos1, pos2])


	def gen_pac_rectangle(self, pos1, pos2):

		return 'rect ({:.3f} {:.3f}) ({:.3f} {:.3f});\n'.format(pos1[0], pos1[1], pos2[0], pos2[1])


	def add_sym_text(self, layer_name, text, pos):

		if(layer_name == 'Name'):
			layer = 95
		elif(layer_name == 'Value'):
			layer = 96
		else:
			layer = 97

		self.current_symbol['texts'].append([layer, text, pos])


	def gen_sym_text(self, text, pos):

		return 'text \'{}\' R0 ({} {})'.format(text, pos[0] * sym_scale, pos[1] * sym_scale)


	def add_pac_text(self, layer_name, text, pos):

		if(layer_name == 'Name'):
			layer = 25
		elif(layer_name == 'Value'):
			layer = 27
		else:
			layer = 51

		self.current_package['texts'].append([layer, text, pos])


	def gen_pac_text(self, text, pos):

		return 'text \'{}\' R0 ({} {})'.format(text, pos[0], pos[1])


if(__name__ == '__main__'):

	import importlib
	import symbols
	from tollen import TolLen

	target = get_target()

	## Add some symbols

	target.add_symbol('Diode')

	sym = importlib.import_module('symbols.diode')
	sym.draw(target)

	target.add_symbol('LED')

	sym = importlib.import_module('symbols.led')
	sym.draw(target)

	target.add_symbol('Zener')

	sym = importlib.import_module('symbols.zener')
	sym.draw(target)

	target.add_symbol('Varicap')

	sym = importlib.import_module('symbols.varicap')
	sym.draw(target)

	target.add_symbol('Resistor')

	sym = importlib.import_module('symbols.resistor')
	sym.draw(target)

	target.add_symbol('Capacitor')

	sym = importlib.import_module('symbols.capacitor')
	sym.draw(target)

	target.add_symbol('Inductor')

	sym = importlib.import_module('symbols.inductor')
	sym.draw(target)

	target.add_symbol('NPN')

	sym = importlib.import_module('symbols.npn')
	sym.draw(target)

	target.add_symbol('PNP')

	sym = importlib.import_module('symbols.pnp')
	sym.draw(target)

	## Manually add a package

	target.add_package('DIOM2012')

	target.add_pac_pad(0, 0, (1, 1), (-1, 0), 0)
	target.add_pac_pad(0, 0, (1, 1), (1, 0), 1)
	target.add_pac_line('Courtyard', 0.1, [(-2,-1), (-2,1), (2,1), (2,-1), ('end', 0)])
	target.add_pac_circle('Silk', 0.1, (-1, 0.75))
	target.add_pac_line('Silk', 0.1, [(-0.5,-0.5), (0.5,-0.5)])
	target.add_pac_line('Silk', 0.1, [(-0.5,0.5), (0.5,0.5)])
	target.add_pac_rectangle('Silk', (-0.5,-0.5), (0,0.5))
	target.add_pac_text('Name', '>NAME', (-0.5,0))

	## Add some packages via parameters

	from ipc7351 import IPC7351
	dr = importlib.import_module('packages.double_row')

	soic8 = {	'A': TolLen(3.9, 4.4),
				'B': TolLen(4.9, 5.2),
				'E': 1.27,
				'L': TolLen(5.90, 6.10),
				'T': TolLen(0.40, 1.27),
				'W': TolLen(0.31, 0.51),
				'npin': 8,
				'deleted': None,
				'mark': 'circle' }

	diode = {	'A': TolLen(1.85, 2.15),
				'B': TolLen(1.10, 1.40),
				'E': 0,
				'L': TolLen(1.85, 2.15),
				'S': TolLen(0.55, 1.32),
				'T': TolLen(0.15, 0.65),
				'W': TolLen(1.10, 1.40),
				'npin': 2,
				'deleted': None,
				'mark': 'diode' }

	sot23 = {	'A': TolLen(1.20, 1.40),
				'B': TolLen(2.80, 3.00),
				'E': 0.95,
				'L': TolLen(2.30, 2.60),
				'S': TolLen(1.10, 1.47),
				'T': TolLen(0.45, 0.60),
				'W': TolLen(0.36, 0.46)}

	process = {	'F': TolLen(0, 0.05, 1),
				'P': TolLen(0, 0.05, 1) }

	target.add_package('SOP127P6-8')
	soic8 = dr.DoubleRow(soic8, IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)']['B'], process)
	soic8.gen(target)

	target.add_package('DIOM2012-C')
	diode = dr.DoubleRow(diode, IPC7351['Rectangular or Square-End Components (Capacitors and Resistors) (>= 1608 (0603))']['C'], process)
	diode.gen(target)

	target.add_package('SOT23')

	mod = importlib.import_module('packages.sot23')
	pac = mod.get_package(sot23, 'IPC7351-C', process)
	pac.gen(target)

	## Output result

	target.output('target_eagle_test.scr')
