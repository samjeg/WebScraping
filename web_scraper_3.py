from lxml.etree import ParseError
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup
import requests 
import json

class RecipeItem:

    def __init__(self):
        self.title = ""
        self.paragraph = ""
        self.image = ""
        self.rating = 0.0
        self.vegetarian = False
        self.vegan = False
        self.healthy = False



class WebScraper:

    def __init__(self):
        self.url = "https://www.bbcgoodfood.com/recipes/"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.html_dom = self.get_recipe_html("One-pot paneer curry pie/")
        self.soup = BeautifulSoup(self.response.text, 'html.parser')




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
    def get_recipe_html(self, title):
        html_dom = None
        try:
            url = "https://www.bbcgoodfood.com/recipes/%s"%title
            headers = {"Content-Type": "text/html", }
            response = requests.get(url, headers=headers)
            html_doc = response.content 
            html_dom = self.parse_html_doc(html_doc)
        except ParseError as e:
            print(e) 
        return html_dom


    # # get title text from recipe items
    # def get_detail_summary(self, title):
    #     # makes request to the recipe website and uses the path to get the html element

    #     summary = ""
    #     html_dom = self.get_recipe_html(title)
    #     "/html/body/div[1]/div[3]/main/div/section/div/div[3]/div[3]/div/p"
    #     "/html/body/div[1]/div[3]"
    #     path = "/html/body/div[1]/div[3]/main/div/section/div"
    #     e_summary = self.html_dom.xpath(path)
    #     if e_summary is not None:
    #         print(e_summary)

    #     return summary

    # get p tag text from recipe items
    def get_p_tags(self):
        # p_tags = self.soup.find_all('p')
        url = "/html/body/div[1]/div[3]/main/div/section/div/div[3]/div[3]/div"
        # html_dom = self.get_recipe_html("One-pot paneer curry pie/")
        div = self.html_dom.xpath(url)
        print("div %s"%div)
        result = []
 
        # for p_tag in p_tags:
        #     if p_tag is not None:
        #         print("p tag: %s"%p_tag)   

        return result

    # prints recipe object
    def print_recipe_item(self, i):
        recipe_item = self.get_recipe_item(i)
        print("recipe item: ")
        print("title: %s"%recipe_item.title)
        print("paragraph: %s"%recipe_item.paragraph)
        print("rating: %s"%recipe_item.rating)
        print("is healthy: %s"%recipe_item.healthy)
        print("is vegetarian: %s"%recipe_item.vegetarian)
        print("is vegan: %s"%recipe_item.vegan)
        print("image: %s"%recipe_item.image)


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
web_scraper.get_p_tags()

