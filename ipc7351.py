## IPC-7351 packages:
# BGA127P BGA150P BGA100P BGA80P BGA75P BGA65P BGA50P SBGA127P
# CAPCA CAPCP CAPC CAPCWR CAPM CAPMP CAPAE
# CFP127P
# CGA
# DIOM DIOMELF
# INDC INDCA INDM INDP
# PLCC PLCCR PLCCS PLCCRS
# PQFPS PQFPC
# BQFPS BQFPC
# QFP100P QFP80P QFP65P
# SQFP50P SQFP40P SQFP30P
# TQFP80P TQFP65P TQFP50P TQFP40P TQFP30P
# CQFP127P CQFP80P CQFP63P
# QFN80P QFN65P QFN50P QFN40P
# LCC LCCS
# QBCC
# RESC RESCA RESM RESMELF
# SOJ127P SOJ65P SOIC127P
# SOP127P SOP100P SOP80P SOP65P SOP63
# SSOP50P SSOP40P SSOP30P
# TSOP127P TSOP100P TSOP80P TSOP65P
# TSSOP55P TSSOP50P TSSOP40P TSSOP30P
# VSOP762P
# SOD
# SON
# SOT89 SOT143 SOT343 SOT143R SOT343R SOT SOT65P SOT95P
# TO

IPC7351 = {}

IPC7351['Flat Ribbon L and Gull-Wing Leads (> 0.625mm pitch)'] = {
	'A':
		{
			'J_T': 0.55,
			'J_H': 0.45,
			'J_S': 0.05,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.35,
			'J_H': 0.35,
			'J_S': 0.03,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.15,
			'J_H': 0.25,
			'J_S': 0.01,
			'CE': 0.1
		}
}

IPC7351['Flat Ribbon L and Gull-Wing Leads (<= 0.625mm pitch)'] = {
	'A':
		{
			'J_T': 0.55,
			'J_H': 0.45,
			'J_S': 0.01,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.35,
			'J_H': 0.35,
			'J_S': -0.02,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.15,
			'J_H': 0.25,
			'J_S': -0.04,
			'CE': 0.1
		}
}

IPC7351['J Leads'] = {
	'A':
		{
			'J_T': 0.55,
			'J_H': -0.10,
			'J_S': 0.05,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.35,
			'J_H': -0.20,
			'J_S': 0.03,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.15,
			'J_H': -0.30,
			'J_S': 0.01,
			'CE': 0.1
		}
}

IPC7351['Rectangular or Square-End Components (Capacitors and Resistors) (>= 1608 (0603))'] = {
	'A':
		{
			'J_T': 0.55,
			'J_H': -0.05,
			'J_S': 0.05,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.35,
			'J_H': -0.05,
			'J_S': 0.00,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.15,
			'J_H': -0.05,
			'J_S': -0.05,
			'CE': 0.1
		}
}

IPC7351['Rectangular or Square-End Components (Capacitors and Resistors) (< 1608 (0603))'] = {
	'A':
		{
			'J_T': 0.20,
			'J_H': -0.05,
			'J_S': 0.05,
			'CE': 0.2
		},
	'B':
		{
			'J_T': 0.10,
			'J_H': -0.05,
			'J_S': 0.00,
			'CE': 0.15
		},
	'C':
		{
			'J_T': 0.00,
			'J_H': -0.05,
			'J_S': 0.00,
			'CE': 0.1
		}
}

IPC7351['Cylindrical End Cap Terinations (MELF)'] = {
	'A':
		{
			'J_T': 0.6,
			'J_H': 0.2,
			'J_S': 0.1,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.4,
			'J_H': 0.1,
			'J_S': 0.05,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.2,
			'J_H': 0.02,
			'J_S': 0.01,
			'CE': 0.1
		}
}

IPC7351['Bottom Only Terminations'] = {
	'A':
		{
			'J_T': 0.55,
			'J_H': 0.45,
			'J_S': 0.08,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.35,
			'J_H': 0.35,
			'J_S': 0.03,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.15,
			'J_H': 0.25,
			'J_S': 0.01,
			'CE': 0.1
		}
}

IPC7351['Leadless Chip Carrier with Castellated Terminations'] = {
	'A':
		{
			'J_T': 0.65,
			'J_H': 0.25,
			'J_S': 0.05,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.55,
			'J_H': 0.15,
			'J_S': -0.05,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.45,
			'J_H': 0.05,
			'J_S': -0.15,
			'CE': 0.1
		}
}

IPC7351['Butt Joints'] = {
	'A':
		{
			'J_T': 1.0,
			'J_H': 1.0,
			'J_S': 0.3,
			'CE': 1.5
		},
	'B':
		{
			'J_T': 0.8,
			'J_H': 0.8,
			'J_S': 0.2,
			'CE': 0.8
		},
	'C':
		{
			'J_T': 0.6,
			'J_H': 0.6,
			'J_S': 0.1,
			'CE': 0.2
		}
}

IPC7351['Inward Flat Ribbon L and Gull-Wing Leads (Tantalum Capacitors)'] = {
	'A':
		{
			'J_T': 0.25,
			'J_H': 0.8,
			'J_S': 0.01,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.15,
			'J_H': 0.5,
			'J_S': -0.05,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.07,
			'J_H': 0.2,
			'J_S': -0.10,
			'CE': 0.1
		}
}

IPC7351['Flat Lug Leads'] = {
	'A':
		{
			'J_T': 0.55,
			'J_H': 0.45,
			'J_S': 0.05,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.35,
			'J_H': 0.35,
			'J_S': 0.01,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.15,
			'J_H': 0.25,
			'J_S': -0.04,
			'CE': 0.1
		}
}

IPC7351['Flat, No Lead'] = {
	'A':
		{
			'J_T': 0.40,
			'J_H': 0.00,
			'J_S': -0.04,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.30,
			'J_H': 0.00,
			'J_S': -0.04,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.20,
			'J_H': 0.00,
			'J_S': -0.04,
			'CE': 0.1
		}
}

IPC7351['Small Outline (SO), No-Lead'] = {
	'A':
		{
			'J_T': 0.40,
			'J_H': 0.00,
			'J_S': -0.04,
			'CE': 0.5
		},
	'B':
		{
			'J_T': 0.30,
			'J_H': 0.00,
			'J_S': -0.04,
			'CE': 0.25
		},
	'C':
		{
			'J_T': 0.20,
			'J_H': 0.00,
			'J_S': -0.04,
			'CE': 0.1
		}
}
