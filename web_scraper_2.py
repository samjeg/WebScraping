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
    length = 0

    def __init__(self):
        self.length = self.get_total_recipe_items()
        self.html_dom = self.get_recipe_html()
        self.url = "https://www.bbcgoodfood.com/recipes/collection/vegetarian-comfort-food-recipes"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def parse_html_doc(slef, _html_doc):
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
        try:
            url = "https://www.bbcgoodfood.com/recipes/collection/vegetarian-comfort-food-recipes"
            headers = {"Content-Type": "text/html", }
            response = requests.get(url, headers=headers)
            html_doc = response.content 
            html_dom = self.parse_html_doc(html_doc)
        except ParseError as e:
            print(e)
        return html_dom

    def get_total_recipe_items(self):
        url = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div"
        html_dom = self.get_recipe_html()
        rows = html_dom.xpath(url)
        length = len(rows[0])
        return length

    # get title text from recipe items
    def get_title(self, i):
        # makes request to the recipe website and uses the path to get the html element
        title = ""
        path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[1]/h4/a"
        e_title = self.html_dom.xpath(path)
        if e_title is not None:
            if len(e_title[0].text) > 0:
                title = e_title[0].text

        return title

    # get p tag text from recipe items
    def get_p_tag(self, i):
        # makes request to the recipe website and uses the path to get the html element
        p_tag = ""     
        path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[3]/p"   
        e_p_tag = self.html_dom.xpath(path)
        if e_p_tag is not None:
            if len(e_p_tag[0].text) > 0:
                p_tag = e_p_tag[0].text

        return p_tag

    # get p tag text from recipe items
    def get_image(self):
        images = self.soup.find_all('img')
        # print(images)

        for image in images:
            print("image :%s \n"%image)
            if image is not None:
                if 'src' in image is not None:
                    print("image  ---   %s \n"%image['src'])
                elif 'data-src' in image is not None:
                    print("image  ---   %s \n"%image['data-src'])                    








recipe_item = RecipeItem()
web_scraper = WebScraper()
recipe_item.title = web_scraper.get_title(2)
recipe_item.rating = 4.0
recipe_item.paragraph = web_scraper.get_p_tag(2)
# recipe_item.image = web_scraper.get_image(2)
recipe_item.healthy = True
recipe_item.vegetarian = True
recipe_item.vegan = True
text = "wp-image-396370 align size-square_thumbnail image-handler__image image-handler__image--aspect no-wrap is-loaded"

print("recipe: %s, %s, %s, %s" %(recipe_item.title, recipe_item.rating, recipe_item.paragraph, web_scraper.get_image()))
