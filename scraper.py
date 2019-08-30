import requests
import pandas as pd
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
import string
import re
import os
import time
from math import *
from fractions import Fraction

links = []
alphabets = sorted(set(string.ascii_lowercase))

f1 = []
f2 = []
f1_odds = []
f2_odds = []


def safe_eval(expr):
    try:
        return round(eval(expr), 2)
    except:
        return expr


def frac(express):
    if express == 'EVS':

        return express == '1'
    else:
        tokens = express.split('/')
        t1 = int(tokens[0])
        t2 = int(tokens[1])
        return t1 / t2




def scrape_data():
    data = requests.get("https://sports.williamhill.com/betting/en-gb/ufc")
    soup = BeautifulSoup(data.text, 'html.parser')
    divs = soup.findAll("div", {"class": "event"})
    for div in divs:
        link = div.findAll('a')[0]
        names = link.findAll('span')
        p1 = names[0].text
        p2 = names[1].text
        buttons_having_odds = div.findAll('button')
        p1_odds_frac = frac(buttons_having_odds[0]["data-odds"])
        p2_odds_frac = frac(buttons_having_odds[1]["data-odds"])
        p1_odds = (p1_odds_frac)
        p2_odds = (p2_odds_frac)
        f1.append(p1)
        f2.append(p2)
        f1_odds.append(p1_odds)
        f2_odds.append(p2_odds)

        scrape_data()


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
