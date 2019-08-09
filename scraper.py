import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import re
import datetime
import sqlite3
import time
import os

f1 = []
f2 = []
f1_odds = []
f2_odds = []

def scrape_data():
    # set up page to extract table
    data = requests.get("https://www.oddschecker.com/ufc-mma")
    soup = BeautifulSoup(data.text, 'html.parser')

    table = soup.find('table' , {'class': 'all-odds-click'})

    header =table.find_all('tr' , {'class': 'hda-header'})

    fighter = table.find_all('td', {'class': 'all-odds-click'})

    c=fighter[0].text.strip()
    d=fighter[1].text.strip()

    f1.append(c)
    f2.append(d)


    odds = table.find_all('td', {'class': 'basket-add'})


    a=odds[0].text.strip()
    b=odds[1].text.strip()

    f1_odds.append(a)
    f2_odds.append(b)


    return None

def create_df():
    df = pd.DataFrame()
    df["Fighter1"]= f1
    df["Fighter1_Odds"] = f1_odds
    df["Fighter2"]= f2
    df["Fighter2_Odds"]= f2_odds

    return df

scrape_data()
df = create_df()

conn = sqlite3.connect('data.sqlite')
df.to_sql('data', conn, if_exists='replace')
print('Db successfully constructed and saved')
conn.close()
