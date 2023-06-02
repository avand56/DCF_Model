import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.model_selection
import sklearn.linear_model
from scipy.stats import t
import yfinance as yf
import requests
import io
from lxml import html
import requests
import json
import argparse
from collections import OrderedDict
import io

def get_page(url):
    # Set up the request headers that we're going to use, to simulate
    # a request by the Chrome browser. Simulating a request from a browser
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Pragma': 'no-cache',
        'Referrer': 'https://google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }

    return requests.get(url, headers=headers)

def parse_rows(table_rows):
    parsed_rows = []

    for table_row in table_rows:
        parsed_row = []
        el = table_row.xpath("./div")

        none_count = 0

        for rs in el:
            try:
                (text,) = rs.xpath('.//span/text()[1]')
                parsed_row.append(text)
            except ValueError:
                parsed_row.append(np.NaN)
                none_count += 1

        if (none_count < 4):
            parsed_rows.append(parsed_row)
            
    return pd.DataFrame(parsed_rows)


def clean_data(df):
    df = df.set_index(0) # Set the index to the first column: 'Period Ending'.
    df = df.transpose() # Transpose the DataFrame, so that our header contains the account names
    
    # Rename the "Breakdown" column to "Date"
    cols = list(df.columns)
    cols[0] = 'Date'
    df = df.set_axis(cols, axis='columns', inplace=False)
    
    numeric_columns = list(df.columns)[1::] # Take all columns, except the first (which is the 'Date' column)

    for column_index in range(1, len(df.columns)): # Take all columns, except the first (which is the 'Date' column)
        df.iloc[:,column_index] = df.iloc[:,column_index].str.replace(',', '') # Remove the thousands separator
        df.iloc[:,column_index] = df.iloc[:,column_index].astype(np.float64) # Convert the column to float64
        
    return df

def scrape_table(url):
    # Fetch the page that we're going to parse
    page = get_page(url)

    # Parse the page with LXML, so that we can start doing some XPATH queries
    # to extract the data that we want
    tree = html.fromstring(page.content)

    # Fetch all div elements which have class 'D(tbr)'
    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")
    
    # Ensure that some table rows are found; if none are found, then it's possible
    # that Yahoo Finance has changed their page layout, or have detected
    # that you're scraping the page.
    assert len(table_rows) > 0
    
    df = parse_rows(table_rows)
    df = clean_data(df)
        
    return df

def scraping(symbol):
    #scrape balance sheet
    bal=scrape_table('https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol)

    #scrape the financial statements
    fin=scrape_table('https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol)

    #scrape cash flow
    cash=scrape_table('https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol)

    return cash, bal, fin

def predict_sales(fin, growth_rate):
    years = ['2023A', '2024B', '2025P', '2026P', '2027P','2028P']
    sales = pd.Series(index=years, dtype = 'float64')
    sales['2023A'] = fin['Total Revenue'][1]
    for year in range(1, 6):
        sales[year] = sales[year - 1] * (1 + growth_rate)
    return sales, years

def compute_wacc(cost_dept, tax_rate, dept, equity, cost_equity):
    wacc = (cost_dept*(1-tax_rate)*(dept/(dept+equity)))+(cost_equity*(equity/(dept+equity)))
    return wacc

def compute_terminal_value(cost_of_capital,terminal_growth,free_cash_flow):
    terminal_value = ((free_cash_flow[-1] * (1 + terminal_growth)) / 
                    (cost_of_capital - terminal_growth))
    return terminal_value

def compute_discount_factors(cost_of_capital):
    discount_factors = [(1 / (1 + cost_of_capital)) ** i for i in range (1,6)]
    return discount_factors

def compute_dcf_value(free_cash_flow, discount_factors, terminal_value, sales, ebit):
    dcf_value = (sum(free_cash_flow[1:] * discount_factors) +
                terminal_value * discount_factors[-1])
    output = pd.DataFrame([sales, ebit, free_cash_flow],
        index=['Sales', 'EBIT', 'Free Cash Flow']).round(1)
    return dcf_value, output

def image_save_API():
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
