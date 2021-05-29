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
        self.letters = set(list("abcdefghijklmnopqrstuvwxyz"))

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
    def recipe_html(self):
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
    def recipe_detail_html(self, title):
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

    def total_recipe_items(self):
        url = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div"
        html_dom = self.recipe_html()
        rows = html_dom.xpath(url)
        length = len(rows[0])

        return length

    def titles(self):
        length = self.total_recipe_items()
        titles = [self.title(i) for i in range(length)]
        titles2 = []
        
        for title in titles:
            if len(title) > 0:
                titles2.append(title)

        return titles2

    # get all recipe item data from thier respective pages 
    def recipes(self):
        titles = self.titles()
        recipes = []

        for title in titles:
            recipes.append(self.recipe_detail(title))

        return recipes

    # get p tag text from recipe detail
    def p_tags(self, title):
        soup = self.init_html_parser(title)
        ps = soup.find_all('p')
        ps = [ps[i].text for i in range(1, len(ps))]

        return ps
    
    # get summary text from recipe detail
    def summary(self, title):
        soup = self.init_html_parser(title)
        url = "/html/body/div[1]/div[3]/main/div/section/div/div[3]/div[3]/div/p"
        html_dom = self.recipe_detail_html(title)
        summary = html_dom.xpath(url)    

        if summary:
            summary = summary[0].text     
        else:
            summary = ""

        return summary
        
    # get ingredients text from recipe detail page 
    def ingredients(self, title):
        li_class = "pb-xxs pt-xxs list-item list-item--separator"
        html_dom = self.recipe_detail_html(title)
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
    def title(self, i):
        # makes request to the recipe website and uses the path to get the html element
        title = ""
        html_dom = self.recipe_html()
        path = "/html/body/div[4]/div[2]/article/div[1]/div/div[1]/div[1]/div[3]/div[1]/div/div/div[" + str(i) + "]/div/div[1]/div[2]/div[1]/h4/a"
        e_title = html_dom.xpath(path)
        
        if len(e_title) > 0:
            title = e_title[0].text
            title = title.lower()
            title = self.only_letters(title)
            title = self.space_to_hypens(title)


        return title

    # remove escape characters
    def remove_escapes(self, string):
        # check for unicode character and remove it 
        i = 0
        while i < len(string):
            if string[i] == '\u00a0':
                break
            i += 1
        
        if i == len(string):
            string.replace('\u00a0', '') 

        return string

    # get data from recipe detail page using the recipe title 
    def recipe_detail(self, title):
        summary = self.summary(title)
        ingredients = self.ingredients(title)
        p_tags = self.p_tags(title)
        rd = RecipeDetail()
        rd.title = title
        rd.summary = summary 
        rd.ingredients = ingredients
        rd.steps = p_tags        

        return rd

    # get recipe pages
    def recipe_pages(self, titles):
        pages = []

        for title in titles:
            recipe_detail = self.recipe_detail(title)
            pages.append(self.sanitize_recipe_detail(recipe_detail))

        return pages

    # sanitize json list remove escape characters and empty space 
    def sanitize_recipe_detail(self, recipe_detail):
        recipe_detail.title = recipe_detail.title.replace('\u2019', "'")
        recipe_detail.title = recipe_detail.title.replace('\u2018',"'")        
        recipe_detail.summary = self.sanitize_recipe_summary(recipe_detail.summary)
        recipe_detail.steps = self.sanitize_recipe_steps(recipe_detail.steps)
        recipe_detail.ingredients = self.sanitize_recipe_ingredients(recipe_detail.ingredients)

        return recipe_detail 

    # sanitize json list remove escape characters and empty space 
    def sanitize_recipe_summary(self, summary):
        
        summary = summary.strip()
        summary = summary.replace('\n', "")
        summary = summary.strip('\u00a0\n')
        summary = summary.replace('\u00a0', '')
        summary = summary.replace('\u2019', "'")  
        summary = self.remove_escapes(summary)
            
        return summary

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

    # leaves only the lowercase letters in the string, as well as any empty spaces 
    def only_letters(self, s: str) -> str:
        self.letters.add(" ")
        self.letters.add("-")
        s2 = ""

        for char in s:
            if char in self.letters:
                s2 += char
    
        return s2

    def space_to_hypens(self, s: str) -> str:
        length = len(s)
        s2 = ""
        
        for i in range(length - 1):
            if s[i] == " " and s[i + 1] != " ": # look ahead before adding hypen 
                s2 += "-"
            elif s[i] != " " or s[i] == "-":
                s2 += s[i]

        s2 += s[length - 1] # add last character

        return s2

    # convert recipe details to json file
    def convert_recipe_details_to_json_file(self):
        web_scraper = WebScraper()
        titles = self.titles()
        pages = self.recipe_pages(titles)
        length = len(pages)
        pages2 = []

        for i in range(length):
            page = pages[i].__dict__
            
            # shorten for loops in method 
            # use multi-threading speed up runtime of possible
            steps2 = []
            for step in page["steps"]:
                stp = step.replace("\r\n", "")
                stp = stp.replace("\n", "")
                steps2.append(stp)
            page["steps"] = steps2

            ingredients2 = []
            for ingredient in page["ingredients"]:
                ingrdnt = ingredient.replace("\r\n", "")
                ingrdnt = ingrdnt.replace("\n", "")
                ingredients2.append(ingrdnt)
            page["ingredients"] = ingredients2

            pages2.append(page)

        pages2 = json.dumps(pages2, ensure_ascii=False).encode("utf8")
        pages2 = pages2.decode()
        
        with open('recipe_details.json', 'w') as f:
            f.write(pages2)
            f.close()

wb = WebScraper()
wb.convert_recipe_details_to_json_file()