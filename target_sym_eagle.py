#!/usr/bin/env python3

def get_target():
	return SYM_Eagle()

scale = 100
wire_scale = 16

class SYM_Eagle:

	def __init__(self):

		self.symbols = []


	def add_symbol(self, name):

		self.current_symbol = { 'name': name, 'pins': [], 'lines': [] }
		self.symbols.append(self.current_symbol)


	def output(self, path):

		scr = '''\
# Created by LandPatternGen

grid mil;
set wire_bend 2;

'''
		for symbol in self.symbols:
			scr += 'edit \'{name}.sym\';\n'.format(name=symbol['name'])

			scr += 'layer 94;\n'

			for pin in symbol['pins']:
				scr += self.gen_pin(pin[0], pin[1])

			for line in symbol['lines']:
				scr += self.gen_line(line[1], line[2])

			scr += '\n'

		f = open(path, 'w')
		f.write(scr)
		f.close


	def add_pin(self, id, pos):

		self.current_symbol['pins'].append([id, pos])


	def gen_pin(self, id, pos):
		return 'pin \'{id}\' I/O None Point R0 Both 0 ({x} {y});\n'.format(id=id, x=pos[0]*scale, y=pos[1]*scale);


	def add_line(self, layer_name, width, vertices):

		if(layer_name == 'Symbols'):
			layer = 94
		else:
			layer = 98

		self.current_symbol['lines'].append([layer, width, vertices])


	def gen_line(self, width, vertices):

		wires = ''

		for i in range(len(vertices)):
			if(i+1 < len(vertices)):

				if(vertices[i+1][0] == 'end'):
					vertices[i+1] = vertices[0];

				wires += 'wire {} ({} {}) ({} {});\n'.format(
							width*wire_scale,
							vertices[i][0]*scale,
							vertices[i][1]*scale,
							vertices[i+1][0]*scale,
							vertices[i+1][1]*scale)

		return wires


if(__name__ == '__main__'):

	target = get_target()
	target.add_symbol('Diode')

	target.add_pin('A', (-1, 0))
	target.add_pin('K', (2, 0))
	target.add_line('Symbols', 1, [(-1,0), (0,0)])
	target.add_line('Symbols', 1, [(0,0.5), (0,-0.5), (1,0), ('end',0)])
	target.add_line('Symbols', 1, [(1,0.5), (1,-0.5)])
	target.add_line('Symbols', 1, [(1,0), (2,0)])

	target.output('test.scr')
