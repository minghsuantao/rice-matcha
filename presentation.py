 
from flask import Flask, render_template, request
import random
import requests
import sqlite3
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    cur.execute('Select CityName from Attraction GROUP BY CityName')
    results = cur.fetchall()
    length = len(results)

    #print(results)
    conn.close()
    return render_template('index.html',results= results, length=length)

@app.route('/text', methods=['POST'])
def handle_the_form():  
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    city = request.form["cities"]
    cur.execute(f"SELECT Text from City WHERE CityName = '{city}' ")
    text_result = cur.fetchall()[0][0]
    
    print(text_result)
    conn.close()
    return render_template('text.html',city = city, text = text_result)

@app.route('/attraction/<city>')
def attraction(city):
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    print(city)
    cur.execute(f"Select AttractionName, Category, Rating, Review, CityName from Attraction WHERE CityName = '{city}'")
    results = cur.fetchall() #a list of five attractions

    #print(results)
    conn.close()
    return render_template('attraction.html',city = city, results= results)


@app.route('/plot_avg_rating')
def plot_rating():
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    cur.execute('Select CityName, avg(rating) from Attraction GROUP BY CityName Order by avg(rating)')
    results = cur.fetchall()
    conn.close()

    x_vals = []
    y_vals = []
    for (cityname, avg_rating) in results:
        x_vals.append(cityname)
        y_vals.append(avg_rating)
    bars_data = go.Bar(
        x=x_vals,
        y=y_vals
    )
    fig = go.Figure(data=bars_data)
    div = fig.to_html(full_html=False)
    return render_template("plot_avg_rating.html", plot_div=div)

@app.route('/plot_avg_reviews')
def plot_review():
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    cur.execute('Select CityName, avg(review) from Attraction GROUP BY CityName Order by avg(review)')
    results = cur.fetchall()
    conn.close()

    x_vals = []
    y_vals = []
    for (cityname, avg_review) in results:
        #print(cityname, avg_review)
        x_vals.append(cityname)
        y_vals.append(avg_review)
    bars_data = go.Bar(
        x=x_vals,
        y=y_vals
    )
    fig = go.Figure(data=bars_data)
    div = fig.to_html(full_html=False)
    return render_template("plot_avg_reviews.html", plot_div=div)


if __name__ == '__main__':
    app.run(debug=True)


