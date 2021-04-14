import json

class DataSanitizer:

    def __init__(self):
        self.json_list = []

    # stream data from the json file and return it as output
    def get_json_object(self):
        raw = ""

        # read file 
        with open("recipe_items.json", "r") as f:
            raw = f.read()

        self.json_list = json.loads(str(raw))
        
        for item in self.json_list:
            print("title %s %s"%(type(item.title), type(item[0].title))
            # item[0].title = item[0].title.strip()
            # item[0].paragraph = item[0].paragrapth.strip()
            # print("paragraph: %s title: %s"%(item[0].title, item[0].paragraph))


ds = DataSanitizer()
ds.get_json_object()
