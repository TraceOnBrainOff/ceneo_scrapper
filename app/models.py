#import bibliotek
import requests
from bs4 import BeautifulSoup
import textwrap
import json
from utils import extract_element, remove_whitespaces

class Product:
    def __init__(self, product_id = None, name = None, opinions = []):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions
    def __str__(self):
        return f'Product id: {self.product_id}\nName: {self.name}\nOpinions:\n'+"\n".join(textwrap.indent(str(opinion),"    ") for opinion in self.opinions)
    def __repr__(self):
        pass
    def extract_product(self):
        url_prefix = "https://www.ceneo.pl"
        url_postfix = "#tab=reviews"
        url = url_prefix+"/"+self.product_id+url_postfix
        page_respons = requests.get(url)
        page_tree = BeautifulSoup(page_respons.text, 'html.parser')
        self.name = extract_element(page_tree,"h1","product-name") 
        try:
            opinions_count = int(extract_element(page_tree,"a","product-reviews-link","span"))
        except AttributeError:
            opinions_count = 0
        if opinions_count > 0:
            while url:
                #poranie kodu html strony zpodanego URL
                page_respons = requests.get(url)
                page_tree = BeautifulSoup(page_respons.text, 'html.parser')

                #wydobycie z kodu HTML strony fragmentów odpowiadajcych poszczególnym opiniom 
                opinions = page_tree.find_all("div", "js_product-review")

                #wydobycie składowych dla pojedynczej opinii
                for opinion in opinions:
                    op = Opinion()
                    op.extract_opinion(opinion)
                    op.transform_opinion()
                    self.opinions.append(op)
                try:
                    url = url_prefix+page_tree.find("a", "pagination__next")["href"]
                except TypeError:
                    url = None
    def save_product(self):
        with open("./opinions_json/"+self.product_id+'.json', 'w', encoding="utf-8") as fp:
            json.dump(self.opinions, fp, ensure_ascii=False, indent=4, separators=(',', ': '))

class Opinion:
    #słownik z składowymi opinii i ich selektorami
    tags = {
        "recommendation":["span","user-post__author-recomendation","em"],
        "stars":["span", "user-post__score-count"],
        "content":["div","user-post__text"],
        "author":["span", "user-post__author-name"], 
        "useful":["button","vote-yes", "span"],
        "useless":["button","vote-no", "span"],
        "purchased":["div", "review-pz", "em"]
    }
    
    #definicja klnstruktora (inicjalizatora) klasy Opinion
    def __init__(self, opinion_id=None, author=None, recommendation=None, stars=None, content=None, pros=None, cons=None, 
                 useful=None, useless=None, purchased=None, purchase_date=None, review_date=None):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.useful = useful
        self.useless = useless
        self.purchased = purchased
        self.purchase_date = purchase_date
        self.review_date = review_date
    def __str__(self):
        return f'Opinion id: {self.opinion_id}\nAuthor: {self.author}\nStars: {self.stars}\nZalety: {self.pros}\n'
    def __repr__(self):
        pass
    def extract_opinion(self, opinion):
        for key, args in self.tags.items():
            setattr(self, key, extract_element(opinion, *args))   
        self.opinion_id = int(opinion["data-entry-id"])
        try:
            self.pros = ", ".join(pros.get_text().strip() for pros in opinion.find("div", "review-feature__title--positives").find_next_siblings("div","review-feature__item"))
        except AttributeError:
            self.pros = None
        try:
            self.cons = ", ".join(pros.get_text().strip() for pros in opinion.find("div", "review-feature__title--negatives").find_next_siblings("div","review-feature__item"))
        except AttributeError:
            self.cons = None
        dates = opinion.find("span", "user-post__published").find_all("time")
        self.review_date = dates.pop(0)["datetime"]
        try:
            self.purchase_date = dates.pop(0)["datetime"]
        except IndexError:
            self.purchase_date = None
    def transform_opinion(self):
        self.purchased = (self.purchased=="Opinia potwierdzona zakupem")
        self.useful = int(self.useful)
        self.useless = int(self.useless)
        self.content = remove_whitespaces(self.content)

product = Product("79688141")
product.extract_product()
print(product)