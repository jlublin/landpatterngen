#!/usr/bin/env python3
import re
import importlib

def parse_package(row):
	tokens = get_tokens(row)
	tree = get_tree(tokens)[0]
	return tree

def parse_symbol(row):
	tokens = get_tokens(row)
	tree = get_tree(tokens)[0]
	return tree

def parse_device(row):
	tokens = get_tokens(row)
	tree = get_tree(tokens)[0]
	return tree

def get_tokens(s):

	# Skip whitespaces
	s = s.strip()

	if(len(s) == 0):
		return []

	# Match 'string'
	m1 = '\'([^\']*)\''
	if(re.match(m1, s)):
		s2 = re.split(m1, s, maxsplit=1)
		return [s2[1]] + get_tokens(s2[2])

	# Match (
	m2 = '(\()'
	if(re.match(m2, s)):
		s2 = re.split(m2, s, maxsplit=1)
		return [s2[1]] + get_tokens(s2[2])

	# Match )
	m3 = '(\))'
	if(re.match(m3, s)):
		s2 = re.split(m3, s, maxsplit=1)
		return [s2[1]] + get_tokens(s2[2])

	# String token without ''
	m4 = '([^ \(\)]*)'
	s2 = re.split(m4, s, maxsplit=1)
	return [s2[1]] + get_tokens(s2[2])

def get_tree(tokens):

	if(tokens == []):
		return [], 0

	tree = []
	i = 0

	while(i < len(tokens)):
		t = tokens[i]

		if(t == '('):
			l, j = get_tree(tokens[(i+1):])
			tree.append(l)
			i += j + 2
		elif(t == ')'):
			return tree, i
		else:
			tree.append(tokens[i])
			i += 1

	return tree, i

if(__name__ == '__main__'):
	import sys
	import target_eagle
	from tollen import TolLen
	target = target_eagle.get_target()

	if(len(sys.argv) < 2):
		print('Usage: {} <in.lbr>'.format(sys.argv[0]))

	f = open(sys.argv[1])
	fout = open(1, 'w')

	current = None

	packages = []
	symbols = []
	devices = []

	process = {	'F': TolLen(0, 0.05, 1),
				'P': TolLen(0, 0.05, 1) }

	for row in f:

		if(row.startswith('# Packages')):
			current = 'Packages'
		elif(row.startswith('# Symbols')):
			current = 'Symbols'
		elif(row.startswith('# Devices')):
			current = 'Devices'

		elif(current == 'Packages'):
			packages.append(parse_package(row))
		elif(current == 'Symbols'):
			symbols.append(parse_symbol(row))
		elif(current == 'Devices'):
			devices.append(parse_device(row))

	for pac in packages:
		if(pac == []):
			continue

		target.add_package(pac[0])
		mod = importlib.import_module('packages.{}'.format(pac[1]))
		pac = mod.get_package(pac[2:], 'IPC7351-B', process)
		pac.gen(target)

	for sym in symbols:
		if(sym == []):
			continue

		target.add_symbol(sym[0])
		sym = importlib.import_module('symbols.{}'.format(sym[1]))
		sym.draw(target)

	for dev in devices:
		if(dev == []):
			continue

		target.add_device(dev[0], dev[1], dev[2], dev[3])

		for sym in dev[4]:
			target.add_dev_symbol(sym)

		for pac in dev[5:]:
			target.add_dev_package(pac[0], *pac[1:])

	target.output(fout)
	fout.close()
