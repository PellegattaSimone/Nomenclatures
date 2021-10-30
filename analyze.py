from periodictable import InputError, Element, Type
from binary import *
from ternary import *

class Parser:
	def __init__(self):
		self.__element = ''	# element symbol
		self.__quantity = 1	# how many instances of an element
		self.__compound = []	# all elements
		self.__parenthesis = 0	# is a parenthesis open? 0: no, 1: yes, 2: just closed
		self.__list = []	# temporary store elements inside parenthesis

	def __newElement(self):
		if self.__element != '':	# if not empty
			if self.__parenthesis == 0:
				self.__compound.append(Element(self.__element, self.__quantity))	# add to compound list
			else:
				self.__list.append(Element(self.__element, self.__quantity))	# add to parenthesis list

			self.__element = ''
			self.__quantity = 1	# reset both element and quantity for the next one

	def __closeParenthesis(self, quantity = 1):
		for element in self.__list:
			element.quantity *= quantity	# multiply quantity by parenthesis number
		
		self.__compound += self.__list	# transfer parenthesis list to elements list
		self.__list = []

		self.__parenthesis = 0	# closed

	def parseString(self, formula):
		try:
			for letter in formula:
				if letter.isupper():
					self.__newElement()
					self.__element += letter

				elif letter.islower():
					self.__element += letter

				elif letter.isnumeric():
					if(self.__parenthesis == 2):	# if parenthesis just closed
						self.__closeParenthesis(int(letter))	# group quantity > 10 not supported
					elif self.__quantity == 1:
						self.__quantity = int(letter)
					else:
						self.__quantity = self.__quantity * 10 + int(letter)	# in case of two-digit numbers

				elif letter == '(':
					self.__newElement()	# else in letter.isupper() it would find an open parenthesis
					self.__parenthesis = 1	# open

				elif letter == ')':
					self.__newElement()
					self.__parenthesis = 2	# just closed (for letter.isnumeric())

				else:
					raise InputError(letter + " non è un carattere valido")
			else:	# the end of the for loop
				self.__newElement()

				if(self.__parenthesis == 2):	# if parenthesis just closed
					self.__closeParenthesis()
			
			return self.__compound

		except Exception as e:
			# temp:further handling (?)
			raise e
	
	@staticmethod
	def compoundType(*list):
		# match list:
			# case 2:
				# pass
			# case 3:
				# pass

		if len(list) == 2:
			if list[1].symbol == 'O':	# if the second element is oxigen
				if list[0].type == Type.METAL:
					return BasicOxide(*list)

				elif list[0].type not in (Type.NONMETAL, Type.HALOGEN):	# optional check
					raise InputError("Il primo elemento di un ossido deve essere un metallo o un non metallo")

				return AcidOxide(*list)

			elif list[0].symbol == 'H':	# if the first element is hydrogen
				if list[1].type != Type.HALOGEN:	# optional check
					raise InputError("Il secondo elemento di un idracido deve essere un alogeno")

				return Hydracid(*list)

			elif list[1].symbol == 'H':	# if the second element is hydrogen
				if list[0].type == Type.METAL:
					return MetallicHydride(*list)

				elif list[0].type != Type.NONMETAL:	# optional check (not halogens: hydracid)
					raise InputError("Il primo elemento di un ossido deve essere un metallo o un non metallo")

				return CovalentHydride(*list)

			else:
				if list[0].type != Type.METAL:	# optional check
					raise InputError("Il primo elemento di un sale binario deve essere un metallo")
				elif list[1].type not in (Type.NONMETAL, Type.HALOGEN):	# optional check
					raise InputError("Il secondo elemento di un sale binario deve essere un non metallo")

				return BinarySalt(*list)

		elif len(list) == 3:
			if list[1].symbol == 'O' and list[2].symbol == 'H':	# if it contains an hydroxy group
				if list[0].type != Type.METAL:	# optional check
					raise InputError("Il primo elemento di un idrossido deve essere un metallo")

				return Hydroxide(*list)

			elif list[0].symbol == 'H':	# if the first element is hydrogen
				if list[1].type not in (Type.NONMETAL, Type.HALOGEN):	# optional check
					raise InputError("Il secondo elemento di un ossiacido deve essere un non metallo")
				elif list[2].symbol != 'O':	# optional check
					raise InputError("Il terzo elemento di un ossiacido deve essere l'ossigeno")

				return Oxiacid(*list)

			else:
				if list[0].type != Type.METAL:	# optional check
					raise InputError("Il primo elemento di un sale ternario deve essere un metallo")
				elif list[1].type not in (Type.NONMETAL, Type.HALOGEN):	# optional check
					raise InputError("Il primo elemento di un sale ternario deve essere un metallo")
				elif list[2].symbol != 'O':	# optional check
					raise InputError("Il terzo elemento di un sale ternario deve essere l'ossigeno")

				return TernarySalt(*list)
		else:
			raise InputError("La formula contiene " + str(len(list)) + " elementi")