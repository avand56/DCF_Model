from dcf_helper_functions import (
    parse_rows, 
    get_page, 
    scrape_table, 
    clean_data, 
    scraping, 
    predict_sales, 
    compute_terminal_value,
    compute_discount_factors, 
    compute_wacc, 
    compute_dcf_value
)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests
from sklearn.linear_model import LinearRegression

def run_mcs(symbol, growth_rate, terminal_growth, iterations, risk_free_rate, beta,market_rate_return):
    cash, bal, fin = scraping(symbol)
    sales, years = predict_sales(fin, growth_rate)
    debt=bal['Total Debt'][2]
    cost_debt = fin['Net Interest Income'][2]/debt
    ebitda_margin = fin['Normalized EBITDA'][2]/sales[0]
    depr_percent = fin['Reconciled Depreciation'][2]/sales[0]
    ebitda = sales * ebitda_margin
    depreciation = sales * depr_percent
    ebit = ebitda - depreciation
    nwc_percent = bal['Working Capital'][2]/sales[0]
    nwc = sales * nwc_percent
    change_in_nwc = nwc.shift(1) - nwc 
    capex_percent = depr_percent
    #capex = cash['Capital Expenditure'] #-(sales * capex_percent)
    capex = -(sales * capex_percent)
    tax_rate = 0.21
    tax_payment = -ebit * tax_rate
    tax_payment = tax_payment.apply(lambda x: min(x, 0))
    #free_cash_flow = cash['Free Cash Flow'] #ebit + depreciation + tax_payment + capex + change_in_nwc
    free_cash_flow = ebit + depreciation + tax_payment + capex + change_in_nwc
    equity = bal['Common Stock Equity'][2]
    risk_premium = market_rate_return -risk_free_rate
    cost_equity = risk_free_rate + beta * risk_premium
    cost_of_capital = compute_wacc(cost_debt, tax_rate, debt, equity, cost_equity)
    terminal_value = compute_terminal_value(cost_of_capital, terminal_growth, free_cash_flow)
    discount_factors = compute_discount_factors(cost_of_capital)
    dcf_value, output = compute_dcf_value(free_cash_flow, discount_factors, terminal_value, sales, ebit)
    
    # Create probability distributions
    sales_growth_dist = np.random.normal(loc=growth_rate, scale=0.01, size=iterations)
    ebitda_margin_dist = np.random.normal(loc=ebitda_margin, scale=0.02, size=iterations)
    nwc_percent_dist = np.random.normal(loc=nwc_percent, scale=0.01, size=iterations)

    # Calculate DCF value for each set of random inputs
    output_distribution = []
    for i in range(iterations):
        for year in range(1, 6):
            sales[year] = sales[year - 1] * (1 + sales_growth_dist[0])
        ebitda = sales * ebitda_margin_dist[i]
        depreciation = (sales * depr_percent)
        ebit = ebitda - depreciation
        nwc = sales * nwc_percent_dist[i]
        change_in_nwc = nwc.shift(1) - nwc 
        capex = -(sales * capex_percent)
        tax_payment = -ebit * tax_rate
        tax_payment = tax_payment.apply(lambda x: min(x, 0))
        free_cash_flow = ebit + depreciation + tax_payment + capex + change_in_nwc
    
        # DCF valuation
        terminal_value = ((free_cash_flow[-1] * (1 + terminal_growth)) / 
                    (cost_of_capital - terminal_growth))
        free_cash_flow[-1] += terminal_value
        discount_factors = compute_discount_factors(cost_of_capital)
        dcf_value = sum(free_cash_flow[1:] * discount_factors)
        output_distribution.append(dcf_value)

    return output_distribution

def do_plot(output_distribution
        ):

    plt.hist(output_distribution, 
        bins=50, 
        density=True, 
        color="r")
    plt.xlabel('Market Capitalization ($1000)')
    plt.ylabel('Counts')
    plt.title('Monte Carlo Simulation of DCF Model')

    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
    