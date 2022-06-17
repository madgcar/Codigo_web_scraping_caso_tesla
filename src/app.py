# your app code here

# Step 2
print("Hello world")

# Step 3
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import sqlite3

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

html_data = requests.get(url).text
#print(html_data)

#step 4

result = BeautifulSoup(html_data,"html.parser")
#print(result)

# Step 5

Tablas = result.find_all("table")
#print(Tablas)

for index,table in enumerate(Tablas):
    if ("Tesla Quarterly Revenue" in str(table)):
        Tablas_index = index
#print(my_index)

# create DataFrame Tesla
Tesla = pd.DataFrame(columns=['Date','Revenue'])

for row in Tablas[Tablas_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$","").replace(",","")
        Tesla = Tesla.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)
#print(Tesla)

# Para saber cuantos Nan tengo en Revenue

#Tesla["Revenue"].isna()

Tesla_revenue = Tesla[Tesla['Revenue'] != ""]
#print(Tesla_revenue)

# Elimino toda la fila ojo con esto

# Step 6
#Make sure tesla_revenue is still a dataframe

#print(type(Tesla_revenue))

#Insert the data into sqlite3 by converting the dataframe into a list of tuples
valores = Tesla_revenue.to_records(index=False)
Lis_valores = list(valores)
#print(Lis_valores)


# Step 8
# first create data base in Heroku 
# I used Postgres 4.0
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd 
import os

#load_dotenv()

#connection_string= os.getenv('sqltesladb')
#print(connection_string)
#engine = create_engine(connection_string)
#engine.connect()
import sqlite3
conn = sqlite3.connect('sqltesladb.db')
c = conn.cursor()

c.execute('''CREATE TABLE revenue(Date, Revenue)''')

#Inserte los valores en una base de datos de sql

#engine = create_engine('sqlite://', echo = False)
#Tesla_revenue.to_sql('Tesla', con=engine)
#engine.execute('SELECT * FROM Tesla').fetchall()

c.executemany('INSERT INTO revenue VALUES(?,?)', Lis_valores)

conn.commit()

# Step 9: Now retrieve the data from the database
for row in c.execute('SELECT * FROM revenue'):
    print(row)

# Step 10: Finally create a plot to visualize the data
#What kind of visualizations show we do?
import matplotlib.pyplot as plt 
df = pd.read_sql('SELECT * FROM revenue', conn)
df['Revenue'].hist()



