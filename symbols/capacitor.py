def draw(target):

	target.add_sym_pin('1', (-1, 0))
	target.add_sym_pin('2', (2, 0))
	target.add_sym_line('Symbols', 1, [(0,1), (0,0.2)])
	target.add_sym_line('Symbols', 1, [(0,-0.2), (0,-1)])
	target.add_sym_line('Symbols', 2, [(-0.8,0.2), (0.8,0.2)])
	target.add_sym_line('Symbols', 2, [(-0.8,-0.2), (0.8,-0.2)])

	# Eagle specific, needs an add name/value function
	target.add_sym_text('Name', '>NAME', (1,1))
	target.add_sym_text('Value', '>VALUE', (1,-1))
