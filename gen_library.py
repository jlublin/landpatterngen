#!/usr/bin/env python3
import re
import importlib
import sqlite3
import sys

def parse_tollens(part):

	keys = list(part.keys());
	for key in keys:
		if(key[-2:] == '_l' and
		   key[:-2] + '_h' in part):
			part[key[:-2]] = TolLen(float(part[key[:-2] + '_l']), float(part[key[:-2] + '_h']))
			part.pop(key[:-2] + '_l');
			part.pop(key[:-2] + '_h');


if(__name__ == '__main__'):
	import sys
	import target_eagle
	from tollen import TolLen
	target = target_eagle.get_target()

	if(len(sys.argv) < 2):
		print('Usage: {} <library.lbr>'.format(sys.argv[0]), file=sys.stderr)

	fout = open(1, 'w')

	process = {	'F': TolLen(0, 0.05, 1),
				'P': TolLen(0, 0.05, 1) }

	conn = sqlite3.connect(sys.argv[1])
	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	# Print library

	c.execute('SELECT * FROM library')
	print('Library version: {}\nName: {}\n{}'.format(*c.fetchone()), file=sys.stderr)

	c.execute('SELECT * FROM symbols')
	for sym in c.fetchall():

		target.add_symbol(sym['name'])
		sym = importlib.import_module('symbols.{}'.format(sym['type']))
		sym.draw(target)

	c.execute('SELECT * FROM packages')
	for pac in c.fetchall():
		package = dict(pac)

		if(package['type'] in ['dual_row', 'sot23']):
			c.execute('SELECT * FROM pac_{} WHERE package_id = :id'.format(package['type']), {'id': pac[0]})
			package.update(dict(c.fetchone()))

		else:
			print('Unknown type {}'.format(package['type']), file=sys.stderr)
			sys.exit()

		c.execute('SELECT * FROM pac_deleted_pins WHERE package_id = :id', {'id': pac[0]})
		package['deleted_pins'] = [x['pin'] for x in c.fetchall()]

		c.execute('SELECT * FROM pac_holes WHERE package_id = :id', {'id': pac[0]})
		package['holes'] = [dict(x) for x in c.fetchall()]

		c.execute('SELECT * FROM pac_mount_pads WHERE package_id = :id', {'id': pac[0]})
		package['mount_pads'] = [dict(x) for x in c.fetchall()]

		parse_tollens(package)
		target.add_package(package['name'])
		mod = importlib.import_module('packages.{}'.format(package['type']))
		pac = mod.get_package(package, 'IPC7351-B', process)
		pac.gen(target)


	c.execute('SELECT * FROM devices')
	for dev in c.fetchall():
		device = dict(dev)
		device.update({'symbols': [], 'packages': []})

		c.execute('SELECT * FROM dev_symbols WHERE device_id = :id', {'id': dev[0]})
		for sym in [dict(x) for x in c.fetchall()]:
			device['symbols'].append(sym)

		for pac in c.execute('SELECT * FROM dev_packages WHERE device_id = :id', {'id': dev[0]}):
			package = dict(pac)

			c.execute('SELECT * FROM dev_pac_attributes WHERE dev_pac_id = :id', {'id': pac[0]})
			package['attributes'] = [dict(x) for x in c.fetchall()]

			c.execute('SELECT * FROM dev_pac_connections WHERE dev_pac_id = :id', {'id': pac[0]})
			package['connections'] = [dict(x) for x in c.fetchall()]

			device['packages'].append(package)

		target.add_device(device)

	target.output(fout)
	fout.close()
