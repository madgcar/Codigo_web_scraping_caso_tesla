
# Steap 4
import requests
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url)
html_doc = html_data.text
soup = BeautifulSoup(html_doc)
pretty_soup = soup.prettify()
print(pretty_soup)

# Steap 5

soup1 = BeautifulSoup(html_data.content, "html.parser")
#print(soup1)

All_tables = soup1.find_all("table")
#print(All_tables)

#Tabla_Tesla = soup1.find_all("Tesla quarterly revenue")
#print(Tabla_Tesla)

for index,table in enumerate(All_tables):
    if "Tesla Quarterly Revenue" in str(All_tables):
        my_index = index

#print(my_index)

# create the dataframe
import pandas as pd
Tesla = pd.DataFrame(columns=['date','revenue'])
#print(Tesla)
for row in All_tables[my_index].tbody.find_all('tr'):
    col = row.find_all('td')
    if col != "":
        fecha = col[0].text
        ingreso = col[1].text.replace("$","").replace(",","")
        Tesla = Tesla.append({"date":fecha, "revenue":ingreso}, ignore_index=True)

print(Tesla)



