from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from DCF_Plots import run_mcs, do_plot

app = Flask(__name__)

# Define the root route
@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/callback/<endpoint>')
def cb(endpoint):   
    if endpoint == "getStock":
        return gm(request.args.get('stock'),request.args.get('growth_rate'),request.args.get('terminal_growth'),request.args.get('iterations'),request.args.get('risk_free_rate'),request.args.get('beta'),request.args.get('market_rate_return'))
    elif endpoint == "getInfo":
        ticker = request.args.get('data')
        stock = request.args.get('stock')
        growth_rate = request.args.get('growth_rate')
        terminal_growth = request.args.get('terminal_growth')
        iterations = request.args.get('iterations')
        risk_free_rate = request.args.get('risk_free_rate')
        beta = request.args.get('beta')
        market_rate_return = request.args.get('market_rate_return')
        st = yf.Ticker(ticker)
        return json.dumps(st.info, stock, growth_rate, terminal_growth, iterations, risk_free_rate, beta, market_rate_return)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph
def gm(symbol,growth_rate, terminal_growth, iterations, risk_free_rate, beta, market_rate_return):

    output_distribution=run_mcs(
        symbol, 
        growth_rate, 
        terminal_growth, 
        iterations, 
        risk_free_rate, 
        beta,
        market_rate_return
        )
  
    # Create a histogram
    fig = px.histogram(output_distribution,
        nbins=50, template="seaborn")

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON