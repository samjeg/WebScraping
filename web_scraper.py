import requests
import urllib.request
import time 
from bs4 import BeautifulSoup

# The URL to webscrape from 
url = 'https://www.bbcgoodfood.com/recipes/category/all-healthy'

# Connect to the URL
response = requests.get(url)
# print("response text: %s" %response.text)
# print("response content: %s" %response.content)
print("response body: %s" %response)

# Parse HTML and save object 
soup = BeautifulSoup(response.text, "html.parser")

line_count = 1
recipe_items = soup.findAll('p')
print(recipe_items)
for p_tag in recipe_items:
	if line_count <= 8:
		next_content = p_tag.getText()
		print("text content: %s" %next_content)

	line_count+=1

