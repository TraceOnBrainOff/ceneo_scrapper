#import bibliotek
import requests
import traceback
import json
from bs4 import BeautifulSoup
#URL strony z opiniami
url_prefix = "https://www.ceneo.pl"
url_postfix = "/45002653#tab=reviews"

def extractData(opinion, tag, cl, child=None):
    try:
        if child:
            return opinion.find(tag, cl).find(child).get_text().strip()
        else:
            return opinion.find(tag, cl).get_text().strip()
    except:
        return None

class Opinion:
    def __init__(self, opinion):
        try:
            opinion_id = opinion["data-entry-id"]
            dates = opinion.find("span", "review-time").find_all("time")
            review_date = dates.pop(0)["datetime"]
            try:
                purchase_date = dates.pop(0)["datetime"]
            except IndexError:
                purchase_date = None
            
            self.opinionId = opinion_id
            self.opinionData = {
                "opinion_id": opinion_id,
                "summary": extractData(opinion, "div", "product-review-summary", 'em'),
                "purchased": extractData(opinion, "div", "product-review-pz", 'em')=="Opinia potwierdzona zakupem",
                "author": extractData(opinion, "div", "reviewer-name-line"),
                "stars": extractData(opinion, "span", "review-score-count"),
                "useful": extractData(opinion, "button", "vote-yes", "span"),
                "useless": extractData(opinion, "button", "vote-no", "span"),
                "content": extractData(opinion, "p", "product-review-body"),
                "review_date": review_date,
                "purchase_date": purchase_date,
                "pros": extractData(opinion, "div", "pros-cell", "ul"),
                "cons": extractData(opinion, "div", "cons-cell", "ul")
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