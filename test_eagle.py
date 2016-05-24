import target_eagle
import importlib
import symbols
from tollen import TolLen

target = target_eagle.get_target()

## Add some symbols

target.add_symbol('Diode')

sym = importlib.import_module('symbols.diode')
sym.draw(target)

target.add_symbol('LED')

sym = importlib.import_module('symbols.led')
sym.draw(target)

target.add_symbol('Zener')

sym = importlib.import_module('symbols.zener')
sym.draw(target)

target.add_symbol('Varicap')

sym = importlib.import_module('symbols.varicap')
sym.draw(target)

target.add_symbol('Resistor')

sym = importlib.import_module('symbols.resistor')
sym.draw(target)

target.add_symbol('Capacitor')

sym = importlib.import_module('symbols.capacitor')
sym.draw(target)

target.add_symbol('Inductor')

sym = importlib.import_module('symbols.inductor')
sym.draw(target)

target.add_symbol('NPN')

sym = importlib.import_module('symbols.npn')
sym.draw(target)

target.add_symbol('PNP')

sym = importlib.import_module('symbols.pnp')
sym.draw(target)

## Manually add a package

target.add_package('DIOM2012')

target.add_pac_pad(0, 0, (1, 1), (-1, 0), 0)
target.add_pac_pad(0, 0, (1, 1), (1, 0), 1)
target.add_pac_line('Courtyard', 0.1, [(-2,-1), (-2,1), (2,1), (2,-1), ('end', 0)])
target.add_pac_circle('Silk', 0.1, (-1, 0.75))
target.add_pac_line('Silk', 0.1, [(-0.5,-0.5), (0.5,-0.5)])
target.add_pac_line('Silk', 0.1, [(-0.5,0.5), (0.5,0.5)])
target.add_pac_rectangle('Silk', (-0.5,-0.5), (0,0.5))
target.add_pac_text('Name', '>NAME', (-0.5,0))

## Add some packages via parameters

soic8 = {	'E1': TolLen(3.9, 4.4),
			'D': TolLen(4.9, 5.2),
			'e': 1.27,
			'E': TolLen(5.90, 6.10),
			'L': TolLen(0.40, 1.27),
			'b': TolLen(0.31, 0.51),
			'npin': 8,
			'deleted': None,
			'mark': 'circle' }

diode = {	'E1': TolLen(1.85, 2.15),
			'D': TolLen(1.10, 1.40),
			'e': 0,
			'E': TolLen(1.85, 2.15),
			'S': TolLen(0.55, 1.32),
			'L': TolLen(0.15, 0.65),
			'b': TolLen(1.10, 1.40),
			'npin': 2,
			'deleted': None,
			'mark': 'diode' }

sot23_3 = {	'E1': TolLen(1.20, 1.40),
			'D': TolLen(2.80, 3.00),
			'e': 0.95,
			'E': TolLen(2.30, 2.60),
			'S': TolLen(1.10, 1.47),
			'L': TolLen(0.45, 0.60),
			'b': TolLen(0.36, 0.46),
			'npin': 3}

quad = {	'E1': TolLen(3.80, 3.20),
			'D1': TolLen(2.80, 3.20),
			'e': 0.95,
			'E': TolLen(4.60, 5.80),
			'D': TolLen(3.60, 3.80),
			'L': TolLen(0.45, 0.60),
			'b': TolLen(0.36, 0.46),
			'npin1': 2,
			'npin2': 3,
			'deleted': None,
			'mark': 'circle' }

bga1 = {	'E': TolLen(5.60, 5.80),
			'D': TolLen(5.60, 5.80),
			'd': 0.95,
			'e': 0.95,
			'b': TolLen(0.36, 0.44),
			'npin1': 5,
			'npin2': 5,
			'deleted': None,
			'mark': 'circle' }

process = {	'F': TolLen(0, 0.05, 1),
			'P': TolLen(0, 0.05, 1) }

from ipc7351 import IPC7351

dr = importlib.import_module('packages.dual_row')

target.add_package('SOP127P6-8')
soic8 = dr.DualRow(soic8, IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)']['B'], process)
soic8.gen(target)

target.add_package('DIOM2012-C')
diode = dr.DualRow(diode, IPC7351['Rectangular or Square-End Components (Capacitors and Resistors) (>= 1608 (0603))']['C'], process)
diode.gen(target)

target.add_package('SOT23-3')

mod = importlib.import_module('packages.sot23')
pac = mod.get_package(sot23_3, 'IPC7351-C', process)
pac.gen(target)

target.add_package('SOT23-5')
sot23_3['npin'] = 5

mod = importlib.import_module('packages.sot23')
pac = mod.get_package(sot23_3, 'IPC7351-C', process)
pac.gen(target)

target.add_package('SOT23-6')
sot23_3['npin'] = 6

mod = importlib.import_module('packages.sot23')
pac = mod.get_package(sot23_3, 'IPC7351-C', process)
pac.gen(target)

target.add_package('SOT23-8')
sot23_3['npin'] = 8
sot23_3['D'] += TolLen(0.95,0.95)

mod = importlib.import_module('packages.sot23')
pac = mod.get_package(sot23_3, 'IPC7351-C', process)
pac.gen(target)

qr = importlib.import_module('packages.quad_row')
target.add_package('QUAD-8')
pac = qr.QuadRow(quad, IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)']['B'], process)
pac.gen(target)

bga = importlib.import_module('packages.bga')
target.add_package('BGA')
pac = bga.BGA(bga1, IPC7351['Ball Grid Array']['B'], process)
pac.gen(target)

target.add_device('BAT54', 'D', False, 'BAT54 diode')
target.add_dev_symbol('diode')
target.add_dev_package('SOT23-3', '', [], [['A.A', 1], ['A.K', 3]])

## Output result

f = open('test_eagle.scr', 'w')
target.output(f)
f.close()
