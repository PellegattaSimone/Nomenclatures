from periodictable import InputError
from compounds import *

class Hydroxide:
	def __init__(self, metal, oxygen, hydrogen):
		self.metal = metal
		self.oxygen = oxygen
		self.hydrogen = hydrogen

	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "metal")

		if nomenclature == Nomenclature.TRADITIONAL:
			pos = Compound.oxPosition(self.metal, ox).value	# 0, 1, 2, 3, 4

			return "idrossido " + ("di " + self.metal.name if pos == Traditional.UNIQUE.value else ("ipo" if pos == Traditional.IPO.value else ("per" if pos == Traditional.PER.value else '')) + self.metal.prefix + ("oso" if pos <= Traditional.OSO.value else "ico"))

		elif nomenclature == Nomenclature.IUPAC:
			return Compound.getPrefixNo1(self.oxygen.quantity) + "idrossido di " + Compound.getPrefixNo1(self.metal.quantity) + self.metal.name

		elif nomenclature == Nomenclature.STOCK:
			return "idrossido di " + self.metal.name + Compound.getRomanParenthesis(ox)

		else:
			raise InputError("Nomenclatura non valida")

class Oxiacid:
	def __init__(self, hydrogen, nonmetal, oxygen):
		self.hydrogen = hydrogen
		self.nonmetal = nonmetal
		self.oxygen = oxygen

	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "nonmetal")

		if nomenclature == Nomenclature.TRADITIONAL:
			pos = Compound.oxPosition(self.nonmetal, ox).value	# 0, 1, 2, 3, 4

			return "acido " + ("ipo" if pos == Traditional.IPO.value else ("per" if pos == Traditional.PER.value else '')) + self.nonmetal.prefix + ("oso" if pos <= Traditional.OSO.value else "ico")	# non metals do not have unique oxidation numbers # temp: meta, piro, orto

		elif nomenclature == Nomenclature.IUPAC:
			return "acido " + Compound.getPrefixNo1(self.oxygen.quantity) + "osso" + self.nonmetal.prefix + "ico" + Compound.getRomanParenthesis(ox)

		elif nomenclature == Nomenclature.STOCK:
			raise InputError("Nomenclatura stock non esistente per questo composto")

		else:
			raise InputError("Nomenclatura non valida")

class TernarySalt:
	def __init__(self, metal, nonmetal, oxygen):
		self.metal = metal
		self.nonmetal = nonmetal
		self.oxygen = oxygen

	def mount(self, nomenclature = Nomenclature.IUPAC):
		oxNonMet = Compound.parseOx(self, "nonmetal")
		oxMet = Compound.parseOx(self, "metal")

		if nomenclature == Nomenclature.TRADITIONAL:
			posNonMet = Compound.oxPosition(self.nonmetal, oxNonMet).value	# 0, 1, 2, 3, 4
			posMet = Compound.oxPosition(self.metal, oxMet).value	# 0, 1, 2, 3, 4

			return "ipo" if posNonMet == Traditional.IPO.value else ("per" if posNonMet == Traditional.PER.value else '') + self.nonmetal.prefix2 + ("ito" if posNonMet <= Traditional.OSO.value else "ato") + ' ' + ("di " + self.metal.name if posMet == Traditional.UNIQUE.value else ("ipo" if posMet == Traditional.IPO.value else ("per" if posMet == Traditional.PER.value else '')) + self.metal.prefix + ("oso" if posMet <= Traditional.OSO.value else "ico"))	# temp: remove parenthesis if redundant

		elif nomenclature == Nomenclature.IUPAC:
			return Compound.getPrefixNo1(self.oxygen.quantity) + "osso" + self.nonmetal.prefix2 + 'ato' + Compound.getRomanParenthesis(oxNonMet) + ' di ' + self.metal.name + Compound.getRomanParenthesis(oxMet)

		elif nomenclature == Nomenclature.STOCK:
			raise InputError("Nomenclatura stock non esistente per questo composto")

		else:
			raise InputError("Nomenclatura non valida")