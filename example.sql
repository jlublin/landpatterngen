CREATE TABLE 'library'
(
	version,
	name,
	description
);

CREATE TABLE 'devices'
(
	id INTEGER PRIMARY KEY,
	name,
	prefix,
	value, -- Bool: Has value
	description
);

CREATE TABLE 'dev_symbols'
(
	device_id,
	name,
	symbol
);

CREATE TABLE 'dev_packages'
(
	id INTEGER PRIMARY KEY,
	device_id,
	name,
	variant
);

CREATE TABLE 'dev_pac_attributes'
(
	dev_pac_id,
	attribute
);

CREATE TABLE 'dev_pac_connections'
(
	dev_pac_id,
	name,
	pin
);

CREATE TABLE 'symbols'
(
	id INTEGER PRIMARY KEY,
	name,
	type
);

CREATE TABLE 'packages'
(
	id INTEGER PRIMARY KEY,
	name,
	type
);

CREATE TABLE 'pac_deleted_pins' (package_id, pin);
CREATE TABLE 'pac_holes' (package_id, d, x, y);
CREATE TABLE 'pac_mount_pads' (package_id, w, h, x, y);

-- Also has deleted pins, holes, mount pads
CREATE TABLE 'pac_dual_row'
(
	package_id,
	E1_l, E1_h,
	D_l, D_h,
	e,
	E_l, E_h,
	S_l, S_h,
	L_l, L_h,
	b_l, b_h,
	npin,
	mark,
	lead_type,
	C, G, X, Y, Z,
	pin_order,
	row_offset1, row_offset2
);

CREATE TABLE 'pac_sot23'
(
	package_id,
	E1_l, E1_h,
	D_l, D_h,
	e,
	E_l, E_h,
	S_l, S_h,
	L_l, L_h,
	b_l, b_h,
	npin
);

INSERT INTO 'library' VALUES (0.2, 'Example', 'Example library');

INSERT INTO 'packages' VALUES (NULL, 'SOT23-3', 'sot23');
INSERT INTO 'pac_sot23' VALUES
(
	1, -- package_id
	1.20, 1.40,
	2.80, 3.00,
	0.95,
	2.30, 2.60,
	1.10, 1.47,
	0.45, 0.60,
	0.36, 0.46,
	3
);

INSERT INTO 'packages' VALUES (NULL, 'SOT23-6', 'sot23');
INSERT INTO 'pac_sot23' VALUES
(
	2, -- package_id
	1.20, 1.40,
	2.80, 3.00,
	0.95,
	2.30, 2.60,
	1.10, 1.47,
	0.45, 0.60,
	0.36, 0.46,
	6
);

INSERT INTO 'packages' VALUES (NULL, 'TE-M.2', 'dual_row');
INSERT INTO 'pac_dual_row' VALUES
(
	3, -- package_id
	8.0, 8.0,
	21.8, 22.0,
	0.5,
	2.30, 2.60,
	1.10, 1.47,
	0.45, 0.60,
	0.36, 0.46,
	76, '-',
	'Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)',
	NULL, 6.0, 0.3, 1.55, 9.1,
	1,
	-0.25, 0
);
INSERT INTO 'pac_deleted_pins' VALUES (3, 38);
INSERT INTO 'pac_holes' VALUES (3, 1.1, -1.5, 10);
INSERT INTO 'pac_holes' VALUES (3, 1.6, -1.5, -10);

INSERT INTO 'symbols' VALUES (NULL, 'diode', 'diode');

INSERT INTO 'devices' VALUES (NULL, 'BAT54', 'D', 0, 'BAT54 diode');
INSERT INTO 'dev_symbols' VALUES(1, 'A', 'diode');
INSERT INTO 'dev_packages' VALUES(NULL, 1, 'SOT23-3', '');
INSERT INTO 'dev_pac_connections' VALUES(1, 'A.A', 1);
INSERT INTO 'dev_pac_connections' VALUES(1, 'A.K', 3);
INSERT INTO 'dev_packages' VALUES(NULL, 1, 'SOT23-6', 'nonexistant');
INSERT INTO 'dev_pac_connections' VALUES(2, 'A.A', 1);
INSERT INTO 'dev_pac_connections' VALUES(2, 'A.K', 3);
