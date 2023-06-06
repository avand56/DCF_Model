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
        return gm(request.form.get('data'))

def gm():

    symbol=request.form.get('symbol')
    growth_rate=float(request.form.get('growth_rate'))
    terminal_growth=float(request.form.get('terminal_growth'))
    iterations=int(request.form.get('iterations'))
    risk_free_rate=float(request.form.get('risk_free_rate'))
    beta=float(request.form.get('beta'))
    market_rate_return=float(request.form.get('market_rate_return'))

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
