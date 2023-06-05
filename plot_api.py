from flask import Flask, send_file, make_response, render_template 
from DCF_Plots import run_mcs, do_plot
import matplotlib.pyplot as plt
from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
app = Flask(__name__)

@app.route('/plots/DCF/DCF_Histograms', methods=['GET','POST'])
def Historgram_Sim():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        growth_rate = request.form.get('growth_rate')
        terminal_growth = request.form.get('terminal_growth')
        iterations = request.form.get('iterations')
        risk_free_rate = request.form.get('risk_free_rate')
        beta = request.form.get('beta')
        div = request.form.get('div')
        market_rate_return = request.form.get('market_rate_return')
        

    # choose a ticker symbol
    symbol = 'MSFT' # get user
    growth_rate=0.1 # get from user
    terminal_growth=0.025
    iterations = 10000 
    risk_free_rate = 0.038 #%, 10 year treasury
    beta = 1.3 # similar to volatility
    div = 0.02 # S&P500 dividend return
    market_rate_return = 0.075 + div #S&P500 historical return + dividends
    st = yf.Ticker(symbol)

    output_distribution=run_mcs(
        symbol, 
        growth_rate, 
        terminal_growth, 
        iterations, 
        risk_free_rate, 
        beta,
        market_rate_return
        )

    bytes_obj = do_plot(output_distribution)

    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=False)
