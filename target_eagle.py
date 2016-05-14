#!/usr/bin/env python3

def get_target(name):
	return Eagle(name)

class Eagle:
	def __init__(self, name):
		self.scr = '''\
# Created by LandPatternGen

grid mm;
set wire_bend 2;

edit '{name}.pac';
'''.format(name=name)


	def output(self, path):
		f = open(path, 'w')
		f.write(self.scr)
		f.close


	def add_pad(self, type, angle, size, pos, number):

		# TODO: Types and angle

		self.scr += '''\
layer 1;
smd '{id}' {w} {h} -0 R0 ({x} {y});
'''.format(id=number, w=size[0], h=size[1], x=pos[0], y=pos[1]);


	def add_line(self, layer_name, width, vertices):

		if(layer_name == 'Courtyard'):
			layer = 41
		elif(layer_name == 'Silk'):
			layer = 21
		else:
			layer = 51

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

		self.scr += '''\
layer {};
{}
'''.format(layer, wires)


	def add_circle(self, layer_name, diameter, pos):

		if(layer_name == 'Courtyard'):
			layer = 41
		elif(layer_name == 'Silk'):
			layer = 21
		else:
			layer = 51

		self.scr += '''\
layer {};
circle ({:.3f} {:.3f}) ({:.3f} {:.3f});
'''.format(layer, pos[0], pos[1], pos[0] + diameter, pos[1])


	def add_rectangle(self, layer_name, pos1, pos2):

		if(layer_name == 'Courtyard'):
			layer = 41
		elif(layer_name == 'Silk'):
			layer = 21
		else:
			layer = 51

		self.scr += '''\
layer {};
rect ({:.3f} {:.3f}) ({:.3f} {:.3f});
'''.format(	layer, pos1[0], pos1[1], pos2[0], pos2[1])
