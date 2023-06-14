from flask import Flask, config, render_template, request, redirect, url_for
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from DCF_Plots import run_mcs, do_plot

app = Flask(__name__)

@app.route('/stocks', methods = ['POST', 'GET'])
def cb():
    return gm(request.args.get('data'), float(request.args.get('growth_rate'))) #, float(request.args.get('terminal_growth')), float(request.args.get('iterations')), float(request.args.get('risk_free_rate')), float(request.args.get('beta')), float(request.args.get('market_rate_return')))

    
@app.route('/')
def index():
    return render_template('charts.html')

def gm(symbol="MSFT", growth_rate = 0.10):#, terminal_growth = 0.04, iterations = 10000.0,  risk_free_rate = 0.04, beta = 1.00, market_rate_return = 0.08):

    output_distribution=run_mcs(
        symbol, 
        growth_rate, 
        0.04,
        10000,
        0.04,
        1.0,
        0.08
        )
  
    # Create a histogram
    fig = px.histogram(output_distribution,
        nbins=50, template="seaborn")

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
