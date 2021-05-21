import lxml.html
import requests


class Scrape:

	def content(self):

		html = requests.get('https://store.steampowered.com/explore/new/')
		doc = lxml.html.fromstring(html.content)
