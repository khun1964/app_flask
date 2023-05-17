import os
import json
import feedparser
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

# Configuration de l'URI de la base de données et désactivation du suivi des modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fluxrss.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
#Oui je sais...
app.secret_key = '07671C8CA4CC9D8A660B9DDD23F0D75C7260ED385A10267074569F1C452B8441'


# @app.before_request
# def create_table():
#     db.create_all()
    

SWAGGER_URL = '/docs' 
API_URL = '/static/swagger.json' 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "app_flask"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    

db = SQLAlchemy(app)


class RssFeed(db.Model):
    """
Class RssFeed hérite de db.Model pour modeler un flux RSS.

Attributs:
    id (int): id pour chaque flux RSS (primary_key).
    name (str): Nom du flux RSS, ne peut pas être nul.
    url (str): URL du flux RSS, ne peut pas être nul.
    image (str): URL de l'image associée au flux RSS (optionnel).

        -aucune relation

Méthodes:
    __repr__(self): Retourne une représentation sous forme de chaîne de caractères de l'objet RssFeed.
"""
    
    __tablename__= "rssFeed"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))
    
    def __init__(self, id, name, url, image):
        self.id = id
        self.name = name
        self.url = url
        self.image = image
        
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}    
        
    def __repr__(self):
        return f'<RssFeed {self.id}: {self.name}>'

@app.route('/feeds')
def get_all_feeds():
    feeds = RssFeed.query.all()
    response = [f.as_dict() for f in feeds]
    return response

@app.route('/feeds/<int:id>', methods=['GET'])
def get_one_feed(id):
    feed = RssFeed.query.get(id)
    articles = fetch_feed(feed.url)
    return jsonify(articles)

@app.route('/feeds/<int:id>/metadata', methods=['GET'])
def get_feed_metadata(id):
    feed = RssFeed.query.get(id)
    return feed.as_dict()

@app.route('/show/<int:id>', methods=['GET'])
def show(id):
    """
    Fonction show() pour afficher un flux RSS spécifique et ses articles.

    Args:
        id (int): Identifiant du flux RSS.

    Returns:
        str: Rendu du template 'show.html' avec les détails du flux RSS et la liste des articles.
    """
    
    feed = RssFeed.query.get(id)
    
    articles = fetch_feed(feed.url)
    
    if int(id):
        return render_template('show.html', feed=feed, articles=articles)
    else:
        flash('Unknown feed or articles', 'error')
        return redirect(url_for('home')) 

@app.route('/new', methods=['POST', 'GET'])
def add_feed():
    """
    Fonction add_feed() pour ajouter un nouveau flux RSS. Gère les requêtes GET et POST.

    Returns:
        str: Rendu du template 'new.html' en cas de requête GET, ou redirection vers la page d'accueil après l'ajout en cas de requête POST.
    """
    if request.method == 'GET':
        return render_template('new.html')
    name = request.form['name']
    url = request.form['url']
    image = request.form['image']
    feed = RssFeed(name=name, url=url, image=image)
    db.session.add(feed)
    db.session.commit()
    flash('Feed added successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    """
    Fonction edit() pour modifier un flux RSS existant. Gère les requêtes GET et POST.

    Args:
        id (int): Identifiant du flux RSS à modifier.

    Returns:
        str: Rendu du template 'new.html' en cas de requête GET, ou redirection vers la page d'accueil après la mise à jour en cas de requête POST.
    """
    
    feed = RssFeed.query.get(id)
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        image = request.form['image']
        feed.name = name 
        feed.url = url 
        feed.image = image
        db.session.commit()
        flash('Feed updated successfully!', 'success')    
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        return render_template('new.html', feed=feed)

@app.route('/delete/<int:id>')
def delete(id):

    """
        Fonction delete() pour supprimer un flux RSS.

        Args:
            id (int): Identifiant du flux RSS à supprimer.

        Returns:
            str: Redirection vers la page d'accueil après la suppression.
    """
    
    feed = RssFeed.query.get(id)
    db.session.delete(feed)
    db.session.commit()
    flash('Feed deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    
    """Fonction upload() pour importer des flux RSS à partir d'un fichier JSON. Gère les requêtes GET et POST

    str: Rendu du template 'upload.html' en cas de requête GET, ou redirection vers la page d'accueil après la mise à jour en cas de requête POST.
    """
    
    if request.method == 'GET':
        return render_template('upload.html')
    
    file = request.files['file']
    if not file or file.filename == '':
        flash('No file selected for uploading', 'error')
        return redirect(url_for('upload'))

    if not file.filename.endswith('.json'):
        flash('Invalid file format. Please upload a JSON file', 'error')
        return redirect(url_for('upload'))
    
    try:
        data = json.load(file)
        print(type(data))
        for feed_data in data:
            name = feed_data.get('name')
            url = feed_data.get('url')
            if not name or not url:
                raise ValueError('Missing required fields in feed object')
            image = feed_data.get('image')
            feed = RssFeed(name=name, url=url, image=image)
            db.session.add(feed)
        db.session.commit()
        flash('File uploaded successfully!', 'success')
    except Exception as e:
        flash('Error uploading file: {}'.format(str(e)), 'error')
    
    return redirect(url_for('home'))

def fetch_feed(url):
    feed = feedparser.parse(url)
    articles = []
    for f in feed.entries:
        article = {
            'title': f.title,
            'link': f.link,
        }
        articles.append(article)
        
    return articles


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

