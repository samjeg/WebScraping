from lxml.etree import ParseError
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup
import requests 
import json

class RecipeDetail:

    def __init__(self):
    	self.title = ""
        self.summary = ""
        self.ingredients = []
        self.steps = []


class WebScraper:

    def __init__(self):
        self.summary = None

    def parse_html_doc(self, _html_doc):
        _html_dom = None

        try:
            _parser = etree.HTMLParser()

            _html_dom = etree.HTML(_html_doc, _parser)
        except ParserError as e:
            print(e)
        return _html_dom 

    # makes a request to the bbcgoodfoods website and 
    # returns a html of the webpage as a response
    def get_recipe_html(self):
        html_dom = None
        try:
            url = "https://www.bbcgoodfood.com/recipes/collection/vegetarian-comfort-food-recipes"
            headers = {"Content-Type": "text/html", }
            response = requests.get(url, headers=headers)
            html_doc = response.content 
            html_dom = self.parse_html_doc(html_doc)
        except ParseError as e:
            print(e) 
        return html_dom

    # makes a request to the bbcgoodfoods website and 
    # returns a html of the webpage as a response
    def get_recipe_detail_html(self, title):
        html_dom = None
        try:
            url = "https://www.bbcgoodfood.com/recipes/%s/"%title
            headers = {"Content-Type": "text/html", }
            response = requests.get(url, headers=headers)
            html_doc = response.content 
            html_dom = self.parse_html_doc(html_doc)
        except ParseError as e:
            print(e) 
        return html_dom

    # initialise bs4 object
    def init_html_parser(self, title):
        url = "https://www.bbcgoodfood.com/recipes/%s/"%title
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

    def get_total_recipe_items(self):
        url = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div"
        html_dom = self.get_recipe_html()
        rows = html_dom.xpath(url)
        length = len(rows[0])

        return length

    def get_titles(self):
        length = self.get_total_recipe_items()
        titles = [self.get_title(i) for i in range(length)]
        titles2 = []
        
        for title in titles:
            if len(title) > 0:
            	titles2.append(title)

        return titles2

    def get_recipe_detail(self, i):
        recipe_detail = None

    # a get request to get ingredients list
    def get_ingredients(self, title):
        soup = self.init_html_parser(title)
        ls = soup.find_all('li') 
        ingredients = [ls[i].text for i in range(165, 187)]

        return ingredients

    # get p tag text from recipe items
    def get_p_tags(self, title):
        soup = self.init_html_parser(title)
        ps = soup.find_all('p')
        ps = [ps[i].text for i in range(1, len(ps))]

        self.summary = ps[0]

        return ps 

    # get title text from recipe items
    def get_title(self, i):
        # makes request to the recipe website and uses the path to get the html element
        title = ""
        html_dom = self.get_recipe_html()
        path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[1]/h4/a"
        e_title = html_dom.xpath(path)
        
        if len(e_title) > 0:
	        title = e_title[0].text

        return title

    # remove escape characters
    def remove_escapes(self, string):
        # check for unicode character and remove it 
        for i, ch in enumerate(string):
            if ch == '\u00a0':
                break
        
        if i == len(string):
            string.replace('\u00a0', '') 

        return string




web_scraper = WebScraper()
web_scraper.get_p_tags("one-pot-paneer-curry-pie")
web_scraper.get_ingredients("one-pot-paneer-curry-pie")
web_scraper.get_titles()

