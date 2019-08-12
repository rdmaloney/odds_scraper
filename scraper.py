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

links = []
alphabets = sorted(set(string.ascii_lowercase))

f1 = []
f2 = []
f1_odds = []
f2_odds = []


def scrape_data():
    data = requests.get("https://sports.williamhill.com/betting/en-gb/ufc")
    soup = BeautifulSoup(data.text, 'html.parser')
    links = soup.find_all('a',{'class': 'btmarket__name btmarket__name--featured'}, href=True)

    for link in links:
        
        links.append(link.get('href'))

        for link in links:
            print(f"Now currently scraping link: {link}")

            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'html.parser')
            time.sleep(1)            

            fighters = soup.find_all('p', {'class': "btmarket__name"})
            c = fighters[0].text.strip()
            d = fighters[1].text.strip()

            f1.append(c)
            f2.append(d)

            odds = soup.find_all('span', {'class': "betbutton_odds"})

            a = odds[0].text.strip()
            b = odds[1].text.strip()

            f1_odds.append(a)
            f2_odds.append(b)

        return None

    def create_df():
        df = pd.DataFrame()
        df["Fighter1"] = f1
        df["Fighter1_Odds"] = f1_odds
        df["Fighter2"] = f2
        df["Fighter2_Odds"] = f2_odds

        return df

    scrape_data()
    df = create_df()

    conn = sqlite3.connect('data.sqlite')
    df.to_sql('data', conn, if_exists='replace')
    print('Db successfully constructed and saved')
    conn.close()
