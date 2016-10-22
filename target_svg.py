#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def get_target():
	return SVG()

class SVG:
	def __init__(self):
		self.svg = ET.parse('skeleton.svg')


	def output(self, path):
		self.svg.write(path)


	def add_package(self, package):
		'''
		Target SVG only handles one drawing at a time, only last added drawing will be part of output
		'''
		self.svg = ET.parse('skeleton.svg')

		self.package = \
			{
				'name': package['name'],
				'pads': [],
				'mnt_pads': [],
				'holes': [],
				'lines': [],
				'circles': [],
				'rectangles': [] ,
				'texts': []
			}


	def output(self, fout):

		import pprint
		pprint.pprint(self.package)

		package = self.package

		for pad in package['pads']:
			self.gen_pac_pad(pad)
		if(0):
			for mnt_pad in package['mnt_pads']:
				self.gen_pac_mnt_pad(mnt_pad)

			for hole in package['holes']:
				self.gen_pac_hole(hole)

			for line in package['lines']:
				self.gen_pac_line(line)

			for circle in package['circles']:
				self.gen_pac_circle(circle)

			for rect in package['rectangles']:
				self.gen_pac_rectangle(rect)

			for text in package['texts']:
				self.gen_pac_text(text)

		self.svg.write(fout)


	def add_pac_pad(self, type, angle, size, pos, number):

		self.package['pads'].append(
			{
				'type': type,
				'angle': angle,
				'size': size,
				'pos': pos,
				'number': number
			})

	def add_pac_hole(self, diameter, pos):

		self.package['holes'].append(
			{
				'd': diameter,
				'pos': pos
			})

	def add_pac_line(self, layer, width, vertices):

		self.package['holes'].append(
			{
				'layer': layer,
				'w': width,
				'vertices': vertices
			})

	def gen_pac_pad(self, pad): # type, angle, size, pos, number
		top_layer = self.svg.find('.//g[@id="Top"]')

		# TODO: Types and angle

		el = ET.SubElement(top_layer, 'rect')
		el.set('style', 'fill:#ff0000;fill-opacity:1;stroke:none;stroke-width:10;stroke-linecap:square;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1')
		el.set('id', 'pin_{}'.format(pad['number']))
		el.set('width', '{}'.format(pad['size'][0]))
		el.set('height', '{}'.format(pad['size'][1]))
		el.set('x', '{}'.format(pad['pos'][0]))
		el.set('y', '{}'.format(pad['pos'][1]))


	def gen_line(self, layer_name, width, vertices):

		layer = self.svg.find('.//g[@id="{}"]'.format(layer_name))

		if(layer_name == 'Courtyard'):
			color = '#e63a81'
		elif(layer_name == 'Silk'):
			color = '#111111'
		else:
			color = '#000000'

		line = ET.SubElement(layer, 'path')
		line.set('style', 'fill:none;fill-rule:evenodd;stroke:{color};stroke-width:{}mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none'.format(width, color=color))

		pathdata = ''
		first = True

		for (x,y) in vertices:
			if(first):
				pathdata += 'M ' + '{},{}'.format(x*3.543307,y*3.543307)
				first = False
			elif(x == 'end'):
				pathdata += ' z'
			else:
				pathdata += ' L ' + '{},{}'.format(x*3.543307,y*3.543307)

		line.set('d', pathdata)


	def gen_circle(self, layer_name, diameter, pos):

		layer = self.svg.find('.//g[@id="{}"]'.format(layer_name))

		if(layer_name == 'Courtyard'):
			color = '#e63a81'
		elif(layer_name == 'Silk'):
			color = '#111111'
		else:
			color = '#000000'

		circle = ET.SubElement(layer, 'circle')
		circle.set('style', 'fill:#{color};fill-opacity:1;stroke:none;stroke-width:0.0;stroke-linecap:square;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"'.format(color=color))

		circle.set('cx', '{}'.format(pos[0]*3.543307))
		circle.set('cy', '{}'.format(pos[1]*3.543307))
		circle.set('r', '{}'.format(diameter/2*3.543307))


if(__name__ == '__main__'):

	target = get_target()

	target.output('test.svg')
