from flask import Flask, config, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))
   
@app.route('/')
def index():
    return render_template('chartsajax.html',  graphJSON=gm())

def gm(country='United Kingdom'):
    df = pd.DataFrame(px.data.gapminder())

    fig = px.line(df[df['country']==country], x="year", y="gdpPercap")
    
    
    

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(fig.data[0])
    #fig.data[0]['staticPlot']=True
    
    return graphJSON




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
