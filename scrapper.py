#import bibliotek
import requests
from bs4 import BeautifulSoup
#URL strony z opiniami
url = "https://www.ceneo.pl/45002653#tab=reviews"
#Pobranie kodu HTML tej strony (kod response 200 to OK)
page_response = requests.get(url)
page_tree = BeautifulSoup(page_response.text, 'html.parser') #parses return string as an navigateable table like object 
#wydobycie fragmentów kodu HTML strony fragmentów odpowiadających poszczególnym opiniom
opinions = page_tree.find_all("li", "review-box js_product-review") #finds all reviews and puts them in a list-like class object

opinion = opinions.pop() #Removes from stack and returns the content

opinion_id = opinion["data-entry-id"]
author = opinion.find("div", "reviewer-name-line").string
summary = opinion.find("div", "product-review-summary").find("em").string
stars = opinion.find("span", "review-score-count").find("em")
purchased = opinion.find("div", "product-review-pz").string
useful = opinion.find("button", "vote-yes").find("span").string
not_useful = opinion.find("button", "vote-no").find("span").string
content = opinion.find("p", "product-review-body").get_text()

print(opinion_id,author,summary,stars,purchased,useful,not_useful,content)

#automate for all opinions. Try to figure out dates for `purchased`