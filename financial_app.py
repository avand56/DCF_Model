from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from DCF_Plots import run_mcs, do_plot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('hi.html')

@app.route('/stocks', methods=['POST', 'GET'])
def cb():
        return gm(request.args.get('data'))

def gm(data):
    
    symbol=data['symbol']
    growth_rate=data['growth_rate']
    terminal_growth=data['terminal_growth']
    iterations=data['iterations']
    risk_free_rate=data['risk_free_rate']
    beta=data['beta']
    market_rate_return=data['market_rate_return']

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
