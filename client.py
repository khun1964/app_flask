import os
import json
import feedparser
import requests
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

@app.route('/')
def home():
    feeds = get_data("feeds")
    return render_template('home.html', feeds=feeds)        
        
@app.route('/show/<int:id>')
def show(id):
    feed = get_data(f"feeds/{id}/metadata")
    articles = get_data(f"feeds/{id}")
    
    return render_template('show.html', feed=feed,  articles=articles)
        
def get_data(path):
    url = f"http://load_balancer/{path}"
    r = requests.get(url)
  
    if r.status_code == 200:
        content = json.loads(r.text)
        return content
    else:
        flash(f"Error retrieving data, status code: {r.status_code, }")