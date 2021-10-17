from periodictable import *	##
from compounds import *		##
from binary import *		##
from ternary import *		##
from analyze import *	# mandatory

'''
	Still missing:
	* remove parenthesis when redundant
	* analyze compounds with more than 4 oxidation number for traditional (if somehow possible)
	* meta - piro - orto
'''

print("Pellegatta Simone, October 2021")

while True:
	try:
		print()	# return

		formula = input("Inserisci un composto inorganico binario o ternario: ")
		compound = Parser.compoundType(*Parser.parseString(formula))	# analyze formula

		if 'nomenclature' not in globals() or nomenclature != 0:	# if nomenclature does not exists and has not been set to 'all'
			nomenclature = int(input("0: Tutte, 1: Tradizionale, 2: IUPAC, 3: Stock: "))

		print()	# return

		if nomenclature == 0:	# if nomenclature has been set to 'all'
			for i in Nomenclature:
				name = i.name.capitalize() + ': ' + compound.mount(Nomenclature(i.value))	# nomenclature: name
				print(name)	# print
		else:
			name = compound.mount(Nomenclature(nomenclature - 1))	# mount name
			print(name)	# print


	except InputError as e:
		print(e)	# print error
	except AssertionError as e:
		print("Errore di assert")
		raise e
	except Exception as e:
		print("Errore interno")
		raise e