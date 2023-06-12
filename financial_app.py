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
    return gm(request.args.get('data'), request.args.get('growth_rate'))

    
@app.route('/')
def index():
    return render_template('charts.html')

def gm(symbol="MSFT", growth_rate = 0.10):

    output_distribution=run_mcs(
        symbol, 
        growth_rate, 
        0.04, 
        10000, 
        0.04, 
        1.00,
        0.08
        )
  
    # Create a histogram
    fig = px.histogram(output_distribution,
        nbins=50, template="seaborn", x='Market Cap', y="Simulation Outcomes",title="Stock Market Cap Valuation")

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
