from periodictable import InputError
from compounds import *
from abc import ABC, abstractmethod

class Oxide(ABC):	# abstract
	@abstractmethod
	def __init__(self, oxygen):
		self.oxygen = oxygen

	@staticmethod
	def _iupac(element, oxygen):
		return Compound.getPrefixNo1(oxygen.quantity) + "ossido di " + Compound.getPrefixNo1(element.quantity) + element.name	# omit 'mono'
	
	@staticmethod
	def _stock(element, ox):
		return "ossido di " + element.name + Compound.getRomanParenthesis(ox)

class BasicOxide(Oxide):
	def __init__(self, metal, oxygen):
		self.metal = metal
		super().__init__(oxygen)
	
	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "metal")	# oxidation number of the elements

		if nomenclature == Nomenclature.TRADITIONAL:
			pos = Compound.oxPosition(self.metal, ox).value	# 0, 1, 2, 3, 4

			return "ossido " + ("di " + self.metal.name if pos == Traditional.UNIQUE.value else ("ipo" if pos == Traditional.IPO.value else ("per" if pos == Traditional.PER.value else '')) + self.metal.prefix + ("oso" if pos <= Traditional.OSO.value else "ico"))

		elif nomenclature == Nomenclature.IUPAC:
			return super()._iupac(self.metal, self.oxygen)

		elif nomenclature == Nomenclature.STOCK:
			return super()._stock(self.metal, ox)

		else:
			raise InputError("Nomenclatura non valida")

class AcidOxide(Oxide):
	def __init__(self, nonmetal, oxygen):
		self.nonmetal = nonmetal
		super().__init__(oxygen)

	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "nonmetal")	# oxidation number of the elements

		if nomenclature == Nomenclature.TRADITIONAL:
			pos = Compound.oxPosition(self.nonmetal, ox).value	# 0, 1, 2, 3, 4

			return "anidride " + ("ipo" if pos == Traditional.IPO.value else ("per" if pos == Traditional.PER.value else '')) + self.nonmetal.prefix + ("osa" if pos <= Traditional.OSO.value else "ica")	# non metals do not have unique oxidation numbers

		elif nomenclature == Nomenclature.IUPAC:
			return super()._iupac(self.nonmetal, self.oxygen)

		elif nomenclature == Nomenclature.STOCK:
			return super()._stock(self.nonmetal, ox)

		else:
			raise InputError("Nomenclatura non valida")

class Hydracid:
	def __init__(self, hydrogen, halogen):
		self.hydrogen = hydrogen
		self.halogen = halogen
	
	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "halogen")	# oxidation number of the elements

		if nomenclature == Nomenclature.TRADITIONAL:
			return "acido " + self.halogen.prefix2 + "idrico"	# prefix2 for S 

		elif nomenclature == Nomenclature.IUPAC:
			return Compound.getPrefixNo1(self.halogen.quantity) + self.halogen.prefix + "uro di " + Compound.getPrefixNo1(self.hydrogen.quantity) + self.hydrogen.name

		elif nomenclature == Nomenclature.STOCK:
			return self.halogen.prefix + "uro di " + self.hydrogen.name + Compound.getRomanParenthesis(ox, True)	# absolute value for oxidation number

		else:
			raise InputError("Nomenclatura non valida")


class Hydride(ABC):	# abstract class
	@abstractmethod
	def __init__(self, hydrogen):
		self.hydrogen = hydrogen

	@staticmethod
	def _traditional(element, hydrogen, ox):
		formula = element.symbol + (str(element.quantity) if element.quantity > 1 else '') + hydrogen.symbol + (str(hydrogen.quantity) if hydrogen.quantity > 1 else '')	# input formula
		if formula in Hydride.__common:
			return Hydride.__common[formula]
		else:
			pos = Compound.oxPosition(element, ox).value	# 0, 1, 2, 3, 4

			return "idruro " + ("di " + element.name if pos == Traditional.UNIQUE.value else ("ipo" if pos == Traditional.IPO.value else ("per" if pos == Traditional.PER.value else '')) + element.prefix + ("oso" if pos <= Traditional.OSO.value else "ico"))

	@staticmethod
	def _iupac(element, hydrogen):
		return Compound.prefixes[hydrogen.quantity] + "idruro di " + Compound.getPrefixNo1(element.quantity) + element.name	# omit 'mono'
	
	@staticmethod
	def _stock(element, ox, absolute = False):
		return "idruro di " + element.name + Compound.getRomanParenthesis(ox, absolute)

	__common = {
		'BH3': "borano",
		'AlH3': "alano",
		'GaH3': "gallano",
		'CH4': "metano",
		'SiH4': "silano",
		'GeH4': "germano",
		'NH3': "ammoniaca",
		'PH3': "fosfina",
		'AsH3': "arsina",
		# 'C2H4': "etano",
		# 'C3H8': "propano",
		# 'C4H10': "butano",
		# 'C5H12': "pentano",
		# 'C6H14': "esano",
		# 'C7H16': "eptano",
		# 'C8H18': "ottano",
		# 'C9H20': "nonano",
		# 'C10H22': "decano",
		# 'C11H24': "undecano",
		# 'C12H26': "dodecano",
	}

class MetallicHydride(Hydride):
	def __init__(self, metal, hydrogen):
		self.metal = metal
		super().__init__(hydrogen)

	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "metal")	# oxidation number of the elements

		if nomenclature == Nomenclature.TRADITIONAL:
			return super()._traditional(self.metal, self.hydrogen, ox)

		elif nomenclature == Nomenclature.IUPAC:
			return super()._iupac(self.metal, self.hydrogen)

		elif nomenclature == Nomenclature.STOCK:
			return super()._stock(self.metal, ox)

		else:
			raise InputError("Nomenclatura non valida")

class CovalentHydride(Hydride):
	def __init__(self, nonmetal, hydrogen):
		self.nonmetal = nonmetal
		super().__init__(hydrogen)

	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "nonmetal")	# oxidation number of the elements

		if nomenclature == Nomenclature.TRADITIONAL:
			return super()._traditional(self.nonmetal, self.hydrogen, ox)

		elif nomenclature == Nomenclature.IUPAC:
			return super()._iupac(self.nonmetal, self.hydrogen)

		elif nomenclature == Nomenclature.STOCK:
			return super()._stock(self.nonmetal, ox, True)	# absolute value for oxidation number

		else:
			raise InputError("Nomenclatura non valida")

class BinarySalt:
	def __init__(self, metal, nonmetal):
		self.metal = metal
		self.nonmetal = nonmetal

	def mount(self, nomenclature = Nomenclature.IUPAC):
		ox = Compound.parseOx(self, "metal")	# oxidation number of the elements

		if nomenclature == Nomenclature.TRADITIONAL:
			pos = Compound.oxPosition(self.metal, ox).value	# 0, 1, 2, 3, 4

			return self.nonmetal.prefix + "uro " + ("di " + self.metal.name if pos == Traditional.UNIQUE.value else ("ipo" if pos == Traditional.IPO.value else ("per" if pos == Traditional.PER.value else '')) + self.metal.prefix + ("oso" if pos <= Traditional.OSO.value else "ico"))

		elif nomenclature == Nomenclature.IUPAC:
			return Compound.getPrefixNo1(self.nonmetal.quantity) + self.nonmetal.prefix + "uro di " + Compound.getPrefixNo1(self.metal.quantity) + self.metal.name

		elif nomenclature == Nomenclature.STOCK:
			return self.nonmetal.prefix + "uro di " + self.metal.name + Compound.getRomanParenthesis(ox)	# absolute value for oxidation number

		else:
			raise InputError("Nomenclatura non valida")