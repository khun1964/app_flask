# Exemple d'application web crud avec python flask

# Détails de l'application
Cette application Flask permet de gérer des flux RSS. Elle utilise une base de données SQLite pour stocker les informations des flux, et permet d'ajouter, de modifier et de supprimer des flux. Les articles associés à chaque flux sont récupérés grâce à la bibliothèque feedparser.


## Utilisation et documentation

L'application contient les routes suivantes :

- `/` : page d'accueil qui affiche tous les flux RSS enregistrés
- `/show/<int:id>` : affiche un flux RSS spécifique ainsi que les articles associés
- `/new` : permet d'ajouter un nouveau flux RSS
- `/edit/<int:id>` : permet de modifier un flux RSS existant
- `/delete/<int:id>` : permet de supprimer un flux RSS existant
- `/upload` : permet d'importer des flux RSS à partir d'un fichier JSON

L'application utilise également la bibliothèque Flask-Swagger-UI pour afficher la documentation de l'API. La documentation est disponible à l'adresse `/docs`.

## Exemples d'utilisation

```python
# Ajout d'un nouveau flux RSS
@app.route('/new', methods=['POST'])
def add_feed():
    name = request.form['name']
    url = request.form['url']
    image = request.form['image']
    feed = RssFeed(name=name, url=url, image=image)
    db.session.add(feed)
    db.session.commit()
    flash('Feed added successfully!', 'success')
    return redirect(url_for('home'))

# Modification d'un flux RSS
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    feed = RssFeed.query.get(id)
    name = request.form['name']
    url = request.form['url']
    image = request.form['image']
    feed.name = name
    feed.url = url
    feed.image = image
    db.session.commit()
    flash('Feed updated successfully!', 'success')    
    return redirect(url_for('home'))

# Suppression d'un flux RSS
@app.route('/delete/<int:id>')
def delete(id):
    feed = RssFeed.query.get(id)
    db.session.delete(feed)
    db.session.commit()
    flash('Feed deleted successfully!', 'success')
    return redirect(url_for('home'))
```

## Installation

Pour installer et exécuter l'application :*
1. Installer Python sur votre environnement de travail
2. Installer les dépendances en exécutant la commande `pip install -r requirements.txt`
3. Exécuter l'application avec la commande `flask --app main run`
4. Rendez-vous sur à l'adresse locale 127.0.0.1:5000

## Auteurs
poei Dev칠ops
