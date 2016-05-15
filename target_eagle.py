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

		self.current_symbol = { 'name': name, 'pins': [], 'lines': [], 'texts': [] }
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

	target = get_target()

	target.add_symbol('Diode')

	target.add_sym_pin('A', (-1, 0))
	target.add_sym_pin('K', (2, 0))
	target.add_sym_line('Symbols', 1, [(-1,0), (0,0)])
	target.add_sym_line('Symbols', 1, [(0,0.5), (0,-0.5), (1,0), ('end',0)])
	target.add_sym_line('Symbols', 1, [(1,0.5), (1,-0.5)])
	target.add_sym_line('Symbols', 1, [(1,0), (2,0)])
	target.add_sym_text('Name', '>NAME', (-1,1))

	target.add_package('DIOM2012')

	target.add_pac_pad(0, 0, (1, 1), (-1, 0), 0)
	target.add_pac_pad(0, 0, (1, 1), (1, 0), 1)
	target.add_pac_line('Courtyard', 0.1, [(-2,-1), (-2,1), (2,1), (2,-1), ('end', 0)])
	target.add_pac_circle('Silk', 0.1, (-1, 0.75))
	target.add_pac_line('Silk', 0.1, [(-0.5,-0.5), (0.5,-0.5)])
	target.add_pac_line('Silk', 0.1, [(-0.5,0.5), (0.5,0.5)])
	target.add_pac_rectangle('Silk', (-0.5,-0.5), (0,0.5))
	target.add_pac_text('Name', '>NAME', (-0.5,0))

	target.output('target_eagle_test.scr')
