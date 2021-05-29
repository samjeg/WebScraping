
class parse:

	def __init__(self):
		self.letters = set(list("abcdefghijklmnopqrstuvwxyz"))


	def only_letters(slef, s: str) -> str:
		s2 = ""

		for char in s:
			if(self.letters.contains(char)):
				s2 += char
    
	    return s2
    
    # find string from list and add prefix 
	def add_prefix(self, ls: list[str], st: str, prefix: str) -> list[str]:
		length = len(ls)
		found = False
		i = 0

		while i < length and not found:
			if ls[i] is st:
				temp = "%s%s"%(prefix, st)
				ls[i] = temp
				found = True
			i += 1

		return ls


