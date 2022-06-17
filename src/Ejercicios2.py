
# Step 3
import requests
from urllib.request import urlopen, Request

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

#request = Request(url)

html_data = urlopen(request)

html = html_data.read()
print(html)

#print(type(html_data))
html_data.close()

# Step 4

from bs4 import BeautifulSoup







