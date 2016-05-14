#!/usr/bin/env python3

def get_target(name):
	return SYM_Eagle(name)

scale = 100
wire_scale = 16

class SYM_Eagle:

	def __init__(self, name):

		self.name = name
		self.pins = []
		self.lines = []


	def output(self, path):

		scr = '''\
# Created by LandPatternGen

grid mil;
set wire_bend 2;

edit '{name}.sym';
'''.format(name=self.name)

		scr += 'layer 94;\n'

		for pin in self.pins:
			scr += self.gen_pin(pin[0], pin[1])

		for line in self.lines:
			scr += self.gen_line(line[1], line[2])

		f = open(path, 'w')
		f.write(scr)
		f.close


	def add_pin(self, id, pos):

		self.pins.append([id, pos])


	def gen_pin(self, id, pos):
		return 'pin \'{id}\' I/O None Point R0 Both 0 ({x} {y});\n'.format(id=id, x=pos[0]*scale, y=pos[1]*scale);


	def add_line(self, layer_name, width, vertices):

		if(layer_name == 'Symbols'):
			layer = 94
		else:
			layer = 98

		self.lines.append([layer, width, vertices])


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

	target = get_target(('Diode'))

	target.add_pin('A', (-1, 0))
	target.add_pin('K', (2, 0))
	target.add_line('Symbols', 1, [(-1,0), (0,0)])
	target.add_line('Symbols', 1, [(0,0.5), (0,-0.5), (1,0), ('end',0)])
	target.add_line('Symbols', 1, [(1,0.5), (1,-0.5)])
	target.add_line('Symbols', 1, [(1,0), (2,0)])

	target.output('test.scr')
