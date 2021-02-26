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
        self.images = ""
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
    def get_images(self):
        images = self.soup.find_all('img')
        result = []

        for image in images:
            if image is not None and image.has_attr('height') and image['height'] == '458':
                if image.has_attr('src'):
                    result.append(image['src'])
                elif image.has_attr('data-src'):
                    result.append(image['data-src'])

        return result


    # get star rating of recipe item
    def get_rating(self, i):
        rest = "outof5starrating"
        span_txt = ""
        rating = 0
        path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[2]/div/div/span/span"
        e_span = self.html_dom.xpath(path)
        if e_span is not None:
            if len(e_span[0].text) > 0:
                span_txt = e_span[0].text
                span_txt = span_txt.replace(" ", "")
                print("after trimming span text: %s"%span_txt)
                span_txt = span_txt.removesuffix(rest)
                rating = int(float(span_txt))
                print("rating: %s - type: %s"%(rating, type(rating)))

        return rating

    # get attributes from recipe items 
    def get_attributes(self, i):
        # Indexing issue must be sorted
        # there are items that are 
        # not recipe items
        attributes = { 'vegetarian': False, 
                       'vegan': False, 
                       'healthy': False
                     }
        list_path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[2]"
        elements = self.html_dom.xpath(list_path)
        attr_len = len(elements[0])

        for e in range(2, attr_len + 1):
            path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[2]/span[" + str(e) + "]/div/div[2]"
            e_span = self.html_dom.xpath(path)
            span_txt = e_span[0].text
            span_txt = span_txt.strip()
            print("attr: %s"%span_txt)
            if span_txt == "Vegan":
                attributes["vegan"] = True
                attributes["vegetarian"] = True
            elif span_txt == "Vegetarian":
                attributes["vegetarian"] = True
            elif span_txt == "Healthy":
                attributes["healthy"] = True

        return attributes




"/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[5]/div/div[2]/span[4]/div"
recipe_item = RecipeItem()
web_scraper = WebScraper()
recipe_item.title = web_scraper.get_title(2)
recipe_item.rating = web_scraper.get_rating(13)
recipe_item.paragraph = web_scraper.get_p_tag(2)
images = web_scraper.get_images()
recipe_item.image = images[1]
recipe_item.healthy = True
recipe_item.vegetarian = True
recipe_item.vegan = True
""
"/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[2]/div/div[2]/span[1]/div/div[2]"
"/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[1]/div/div[2]/span[1]/div/div[2]"
"/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[1]/div/div[2]/span[2]/div/div[2]"
"/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[5]/div/div[2]/span[4]/div/div[2]"
"/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[10]/div/div[2]/span[3]/div/div[2]"
# html_dom = web_scraper.get_recipe_html()
# attributes = html_dom.xpath(path)
# attr_len = len(attributes[0])
attributes = web_scraper.get_attributes(11)
print("healthy: %s vegan: %s vegetarian: %s"%(attributes["healthy"], attributes["vegan"], attributes["vegetarian"]))
# print("recipe: %s, %s, %s, %s, %s, %s, %s" %(recipe_item.title, recipe_item.rating, recipe_item.paragraph, recipe_item.image, web_scraper.length, recipe_item.rating, attr_len))
