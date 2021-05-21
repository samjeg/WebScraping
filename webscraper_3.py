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

    # get data from recipe detail page using the recipe title 
    def get_recipe_detail(self, title):
        summary = self.get_summary(title)
        ingredients = self.get_ingredients(title)
        p_tags = self.get_p_tags(title)
        rd = RecipeDetail()
        rd.title = title
        rd.summary = summary 
        rd.ingredients = ingredients
        rd.steps = p_tags        

        return rd

    # get all recipe item data from thier respective pages 
    def get_recipes(self):
        titles = self.get_titles()
        recipes = []

        for title in titles:
            recipes.append(self.get_recipe_detail(title))

        return recipes

    # a get request to get ingredients list
    def get_ingredients(self, title):
        soup = self.init_html_parser(title)
        ls = soup.find_all('li') 
        ingredients = [ls[i].text for i in range(165, 187)]

        return ingredients

    # get p tag text from recipe detail
    def get_p_tags(self, title):
        soup = self.init_html_parser(title)
        ps = soup.find_all('p')
        ps = [ps[i].text for i in range(1, len(ps))]

        return ps
    
    # get summary text from recipe detail
    def get_summary(self, title):
        soup = self.init_html_parser(title)
        url = "/html/body/div[1]/div[3]/main/div/section/div/div[3]/div[3]/div/p"
        html_dom = self.get_recipe_detail_html(title)
        summary = html_dom.xpath(url)

        return summary
        
    # get ingredients text from recipe detail page 
    def ingredients_2(self, title):
        li_class = "pb-xxs pt-xxs list-item list-item--separator"
        html_dom = self.get_recipe_detail_html(title)
        ls = html_dom.xpath("//li[@class='%s']"%li_class)
        length = len(ls)
        ls = [ls[i] for i in range(length)]
        res = []
        
        for item in ls:
            start = ""
            children = item.getchildren()

            if item.text is not None:
                start = item.text

            res.append("%s%s%s"%(start, self.elements_to_string(children), self.nested_text(children)))            

        return res


    # store the text from each element in single string
    def  elements_to_string(self, ls):
        s = ""

        for i in range(len(ls)):
            s += ls[i].text

        return s

    # store the text after each element in single string
    def nested_text(self, ls):
        s = ""

        for i in range(len(ls)):
            s += ls[i].tail if ls[i].tail is not None else "" 

        return s


                

        
    # get title text from recipe detail
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

    # sanitize json list remove escape characters and empty space 
    def sanitize_recipe_detail(self, recipe_detail):

        for attr in recipe_detail:
            attr.title = attr.title.replace('\u2019', "'")
            attr.title = attr.title.replace('\u2018',"'")            
            attr.summary = attr.summary.strip()
            attr.summary = attr.summary.replace('\n', "")
            attr.summary = attr.summary.strip('\u00a0\n')
            attr.summary = attr.summary.replace('\u00a0', '')
            attr.summary = attr.summary.replace('\u2019', "'")  
            attr.summary = self.remove_escapes(attr.summary)
            attr.steps = self.sanitize_recipe_steps(attr.steps)
            attr.ingredients = self.sanitize_recipe_ingredients(attr.ingredients)

        return recipe_detail

    # sanitize json list remove escape characters and empty space 
    def sanitize_recipe_steps(self, steps):

        for step in steps:        
            step = step.strip()
            step = step.replace('\n', "")
            step = step.strip('\u00a0\n')
            step = step.replace('\u00a0', '')
            step = step.replace('\u2019', "'")  
            step = self.remove_escapes(step)
            
        return steps

    # sanitize json list remove escape characters and empty space 
    def sanitize_recipe_ingredients(self, ingredients):

        for ingredient in ingredients:        
            ingredient = ingredient.strip()
            ingredient = ingredient.replace('\n', "")
            ingredient = ingredient.strip('\u00a0\n')
            ingredient = ingredient.replace('\u00a0', '')
            ingredient = ingredient.replace('\u2019', "'")  
            ingredient = self.remove_escapes(ingredient)

        return ingredients

        # convert recipe details to json file
    def convert_recipe_details_to_json_file(self):
        web_scraper = WebScraper()
        titles = self.get_titles()
        details = [web_scraper.get_recipe_detail(title) for title in titles]
        details = [web_scraper.sanitize_recipe_detail(detail) for detail in details]
        details = json.dumps([detail.__dict__ for detail in details])
        
        with open('recipe_details.json', 'w') as f:
            f.write(details)
            f.close()


web_scraper = WebScraper()
# web_scraper.convert_recipe_details_to_json_file()
web_scraper.ingredients_2("beer-mac-n-cheese")



