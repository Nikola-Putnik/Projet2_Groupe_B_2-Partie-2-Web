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
    
    # variables globales, qui ne seront calculées qu'une seule fois, au premier chargement de la page.
    global lsinf1101_data_day
    lsinf1101_data_day = ()
    
    global lsinf1101_data_month
    lsinf1101_data_month = ()
    
    global lepl1402_data_day
    lepl1402_data_day = ()
    
    global lepl1402_data_month
    lepl1402_data_month = ()
    
    global lsinf1252_data_day
    lsinf1252_data_day = ()
    
    global lsinf1252_data_month
    lsinf1252_data_month = ()
    

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
    
    def submissions_by_dates(course, scale):
        """
        pre  : course = le nom d'un cours (string)
               scale = un ordre de grandeur de durée, ex: 'day', 'month' (string)
        post : un tuple contenant contenant 2 éléments
               0: 1e tuple: 0- une liste avec les dates de toutes les soumissions
                            1- une liste avec les nombres de soumissions correspondant aux dates de la première liste
               1: 2e tuple: 0- une liste avec les dates de toutes les soumissions réussies (valides)
                            1- une liste avec les nombres de soumissions réussies correspondant aux dates de la première liste
        """
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        subs = {}
        subs_valid = {}

        for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = '{}' ORDER BY submitted_on".format(course)):
            current_date = row[0][:-9] # '2020-02-16T22:57:05'
            current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
            
            if scale == 'day':
                current_dateFinal = current_date_formated.strftime("%Y-%m-%d") #("%d-%m-%Y") # '02-16-2020'
                if current_dateFinal not in subs:
                    subs[current_dateFinal] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
                else:
                    subs[current_dateFinal] += 1 # si elle y est déjà, on augmente sa valeur de 1
                
                if row[1] == "success":
                    if current_dateFinal not in subs_valid:
                        subs_valid[current_dateFinal] = 1
                    else:
                        subs_valid[current_dateFinal] += 1
            
            elif scale == 'month':
                current_dateFinal = current_date_formated.strftime("%Y-%m") #("%B %Y") # February 2020
                if current_dateFinal not in subs:
                    subs[current_dateFinal] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
                else:
                    subs[current_dateFinal] += 1 # si elle y est déjà, on augmente sa valeur de 1
                
                if row[1] == "success":
                    if current_dateFinal not in subs_valid:
                        subs_valid[current_dateFinal] = 1
                    else:
                        subs_valid[current_dateFinal] += 1
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        subm_dates = list(subs.keys())
        subm_nbr = list(subs.values())
        
        subm_dates_valid = list(subs_valid.keys())
        subm_nbr_valid = list(subs_valid.values())
        
        return ((subm_dates, subm_nbr), (subm_dates_valid, subm_nbr_valid))
    
    
    #premier graphique sur les donnees inginious
    #soumissions au cours du temps pour LSINF1101-PYTHON
    @app.route('/lsinf1101')
    def lsinf1101():
        
        global lsinf1101_data_day
        
        if len(lsinf1101_data_day) == 0:
            lsinf1101_data_day = submissions_by_dates('LSINF1101-PYTHON', 'day')
        
        subm_dates = lsinf1101_data_day[0][0]
        subm_nbr = lsinf1101_data_day[0][1]
        
        subm_dates_valid = lsinf1101_data_day[1][0]
        subm_nbr_valid = lsinf1101_data_day[1][1]
        
        graph = 'line'
        titre_page = 'LSINF1101-PYTHON'
        cours = 'lsinf1101'
        
        size = request.args.get('size')
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid, size = size)

    
    @app.route('/lsinf1101/months')
    def lsinf1101_months():
        
        global lsinf1101_data_month
        
        if len(lsinf1101_data_month) == 0:
            lsinf1101_data_month = submissions_by_dates('LSINF1101-PYTHON', 'month')
        
        subm_dates = lsinf1101_data_month[0][0]
        subm_nbr = lsinf1101_data_month[0][1]
        
        subm_dates_valid = lsinf1101_data_month[1][0]
        subm_nbr_valid = lsinf1101_data_month[1][1]
        
        graph = 'bar'
        titre_page = 'LSINF1101-PYTHON (mois)'
        cours = 'lsinf1101'
        
        size = request.args.get('size')
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid, size = size)
    
    
    @app.route('/lepl1402')
    def lepl1402():
        
        global lepl1402_data_day
        
        if len(lepl1402_data_day) == 0:
            lepl1402_data_day = submissions_by_dates('LEPL1402', 'day')
        
        subm_dates = lepl1402_data_day[0][0]
        subm_nbr = lepl1402_data_day[0][1]
        
        subm_dates_valid = lepl1402_data_day[1][0]
        subm_nbr_valid = lepl1402_data_day[1][1]
        
        graph = 'line'
        titre_page = 'LEPL1402'
        cours = 'lepl1402'
        
        size = request.args.get('size')
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid, size = size)

    
    @app.route('/lepl1402/months')
    def lepl1402_months():
        
        global lepl1402_data_month
        
        if len(lepl1402_data_month) == 0:
            lepl1402_data_month = submissions_by_dates('LEPL1402', 'month')
        
        subm_dates = lepl1402_data_month[0][0]
        subm_nbr = lepl1402_data_month[0][1]
        
        subm_dates_valid = lepl1402_data_month[1][0]
        subm_nbr_valid = lepl1402_data_month[1][1]
        
        graph = 'bar'
        titre_page = 'LEPL1402 (mois)'
        cours = 'lepl1402'
        
        size = request.args.get('size')
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid, size = size)
    
    
    @app.route('/lsinf1252')
    def lsinf1252():
        
        global lsinf1252_data_day
        
        if len(lsinf1252_data_day) == 0:
            lsinf1252_data_day = submissions_by_dates('LSINF1252', 'day')
        
        subm_dates = lsinf1252_data_day[0][0]
        subm_nbr = lsinf1252_data_day[0][1]
        
        subm_dates_valid = lsinf1252_data_day[1][0]
        subm_nbr_valid = lsinf1252_data_day[1][1]
        
        graph = 'line'
        titre_page = 'LSINF1252'
        cours = 'lsinf1252'
        
        size = request.args.get('size')
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid, size = size)

    
    @app.route('/lsinf1252/months')
    def lsinf1252_months():
        
        global lsinf1252_data_month
        
        if len(lsinf1252_data_month) == 0:
            lsinf1252_data_month = submissions_by_dates('LSINF1252', 'month')
        
        subm_dates = lsinf1252_data_month[0][0]
        subm_nbr = lsinf1252_data_month[0][1]
        
        subm_dates_valid = lsinf1252_data_month[1][0]
        subm_nbr_valid = lsinf1252_data_month[1][1]
        
        graph = 'bar'
        titre_page = 'LSINF1252 (mois)'
        cours = 'lsinf1252'
        
        size = request.args.get('size')
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, type = graph, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid, size = size)
        
    return app
    
    """
    for row in cursor.execute("SELECT count(*) from user_tasks WHERE task = 'BinarySearch' AND succeeded = 'true' "):
        print(row[0])
    """
