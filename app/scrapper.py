#import bibliotek
import sys
import requests
import traceback
import json
from bs4 import BeautifulSoup
import sys

class Opinion:
    def __init__(self, opinion):
        self.status = "init"
        try:
            dates = opinion.find("span", "review-time").find_all("time")
            review_date = dates.pop(0)["datetime"]
            try:
                purchase_date = dates.pop(0)["datetime"]
            except IndexError:
                purchase_date = None
            self.opinionData = {
                "opinion_id": opinion["data-entry-id"],
                "summary": self.extractData(opinion, "div", "product-review-summary", 'em'),
                "purchased": self.extractData(opinion, "div", "product-review-pz", 'em')=="Opinia potwierdzona zakupem",
                "author": self.extractData(opinion, "div", "reviewer-name-line"),
                "stars": self.extractData(opinion, "span", "review-score-count"),
                "useful": self.extractData(opinion, "button", "vote-yes", "span"),
                "useless": self.extractData(opinion, "button", "vote-no", "span"),
                "content": self.extractData(opinion, "p", "product-review-body"),
                "review_date": review_date,
                "purchase_date": purchase_date,
                "pros": self.extractData(opinion, "div", "pros-cell", "ul"),
                "cons": self.extractData(opinion, "div", "cons-cell", "ul")
            }
            self.status = "done"
            #print("Got all parameters for "+self.opinionId)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            self.status = "error: " + traceback.format_exc()
            #print(f"ERROR! Entire opinion: {opinion}")
    @staticmethod
    def extractData(opinion, tag, cl, child=None):
        try:
            if child:
                return opinion.find(tag, cl).find(child).get_text().strip()
            else:
                return opinion.find(tag, cl).get_text().strip()
        except:
            return None
    def getStatus(self):
        return self.status

    def getData(self):
        return self.opinionData

class Extractor:
    def __init__(self, product_id):
        self.id = product_id
        self.url_prefix = "https://www.ceneo.pl"
        self.url_postfix = "/"+product_id+"#tab=reviews"
        self.URL = self.url_prefix + self.url_postfix
        self.productName = None
        self.opinions = []
        self.abnormalStatus = []
    def extractOpinions(self):
        while self.url_postfix and len(self.abnormalStatus)==0:
            page_response = requests.get(self.url_prefix+self.url_postfix) #Pobranie kodu HTML tej strony (kod response 200 to OK)
            page_tree = BeautifulSoup(page_response.text, 'html.parser') #parses return string as an navigateable table like object 
            raw_opinions = list(page_tree.find_all("li", "review-box js_product-review")) #finds all reviews and puts them in a list-like class object
            if not self.productName:
                self.productName = page_tree.find("h1", "product-name").get_text().strip()
                print(self.productName)
            #wydobycie fragmentów kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
            for i in range(len(raw_opinions)):
                raw_opinion = raw_opinions[i]
                opinion = Opinion(raw_opinion)
                self.opinions.append(opinion.getData())
            try: 
                self.url_postfix = page_tree.find("a", "pagination__next")["href"]
                print(self.url_prefix + self.url_postfix)
            except TypeError:
                self.url_postfix = None #Means it's the last page
        self.saveData()
    def pageExists(self):
        existance_check = requests.get(self.url_prefix+self.url_postfix)
        if existance_check.status_code != 200:
            return False
        return True
    def saveData(self):
        with open('opinions_json/'+self.id+'.json', 'w', encoding="utf-8") as fp:
            json.dump({
                "productName": self.productName,
                "errors": self.abnormalStatus,
                "opinions": self.opinions
            }, fp, sort_keys=True, indent=4, ensure_ascii=False)
    def saveError(self, er):
        with open('opinions_json/'+self.id+'.json', 'w', encoding="utf-8") as fp:
            json.dump({
                "productName": "None",
                "errors": [er],
                "opinions": []
            }, fp, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    product_id = sys.argv[1]
    a = Extractor(product_id)
    if a.pageExists():
        a.extractOpinions()
    else:
        a.saveError("No response")