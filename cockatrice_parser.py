""" Written by Maxime REVEL
	Strings in French language for now
	Parse in Python to handle XML files, here Cocatrice decks(.cod)
"""

def get_name(line):
	"""
	For a classic line, such as
	        <card number="1" price="0" name="Howling Mine"/>\n
	splitted equals ['		<card number=', '1', 'price=', '0', 'name=', 'Howling Mine', '/>\n']

	This function then returns 'Howling Mine' (card name, 6th element)
	"""
	splitted = line.split('"')
	return splitted[5]

def get_number(line):
	"""
	For a classic line, such as
	        <card number="1" price="0" name="Howling Mine"/>\n
	splitted equals ['		<card number=', '1', 'price=', '0', 'name=', 'Howling Mine', '/>\n']

	This function then returns  '1' (number of copies, 2nd element)
	"""
	splitted = line.split('"')
	return splitted[1] # Already a string, no need to cast

def deck_parser(deck):
	"""
	For a classic line, this function returns a dictionary of copies, such as
	['Deck name'] = ['Deck Myr']
	['Myr sanigriffe'] = ['4'] # Number of copies
	['Island'] = ['12'] ...
	"""

	# Creation of a dictionary to store cards
	dico_deck = {}

	# We remove the beginning (<?xml ?> and <cockatrice_deck /> lines)
	deck.readline() 
	deck.readline()
	# We add the deck name (surrounded by 14 chars at the beginning and 12 at the end)
	dico_deck['Nom du deck'] = deck.readline()[14:-12]
	
	# We look for the line that end "comments"
	s_comment = deck.readline()
	while(s_comment[-12:] != '</comments>\n'):
		s_comment = deck.readline()
	
	## We browse the file till the end
	zone = deck.readline()
	while(zone != '</cockatrice_deck>\n'):
		# We check whether there is a zone (side or main)
		if(zone[:9] == '    <zone'):
			# We read all cards from the zone
			line = deck.readline()
			while(line != '    </zone>\n'):
				name = get_name(line)
				copies = get_number(line)
				# If there was the same card in another zone (side/main), we should not write the number of copies found, but add it instead
				dico_deck[name] = str(int(dico_deck.get(name,0)) + int(copies))
				line = deck.readline()

		zone = deck.readline()
	
	# We return the dictionary
	return dico_deck