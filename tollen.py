import math

class TolLen:
	def __init__(self, a, b, type=0):

		if(type == 0):

			self.min = a
			self.max = b

			self.nom = (self.min + self.max) / 2
			self.tol = (self.max - self.min) / 2

		else:
			self.nom = a
			self.tol = b

			self.update()

	def update(self):

		self.min = self.nom - self.tol
		self.max = self.nom + self.tol

	def __add__(self, x):

		nom = self.nom + x.nom
		tol = math.sqrt(self.tol**2 + x.tol**2)

		return TolLen(nom, tol, 1)

	def __sub__(self, x):

		nom = self.nom - x.nom
		tol = math.sqrt(self.tol**2 + x.tol**2)

		return TolLen(nom, tol, 1)

	def __repr__(self):

		return '({}, {})'.format(self.min, self.max)
