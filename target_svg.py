#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def get_target():
	return SVG()

class SVG:
	def __init__(self):
		self.svg = ET.parse('skeleton.svg')
		self.mmpx = 3.543307

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

		for mnt_pad in package['mnt_pads']: # TODO, adding mnt_pads not done
			self.gen_pac_mnt_pad(mnt_pad)

		for hole in package['holes']:
			self.gen_pac_hole(hole)

		for line in package['lines']:
			self.gen_pac_line(line)

		if(0):

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

		self.package['lines'].append(
			{
				'layer': layer,
				'width': width,
				'vertices': vertices
			})

	def gen_pac_pad(self, pad): # type, angle, size, pos, number

		top_layer = self.svg.find('.//g[@id="Top"]')

		# TODO: Types and angle

		el = ET.SubElement(top_layer, 'rect')
		el.set('style', 'fill:#ff0000;fill-opacity:1;stroke:none;stroke-width:10;stroke-linecap:square;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1')
		el.set('id', 'pin_{}'.format(pad['number']))
		el.set('width', '{}'.format(pad['size'][0]*self.mmpx))
		el.set('height', '{}'.format(pad['size'][1]*self.mmpx))
		el.set('x', '{}'.format((pad['pos'][0] - pad['size'][0]/2)*self.mmpx))
		el.set('y', '{}'.format((pad['pos'][1] - pad['size'][1]/2)*self.mmpx))


	def gen_pac_hole(self, hole):

		top_layer = self.svg.find('.//g[@id="Holes"]')

		circle = ET.SubElement(top_layer, 'circle')

		circle.set('style', 'fill:#eeee00;fill-opacity:1;stroke:none;stroke-width:0.0;stroke-linecap:square;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"')

		circle.set('cx', '{}'.format(hole['pos'][0]*self.mmpx))
		circle.set('cy', '{}'.format(hole['pos'][1]*self.mmpx))
		circle.set('r', '{}'.format(hole['d']/2*self.mmpx))


	def gen_pac_line(self, line):

		layer = self.svg.find('.//g[@id="{}"]'.format(line['layer']))

		if(line['layer'] == 'Courtyard'):
			color = '#e63a81'
		elif(line['layer'] == 'Silk'):
			color = '#111111'
		else:
			color = '#000000'

		el = ET.SubElement(layer, 'path')
		el.set('style', 'fill:none;fill-rule:evenodd;stroke:{color};stroke-width:{}mm;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;stroke-miterlimit:4;stroke-dasharray:none'.format(line['width'], color=color))

		pathdata = ''
		first = True

		for (x,y) in line['vertices']:
			if(first):
				pathdata += 'M ' + '{},{}'.format(x*self.mmpx,y*self.mmpx)
				first = False
			elif(x == 'end'):
				pathdata += ' z'
			else:
				pathdata += ' L ' + '{},{}'.format(x*self.mmpx,y*self.mmpx)

		el.set('d', pathdata)


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

		circle.set('cx', '{}'.format(pos[0]*self.mmpx))
		circle.set('cy', '{}'.format(pos[1]*self.mmpx))
		circle.set('r', '{}'.format(diameter/2*self.mmpx))


if(__name__ == '__main__'):

	target = get_target()

	target.output('test.svg')
