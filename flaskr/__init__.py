from flask import Flask, render_template, request

import sqlite3
import datetime

    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    
    # variables globales, qui ne seront calculées qu'une seule fois, au premier chargement de la page.
    global lsinf1101_data
    lsinf1101_data = ()
    
    global lsinf1101_data_results
    lsinf1101_data_results = ()
    
    global lepl1402_data
    lepl1402_data = ()
    
    global lepl1402_data_results
    lepl1402_data_results = ()
    
    global lsinf1252_data
    lsinf1252_data = ()
    
    global lsinf1252_data_results
    lsinf1252_data_results = ()
    

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
    
    
    @app.route('/moypyt')
    def moyennepyt():
         # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        listecours=[]
        liste_exo=[]
        listemoyenne=[]
        for row in cursor.execute("SELECT DISTINCT(course) FROM submissions"):  
            listecours.append(row[0])
        for row in cursor.execute("SELECT DISTINCT(task) FROM submissions WHERE course ='LSINF1101-PYTHON'"):
            liste_exo.append(row[0])
        x=0
        for i in liste_exo:
            for row in cursor.execute("SELECT avg(grade) FROM submissions WHERE task='{}'".format(i)):
                listemoyenne.append(round(row[0],2))
        return render_template('graphs/graph_moypy.html', titre = "Moyenne des exercices pour le cours LSINF1101", type = 'bar', labels = liste_exo, data =listemoyenne)
        conn.close()
    
    
    @app.route('/moylepl1402')
    def moyennelepl():
         # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        listecours=[]
        liste_exo=[]
        listemoyenne=[]
        for row in cursor.execute("SELECT DISTINCT(course) FROM submissions"):  
            listecours.append(row[0])
        for row in cursor.execute("SELECT DISTINCT(task) FROM submissions WHERE course ='LEPL1402'"):
            liste_exo.append(row[0])
        x=0
        for i in liste_exo:
            for row in cursor.execute("SELECT avg(grade) FROM submissions WHERE task='{}'".format(i)):
                listemoyenne.append(round(row[0],2))
        return render_template('graphs/graph_moylepl.html', titre = "Moyenne des exercices pour le cours LEPL1402", type = 'bar', labels = liste_exo, data =listemoyenne)
        conn.close()
    
    
    @app.route('/moyennelsinf')
    def moyennelsinf():
        conn=sqlite3.connect('data-inginious/inginious.sqlite')
        cursor=conn.cursor()
        listecours=[]
        liste_exo=[]
        listemoyenne=[]
        for row in cursor.execute("SELECT DISTINCT(course) FROM submissions"):  
            listecours.append(row[0])
        for row in cursor.execute("SELECT DISTINCT(task) FROM submissions WHERE course ='LSINF1252'"):
            liste_exo.append(row[0])
        x=0
        for i in liste_exo:
            for row in cursor.execute("SELECT avg(grade) FROM submissions WHERE task='{}'".format(i)):
                listemoyenne.append(round(row[0],2))
        return render_template('graphs/graph_moylsinf.html', titre = "Moyenne des exercices pour le cours LSINF1252", type = 'bar', labels = liste_exo, data =listemoyenne)
        conn.close()
    
    
    def submissions_by_dates(course, exercise):
        """
        pre  : le nom d'un cours (string)
        post : un tuple contenant:
                   0: 1e tuple: 0: 1e tuple: 0- une liste avec les dates de toutes les soumissions (PAR JOUR)
                                             1- une liste avec les nombres de soumissions correspondant aux dates de la première liste (PAR JOUR)
                                1: 2e tuple: 0- une liste avec les dates de toutes les soumissions réussies (valides) (PAR JOUR)
                                             1- une liste avec les nombres de soumissions réussies correspondant aux dates de la première liste (PAR JOUR)
                   1: 2e tuple: 0: 1e tuple: 0- une liste avec les dates de toutes les soumissions (PAR MOIS)
                                             1- une liste avec les nombres de soumissions correspondant aux dates de la première liste (PAR MOIS)
                                1: 2e tuple: 0- une liste avec les dates de toutes les soumissions réussies (valides) (PAR MOIS)
                                             1- une liste avec les nombres de soumissions réussies correspondant aux dates de la première liste (PAR MOIS)
        """
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        date_format = "%Y-%m-%dT%H:%M:%S"
        
        # dico des soumissions par jour
        subs = {}  # dico du nombre de soumissions par jour (chaque clé est une date (str) qui a un nombre de soumissions (int) comme valeur)
        subs_valid = {}  # idem mais uniquement avec les soumissions valides (success)
        # dico des soumissions par mois
        subs_M = {}
        subs_M_valid = {}
        
        if exercise == None:
            for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = '{}' ORDER BY submitted_on".format(course)):
                current_date = row[0][:-9] # '2020-02-16T22:57:05'
                current_date_formated = datetime.datetime.strptime(current_date, date_format)  # datetime.datetime(2020, 2, 16, 22, 57, 5)
                
                # par jour
                current_dateFinal = current_date_formated.strftime("%Y-%m-%d")  # ex: '02-16-2020'
                if current_dateFinal not in subs:
                    subs[current_dateFinal] = 1  # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
                else:
                    subs[current_dateFinal] += 1  # si elle y est déjà, on augmente sa valeur de 1
                if row[1] == "success":
                    if current_dateFinal not in subs_valid:
                        subs_valid[current_dateFinal] = 1
                    else:
                        subs_valid[current_dateFinal] += 1
                
                # par mois
                current_dateM_Final = current_date_formated.strftime("%Y-%m")  # ex: 'February 2020'
                if current_dateM_Final not in subs_M:
                    subs_M[current_dateM_Final] = 1  # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
                else:
                    subs_M[current_dateM_Final] += 1  # si elle y est déjà, on augmente sa valeur de 1
                if row[1] == "success":
                    if current_dateM_Final not in subs_M_valid:
                        subs_M_valid[current_dateM_Final] = 1
                    else:
                        subs_M_valid[current_dateM_Final] += 1
        
        else:
            for row in cursor.execute("SELECT submitted_on, result from submissions WHERE course = '{}' AND task = '{}' ORDER BY submitted_on".format(course, exercise)):
                current_date = row[0][:-9] # '2020-02-16T22:57:05'
                current_date_formated = datetime.datetime.strptime(current_date, date_format)  # datetime.datetime(2020, 2, 16, 22, 57, 5)
                
                # par jour
                current_dateFinal = current_date_formated.strftime("%Y-%m-%d")  # ex: '02-16-2020'
                if current_dateFinal not in subs:
                    subs[current_dateFinal] = 1  # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
                else:
                    subs[current_dateFinal] += 1  # si elle y est déjà, on augmente sa valeur de 1
                if row[1] == "success":
                    if current_dateFinal not in subs_valid:
                        subs_valid[current_dateFinal] = 1
                    else:
                        subs_valid[current_dateFinal] += 1
                
                # par mois
                current_dateM_Final = current_date_formated.strftime("%Y-%m")  # ex: 'February 2020'
                if current_dateM_Final not in subs_M:
                    subs_M[current_dateM_Final] = 1  # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
                else:
                    subs_M[current_dateM_Final] += 1  # si elle y est déjà, on augmente sa valeur de 1
                if row[1] == "success":
                    if current_dateM_Final not in subs_M_valid:
                        subs_M_valid[current_dateM_Final] = 1
                    else:
                        subs_M_valid[current_dateM_Final] += 1
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        # par jour
        subm_dates = list(subs.keys())
        subm_nbr = list(subs.values())
        subm_dates_valid = list(subs_valid.keys())
        subm_nbr_valid = list(subs_valid.values())
        
        # par mois
        subm_dates_M = list(subs_M.keys())
        subm_nbr_M = list(subs_M.values())
        subm_dates_M_valid = list(subs_M_valid.keys())
        subm_nbr_M_valid = list(subs_M_valid.values())
        
        return (((subm_dates, subm_nbr), (subm_dates_valid, subm_nbr_valid)), ((subm_dates_M, subm_nbr_M), (subm_dates_M_valid, subm_nbr_M_valid)))
    
    
    def exercices(course, sort):
        """
        pre  : le nom d'un cours (string)
        post : un tuple contenant:
                   0: 1e tuple: 0- une liste avec le nom des tasks (strings)
                                1- une liste avec les nombres de soumissions correspondant aux dates de la première liste (PAR JOUR)
                   1: 2e tuple: 0- une liste avec le nom des tasks validées (strings)
                                1- une liste avec les nombres de soumissions réussies correspondant aux dates de la première liste (PAR MOIS)
                   2: pourcentage: une liste avec le pourcentage d'étudiants ayant réussis les tâches
        """
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
        # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        tasks_users = {}  # dico du nombre d'utilisateurs par exercices (chaque clé est un exercice (str) qui a un nombre d'utilisateurs (int) comme valeur)
        tasks_users_valid = {}  # idem mais uniquement avec les soumissions valides (success)
        
        for row in cursor.execute("SELECT task, succeeded from user_tasks WHERE course = '{}' ORDER BY task".format(course)):
            current_task = row[0]
            if current_task not in tasks_users:
                tasks_users[current_task] = 1  # si la task est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                tasks_users[current_task] += 1  # si elle y est déjà, on augmente sa valeur de 1
            if row[1] == "true":
                if current_task not in tasks_users_valid:
                    tasks_users_valid[current_task] = 1
                else:
                    tasks_users_valid[current_task] += 1
            else:
                if current_task not in tasks_users_valid:
                    tasks_users_valid[current_task] = 0
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        tasks = list(tasks_users.keys())
        user_nbr = list(tasks_users.values())
        tasks_valid = list(tasks_users_valid.keys())
        user_nbr_valid = list(tasks_users_valid.values())
        
        pourcentage = []
        pourcentage_copy = pourcentage
        
        for i in range(len(user_nbr)):
            pourcentage.append(round((user_nbr_valid[i]/user_nbr[i])*100, 2))
        
        if sort == 'percentage':
            pourcentage, tasks, user_nbr_valid, user_nbr = (list(t) for t in zip(*sorted(zip(pourcentage, tasks, user_nbr_valid, user_nbr))))
        
        elif sort == 'percentage_reverse':
            pourcentage, tasks, user_nbr_valid, user_nbr = (list(t) for t in zip(*sorted(zip(pourcentage, tasks, user_nbr_valid, user_nbr))))
            pourcentage.reverse()
            tasks.reverse()
            user_nbr_valid.reverse()
            user_nbr.reverse()
        
        return ((tasks, user_nbr), (tasks_valid, user_nbr_valid), pourcentage)
        
    
    def results(course, exercise):
        """
        pre  : le nom d'un cours (string)
        post : un tuple dont le 1er élément est la liste des resultats possible des soumissions (liste de strings)
                             le 2em élément est la liste des nombres de soumissions correspondant à ces résultats (liste d'entiers)
                             le 3em élément est la liste des pourcentages par rapport au total des soumissions correspondant à ces résultats (liste de reels)
        """
        
        # Accès à la base de données
        conn = sqlite3.connect('data-inginious/inginious.sqlite')
        
         # Le curseur permettra l'envoi des commandes SQL
        cursor = conn.cursor()
        
        if exercise == None:
            # ouais je sais ca se répète, mais le temps d'exécution de count est plutot court, donc izi quoi
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' ".format(course)):
                subm = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'success' ".format(course)):
                success = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'failed' ".format(course)):
                failed = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'killed' ".format(course)):
                killed = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'overflow' ".format(course)):
                overflow = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'timeout' ".format(course)):
                timeout = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'crash' ".format(course)):
                crash = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND result = 'error' ".format(course)):
                error = row[0]
        
        else:
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' ".format(course)):
                subm = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'success' ".format(course, exercise)):
                success = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'failed' ".format(course, exercise)):
                failed = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'killed' ".format(course, exercise)):
                killed = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'overflow' ".format(course, exercise)):
                overflow = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'timeout' ".format(course, exercise)):
                timeout = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'crash' ".format(course, exercise)):
                crash = row[0]
            
            for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' AND result = 'error' ".format(course, exercise)):
                error = row[0]
        
        # Toujours fermer la connexion quand elle n'est plus utile
        conn.close()
        
        # on garde cette partie dans cet ordre
        labels_results = ['subimssions', 'success', 'failed']
        data_results = [subm, success, failed]
        
        # on trie cette partie du plus grand au plus petit
        labels_ToSort = ['killed', 'overflow', 'timeout', 'crash', 'error']
        data_ToSort = [killed, overflow, timeout, crash, error]
        data_ToSort, labels_ToSort = (list(t) for t in zip(*sorted(zip(data_ToSort, labels_ToSort))))
        data_ToSort.reverse()
        labels_ToSort.reverse()
        
        # on ajoute les parties triées aux 2 listes
        # de sorte à avoir : [subm, success, failed, *le reste trié par ordre décroisssant*]
        labels_results += labels_ToSort
        data_results += data_ToSort
        
        pourcentage = []
        for i in data_results:
            if data_results[0] == 0:
                pourcentage.append(0)
            else:
                pourcentage.append((i/data_results[0])*100)
        
        return (labels_results, data_results, pourcentage)
    
    
    @app.route('/lsinf1101')
    def lsinf1101():
        
        titre_page = 'LSINF1101-PYTHON'
        cours = 'lsinf1101'
        
        size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
        if request.args.get('size') is not None:
            size = request.args.get('size')
        
        global lsinf1101_data
        
        if len(lsinf1101_data) == 0:
            lsinf1101_data = submissions_by_dates('LSINF1101-PYTHON', None)
        
        #######
        # courbe soumissions par jour
        #######
        
        # dates et nombres de soumissions (par jour)
        subm_dates = lsinf1101_data[0][0][0]
        subm_nbr = lsinf1101_data[0][0][1]
        
        # dates et nombres de soumissions valides (par jour)
        subm_dates_valid = lsinf1101_data[0][1][0]
        subm_nbr_valid = lsinf1101_data[0][1][1]
        
        # graphique par defaut (courbe soumissions par jour)
        titre_subm = 'Soumissions'
        type_subm = 'line'  # le type de graphique
        
        min = subm_dates[0]
        max = subm_dates[-1]
        
        if request.args.get('min') is not None:
            min = request.args.get('min')
        if request.args.get('max') is not None:
            max = request.args.get('max')
        
        # les dates affichées dans les formulaires
        form_min = min
        form_max = max
        
        # réglage de l'unité du graphique
        maxD = datetime.datetime.strptime(max, "%Y-%m-%d")
        minD = datetime.datetime.strptime(min, "%Y-%m-%d")
        difference = maxD - minD
        if difference < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
            unit = 'day'
        elif difference < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
            unit = 'week'
        elif difference < datetime.timedelta(days=720):
            unit = 'month'
        else:
            unit = 'year'
        
        #######
        # graph soumissions par mois
        #######
        
        subm_dates_M = lsinf1101_data[1][0][0]
        subm_nbr_M = lsinf1101_data[1][0][1]
        
        subm_dates_M_valid = lsinf1101_data[1][1][0]
        subm_nbr_M_valid = lsinf1101_data[1][1][1]
        
        titre_subm_M = 'Soumissions par Mois'
        type_subm_M = 'bar'
        
        min_M = subm_dates_M[0]
        max_M = subm_dates_M[-1]
        
        if request.args.get('min_M') is not None:
            min_M = request.args.get('min_M')
        if request.args.get('max_M') is not None:
            max_M = request.args.get('max_M')
        
        # les dates affichées dans les formulaires
        form_min_M = min_M
        form_max_M = max_M
        
        # pour une raison inconnue, sur le graphique le 1er et le dernier mois sont coupés, on va donc ajouter un mois au début et à la fin du graphique
        maxD_M = datetime.datetime.strptime(max_M, "%Y-%m")
        max_M = maxD_M + datetime.timedelta(days=31) # ajouter 31 jours permet d'avancer d'un mois
        max_M = max_M.strftime("%Y-%m")
        minD_M = datetime.datetime.strptime(min_M, "%Y-%m")
        min_M = minD_M - datetime.timedelta(days=15) # enlever entre 1 et 28 jours permet de reculer d'un mois 
        min_M = min_M.strftime("%Y-%m")
        
        # l'unité du graphique
        unit_M = 'month'
        
        #######
        # graph des résultats (pie chart)
        #######
        
        global lsinf1101_data_results
        
        if len(lsinf1101_data_results) == 0:
            lsinf1101_data_results = results('LSINF1101-PYTHON', None)
            
        labels_results = lsinf1101_data_results[0]
        data_results = lsinf1101_data_results[1]
        pourcentage = lsinf1101_data_results[2]
        
        titre_results = 'Résultats'
        type_results = 'pie'
        datatype = 'nombre'
        
        if request.args.get('datatype') is not None:
            datatype = request.args.get('datatype')
            if datatype == 'pourcentage':
                data_results = pourcentage
        
        #######
        # GET main
        #######
        
        main = 'subm'  # le graphique principal (default = graph des soumissions par jour)
        titre_graph = titre_subm  # le titre du graphique principal (par default: titre_subm = titre de la courbe soumissions par jour)
        
        if request.args.get('main') is not None:
            main = request.args.get('main')
        
        if main == 'default':  # graph des soumissions par jour (line/courbe)
            titre_graph = titre_subm
        elif main == 'month':  # graph des soumissions par mois (bar)
            titre_graph = titre_subm_M
        elif main == 'results':  # graph des résultats (pie chart)
            titre_graph = titre_results
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
        
                               titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                               min = min, max = max, form_min = form_min, form_max = form_max, unit = unit,
                               
                               titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                               min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                               
                               titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype)
    
    
    @app.route('/lsinf1101/exercices_list')
    def lsinf1101_exercices_list():
        
        titre_page = 'LSINF1101-PYTHON'
        cours = 'lsinf1101'
        
        task = "no_task"
        if request.args.get('task') is not None:
            task = request.args.get('task')
            if task != "no_task":
                titre_page = 'LSINF1101-PYTHON' + ' - ' + task
        
        size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
        if request.args.get('size') is not None:
            size = request.args.get('size')
        
        lsinf1101_data = submissions_by_dates('LSINF1101-PYTHON', task)
        
        #######
        # courbe soumissions par jour
        #######
        
        # dates et nombres de soumissions (par jour)
        subm_dates = lsinf1101_data[0][0][0]
        subm_nbr = lsinf1101_data[0][0][1]
        
        # dates et nombres de soumissions valides (par jour)
        subm_dates_valid = lsinf1101_data[0][1][0]
        subm_nbr_valid = lsinf1101_data[0][1][1]
        
        # graphique par defaut (courbe soumissions par jour)
        titre_subm = 'Soumissions'
        type_subm = 'line'  # le type de graphique
        
        if len(subm_dates) > 0:
            min = subm_dates[0]
            max = subm_dates[-1]
        else:  # des valeurs bidon
            min = '2018-01-01'
            max = '2020-06-01'
            
        if request.args.get('min') is not None:
            min = request.args.get('min')
        if request.args.get('max') is not None:
            max = request.args.get('max')
        
        # les dates affichées dans les formulaires
        form_min = min
        form_max = max
        
        # réglage de l'unité du graphique
        maxD = datetime.datetime.strptime(max, "%Y-%m-%d")
        minD = datetime.datetime.strptime(min, "%Y-%m-%d")
        difference = maxD - minD
        if difference < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
            unit = 'day'
        elif difference < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
            unit = 'week'
        elif difference < datetime.timedelta(days=720):
            unit = 'month'
        else:
            unit = 'year'
        
        #######
        # graph soumissions par mois
        #######
        
        subm_dates_M = lsinf1101_data[1][0][0]
        subm_nbr_M = lsinf1101_data[1][0][1]
        
        subm_dates_M_valid = lsinf1101_data[1][1][0]
        subm_nbr_M_valid = lsinf1101_data[1][1][1]
        
        titre_subm_M = 'Soumissions par Mois'
        type_subm_M = 'bar'
        
        if len(subm_dates_M) > 0:
            min_M = subm_dates_M[0]
            max_M = subm_dates_M[-1]
        else:  # des valeurs bidon
            min_M = '2018-01'
            max_M = '2020-06'
            
        if request.args.get('min_M') is not None:
            min_M = request.args.get('min_M')
        if request.args.get('max_M') is not None:
            max_M = request.args.get('max_M')
        
        # les dates affichées dans les formulaires
        form_min_M = min_M
        form_max_M = max_M
        
        # pour une raison inconnue, sur le graphique le 1er et le dernier mois sont coupés, on va donc ajouter un mois au début et à la fin du graphique
        maxD_M = datetime.datetime.strptime(max_M, "%Y-%m")
        max_M = maxD_M + datetime.timedelta(days=31) # ajouter 31 jours permet d'avancer d'un mois
        max_M = max_M.strftime("%Y-%m")
        minD_M = datetime.datetime.strptime(min_M, "%Y-%m")
        min_M = minD_M - datetime.timedelta(days=15) # enlever entre 1 et 28 jours permet de reculer d'un mois 
        min_M = min_M.strftime("%Y-%m")
        
        # l'unité du graphique
        unit_M = 'month'
        
        #######
        # graph des résultats (pie chart)
        #######
        
        lsinf1101_data_results = results('LSINF1101-PYTHON', task)
            
        labels_results = lsinf1101_data_results[0]
        data_results = lsinf1101_data_results[1]
        pourcentage = lsinf1101_data_results[2]
        
        titre_results = 'Résultats'
        type_results = 'pie'
        datatype = 'nombre'
        
        if request.args.get('datatype') is not None:
            datatype = request.args.get('datatype')
            if datatype == 'pourcentage':
                data_results = pourcentage
        
        #######
        # GET main
        #######
        
        main = 'subm'  # le graphique principal (default = graph des soumissions par jour)
        titre_graph = titre_subm  # le titre du graphique principal (par default: titre_subm = titre de la courbe soumissions par jour)
        
        if request.args.get('main') is not None:
            main = request.args.get('main')
        
        if main == 'default':  # graph des soumissions par jour (line/courbe)
            titre_graph = titre_subm
        elif main == 'month':  # graph des soumissions par mois (bar)
            titre_graph = titre_subm_M
        elif main == 'results':  # graph des résultats (pie chart)
            titre_graph = titre_results
        
        #######
        # Liste d'exercices
        #######
        
        sort = "def"
        if request.args.get('sort') is not None:
            sort = request.args.get('sort')
        lsinf1101_data_exercices = exercices('LSINF1101-PYTHON', sort)
        # ((tasks, user_nbr), (tasks_valid, user_nbr_valid), pourcentage)
        tasks_name = lsinf1101_data_exercices[0][0]
        tasks_tried = lsinf1101_data_exercices[0][1]
        tasks_succeeded = lsinf1101_data_exercices[1][1]
        percentage = lsinf1101_data_exercices[2]
        
        return render_template('graphs/graph_1-exercices-list.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
        
                               titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                               min = min, max = max, form_min = form_min, form_max = form_max, unit = unit,
                               
                               titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                               min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                               
                               titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype,
                               
                               task = task, tasks_name = tasks_name, tasks_tried = tasks_tried, tasks_succeeded = tasks_succeeded, percentage = percentage, sort = sort)
    
    
    @app.route('/lepl1402')
    def lepl1402():
        
        titre_page = 'LEPL1402'
        cours = 'lepl1402'
        
        size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
        if request.args.get('size') is not None:
            size = request.args.get('size')
        
        global lepl1402_data
        
        if len(lepl1402_data) == 0:
            lepl1402_data = submissions_by_dates('LEPL1402', None)
        
        #######
        # courbe soumissions par jour
        #######
        
        # dates et nombres de soumissions (par jour)
        subm_dates = lepl1402_data[0][0][0]
        subm_nbr = lepl1402_data[0][0][1]
        
        # dates et nombres de soumissions valides (par jour)
        subm_dates_valid = lepl1402_data[0][1][0]
        subm_nbr_valid = lepl1402_data[0][1][1]
        
        # graphique par defaut (courbe soumissions par jour)
        titre_subm = 'Soumissions'
        type_subm = 'line'  # le type de graphique
        
        min = subm_dates[0]
        max = subm_dates[-1]
        
        if request.args.get('min') is not None:
            min = request.args.get('min')
        if request.args.get('max') is not None:
            max = request.args.get('max')
        
        # les dates affichées dans les formulaires
        form_min = min
        form_max = max
        
        # réglage de l'unité du graphique
        maxD = datetime.datetime.strptime(max, "%Y-%m-%d")
        minD = datetime.datetime.strptime(min, "%Y-%m-%d")
        difference = maxD - minD
        if difference < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
            unit = 'day'
        elif difference < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
            unit = 'week'
        elif difference < datetime.timedelta(days=720):
            unit = 'month'
        else:
            unit = 'year'
        
        #######
        # graph soumissions par mois
        #######
        
        subm_dates_M = lepl1402_data[1][0][0]
        subm_nbr_M = lepl1402_data[1][0][1]
        
        subm_dates_M_valid = lepl1402_data[1][1][0]
        subm_nbr_M_valid = lepl1402_data[1][1][1]
        
        titre_subm_M = 'Soumissions par Mois'
        type_subm_M = 'bar'
        
        min_M = subm_dates_M[0]
        max_M = subm_dates_M[-1]
        
        if request.args.get('min_M') is not None:
            min_M = request.args.get('min_M')
        if request.args.get('max_M') is not None:
            max_M = request.args.get('max_M')
        
        # les dates affichées dans les formulaires
        form_min_M = min_M
        form_max_M = max_M
        
        # pour une raison inconnue, sur le graphique le 1er et le dernier mois sont coupés, on va donc ajouter un mois au début et à la fin du graphique
        maxD_M = datetime.datetime.strptime(max_M, "%Y-%m")
        max_M = maxD_M + datetime.timedelta(days=31) # ajouter 31 jours permet d'avancer d'un mois
        max_M = max_M.strftime("%Y-%m")
        minD_M = datetime.datetime.strptime(min_M, "%Y-%m")
        min_M = minD_M - datetime.timedelta(days=15) # enlever entre 1 et 28 jours permet de reculer d'un mois 
        min_M = min_M.strftime("%Y-%m")
        
        # l'unité du graphique
        unit_M = 'month'
        
        #######
        # graph des résultats (pie chart)
        #######
        
        global lepl1402_data_results
        
        if len(lepl1402_data_results) == 0:
            lepl1402_data_results = results('LEPL1402', None)
            
        labels_results = lepl1402_data_results[0]
        data_results = lepl1402_data_results[1]
        pourcentage = lepl1402_data_results[2]
        
        titre_results = 'Résultats'
        type_results = 'pie'
        datatype = 'nombre'
        
        if request.args.get('datatype') is not None:
            datatype = request.args.get('datatype')
            if datatype == 'pourcentage':
                data_results = pourcentage
        
        #######
        # GET main
        #######
        
        main = 'subm'  # le graphique principal (default = graph des soumissions par jour)
        titre_graph = titre_subm  # le titre du graphique principal (par default: titre_subm = titre de la courbe soumissions par jour)
        
        if request.args.get('main') is not None:
            main = request.args.get('main')
        
        if main == 'default':  # graph des soumissions par jour (line/courbe)
            titre_graph = titre_subm
        elif main == 'month':  # graph des soumissions par mois (bar)
            titre_graph = titre_subm_M
        elif main == 'results':  # graph des résultats (pie chart)
            titre_graph = titre_results
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
        
                               titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                               min = min, max = max, form_min = form_min, form_max = form_max, unit = unit,
                               
                               titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                               min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                               
                               titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype)
    
    
    @app.route('/lepl1402/exercices_list')
    def lepl1402_exercices_list():
        
        titre_page = 'LEPL1402'
        cours = 'lepl1402'
        
        task = "no_task"
        if request.args.get('task') is not None:
            task = request.args.get('task')
            if task != "no_task":
                titre_page = 'LEPL1402' + ' - ' + task
        
        size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
        if request.args.get('size') is not None:
            size = request.args.get('size')
        
        lepl1402_data = submissions_by_dates('LEPL1402', task)
        
        #######
        # courbe soumissions par jour
        #######
        
        # dates et nombres de soumissions (par jour)
        subm_dates = lepl1402_data[0][0][0]
        subm_nbr = lepl1402_data[0][0][1]
        
        # dates et nombres de soumissions valides (par jour)
        subm_dates_valid = lepl1402_data[0][1][0]
        subm_nbr_valid = lepl1402_data[0][1][1]
        
        # graphique par defaut (courbe soumissions par jour)
        titre_subm = 'Soumissions'
        type_subm = 'line'  # le type de graphique
        
        if len(subm_dates) > 0:
            min = subm_dates[0]
            max = subm_dates[-1]
        else:  # des valeurs bidon
            min = '2018-01-01'
            max = '2020-06-01'
            
        if request.args.get('min') is not None:
            min = request.args.get('min')
        if request.args.get('max') is not None:
            max = request.args.get('max')
        
        # les dates affichées dans les formulaires
        form_min = min
        form_max = max
        
        # réglage de l'unité du graphique
        maxD = datetime.datetime.strptime(max, "%Y-%m-%d")
        minD = datetime.datetime.strptime(min, "%Y-%m-%d")
        difference = maxD - minD
        if difference < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
            unit = 'day'
        elif difference < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
            unit = 'week'
        elif difference < datetime.timedelta(days=720):
            unit = 'month'
        else:
            unit = 'year'
        
        #######
        # graph soumissions par mois
        #######
        
        subm_dates_M = lepl1402_data[1][0][0]
        subm_nbr_M = lepl1402_data[1][0][1]
        
        subm_dates_M_valid = lepl1402_data[1][1][0]
        subm_nbr_M_valid = lepl1402_data[1][1][1]
        
        titre_subm_M = 'Soumissions par Mois'
        type_subm_M = 'bar'
        
        if len(subm_dates_M) > 0:
            min_M = subm_dates_M[0]
            max_M = subm_dates_M[-1]
        else:  # des valeurs bidon
            min_M = '2018-01'
            max_M = '2020-06'
            
        if request.args.get('min_M') is not None:
            min_M = request.args.get('min_M')
        if request.args.get('max_M') is not None:
            max_M = request.args.get('max_M')
        
        # les dates affichées dans les formulaires
        form_min_M = min_M
        form_max_M = max_M
        
        # pour une raison inconnue, sur le graphique le 1er et le dernier mois sont coupés, on va donc ajouter un mois au début et à la fin du graphique
        maxD_M = datetime.datetime.strptime(max_M, "%Y-%m")
        max_M = maxD_M + datetime.timedelta(days=31) # ajouter 31 jours permet d'avancer d'un mois
        max_M = max_M.strftime("%Y-%m")
        minD_M = datetime.datetime.strptime(min_M, "%Y-%m")
        min_M = minD_M - datetime.timedelta(days=15) # enlever entre 1 et 28 jours permet de reculer d'un mois 
        min_M = min_M.strftime("%Y-%m")
        
        # l'unité du graphique
        unit_M = 'month'
        
        #######
        # graph des résultats (pie chart)
        #######
        
        lepl1402_data_results = results('LEPL1402', task)
            
        labels_results = lepl1402_data_results[0]
        data_results = lepl1402_data_results[1]
        pourcentage = lepl1402_data_results[2]
        
        titre_results = 'Résultats'
        type_results = 'pie'
        datatype = 'nombre'
        
        if request.args.get('datatype') is not None:
            datatype = request.args.get('datatype')
            if datatype == 'pourcentage':
                data_results = pourcentage
        
        #######
        # GET main
        #######
        
        main = 'subm'  # le graphique principal (default = graph des soumissions par jour)
        titre_graph = titre_subm  # le titre du graphique principal (par default: titre_subm = titre de la courbe soumissions par jour)
        
        if request.args.get('main') is not None:
            main = request.args.get('main')
        
        if main == 'default':  # graph des soumissions par jour (line/courbe)
            titre_graph = titre_subm
        elif main == 'month':  # graph des soumissions par mois (bar)
            titre_graph = titre_subm_M
        elif main == 'results':  # graph des résultats (pie chart)
            titre_graph = titre_results
        
        #######
        # Liste d'exercices
        #######
        
        sort = "def"
        if request.args.get('sort') is not None:
            sort = request.args.get('sort')
        lepl1402_data_exercices = exercices('LEPL1402', sort)
        # ((tasks, user_nbr), (tasks_valid, user_nbr_valid), pourcentage)
        tasks_name = lepl1402_data_exercices[0][0]
        tasks_tried = lepl1402_data_exercices[0][1]
        tasks_succeeded = lepl1402_data_exercices[1][1]
        percentage = lepl1402_data_exercices[2]
        
        return render_template('graphs/graph_1-exercices-list.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
        
                               titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                               min = min, max = max, form_min = form_min, form_max = form_max, unit = unit,
                               
                               titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                               min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                               
                               titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype,
                               
                               task = task, tasks_name = tasks_name, tasks_tried = tasks_tried, tasks_succeeded = tasks_succeeded, percentage = percentage, sort = sort)
    
    
    @app.route('/lsinf1252')
    def lsinf1252():
        
        titre_page = 'LSINF1252'
        cours = 'lsinf1252'
        
        size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
        if request.args.get('size') is not None:
            size = request.args.get('size')
        
        global lsinf1252_data
        
        if len(lsinf1252_data) == 0:
            lsinf1252_data = submissions_by_dates('LSINF1252', None)
        
        #######
        # courbe soumissions par jour
        #######
        
        # dates et nombres de soumissions (par jour)
        subm_dates = lsinf1252_data[0][0][0]
        subm_nbr = lsinf1252_data[0][0][1]
        
        # dates et nombres de soumissions valides (par jour)
        subm_dates_valid = lsinf1252_data[0][1][0]
        subm_nbr_valid = lsinf1252_data[0][1][1]
        
        # graphique par defaut (courbe soumissions par jour)
        titre_subm = 'Soumissions'
        type_subm = 'line'  # le type de graphique
        
        min = subm_dates[0]
        max = subm_dates[-1]
        
        if request.args.get('min') is not None:
            min = request.args.get('min')
        if request.args.get('max') is not None:
            max = request.args.get('max')
        
        # les dates affichées dans les formulaires
        form_min = min
        form_max = max
        
        # réglage de l'unité du graphique
        maxD = datetime.datetime.strptime(max, "%Y-%m-%d")
        minD = datetime.datetime.strptime(min, "%Y-%m-%d")
        difference = maxD - minD
        if difference < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
            unit = 'day'
        elif difference < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
            unit = 'week'
        elif difference < datetime.timedelta(days=720):
            unit = 'month'
        else:
            unit = 'year'
        
        #######
        # graph soumissions par mois
        #######
        
        subm_dates_M = lsinf1252_data[1][0][0]
        subm_nbr_M = lsinf1252_data[1][0][1]
        
        subm_dates_M_valid = lsinf1252_data[1][1][0]
        subm_nbr_M_valid = lsinf1252_data[1][1][1]
        
        titre_subm_M = 'Soumissions par Mois'
        type_subm_M = 'bar'
        
        min_M = subm_dates_M[0]
        max_M = subm_dates_M[-1]
        
        if request.args.get('min_M') is not None:
            min_M = request.args.get('min_M')
        if request.args.get('max_M') is not None:
            max_M = request.args.get('max_M')
        
        # les dates affichées dans les formulaires
        form_min_M = min_M
        form_max_M = max_M
        
        # pour une raison inconnue, sur le graphique le 1er et le dernier mois sont coupés, on va donc ajouter un mois au début et à la fin du graphique
        maxD_M = datetime.datetime.strptime(max_M, "%Y-%m")
        max_M = maxD_M + datetime.timedelta(days=31) # ajouter 31 jours permet d'avancer d'un mois
        max_M = max_M.strftime("%Y-%m")
        minD_M = datetime.datetime.strptime(min_M, "%Y-%m")
        min_M = minD_M - datetime.timedelta(days=15) # enlever entre 1 et 28 jours permet de reculer d'un mois 
        min_M = min_M.strftime("%Y-%m")
        
        # l'unité du graphique
        unit_M = 'month'
        
        #######
        # graph des résultats (pie chart)
        #######
        
        global lsinf1252_data_results
        
        if len(lsinf1252_data_results) == 0:
            lsinf1252_data_results = results('LSINF1252', None)
            
        labels_results = lsinf1252_data_results[0]
        data_results = lsinf1252_data_results[1]
        pourcentage = lsinf1252_data_results[2]
        
        titre_results = 'Résultats'
        type_results = 'pie'
        datatype = 'nombre'
        
        if request.args.get('datatype') is not None:
            datatype = request.args.get('datatype')
            if datatype == 'pourcentage':
                data_results = pourcentage
        
        #######
        # GET main
        #######
        
        main = 'subm'  # le graphique principal (default = graph des soumissions par jour)
        titre_graph = titre_subm  # le titre du graphique principal (par default: titre_subm = titre de la courbe soumissions par jour)
        
        if request.args.get('main') is not None:
            main = request.args.get('main')
        
        if main == 'default':  # graph des soumissions par jour (line/courbe)
            titre_graph = titre_subm
        elif main == 'month':  # graph des soumissions par mois (bar)
            titre_graph = titre_subm_M
        elif main == 'results':  # graph des résultats (pie chart)
            titre_graph = titre_results
        
        return render_template('graphs/graph_1.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
        
                               titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                               min = min, max = max, form_min = form_min, form_max = form_max, unit = unit,
                               
                               titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                               min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                               
                               titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype)
    
    
    @app.route('/lsinf1252/exercices_list')
    def lsinf1252_exercices_list():
        
        titre_page = 'LSINF1252'
        cours = 'lsinf1252'
        
        task = "no_task"
        if request.args.get('task') is not None:
            task = request.args.get('task')
            if task != "no_task":
                titre_page = 'LSINF1252' + ' - ' + task
        
        size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
        if request.args.get('size') is not None:
            size = request.args.get('size')
        
        lsinf1252_data = submissions_by_dates('LSINF1252', task)
        
        #######
        # courbe soumissions par jour
        #######
        
        # dates et nombres de soumissions (par jour)
        subm_dates = lsinf1252_data[0][0][0]
        subm_nbr = lsinf1252_data[0][0][1]
        
        # dates et nombres de soumissions valides (par jour)
        subm_dates_valid = lsinf1252_data[0][1][0]
        subm_nbr_valid = lsinf1252_data[0][1][1]
        
        # graphique par defaut (courbe soumissions par jour)
        titre_subm = 'Soumissions'
        type_subm = 'line'  # le type de graphique
        
        if len(subm_dates) > 0:
            min = subm_dates[0]
            max = subm_dates[-1]
        else:  # des valeurs bidon
            min = '2018-01-01'
            max = '2020-06-01'
            
        if request.args.get('min') is not None:
            min = request.args.get('min')
        if request.args.get('max') is not None:
            max = request.args.get('max')
        
        # les dates affichées dans les formulaires
        form_min = min
        form_max = max
        
        # réglage de l'unité du graphique
        maxD = datetime.datetime.strptime(max, "%Y-%m-%d")
        minD = datetime.datetime.strptime(min, "%Y-%m-%d")
        difference = maxD - minD
        if difference < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
            unit = 'day'
        elif difference < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
            unit = 'week'
        elif difference < datetime.timedelta(days=720):
            unit = 'month'
        else:
            unit = 'year'
        
        #######
        # graph soumissions par mois
        #######
        
        subm_dates_M = lsinf1252_data[1][0][0]
        subm_nbr_M = lsinf1252_data[1][0][1]
        
        subm_dates_M_valid = lsinf1252_data[1][1][0]
        subm_nbr_M_valid = lsinf1252_data[1][1][1]
        
        titre_subm_M = 'Soumissions par Mois'
        type_subm_M = 'bar'
        
        if len(subm_dates_M) > 0:
            min_M = subm_dates_M[0]
            max_M = subm_dates_M[-1]
        else:  # des valeurs bidon
            min_M = '2018-01'
            max_M = '2020-06'
            
        if request.args.get('min_M') is not None:
            min_M = request.args.get('min_M')
        if request.args.get('max_M') is not None:
            max_M = request.args.get('max_M')
        
        # les dates affichées dans les formulaires
        form_min_M = min_M
        form_max_M = max_M
        
        # pour une raison inconnue, sur le graphique le 1er et le dernier mois sont coupés, on va donc ajouter un mois au début et à la fin du graphique
        maxD_M = datetime.datetime.strptime(max_M, "%Y-%m")
        max_M = maxD_M + datetime.timedelta(days=31) # ajouter 31 jours permet d'avancer d'un mois
        max_M = max_M.strftime("%Y-%m")
        minD_M = datetime.datetime.strptime(min_M, "%Y-%m")
        min_M = minD_M - datetime.timedelta(days=15) # enlever entre 1 et 28 jours permet de reculer d'un mois 
        min_M = min_M.strftime("%Y-%m")
        
        # l'unité du graphique
        unit_M = 'month'
        
        #######
        # graph des résultats (pie chart)
        #######
        
        lsinf1252_data_results = results('LSINF1252', task)
            
        labels_results = lsinf1252_data_results[0]
        data_results = lsinf1252_data_results[1]
        pourcentage = lsinf1252_data_results[2]
        
        titre_results = 'Résultats'
        type_results = 'pie'
        datatype = 'nombre'
        
        if request.args.get('datatype') is not None:
            datatype = request.args.get('datatype')
            if datatype == 'pourcentage':
                data_results = pourcentage
        
        #######
        # GET main
        #######
        
        main = 'subm'  # le graphique principal (default = graph des soumissions par jour)
        titre_graph = titre_subm  # le titre du graphique principal (par default: titre_subm = titre de la courbe soumissions par jour)
        
        if request.args.get('main') is not None:
            main = request.args.get('main')
        
        if main == 'default':  # graph des soumissions par jour (line/courbe)
            titre_graph = titre_subm
        elif main == 'month':  # graph des soumissions par mois (bar)
            titre_graph = titre_subm_M
        elif main == 'results':  # graph des résultats (pie chart)
            titre_graph = titre_results
        
        #######
        # Liste d'exercices
        #######
        
        sort = "def"
        if request.args.get('sort') is not None:
            sort = request.args.get('sort')
        lsinf1252_data_exercices = exercices('LSINF1252', sort)
        # ((tasks, user_nbr), (tasks_valid, user_nbr_valid), pourcentage)
        tasks_name = lsinf1252_data_exercices[0][0]
        tasks_tried = lsinf1252_data_exercices[0][1]
        tasks_succeeded = lsinf1252_data_exercices[1][1]
        percentage = lsinf1252_data_exercices[2]
        
        return render_template('graphs/graph_1-exercices-list.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
        
                               titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                               min = min, max = max, form_min = form_min, form_max = form_max, unit = unit,
                               
                               titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                               min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                               
                               titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype,
                               
                               task = task, tasks_name = tasks_name, tasks_tried = tasks_tried, tasks_succeeded = tasks_succeeded, percentage = percentage, sort = sort)
    
    
    return app
