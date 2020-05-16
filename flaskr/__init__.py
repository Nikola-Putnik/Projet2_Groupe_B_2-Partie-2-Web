from flask import Flask, render_template, request

import sqlite3
import datetime


app = Flask(__name__, instance_relative_config=True)


# variables globales, qui ne seront calculées qu'une seule fois, au premier chargement de la page.
# variables utilisées pour les options de l'utilisateur
global helpMessage  # help = True -> les messages d'infos sont affichés par défaut
helpMessage = 'True'

global theme  # le theme -> par défaut ce sera le theme1
theme = 'blue'

global modif_time  # pour les options, l'heure de modification
modif_time = "00:00:00"

global calendar  # calendar = True -> les formulaires utilisent le calendrier
calendar = 'True'


# page principale (HOME)
@app.route('/')
def index():
    return render_template('index.html', helpMessage = helpMessage, theme = theme)


# page d'options (OPTIONS)
@app.route('/options')
def options():
    
    subject = ""
    
    if request.args.get('subject') is not None:
        subject = request.args.get('subject')
        
    global helpMessage
    old_helpMessage = helpMessage
    
    if request.args.get('helpMessage') is not None:
        helpMessage = request.args.get('helpMessage')
        
    global theme
    old_theme = theme
    
    if request.args.get('theme') is not None:
        theme = request.args.get('theme')
        
    global calendar
    old_calendar = calendar
    
    if request.args.get('calendar') is not None:
        calendar = request.args.get('calendar')
        
    modif = 'False'
    
    if request.args.get('modif') is not None:
        modif = request.args.get('modif')
    
    global modif_time
    if helpMessage != old_helpMessage or calendar != old_calendar:  # juste un test pour pas que l'heure s'actualise en raffraichissant la page
        modif_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    return render_template('options.html', helpMessage = helpMessage, theme = theme, calendar = calendar,
                           modif = modif, modif_time = modif_time, subject = subject)


def submissions_by_dates(course, exercise=None):
    """
    pre  : course -> le nom d'un cours (string)
           exercise -> le nom d'un exercice, None par défaut (string)
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
    pre  : course -> le nom d'un cours (string)
           sort -> une option de tri (string)
    post : un tuple contenant:
               0: 1e tuple: 0- une liste avec le nom des tasks (strings)
                            1- une liste avec les nombres d'utilisateurs
               1: 2e tuple: 0- une liste avec le nom des tasks validées (strings)
                            1- une liste avec les nombres d'utilisateurs ayant validé
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
    
    for i in range(len(user_nbr)):
        pourcentage.append(round((user_nbr_valid[i]/user_nbr[i])*100, 2))
    
    if 'percentage' in sort:
        pourcentage, tasks, user_nbr_valid, user_nbr = (list(t) for t in zip(*sorted(zip(pourcentage, tasks, user_nbr_valid, user_nbr))))
    
    elif 'tried' in sort:
        user_nbr, pourcentage, tasks, user_nbr_valid = (list(t) for t in zip(*sorted(zip(user_nbr, pourcentage, tasks, user_nbr_valid))))
    
    elif 'successes' in sort:
        user_nbr_valid, user_nbr, pourcentage, tasks = (list(t) for t in zip(*sorted(zip(user_nbr_valid, user_nbr, pourcentage, tasks))))
    
    if 'reverse' in sort:
        pourcentage.reverse()
        tasks.reverse()
        user_nbr_valid.reverse()
        user_nbr.reverse()
    
    return ((tasks, user_nbr), (tasks_valid, user_nbr_valid), pourcentage)
    

def results(course, exercise):
    """
    pre  : course -> le nom d'un cours (string)
           exercice -> le nom d'un exercice (string)
    post : un tuple dont le 1er élément est la liste des resultats possible des soumissions (liste de strings)
                         le 2em élément est la liste des nombres de soumissions correspondant à ces résultats (liste d'entiers)
                         le 3em élément est la liste des pourcentages par rapport au total des soumissions correspondant à ces résultats (liste de reels)
    """
    
    # Accès à la base de données
    conn = sqlite3.connect('data-inginious/inginious.sqlite')
    
    # Le curseur permettra l'envoi des commandes SQL
    cursor = conn.cursor()
    
    if exercise == None:
        
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
        for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND task = '{}' ".format(course, exercise)):
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
            pourcentage.append(round((i/data_results[0])*100, 2))
    
    return (labels_results, data_results, pourcentage)
    

def successes(course, exercise):
    """
    pre  : course -> le nom d'un cours (string)
           exercise -> le nom d'un exercice (string)
    post : un tuple dont le 1er élément est la liste des resultats possible (liste de strings)
                         le 2em élément est la liste des nombres d'étudiants ayant obtenu ces résultats (liste d'entiers)
                         le 3em élément est la liste des pourcentages par rapport au total des étudiants correspondant à ces résultats (liste de reels)
    """
    
    # Accès à la base de données
    conn = sqlite3.connect('data-inginious/inginious.sqlite')
    
    # Le curseur permettra l'envoi des commandes SQL
    cursor = conn.cursor()
    
    for row in cursor.execute("SELECT count(*) from user_tasks WHERE course = '{}' AND task = '{}' ".format(course, exercise)):
        total = row[0]
    
    for row in cursor.execute("SELECT count(*) from user_tasks WHERE course = '{}' AND task = '{}' AND succeeded = 'true' ".format(course, exercise)):
        succeeded = row[0]
    
    for row in cursor.execute("SELECT count(*) from user_tasks WHERE course = '{}' AND task = '{}' AND succeeded = 'false' ".format(course, exercise)):
        failed = row[0]
    
    # Toujours fermer la connexion quand elle n'est plus utile
    conn.close()
    
    # on garde cette partie dans cet ordre
    labels_results = ['total', 'succeeded', 'failed']
    data_results = [total, succeeded, failed]
    
    pourcentage = []
    for i in data_results:
        if data_results[0] == 0:
            pourcentage.append(0)
        else:
            pourcentage.append(round((i/data_results[0])*100, 2))
    
    return (labels_results, data_results, pourcentage)


def successesByTime(course, exercise):
    """
    pre  : course -> le nom d'un cours (string)
           exercise -> le nom d'un exercice (string)
    post : un tuple dont le 1er élément est la liste des dates correspondant à la reussite de l'exercice par un/des etudiant(s) (liste de strings)
                                        -> pour faire simple: l'axe des X
                         le 2em élément est la liste des nombres cumulés d'étudiants ayant reussi l'exercice à chacune de ces dates (liste d'entiers)
                                        -> pour faire simple: l'axe des Y
    """
    
    # Accès à la base de données
    conn = sqlite3.connect('data-inginious/inginious.sqlite')
    
    # Le curseur permettra l'envoi des commandes SQL
    cursor = conn.cursor()
    
    xy = {}
    users = []
    total = 0
    
    for row in cursor.execute("SELECT submitted_on, username from submissions WHERE course = '{}' AND task = '{}' AND result = 'success' ORDER BY submitted_on".format(course, exercise)):
        current_user = row[1]
        if current_user not in users:
            total += 1
            users.append(current_user)
            current_date = row[0][:-18] # '2020-02-16'
            xy[current_date] = total  # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
    
    successes_dates = list(xy.keys())
    successes_nbr_cumulative = list(xy.values())
    
    # Toujours fermer la connexion quand elle n'est plus utile
    conn.close()
    
    return (successes_dates, successes_nbr_cumulative)


def exercise_submissions(course, min10='Flase'):
    """
    pre  : course -> le nom d'un cours (string)
           min10 -> 'True' ou 'False' (default), si min10 == True, ne tiendra compte que des exercices essayés par au moins 10 étudiants
    post : un tuple dont le 1er élément est une liste de 20 exercices triés par le pourcentage de réussites de leurs soumissions, on prend les 10 "pires" puis les 10 "meilleurs"
                                        -> l'axe des X
                         le 2em élément est la liste des pourcentages de soumissions valides pour chacun des exercices de la 1ere liste
                                        -> l'axe des Y
    """
    liste_exo=[]
    listemoyenne=[]
    listetopexo=[]
    listetopmoy=[]
    listeworstexo=[]
    listeworstmoy=[]
    
    conn = sqlite3.connect('data-inginious/inginious.sqlite')
    cursor = conn.cursor()
    
    if min10 == 'True':
        tasks_users = {}  # dico du nombre d'utilisateurs par exercices (chaque clé est un exercice (str) qui a un nombre d'utilisateurs (int) comme valeur)
        for row in cursor.execute("SELECT task, succeeded from user_tasks WHERE course = '{}' ORDER BY task".format(course)):
            current_task = row[0]
            if current_task not in tasks_users:
                tasks_users[current_task] = 1  # si la task est pas dans le dico, on l'ajoute avec une valeur de 1
            else:
                tasks_users[current_task] += 1  # si elle y est déjà, on augmente sa valeur de 1
        
        for row in cursor.execute("SELECT DISTINCT(task) FROM user_tasks WHERE course ='{}'".format(course)):
            if tasks_users[row[0]] >= 10:
                liste_exo.append(row[0])
    else:
        for row in cursor.execute("SELECT DISTINCT(task) FROM user_tasks WHERE course ='{}'".format(course)):
            liste_exo.append(row[0])
    
    
    for i in liste_exo:
        for row in cursor.execute("SELECT avg(grade) FROM user_tasks WHERE task='{}'".format(i)):
            listemoyenne.append((round(row[0],2),i))
    
    conn.close()
    
    listemoyenne = sorted(listemoyenne)
    listetop=(listemoyenne[-11:-1])
    listeworst=(listemoyenne[0:10])
    for x,y in listetop:
        listetopexo.append(x)
        listetopmoy.append(y)
    for x,y in listeworst:
        listeworstexo.append(x)
        listeworstmoy.append(y)
    listedatas = listeworstexo+listetopexo
    listelabel = listeworstmoy+listetopmoy
    
    return (listelabel, listedatas)


def active_hours(course):
    """
    pre  : le nom d'un cours (string)
    post : un tuple dont le 1er élément est une liste des heures de la journée (de 00 à 23)
                         le 2em élément est une liste de pourcentages correspondants aux heures de la 1ere liste
    """
    
    # Accès à la base de données
    conn = sqlite3.connect('data-inginious/inginious.sqlite')
    
    # Le curseur permettra l'envoi des commandes SQL
    cursor = conn.cursor()
    
    # liste avec le nombre de soumissions pour chaque heure, subm_nbr[x] = nombre de soumissions à l'heure 'x'
    subm_nbr = []
    
    for i in range(24):
        if i < 10:
            x = "0"+str(i)
        else:
            x = str(i)
        for row in cursor.execute("SELECT count(*) from submissions WHERE course = '{}' AND substr(submitted_on,12,2) = '{}' ".format(course, x)):
            subm_nbr.append(row[0])
    
    # Toujours fermer la connexion quand elle n'est plus utile
    conn.close()
    
    subm_hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
                  '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    
    total_subm = sum(subm_nbr)
    subm_perc = []
    for i in subm_nbr:
        subm_perc.append(round((i/total_subm)*100, 2))
    
    return (subm_hours, subm_perc)


from . import lsinf1101

from . import lepl1402

from . import lsinf1252


if __name__ == '__main__':
    app.run(debug=True)
