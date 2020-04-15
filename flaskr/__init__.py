from flask import Flask, render_template, request

import sqlite3
import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    
    
    # N'est pas utilisé pour l'instant.
    # Permet de charger les db au lancement de l'application.
    """
    # Accès à la base de données
    conn = sqlite3.connect('data-inginious/inginious.sqlite')
    
    # Le curseur permettra l'envoi des commandes SQL
    cursor = conn.cursor()
    
    date_format = "%Y-%m-%dT%H:%M:%S"
    
    subs_months = {}
    subs_months_valid = {}

    for row in cursor.execute("SELECT submitted_on from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
        current_date = row[0][:-9] # '2020-02-16T22:57:05'
        current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
        
        current_dayDate = current_date_formated.strftime("%d-%m-%Y") # '02-16-2020'
        if current_dayDate not in subs_days:
            subs_days[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
        else:
            subs_days[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
        current_monthDate = current_date_formated.strftime("%B %Y") # February 2020
        if current_monthDate not in subs_months:
            subs_months[current_monthDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
        else:
            subs_months[current_monthDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
    
    # Toujours fermer la connexion quand elle n'est plus utile
    conn.close()
    """
    
    

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

    """
    @app.route('/graph1')
    def graph_test_inginious():
    
        graph_type = request.args.get('gtype')
        
        if graph_type == None:
            submissions_dates = list(subs_days.keys())
            submissions_nbr = list(subs_days.values())
            graphique = 'line'
            titre_page = 'Soumissions Python'
        elif graph_type == 'month':
            submissions_dates = list(subs_months.keys())
            submissions_nbr = list(subs_months.values())
            graphique = 'bar'
            titre_page = 'Soumissions Python (mois)'
        
        return render_template('graphs/graph_1.html', titre = titre_page, type = graphique, labels = str(submissions_dates), data = str(submissions_nbr))
    """
    
    #premier graphique sur les donnees inginious
    #soumissions au cours du temps pour LSINF1101-PYTHON
    @app.route('/lsinf1101')
    def lsinf1101():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs_days = {}
        subs_days_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_dayDate = current_date_formated.strftime("%Y-%m-%d") #("%d-%m-%Y") # '02-16-2020'
            
            if current_dayDate not in subs_days:
                subs_days[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                subs_days[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
            if row[1] == "success":
                if current_dayDate not in subs_days_valid:
                    subs_days_valid[current_dayDate] = 1
                else:
                    subs_days_valid[current_dayDate] += 1
        
        subm_dates = list(subs_days.keys())
        subm_nbr = list(subs_days.values())
        
        subm_dates_valid = list(subs_days_valid.keys())
        subm_nbr_valid = list(subs_days_valid.values())
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graph = 'line'
        titre_page = 'Soumissions Python'
        cours = 'lsinf1101'
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid)

    
    @app.route('/lsinf1101/months')
    def lsinf1101_months():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs_months = {}
        subs_months_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_monthDate = current_date_formated.strftime("%Y-%m") #("%B %Y") # February 2020
            
            if current_monthDate not in subs_months:
                subs_months[current_monthDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                subs_months[current_monthDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
            if row[1] == "success":
                if current_monthDate not in subs_months_valid:
                    subs_months_valid[current_monthDate] = 1
                else:
                    subs_months_valid[current_monthDate] += 1
        
        subm_dates = list(subs_months.keys())
        subm_nbr = list(subs_months.values())
        
        subm_dates_valid = list(subs_months_valid.keys())
        subm_nbr_valid = list(subs_months_valid.values())
            
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graph = 'bar'
        titre_page = 'Soumissions Python (mois)'
        cours = 'lsinf1101'
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid)
    
    
    @app.route('/lepl1402')
    def lepl1402():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs_days = {}
        subs_days_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = 'LEPL1402' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_dayDate = current_date_formated.strftime("%Y-%m-%d") #("%d-%m-%Y") # '02-16-2020'
            
            if current_dayDate not in subs_days:
                subs_days[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                subs_days[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
            if row[1] == "success":
                if current_dayDate not in subs_days_valid:
                    subs_days_valid[current_dayDate] = 1
                else:
                    subs_days_valid[current_dayDate] += 1
        
        subm_dates = list(subs_days.keys())
        subm_nbr = list(subs_days.values())
        
        subm_dates_valid = list(subs_days_valid.keys())
        subm_nbr_valid = list(subs_days_valid.values())
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graph = 'line'
        titre_page = 'Soumissions Python'
        cours = 'lepl1402'
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid)

    
    @app.route('/lepl1402/months')
    def lepl1402_months():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs_months = {}
        subs_months_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = 'LEPL1402' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_monthDate = current_date_formated.strftime("%Y-%m") #("%B %Y") # February 2020
            
            if current_monthDate not in subs_months:
                subs_months[current_monthDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                subs_months[current_monthDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
            if row[1] == "success":
                if current_monthDate not in subs_months_valid:
                    subs_months_valid[current_monthDate] = 1
                else:
                    subs_months_valid[current_monthDate] += 1
        
        subm_dates = list(subs_months.keys())
        subm_nbr = list(subs_months.values())
        
        subm_dates_valid = list(subs_months_valid.keys())
        subm_nbr_valid = list(subs_months_valid.values())
            
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graph = 'bar'
        titre_page = 'Soumissions Python (mois)'
        cours = 'lepl1402'
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid)
    
    
    @app.route('/lsinf1252')
    def lsinf1252():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs_days = {}
        subs_days_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = 'LSINF1252' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_dayDate = current_date_formated.strftime("%Y-%m-%d") #("%d-%m-%Y") # '02-16-2020'
            
            if current_dayDate not in subs_days:
                subs_days[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                subs_days[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
            if row[1] == "success":
                if current_dayDate not in subs_days_valid:
                    subs_days_valid[current_dayDate] = 1
                else:
                    subs_days_valid[current_dayDate] += 1
        
        subm_dates = list(subs_days.keys())
        subm_nbr = list(subs_days.values())
        
        subm_dates_valid = list(subs_days_valid.keys())
        subm_nbr_valid = list(subs_days_valid.values())
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graph = 'line'
        titre_page = 'Soumissions Python'
        cours = 'lsinf1252'
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid)

    
    @app.route('/lsinf1252/months')
    def lsinf1252_months():
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs_months = {}
        subs_months_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = 'LSINF1252' ORDER BY submitted_on"):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            current_monthDate = current_date_formated.strftime("%Y-%m") #("%B %Y") # February 2020
            
            if current_monthDate not in subs_months:
                subs_months[current_monthDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                subs_months[current_monthDate] += 1 # si elle y est déjà, on augmente sa valeur de 1
            
            if row[1] == "success":
                if current_monthDate not in subs_months_valid:
                    subs_months_valid[current_monthDate] = 1
                else:
                    subs_months_valid[current_monthDate] += 1
        
        subm_dates = list(subs_months.keys())
        subm_nbr = list(subs_months.values())
        
        subm_dates_valid = list(subs_months_valid.keys())
        subm_nbr_valid = list(subs_months_valid.values())
            
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        graph = 'bar'
        titre_page = 'Soumissions Python (mois)'
        cours = 'lsinf1252'
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid)
        
    return app
    
    """
    for row in cursor.execute("SELECT count(*) from user_tasks WHERE task = 'BinarySearch' AND succeeded = 'true' "):
        print(row[0])
    """
