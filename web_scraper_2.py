from lxml.etree import ParseError
from lxml import etree
import requests 


class WebScraper:
    length = 0

    def __init__(self):
        self.length = self.get_total_recipe_items()


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



    # get p tag text from recipe items
    def get_p_text(self):
        text_array = []
        # going to the path of each item in the list and 
        # adding the text from the p tag into the text array
        for i in range(self.length):
            url = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[3]/p"
            html_dom = self.get_recipe_html()
            next_p = html_dom.xpath(url)
            if len(next_p) > 0:
                if len(next_p[0].text) > 0:
                    text_array.append(next_p[0].text)


    # # get title tag text from recipe items
    def get_title_text(self):
        text_array = []
        # going to the path of each item in the list and 
        # adding the text from the title tag into the text array
        for i in range(self.length):
            url = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[1]/h4/a"
            html_dom = self.get_recipe_html()
            next_title = html_dom.xpath(url)
            if len(next_title) > 0:
                if len(next_title[0].text) > 0:
                    text_array.append(next_title[0].text)
                    print("title: %s" %next_title[0].text)


    # get_title_text()


scraper = WebScraper()
scraper.get_title_text()