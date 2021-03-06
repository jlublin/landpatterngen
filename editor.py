#!/usr/bin/env python3

import sys, signal
import sqlite3
import re
import importlib
import tempfile
from tollen import TolLen

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidgetItem, QLabel, QLineEdit, QGraphicsScene, QMenu, QAction
from PyQt5.QtCore import QObject, QCommandLineParser, Qt, QUrl
from PyQt5.QtSvg import QSvgWidget, QGraphicsSvgItem
from PyQt5 import uic, QtCore

class Editor:

	def open_file(self, file=None):

		file = file or self.fw.selectedFiles()[0]

		conn = sqlite3.connect(file)
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		# Read library information
		c.execute('SELECT * FROM library')
		lbr = c.fetchone()
		print('Library version: {version}\nName: {name}\n{description}'.format(**lbr), file=sys.stderr)

		self.library = dict(lbr)

		if(lbr['version'] != 0.2):
			print('Unknown library version {}'.format(lbr['version']))
			c.close()
			conn.close()

		# Read devices information
		c.execute('SELECT * FROM devices')
		devices = c.fetchall()
		self.devices = [dict(x) for x in devices]

		self.update_devices_labels()

		i = 0
		for dev in devices:
			# Read devices information
			c.execute('SELECT * FROM dev_packages WHERE device_id=:dev_id', {'dev_id': dev['id']})
			packages = c.fetchall()
			self.devices[i]['dev_packages'] = [dict(x) for x in packages]

			self.set_device(dev, i)

			i += 1

		# Read packages information
		c.execute('SELECT * FROM packages')
		packages = c.fetchall()

		self.packages = [dict(x) for x in packages]

		self.wnd.packages.setRowCount(len(packages))

		package_names = [x['name'] for x in packages]
		self.wnd.packages.setVerticalHeaderLabels(package_names)

		i = 0
		for pac in packages:

			# TODO, why doesn't a dictionary work here?
			d = 'pac_' + pac['type']
			c.execute('SELECT * FROM {} WHERE package_id=:id'.format(d), {'id': pac['id']})
			values = c.fetchone()

			self.packages[i]['values'] = dict(values)

			# Add deleted pins
			c.execute('SELECT pin FROM pac_deleted_pins WHERE package_id=:id', {'id': pac['id']})
			deleted_pins = [x['pin'] for x in c.fetchall()]
			if(deleted_pins):
				self.packages[i]['values']['deleted_pins'] = deleted_pins

			# Add holes
			c.execute('SELECT d,x,y FROM pac_holes WHERE package_id=:id', {'id': pac['id']})
			holes = [dict(x) for x in c.fetchall()]
			if(holes):
				self.packages[i]['values']['holes'] = holes

			# Add mount pads
			c.execute('SELECT w,h,x,y FROM pac_mount_pads WHERE package_id=:id', {'id': pac['id']})
			mount_pads = [dict(x) for x in c.fetchall()]

			if(mount_pads):
				self.packages[i]['values']['mount_pads'] = mount_pads

			self.set_package(pac, i)

			i += 1

		# Show packages tab
		self.wnd.tabWidget_2.setCurrentIndex(0)

		# Add context menus for adding/removing entries
		self.wnd.devices.setContextMenuPolicy(Qt.CustomContextMenu)
		self.wnd.devices.customContextMenuRequested.connect(self.on_device_context)

		self.wnd.packages.setContextMenuPolicy(Qt.CustomContextMenu)
		self.wnd.packages.customContextMenuRequested.connect(self.on_packages_context)

		# Add connections for editing data in tables
		self.wnd.devices.cellChanged.connect(self.update_device)
		self.wnd.packages.cellChanged.connect(self.update_package)

		c.close()
		conn.close()


	def on_device_context(self, pos):

		menu = QMenu('ctx menu', self.wnd)

		i = self.wnd.devices.currentRow()

		addb = QAction('Insert device before', self.wnd)
		adda = QAction('Insert device after', self.wnd)
		delete = QAction('Delete device', self.wnd)

		addb.triggered.connect(lambda: self.add_device(i))
		adda.triggered.connect(lambda: self.add_device(i+1))
		delete.triggered.connect(lambda: self.delete_device(i))

		menu.addAction(addb)
		menu.addAction(adda)
		menu.addAction(delete)

		menu.exec(self.wnd.devices.mapToGlobal(pos))


	def on_packages_context(self, pos):

		menu = QMenu('ctx menu', self.wnd)

		i = self.wnd.packages.currentRow()

		addb = QAction('Insert package before', self.wnd)
		adda = QAction('Insert package after', self.wnd)
		delete = QAction('Delete package', self.wnd)

		addb.triggered.connect(lambda: self.add_package(i))
		adda.triggered.connect(lambda: self.add_package(i+1))
		delete.triggered.connect(lambda: self.delete_package(i))

		menu.addAction(addb)
		menu.addAction(adda)
		menu.addAction(delete)

		menu.exec(self.wnd.packages.mapToGlobal(pos))


	def add_device(self, i):

		device = \
			{
				'name': '',
				'prefix': '',
				'value': 0,
				'description': '',
				'manufacturer': '',
				'datasheet': '',
				'dev_packages': []
			}

		self.devices.insert(i, device)
		self.wnd.devices.insertRow(i)
		self.set_device(device, i)


	def delete_device(self, i):

		self.devices.pop(i)
		self.wnd.devices.removeRow(i)


	def update_device(self, i, j):

		self.devices[i]['manufacturer'] = self.wnd.devices.item(i,1).text()
		self.devices[i]['description'] = self.wnd.devices.item(i,2).text()
		self.devices[i]['datasheet'] = self.wnd.devices.item(i,3).text()

		self.on_devices_select()


	def update_devices_labels(self):

		devices = self.devices
		self.wnd.devices.setRowCount(len(devices))

		device_names = [x['name'] for x in devices]
		self.wnd.devices.setVerticalHeaderLabels(device_names)


	def set_device(self, dev, i):

		packages = self.devices[i]['dev_packages']

		package_names = [x['name'] for x in packages]
		item = QTableWidgetItem(', '.join(package_names))
		item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

		self.wnd.devices.setItem(i, 0, item)
		self.wnd.devices.setItem(i, 1, QTableWidgetItem(dev['manufacturer']))
		self.wnd.devices.setItem(i, 2, QTableWidgetItem(dev['description']))
		self.wnd.devices.setItem(i, 3, QTableWidgetItem(dev['datasheet']))


	def add_package(self, i):

		package = \
			{
				'name': '',
				'type': '',
				'manufacturer': '',
				'datasheet': '',
				'values':
				{
					'pac_deleted_pins': [],
					'pac_holes': [],
					'pac_mount_pads': []
					# TODO, the rest depends on type
				}
			}

		self.packages.insert(i, package)
		self.wnd.packages.insertRow(i)
		self.set_package(package, i)


	def delete_package(self, i):

		self.packages.pop(i)
		self.wnd.packages.removeRow(i)


	def update_package(self, i, j):

		self.packages[i]['manufacturer'] = self.wnd.packages.item(i,1).text()
		self.packages[i]['datasheet'] = self.wnd.packages.item(i,2).text()

		self.on_packages_select()


	def set_package(self, pac, i):

		# Add to Qt table
		item = QTableWidgetItem(pac['type'])
		item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		self.wnd.packages.setItem(i, 0, item)

		self.wnd.packages.setItem(i, 1, QTableWidgetItem(pac['manufacturer']))
		self.wnd.packages.setItem(i, 2, QTableWidgetItem(pac['datasheet']))


	def on_open(self):
		self.fw = QFileDialog(filter='*.sqlite3')

		# The follow is a work-around to fileSelected emitting two signals
#		self.fw.fileSelected.connect(self.open_file)
		self.fw.accepted.connect(self.open_file)

		self.fw.show()


	def on_exit(self):
		self.app.exit()


	def on_packages_select(self):

		w = uic.loadUi('package.ui')
		self.package_ui = w

		i = self.wnd.packages.currentRow()
		package = self.packages[i]
		self.current_package = package

		# Add package types
		import packages
		for type in packages.__all__:
			w.types.addItem(type)

			if(type == package['type']):
				w.types.setCurrentIndex(w.types.count() - 1)

		w.types.currentTextChanged.connect(self.update_package_type)

		# Add package widget
		oldw = self.wnd.verticalLayout_2.itemAt(1)
		self.wnd.verticalLayout_2.removeItem(oldw)
		self.wnd.verticalLayout_2.addWidget(w)
		oldw.widget().setParent(None)

		# Add package values
		try:
			mod = importlib.import_module('packages.{}'.format(package['type']))
		except ImportError:
			return

		x = 0
		y = 0

		for d in mod.get_params():

			val = QLineEdit()
			w.grid_values.addWidget(QLabel(d[0]), y, x + 0)
			w.grid_values.addWidget(val, y, x + 1)

			val.textEdited.connect(lambda x, val=val, d=d: self.on_package_value_edited(d, val, x))

			if(d[1] == 't'):
				min = package['values'][d[0] + '_l']
				max = package['values'][d[0] + '_h']
				val.setText('{} - {}'.format(min, max))
				package['values'][d[0]] = TolLen(min, max)
			elif(d[1] == 'a'):
				pass
			else:
				v = package['values'][d[0]]
				val.setText('{}'.format(v))

			x += 2
			if(x > 3):
				x = 0
				y += 1

		# Add package svg
		w.vert34.removeWidget(w.package_info)
		w.package_info.setParent(None)
		w.package_info = QSvgWidget('packages/{}.svg'.format(package['type']))
		w.vert34.addWidget(w.package_info)

		self.update_package_view()


	def update_package_view(self):

		package = self.current_package

		try:
			mod = importlib.import_module('packages.{}'.format(package['type']))
		except ImportError:
			return

		# Draw package
#		f = tempfile.NamedTemporaryFile()
		f = open('tmp.svg', 'wb')
		import target_svg
		target = target_svg.get_target()
		target.add_package(package)

		process = {	'F': TolLen(0, 0.05, 1),
					'P': TolLen(0, 0.05, 1) }
		pac = mod.get_package(package['values'], 'IPC7351-B', process)
		pac.gen(target)

		target.output(f)
		f.flush()

		# Draw SVG output
		svg = QGraphicsSvgItem(f.name)
		scene = QGraphicsScene()
		scene.addItem(svg)

		self.package_ui.graphicsView.setScene(scene)

		f.close()


	def update_package_type(self, type):

		try:
			mod = importlib.import_module('packages.{}'.format(type))
		except ImportError:
			return

		self.current_package['type'] = type

		for d in mod.get_params():
			if(d[0] not in self.current_package['values']):
				if(d[1] == 't'):
					self.current_package['values'][d[0]] = TolLen(0,0)
				elif(d[1] == 'i'):
					self.current_package['values'][d[0]] = 0
				elif(d[1] == 'f'):
					self.current_package['values'][d[0]] = 0.0
				elif(d[1] == 'm'):
					self.current_package['values'][d[0]] = '-'
				elif(d[1] == 'a'):
					self.current_package['values'][d[0]] = []
				elif(d[1] == 'l'):
					self.current_package['values'][d[0]] = 'Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)'


	def on_package_value_edited(self, d, edit, text):

		import re

		match = False
		package = self.current_package

		if(d[1] == 't'):
			if(re.match('^\s*\d+(\.\d+)?\s*-\s*\d+(\.\d+)?\s*$', text)):
				match = True

				# Update value in package
				r = re.findall('([\d\.]+)', text)
				min = float(r[0])
				max = float(r[1])

				package['values'][d[0]] = TolLen(min, max)
				self.update_package_view()

		elif(d[1] == 'a'):
			if(re.match('^\s*\d*(\s+\d+)*\s*$', text)):
				match = True

		elif(d[1] == 'm'):
			if(re.match('-', text)):
				match = True

		elif(d[1] == 'f'):
			if(re.match('^\s*\d+(\.\d+)?\s*$', text)):
				match = True

				# Update value in package
				val = float(text)

				package['values'][d[0]] = val
				self.update_package_view()

		elif(d[1] == 'i'):
			if(re.match('^\s*\d+\s*$', text)):
				match = True

				# Update value in package
				val = int(text)

				package['values'][d[0]] = val
				self.update_package_view()

		if(match):
			edit.setStyleSheet('')
		else:
			edit.setStyleSheet('QLineEdit { background: rgb(255, 40, 40);}')



	def on_devices_select(self):

		w = uic.loadUi('device.ui')

		oldw = self.wnd.verticalLayout_2.itemAt(1)
		self.wnd.verticalLayout_2.removeItem(oldw)
		self.wnd.verticalLayout_2.addWidget(w)
		oldw.widget().setParent(None)

		i = self.wnd.devices.currentRow()

		if(i >= len(self.devices)):
			return # This can happen when removing entries

		w.listPackages.addItems([x['name'] for x in self.devices[i]['dev_packages']])

		w.name.setText(self.devices[i]['name'])
		w.description.setText(self.devices[i]['description'])

		datasheet = self.devices[i]['datasheet']
		w.datasheet.setOpenExternalLinks(True)

		datasheet = re.sub('"([a-z]*://[^"]*)"', '<a href="\\1">\\1</a>', datasheet)
		w.datasheet.setText(datasheet)


	def on_tab_select(self, i):
		if(i == 0):
			self.on_devices_select()
		elif(i == 1):
			self.on_packages_select()


	def on_device_data(self, w):
		print('New data:', w)


	def run(self):

		self.app = QApplication(sys.argv)

		parser = QCommandLineParser()
		parser.addPositionalArgument('lbr', 'Library to open')
		parser.process(self.app)
		args = parser.positionalArguments()

		self.wnd = uic.loadUi('editor_window.ui')

		self.wnd.actionOpen_DB.triggered.connect(self.on_open)
		self.wnd.actionExit.triggered.connect(self.on_exit)

		self.wnd.devices.itemEntered.connect(self.on_device_data)
		self.wnd.devices.itemSelectionChanged.connect(self.on_devices_select)

		self.wnd.packages.itemSelectionChanged.connect(self.on_packages_select)

		self.wnd.tabWidget_2.currentChanged.connect(self.on_tab_select)

		# Open library if sent as argument
		if(len(args) > 0):
			self.open_file(args[0])

		self.wnd.show()
		sys.exit(self.app.exec_())


if(__name__ == '__main__'):

	# Handle Ctrl-C as usual
	signal.signal(signal.SIGINT, signal.SIG_DFL)

	main = Editor()
	main.run()
