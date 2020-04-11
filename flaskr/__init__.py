from flask import Flask, render_template

import sqlite3
import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # page principale
    @app.route('/')
    def index():
        return render_template('index.html')

    #premier graphique sur le covid19
    @app.route('/graph0')
    def graph_covid():
        fileCSV = open('data-covid/total_cases.csv','r')
        
        pays0 = fileCSV.readline().replace('\n','') # on lit la 1ere ligne (liste des pays)
        pays1 = pays0.split(',')
        nombre_pays = len(pays1)-2 # nombre de pays
        liste_pays = pays1[2:nombre_pays+2] # liste de tous les pays
        
        
        last_day = fileCSV.readlines()[-1].replace('\n','') # on lit la derniere ligne
        liste_last_day = last_day.split(',')
        nombre_pays_infecte = len(liste_last_day)-2 # nombre de pays infectes le dernier jour
        liste_cas_last_day = liste_last_day[2:nombre_pays_infecte+2] # liste du nombre de cas par pays le dernier jour
        
        graphique = 'bar'
        
        return render_template('graphs/graph.html', type = graphique, labels = str(liste_pays), data = str(liste_cas_last_day))

    #premier graphique sur les donnees inginious
    #soumissions au cours du temps pour LSINF1101-PYTHON
    
    @app.route('/graph1')
    def graph_test_inginious():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        xy = {}

        for row in cursor.execute("SELECT submitted_on from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_dayDate = current_date_formated.strftime("%d-%m-%Y") # '02-16-2020'
            if current_dayDate not in xy:
                xy[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                xy[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
        
        submissions_dates = list(xy.keys())
        submissions_nbr = list(xy.values())
            
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graphique = 'line'
        titre_page = 'Soumissions Python'
        
        return render_template('graphs/graph-ingi-test.html', titre = titre_page, type = graphique, labels = str(submissions_dates), data = str(submissions_nbr))

    #version simplifiée
    @app.route('/graph1s')
    def graph_test_inginiousS():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        xy = {}

        for row in cursor.execute("SELECT submitted_on from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_dayDate = current_date_formated.strftime("%B %Y") # February 2020
            if current_dayDate not in xy:
                xy[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                xy[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
        
        submissions_dates = list(xy.keys())
        submissions_nbr = list(xy.values())
            
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graphique = 'bar'
        titre_page = 'Soumissions Python (mois)'
        
        return render_template('graphs/graph-ingi-test.html', titre = titre_page, type = graphique, labels = str(submissions_dates), data = str(submissions_nbr))
        
    return app
    
    """
    for row in cursor.execute("SELECT count(*) from user_tasks WHERE task = 'BinarySearch' AND succeeded = 'true' "):
        print(row[0])
    """
