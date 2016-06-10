#!/usr/bin/env python3

def get_target():
	return Eagle()

sym_scale = 100
sym_wire_scale = 16

class Eagle:

	def __init__(self):

		self.symbols = []
		self.packages = []
		self.devices = []


	def add_symbol(self, name):

		self.current_symbol = { 'name': name, 'pins': [], 'lines': [], 'arcs': [], 'rings': [], 'texts': [] }
		self.symbols.append(self.current_symbol)


	def add_package(self, name):

		self.current_package = { 'name': name, 'pads': [], 'mnt_pads': [], 'holes': [], 'lines': [], 'circles': [], 'rectangles': [] , 'texts': []}
		self.packages.append(self.current_package)


	def add_device(self, name, prefix, value, description):

		self.current_device = { 'name': name, 'prefix': prefix, 'description': description, 'use_value': value, 'symbols': [], 'packages': []}
		self.devices.append(self.current_device)


	def output(self, fout):

		scr = '''\
# Created by LandPatternGen

set wire_bend 2;

'''
		# Generate symbols

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

		# Generate packages

		for package in self.packages:
			scr += 'edit \'{name}.pac\';\n'.format(name=package['name'])
			scr += 'grid mm\n'

			for pad in package['pads']:
				scr += self.gen_pac_pad(pad[0], pad[2], pad[3], pad[4])

			i = 1
			for mnt_pad in package['mnt_pads']:
				scr += self.gen_pac_mnt_pad(mnt_pad[0], mnt_pad[1], i)
				i += 1

			for hole in package['holes']:
				scr += self.gen_pac_hole(hole[0], hole[1])

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

		# Generate devices

		for device in self.devices:
			scr += 'edit \'{name}.dev\';\n'.format(**device)
			scr += 'prefix \'{prefix}\';\n'.format(**device)
			scr += 'description \'{description}\';\n'.format(**device)

			if(device['use_value']):
				scr += 'value on;\n'
			else:
				scr += 'value off;\n'

			i = 0;
			for symbol in device['symbols']:
				scr += self.gen_dev_symbol(symbol, i)
				i += 1

			for package in device['packages']:
				pass
				scr += self.gen_dev_package(package)

			scr += '\n'

		fout.write(scr)


	def add_sym_pin(self, id, pos):

		self.current_symbol['pins'].append([id, pos])


	def gen_sym_pin(self, id, pos):
		return 'pin \'{id}\' I/O None Point R0 Both 0 ({x} {y});\n'.format(id=id, x=pos[0]*sym_scale, y=pos[1]*sym_scale);


	def add_pac_pad(self, type, angle, size, pos, number):

		self.current_package['pads'].append([type, angle, size, pos, number])


	def gen_pac_pad(self, type, size, pos, number):

		# TODO: Types and angle

		if(type == 0):
			r = 0
		elif(type == 1):
			r = 100

		return 'smd \'{id}\' {w} {h} -{r} R0 ({x} {y});\n'.format(id=number, w=size[0], h=size[1], r=r, x=pos[0], y=pos[1]);


	def add_pac_mnt_pad(self, size, pos):

		self.current_package['mnt_pads'].append([size, pos])


	def gen_pac_mnt_pad(self, size, pos, num):

		return 'smd \'{id}\' {w} {h} -{r} R0 ({x} {y});\n'.format(id='MNTPAD{}'.format(num), w=size[0], h=size[1], r=0, x=pos[0], y=pos[1]);


	def add_pac_hole(self, diameter, pos):

		self.current_package['holes'].append([diameter, pos])


	def gen_pac_hole(self, diameter, pos):

		return 'hole {d} ({x} {y});\n'.format(d=diameter, x=pos[0], y=pos[1]);


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


	def add_dev_symbol(self, name):
		self.current_device['symbols'].append(name)


	def gen_dev_symbol(self, symbol, i):

		return 'add {} \'{}\' next (0 {});\n'.format(symbol, chr(b'A'[0]+i), i)


	def add_dev_package(self, name, variant, attributes, connections):

		package = { 'name': name,
		            'variant': variant,
		            'attributes': attributes,
		            'connections': connections }

		self.current_device['packages'].append(package)


	def gen_dev_package(self, package):
		ret = 'package \'{}\' \'{}\';\n'.format(package['name'], package['variant'])

		for connection in package['connections']:
			ret += 'connect \'{}\' \'{}\';\n'.format(connection[0], connection[1])

		for attribute in package['attributes']:
			ret += 'attribute \'{}\' \'{}\';\n'.format(attribute[0], attribute[1])

		return ret
