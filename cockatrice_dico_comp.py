""" Written by Maxime REVEL
	Strings in French language for now
	Compare Cockatrice decks (.cod) in Python, to find ban and/or limited cards
"""

import os
from tkinter import Tk, Button, Label, Entry, Radiobutton, IntVar, filedialog
from cockatrice_parser import deck_parser # We are going to use parsing functions of that file
## Global variables
cockatrice_path = './decks'
dico_formats = {1: " - Vintage", 2: " - Check", 3: " - Pop"}
nb_formats = len(dico_formats)
dico_details = {0: "Aucun deck choisi."}
for key in dico_formats:
	dico_details[key] = ""
dico_showDetails = {}
d_badcards = {}
d_badcards_one = {}

unlimited_cards = ["Island","Plains","Mountain","Swamp","Forest"]
unlimited_cards += ["Snow-Covered Island","Snow-Covered Plains","Snow-Covered Mountain","Snow-Covered Swamp","Snow-Covered Forest"]
unlimited_cards.append("Wastes")
unlimited_cards.append("Shadowlord of the Apostle")

###########################################################################################################################################
#Functions answering buttons
###########################################################################################################################################

def chooseDeckAndCompute():
	"""
	Open window to choose a file (a deck) and launches comparisons
	"""
	global dico_details
	global dico_showDetails

	s_mydeck = filedialog.askopenfilename(initialdir = cockatrice_path, title = 'Choisissez le deck à analyser')
	try:
		mydeck = open(s_mydeck,"r")
		printHeader(mydeck)
		checkFormats()
	except:
		print("**Erreur d'ouverture du deck.**")
		raise "Erreur"

###########################################################################################################################################
# Printing functions
###########################################################################################################################################

def printHeader(deck):
	"""
	Prints deck's name and the format which will be tested in that column
	"""
	global dico_details
	global dico_showDetails
	global d_mydeck

	# We create the deck's cards' dictionary
	d_mydeck = deck_parser(deck)
	
	# In each column
	for i in range(1, nb_formats + 1):
		dico_details[i] = d_mydeck['Nom du deck'] + dico_formats[i] + "\n\n"
		dico_showDetails[i].config(text = dico_details[i])

	del d_mydeck['Nom du deck'] # To avoid to find it again in searching cards' loops

def checkFormats():
	"""
	Prints the unauthorized cards for each format.
	We suppose that format i bans cards from banlists 0 to i-1
	and authorize one copy of banlist i's cards.
	"""
	global dico_details
	global dico_showDetails
	global nb_formats

	check_max_four()
	
	for i in range(1, nb_formats + 1):
		tmp = check_no_one(dico_showDetails[i], dico_details[i], i)
		dico_details[i] = tmp
		tmp = check_max_one(dico_showDetails[i], dico_details[i], i)
		dico_details[i] = tmp

###########################################################################################################################################
# Comparison functions
###########################################################################################################################################

def check_max_four():
	"""
	We compute a deck checking, to be sure that no card is there more than four times.
	"""
	global dico_details
	global dico_showDetails
	global nb_formats
	global unlimited_cards

	s_err = ""
	for cle in d_mydeck:
		if int(d_mydeck[cle]) > 4:
				if cle not in unlimited_cards:
					s_err += "\nCarte en " + d_mydeck[cle] + " exemplaires : " + cle
	if s_err != "":
		dico_details[0] += '\n***********************************\n'
		dico_details[0] = "Cartes en plus de 4 exemplaires :"
		dico_details[0] += s_err
		dico_details[0] += '\n***********************************\n'
	else:
		dico_details[0] = "Pas de carte en plus de 4 exemplaires trouvée"
		dico_details[0] += '\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'

	for i in range(1, nb_formats + 1):
		dico_details[i] += dico_details[0]
		dico_showDetails[i].config(text = dico_details[i])

def check_no_one(label, label_text, num):
	"""
	We compute comparison with all "ban files" with a number which is less or equal than
	Deck's cards should not be in these files
	"""
	global dico_details
	global dico_showDetails
	global badcards
	global d_badcards
	global nb_formats

	for j in range(0, num):
		try:
			badcards = open(cockatrice_path + "/Banlists/Banlist " + str(j) + ".cod","r")
		except:
			print("Erreur d'ouverture de la Banlist n°" + str(j))
			pass
		# Here the try worked
		# We parse the current banlist
		d_badcards.clear()
		d_badcards = deck_parser(badcards)

		# We browse dictionary keys and see whether they are part of forbidden deck (and also whether there are more than 4 copies)
		s_err = ""
		for cle in d_mydeck:
			if cle in d_badcards:
				s_err += "\nCarte interdite : " + cle
		if s_err != "":
			label_text += '\n***********************************\n'
			label_text += "Cartes interdites :"
			label_text += s_err
			label_text += '\n***********************************\n'
			
		else:
			label_text += "Pas de carte interdite trouvée"
			label_text += '\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
		

		badcards.close()

	label.config(text = label_text)
	# We return the text to be modified in the dictionary
	return label_text

def check_max_one(label, label_text, num):
	"""
	We compute comparison with the given restriction file,
	whether each card is not there more than once.
	"""
	global dico_details
	global dico_showDetails
	global badcards
	global d_badcards_one
	global nb_formats

	try:
		badcards_one = open(cockatrice_path + "/Banlists/Banlist " + str(num) + ".cod","r")
	except:
		label_text = "Erreur d'ouverture de la Banlist n°" + str(num)
		print(label_text)
		label.config(text = label_text)
		pass

	# Here the "try" worked
	# We parse the current banlist
	d_badcards_one = deck_parser(badcards_one)

	# We browse keys and check whether they are in forbidden deck
	s_err = ""
	for cle in d_mydeck:
		if cle in d_badcards_one:
			numberOfTimes = int(d_mydeck[cle])
			if numberOfTimes > 1:
				s_err += "\nCarte trouvée " + str(numberOfTimes) + " fois : " + cle

	if s_err != "":
		label_text += '\n***********************************\n'
		label_text += "Cartes limitées en 1 exemplaire, trouvées plus d'1 fois :"
		label_text += s_err
		label_text += '\n***********************************\n'

	else:
		label_text += "Pas de carte limitée en 1 fois trouvée plusieurs fois"
		label_text += '\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
	
	badcards_one.close()

	label.config(text = label_text)
	# We return the text to be modified in dictionary
	return label_text

###########################################################################################################################################
## Graphic part (tkinter)
###########################################################################################################################################

root = Tk()
root.title("MTG Format checker")
# Logo : root.iconbitmap("mtg_seek_logo.bmp")

labelChooseDeckFile = Label(root, text="Choisissez le deck à analyser : ", font=("Comic Sans MS", 12))
buttonChooseDeckFile = Button(root, text="Parcourir...", command=chooseDeckAndCompute, width=20, font=("Comic Sans MS", 12))

for i in range(1, nb_formats + 1):
	dico_showDetails[i] = Label(root, text=dico_details[i], font=("Comic Sans MS", 12))

labelChooseDeckFile.grid(row=1, column=2)
buttonChooseDeckFile.grid(row=2, column=2)

for i in range(1, nb_formats + 1):
	dico_showDetails[i].grid(row=3, column=i)

root.mainloop()

"""
cd AppData/Local/Cockatrice/Cockatrice
python cockatrice_tk_comparator.py
"""