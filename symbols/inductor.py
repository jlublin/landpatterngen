def draw(target):

	target.add_sym_pin('1', (-3, 0))
	target.add_sym_pin('2', (3, 0))
	target.add_sym_line('Symbols', 1, [(-3,0), (-2,0)])
	target.add_sym_line('Symbols', 1, [(2,0), (3,0)])
	target.add_sym_arc('Symbols', 1, (-2,0), (-1.5,0), (-1,0))
	target.add_sym_arc('Symbols', 1, (-1,0), (-0.5,0), (0,0))
	target.add_sym_arc('Symbols', 1, (0,0), (0.5,0), (1,0))
	target.add_sym_arc('Symbols', 1, (1,0), (1.5,0), (2,0))

	# Eagle specific, needs an add name/value function
	target.add_sym_text('Name', '>NAME', (-2,1))
	target.add_sym_text('Value', '>VALUE', (-2,-1))
