
class parse:

	def __init__(self):
		self.letters = set(list("abcdefghijklmnopqrstuvwxyz"))


	def only_letters(slef, s: str) -> str:
		s2 = ""

		for char in s:
			if(self.letters.contains(char)):
				s2 += char
    
    return s2