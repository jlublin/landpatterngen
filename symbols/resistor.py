def draw(target):

	target.add_sym_pin('1', (-1, 0))
	target.add_sym_pin('2', (2, 0))
	target.add_sym_line('Symbols', 1, [(-2,0), (-1,0)])
	target.add_sym_line('Symbols', 1, [(-1,0.35), (1,0.35), (1,-0.35), (-1,-0.35), ('end',0)])
	target.add_sym_line('Symbols', 1, [(1,0), (2,0)])

	# Eagle specific, needs an add name/value function
	target.add_sym_text('Name', '>NAME', (-1,1))
	target.add_sym_text('Value', '>VALUE', (-1,-1))
