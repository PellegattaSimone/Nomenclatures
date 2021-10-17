from abc import ABC, abstractmethod
from enum import Enum

class InputError(ValueError):
	pass

class Type(Enum):
	METAL = 0
	NONMETAL = 1
	HALOGEN = 2
	NOBLEGAS = 3

class Atom(ABC):	# abstract
	@abstractmethod
	def __init__(self, number, name, type):
		self.number = number
		self.name = name 
		self.type = type

class Metal(Atom):
	def __init__(self, number, name, oxidation, prefix = None):
		self.oxidation = oxidation
		if prefix is not None:	# if multiple oxidation numbers
			self.prefix = prefix
		super().__init__(number, name, Type.METAL)

class NonMetal(Atom):
	def __init__(self, number, name, oxidation, prefix, prefix2 = None):
		self.oxidation = oxidation
		self.prefix = prefix
		if prefix2 is None:	# prefix for hydracids and ternary salts
			self.prefix2 = self.prefix
		else:
			self.prefix2 = prefix2
		super().__init__(number, name, Type.NONMETAL)

class Halogen(NonMetal):
	def __init__(self, number, name, oxidation, prefix, prefix2 = None):
		super().__init__(number, name, oxidation, prefix, prefix2)
		self.type = Type.HALOGEN

class NobleGas(Atom):
	def __init__(self, number, name):
		super().__init__(number, name, Type.NOBLEGAS)

class Element:
	def __init__(self, symbol, quantity):
		if symbol in self.__table:
			self.symbol = symbol
			self.quantity = quantity
		else:
			raise InputError("Elemento non esistente: " + symbol)
	
	__table = {
		'H': NonMetal(1, "idrogeno", [-1, +1], "idr"),
		'He': NobleGas(2, "elio"),
		'Li': Metal(3, "litio", [+1]),
		'Be': Metal(4, "berillio", [+2]),
		'B': NonMetal(5, "boro", [+3], "bor"),
		'C': NonMetal(6, "carbonio", [-4, +2, +4], "carbon"),
		'N': NonMetal(7, "azoto", [-3, +2, +3, +4, +5], "nitr"),
		'O': NonMetal(8, "ossigeno", [-2], "oss"),
		'F': Halogen(9, "fluoro", [-1], "fluor"),
		'Ne': NobleGas(10, "neon"),
		'Na': Metal(11, "sodio", [+1]),
		'Mg': Metal(12, "magnesio", [+2]),
		'Al': Metal(13, "alluminio", [+3]),
		'Si': NonMetal(14, "silicio", [-4, +2, +4], "silic"),
		'P': NonMetal(15, "fosforo", [-3, +3, +5], "fosfor", "fosf"),
		'S': Halogen(16, "zolfo", [-2, +4, +6], "solfor", "solf"),	# considered halogen since it makes an hydracid
		'Cl': Halogen(17, "cloro", [-1, +1, +3, +5, +7], "clor"),
		'Ar': NobleGas(18, "argon"),
		'K': Metal(19, "potassio", [+1]),
		'Ca': Metal(20, "calcio", [+2]),
		'Sc': Metal(21, "scandio", [+3]),
		'Ti': Metal(22, "titanio", [+2, +3, +4], "titan"),
		'V': Metal(23, "vanadio", [+2, +3, +4, +5], "vanad"),
		'Cr': Metal(24, "cromo", [+2, +3, +6], "crom"),
		'Mn': Metal(25, "manganese", [+2, +3, +4, +6, +7], "mangan"),
		'Fe': Metal(26, "ferro", [+2, +3], "ferr"),
		'Co': Metal(27, "cobalto", [+2, +3], "cobalt"),
		'Ni': Metal(28, "nichel", [+2, +3], "nichel"),
		'Cu': Metal(29, "rame", [+1, +2], "rame"),
		'Zn': Metal(30, "zinco", [+2]),
		'Ga': Metal(31, "gallio", [+3]),
		'Ge': Metal(32, "germanio", [+2, +4], "german"),
		'As': NonMetal(33, "arsenico", [-3, +3, +5], "arsen"),
		'Se': NonMetal(34, "selenio", [-2, +4, +6], "selen"),
		'Br': Halogen(35, "bromo", [-1, +2, +3, +5], "brom"),
		'Kr': NobleGas(36, "cripton"),
		'Rb': Metal(37, "rubidio", [+1]),
		'Sr': Metal(38, "stronzio", [+2]),
		'Y': Metal(39, "ittrio", [+3]),
		'Zr': Metal(40, "zirconio", [+4]),
		'Nb': Metal(41, "niobio", [+3, +5], "niob"),
		'Mo': Metal(42, "molibdeno", [+1, +2, +3, +4, +5, +6], "molibden"),
		'Tc': Metal(43, "tecnezio", [+4, +5, +6, +7], "tecnez"),
		'Ru': Metal(44, "rutenio", [+2, +3, +4, +5, +6, +7], "ruten"),
		'Rh': Metal(45, "rodio", [+3]),
		'Pd': Metal(46, "palladio", [+2, +4], "pallad"),
		'Ag': Metal(47, "argento", [+1]),
		'Cd': Metal(48, "cadmio", [+2]),
		'In': Metal(49, "indio", [+3]),
		'Sn': Metal(50, "stagno", [+2, +4], "stann"),
		'Sb': Metal(51, "antimonio", [-3, +3, +5], "antimon"),
		'Te': NonMetal(52, "tellurio", [-2, +4, +6], "tellur"),
		'I': Halogen(53, "iodio", [-1, +1, +5, +7], "iod"),
		'Xe': NobleGas(54, "xenon"),
		# ...
		'At': Halogen(85, "astato", [-1, +1, +3, +5, +7], "astat"),
		'Rn': NobleGas(86, "Radon"),
		# ...
	}

	def __getattr__(self, attr):
		return self.__table[self.symbol].__dict__[attr]