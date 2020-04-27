
from flask import Flask, render_template
import random
import requests
import sqlite3
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/plot')
def plot():
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    cur.execute('Select CityName, avg(rating), avg(review) from Attraction GROUP BY CityName')
    results = cur.fetchall()
    conn.close()

    x_vals = []
    y_vals = []
    for (cityname, avg_rating, avg_review) in results:
        x_vals.append(cityname)
        y_vals.append(avg_rating)
    bars_data = go.Bar(
        x=x_vals,
        y=y_vals
    )
    fig = go.Figure(data=bars_data)
    div = fig.to_html(full_html=False)
    return render_template("plot.html", plot_div=div)

if __name__ == '__main__':
    app.run(debug=True)


