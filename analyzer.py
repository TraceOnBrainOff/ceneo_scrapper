import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
print(os.listdir("./opinions_json"))

product_id = input("Podaj id: ")
opinions = pd.read_json('./opinions_json/'+product_id+'.json') #for testing
opinions = opinions.set_index('opinion_id')

opinions["stars"] = opinions["stars"].map(lambda x: float(x.split('/')[0].replace(',', '.')))

stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0,5.1,0.5)), fill_value=0)
fig, ax = plt.subplots()

stars.plot.bar()
plt.show()
print(stars)

recommendation = opinions["recommendation"].value_counts()
fig, ax = plt.subplots()
recommendation.plot.pie(label='', autopct='%.1f%%', colors =["mediumseagreen", 'coral'])
ax.set_title("Rekomendacje")
plt.savefig("./figures_png/"+product_id+'_pie.png')
plt.close()

stars_average = opinions['stars'].mean()
pros = opinions['pros'].count()
cons = opinions['cons'].count()
purchased = opinions['purchased'].sum()
print(stars_average, pros, cons, purchased)

stars_purchased = pd.crosstab(opinions['stars'], opinions['purchased'])
