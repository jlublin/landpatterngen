def draw(target):

	target.add_sym_pin('A', (-1, 0))
	target.add_sym_pin('K', (2, 0))
	target.add_sym_line('Symbols', 1, [(-1,0), (0,0)])
	target.add_sym_line('Symbols', 1, [(0,0.5), (0,-0.5), (1,0), ('end',0)])
	target.add_sym_line('Symbols', 1, [(1.25,0.5), (1,0.5), (1,-0.5), (0.75, -0.5)])
	target.add_sym_line('Symbols', 1, [(1,0), (2,0)])

	# Eagle specific, needs an add name/value function
	target.add_sym_text('Name', '>NAME', (-1,1))
	target.add_sym_text('Value', '>VALUE', (-1,-1))
