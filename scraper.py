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

    rows = soup.find('table', {"at-12 standard-list"})

    for row in rows:

        fighter = rows.find_all('p', {"fixtures-bet-name beta-footnote"})

        f1.append(fighter[0].text)
        f2.append(fighter[1].text)


        odds = rows.find_all('span', {"odds beta-footnote bold add-to-bet-basket"})

        odds_f1 = float(odds[2].text.strip(" "))
        odds_f2 = float(odds[3].text.strip(" "))

        odds_dict = {}
        odds_dict[odds[0].text]=f1_odds
        odds_dict[odds[1].text]= f2_odds


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
