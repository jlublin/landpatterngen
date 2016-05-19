def draw(target):

	target.add_sym_pin('B', (-1, 0))
	target.add_sym_pin('E', (1, -2))
	target.add_sym_pin('C', (1, 2))
	target.add_sym_ring('Symbols', 1, 1, (0.5, 0))
	target.add_sym_line('Symbols', 1, [(1,2), (1,0.9), (0,0.3), (0,-0.3), (1,-0.9),(1,-2)])
	target.add_sym_line('Symbols', 1, [(0,0.6), (0,-0.6)])
	target.add_sym_line('Symbols', 1, [(-1,0), (0,0)])
	target.add_sym_line('Symbols', 1, [(0.9,-0.8), (0.7,-0.5), (0.5,-0.8), ('end',0)])

	# Eagle specific, needs an add name/value function
	target.add_sym_text('Name', '>NAME', (2,1))
	target.add_sym_text('Value', '>VALUE', (2,-1))
