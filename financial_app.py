from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from DCF_Plots import run_mcs, do_plot

app = Flask(__name__)

@app.route('/callback/<endpoint>', methods=['POST', 'GET'])
def cb(endpoint):
    if endpoint == "getStock":
        return gm(request.args.get('stock'),request.args.get('growth_rate'),request.args.get('terminal_growth'),request.args.get('iterations'),request.args.get('risk_free_rate'),request.args.get('beta'),request.args.get('market_rate_return'))
    else:
        return "Bad endpoint", 400
   
@app.route('/')
def index():
    return render_template('index4.html')

def gm(symbol='MSFT',growth_rate=0.10, terminal_growth=0.025, iterations=10000, risk_free_rate=0.04, beta=1, market_rate_return=0.075):

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
