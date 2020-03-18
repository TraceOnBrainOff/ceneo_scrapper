#import bibliotek
import requests
import traceback
from bs4 import BeautifulSoup
#URL strony z opiniami
url = "https://www.ceneo.pl/45002653#tab=reviews"
#Pobranie kodu HTML tej strony (kod response 200 to OK)
page_response = requests.get(url)
page_tree = BeautifulSoup(page_response.text, 'html.parser') #parses return string as an navigateable table like object 
#wydobycie fragmentów kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
opinions = list(page_tree.find_all("li", "review-box js_product-review")) #finds all reviews and puts them in a list-like class object
#automate for all opinions. Try to figure out dates for `purchased`

cOpinions = []
class Opinion:
    def __init__(self, opinion):
        try:
            try:
                summary = opinion.find("div", "product-review-summary").find("em").string #volotile NoneType
            except:
                summary = None
            try:
                purchased = opinion.find("div", "product-review-pz").string #volotile NoneType
            except AttributeError:
                purchased = None
           
            opinion_id = opinion["data-entry-id"]
            author = opinion.find("div", "reviewer-name-line").string
            stars = opinion.find("span", "review-score-count").find("em")
            useful = opinion.find("button", "vote-yes").find("span").string
            not_useful = opinion.find("button", "vote-no").find("span").string
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
            print(opinion_id,author,summary,stars,purchased,useful,not_useful,content)
        except Exception as err:
            traceback.print_tb(err.__traceback__)
            #print(f"ERROR! Entire opinion: {opinion}")


for i in range(len(opinions)):
    opinion = Opinion(opinions[i])
    #opinions.pop(i)