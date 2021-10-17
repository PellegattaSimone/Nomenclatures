from periodictable import InputError
from enum import Enum

class Nomenclature(Enum):
	TRADITIONAL = 0
	IUPAC = 1
	STOCK = 2

class Traditional(Enum):
	UNIQUE = 0	# temp: 5(?) for error in anidride
	IPO = 1
	OSO = 2
	ICO = 3
	PER = 4

class Compound:
	@staticmethod
	def parseOx(compound, element):	# traditional: the elements in which to check if it is the highest oxidation number
		elements = compound.__dict__.copy()	# do not edit the original one

		assert element in elements

		check = elements.pop(element)	# we have to find the oxidation number of this element
		elements = list(elements.values())	# all the other elements

		if len(elements) == 1:	# binary vs ternary compounds
			for result in check.oxidation:
				result *= check.quantity	# oxidation number multiplied by number of elements

				for second in elements[0].oxidation:
					second *= elements[0].quantity

					if result + second == 0:
						return int(result / check.quantity)	# get original value back
		else:
			for result in check.oxidation:
				result *= check.quantity

				for second in elements[0].oxidation:
					second *= elements[0].quantity

					for third in elements[1].oxidation:
						third *= elements[1].quantity

						if result + second + third == 0:
							return int(result / check.quantity)	# get original value back
		
		raise InputError("Formula non valida: i numeri di ossidazione non coincidono")	# if oxidation numbers do not match
	
	@staticmethod
	def oxPosition(element, ox, onlypositive = True):
		oxidations = element.oxidation.copy()

		if onlypositive == True:
			assert ox > 0
			oxidations[:] = [x for x in oxidations if x > 0]	# only positive oxidation numbers

		if len(oxidations) == 1:
			return Traditional(0)

		elif len(oxidations) == 2:
			if ox == oxidations[0]:
				return Traditional.OSO
			else:
				return Traditional.ICO

		elif len(oxidations) == 3:	# not exact: lots of exceptions
			if ox % 2 == 1:	# if is odd
				return Traditional((ox + 1) / 2)	# 1: 1, 3: 2, 5: 3, 7: 4
			else:
				return Traditional(oxidations.index(ox) + 1)	# 1, 2, 3

		elif len(oxidations) == 4:
			return Traditional(oxidations.index(ox) + 1)	# 1, 2, 3, 4
			
		else:
			raise InputError("Impossibile analizzare questa formula")	# temp

	@staticmethod
	def getPrefixNo1(number):
		assert number > 0
		return Compound.prefixes[number] if number != 1 else ''	# to exclude mono prefix
	
	@staticmethod
	def getRomanParenthesis(number, absolute = False):
		if absolute:
			number = abs(number)
		else:
			assert number > 0	# oxidation number must be positive

		return '(' + Compound.roman[number] + ')'

	prefixes = {	# for IUPAC prefixes
		1: "mono",
		2: "di", 
		3: "tri",
		4: "tetra",
		5: "penta",
		6: "esa",
		7: "epta",
		8: "otta",
		9: "nona",
		10: "deca",
		11: "endeca",
		12: "dodeca",
		13: "trideca",
		14: "tetradeca",
		15: "pentadeca",
		16: "esadeca",
		17: "eptadeca",
		18: "ottadeca",
		19: "ennadeca",
		20: "icosa",
	}

	roman = {	# for oxidation number
		1: 'I',
		2: 'II',
		3: 'III',
		4: 'IV',
		5: 'V',
		6: 'VI',
		7: 'VII',
		8: 'VIII',
		9: 'IX',
		10: 'X',
		11: 'XI',
		12: 'XII',
		13: 'XIII',
		14: 'XIV',
		15: 'XV',
		16: 'XVI',
		17: 'XVII',
		18: 'XVIII',
		19: 'XIX',
		20: 'XX',
	}