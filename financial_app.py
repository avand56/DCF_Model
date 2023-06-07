from flask import Flask, config, render_template, request,redirect, url_for
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
from DCF_Plots import run_mcs, do_plot

app = Flask(__name__)

@app.route('/stocks', methods = ['POST', 'GET'])
def cb():
        return gm(request.form.get('symbol'),request.form.get('growth_rate'),request.form.get('terminal_growth'),request.form.get('iterations'),request.form.get('risk_free_rate'),request.form.get('beta'),request.form.get('market_rate_return'))
    
@app.route('/')
def index():
    return render_template('try.html')

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
