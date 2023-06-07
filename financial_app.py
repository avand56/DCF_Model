from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from DCF_Plots import run_mcs, do_plot

app = Flask(__name__)

@app.route('/stocks', methods=['POST', 'GET'])
def cb():
        return gm(request.values.get('symbol'),float(request.values.get('growth_rate')),float(request.values.get('terminal_growth')),int(request.values.get('iterations')),float(request.values.get('risk_free_rate')),float(request.values.get('beta')),float(request.values.get('market_rate_return')))

@app.route('/')
def index():
    return render_template('hi.html')

def gm(symbol,growth_rate,terminal_growth,iterations,risk_free_rate,beta,market_rate_return):

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
