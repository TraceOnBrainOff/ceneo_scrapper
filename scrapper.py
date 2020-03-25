#import bibliotek
import requests
import traceback
import json
from bs4 import BeautifulSoup
#URL strony z opiniami
url_prefix = "https://www.ceneo.pl"
url_postfix = "/45002653#tab=reviews"

class Opinion:
    def __init__(self, opinion):
        try:
            try:
                summary = opinion.find("div", "product-review-summary").find("em").string #volotile NoneType
            except:
                summary = None
            try:
                purchased = opinion.find("div", "product-review-pz").find("em").string #volotile NoneType
            except AttributeError:
                purchased = None
           
            opinion_id = opinion["data-entry-id"]
            author = opinion.find("div", "reviewer-name-line").string
            stars = opinion.find("span", "review-score-count").string
            useful = opinion.find("button", "vote-yes").find("span").string
            useless = opinion.find("button", "vote-no").find("span").string
            content = opinion.find("p", "product-review-body").get_text()
            dates = opinion.find("span", "review-time").find_all("time")
            review_date = dates.pop(0)["datetime"]
            try:
                purchase_date = dates.pop(0)["datetime"]
            except IndexError:
                purchase_date = None

            try:
                pros = opinion.find("div", "pros-cell").find("ul").get_text()
            except AttributeError:
                pros = None
            
            try:
                cons = opinion.find("div", "cons-cell").find("ul").get_text()
            except AttributeError:
                cons = None
            
            self.opinionId = opinion_id
            self.opinionData = {
                "opinion_id": opinion_id,
                "summary": summary,
                "purchased": purchased,
                "author": author,
                "stars": stars,
                "useful": useful,
                "useless": useless,
                "content": content,
                "review_date": review_date,
                "purchase_date": purchase_date,
                "pros": pros,
                "cons": cons
            }
            #print("Got all parameters for "+self.opinionId)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            #print(f"ERROR! Entire opinion: {opinion}")
    def getData(self):
        return self.opinionData


allOpinions = []
while url_postfix:
    page_response = requests.get(url_prefix+url_postfix) #Pobranie kodu HTML tej strony (kod response 200 to OK)
    page_tree = BeautifulSoup(page_response.text, 'html.parser') #parses return string as an navigateable table like object 
    opinions = list(page_tree.find_all("li", "review-box js_product-review")) #finds all reviews and puts them in a list-like class object
    #wydobycie fragmentów kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
    for i in range(len(opinions)):
        data = opinions[i]
        opinion = Opinion(data)
        allOpinions.append(opinion.getData())
    try: 
        url_postfix = page_tree.find("a", "pagination__next")["href"]
        print(url_prefix + url_postfix)
    except TypeError:
        url_postfix = None
    
print(len(allOpinions))
with open('opinions.json', 'w', encoding="utf-8") as fp:
    json.dump(allOpinions, fp, sort_keys=True, indent=4, ensure_ascii=False)