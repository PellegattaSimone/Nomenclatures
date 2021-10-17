from periodictable import InputError, Element, Type
from binary import *
from ternary import *

class Parser:
	__element = ''	# element symbol
	__quantity = 1	# how many instances of an element
	__compound = []	# all elements
	__parenthesis = 0	# is a parenthesis open? 0: no, 1: yes, 2: just closed
	__list = []	# temporary store elements inside parenthesis

	@staticmethod
	def __newElement():
		if Parser.__element != '':	# if not empty
			if Parser.__parenthesis == 0:
				Parser.__compound.append(Element(Parser.__element, Parser.__quantity))	# add to compound list
			else:
				Parser.__list.append(Element(Parser.__element, Parser.__quantity))	# add to parenthesis list

			Parser.__element = ''
			Parser.__quantity = 1	# reset both element and quantity for the next one

	@staticmethod
	def __closeParenthesis(quantity = 1):
		for element in Parser.__list:
			element.quantity *= quantity	# multiply quantity by parenthesis number
		
		Parser.__compound += Parser.__list	# transfer parenthesis list to elements list
		Parser.__list = []

		Parser.__parenthesis = 0	# closed

	@staticmethod
	def parseString(formula):
		Parser.__element = ''	# reset in case of exception in previous formula
		Parser.__quantity = 1	# reset in case of exception in previous formula
		Parser.__compound = []	# list of all elements

		try:
			for letter in formula:
				if letter.isupper():
					Parser.__newElement()
					Parser.__element += letter

				elif letter.islower():
					Parser.__element += letter

				elif letter.isnumeric():
					if(Parser.__parenthesis == 2):	# if parenthesis just closed
						Parser.__closeParenthesis(int(letter))	# group quantity > 10 not supported
					elif Parser.__quantity == 1:
						Parser.__quantity = int(letter)
					else:
						Parser.__quantity = Parser.__quantity * 10 + int(letter)	# in case of two-digit numbers

				elif letter == '(':
					Parser.__newElement()	# else in letter.isupper() it would find an open parenthesis
					Parser.__parenthesis = 1	# open

				elif letter == ')':
					Parser.__newElement()
					Parser.__parenthesis = 2	# just closed (for letter.isnumeric())

				else:
					raise InputError(letter + " non è un carattere valido")
			else:	# the end of the for loop
				Parser.__newElement()

				if(Parser.__parenthesis == 2):	# if parenthesis just closed
					Parser.__closeParenthesis()
			
			return Parser.__compound

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