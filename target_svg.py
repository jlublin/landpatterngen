#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def get_target():
	return SVG()

class SVG:
	def __init__(self):
		self.svg = ET.parse('skeleton.svg')


	def output(self, path):
		self.svg.write(path)


	def add_pad(self, type, angle, size, pos, number):
		top_layer = self.svg.find('.//g[@id="Top"]')

		# TODO: Types and angle

		pad = ET.SubElement(top_layer, 'rect')
		pad.set('style', 'fill:#ff0000;fill-opacity:1;stroke:none;stroke-width:10;stroke-linecap:square;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1')
		pad.set('id', 'pin_' + str(number))
		pad.set('width', str(size[0]) + 'mm')
		pad.set('height', str(size[1]) + 'mm')
		pad.set('x', str(pos[0]) + 'mm')
		pad.set('y', str(pos[1]) + 'mm')


	def add_line(self, layer_name, width, vertices):

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


	def add_circle(self, layer_name, diameter, pos):

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

	target.add_pad(0, 0, (10, 20), (30, 40), 1)
	target.add_line('Courtyard', 1, [(0,0), (50,50), (0,50)])

	target.output('test.svg')
