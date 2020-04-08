import os
import pandas as pd
print(os.listdir("./opinions_json"))

product_id = input("Podaj id: ")
opinions = pd.read_json('./opinions_json/'+product_id[0]+'.json') #for testing
opinions = opinions.set_index('opinion_id')

print(opinions)