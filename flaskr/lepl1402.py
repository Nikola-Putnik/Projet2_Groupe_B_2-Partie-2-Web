from flask import Flask, render_template, request

import sqlite3
import datetime

from . import app
from . import(submissions_by_dates, results, exercise_submissions, active_hours, exercices, successes, successesByTime)

# variables globales, qui ne seront calculées qu'une seule fois, au premier chargement de la page.
global lepl1402_data
lepl1402_data = ()

global lepl1402_data_results
lepl1402_data_results = ()

global lepl1402_exo_subm
lepl1402_exo_subm = ()

global lepl1402_exo_subm_min10
lepl1402_exo_subm_min10 = ()

global lepl1402_active_hours
lepl1402_active_hours = ()


@app.route('/lepl1402')
def lepl1402():
    
    # on doit importer les variables globales ici sinon elles ne s'actualisent pas
    from . import(theme, helpMessage, calendar)
    
    titre_page = 'LEPL1402'
    cours = 'lepl1402'
    
    size = 'default'  # la taille du graphique principal (si defaut => normal, si large => graphique agrandi sur toute la page)
    if request.args.get('size') is not None:
        size = request.args.get('size')
    
    global lepl1402_data
    
    if len(lepl1402_data) == 0:
        lepl1402_data = submissions_by_dates('LEPL1402')
    
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
    titre_subm = 'Soumissions par jour'
    type_subm = 'line'  # le type de graphique
    
    min = subm_dates[0]
    max = subm_dates[-1]
    real_min = min
    real_max = max
    
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
    
    titre_subm_M = 'Soumissions par mois'
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
    # graph des pourcentage de réussites par exercices
    #######
    
    titre_exo_subm = 'Exercices - Notes moyennes'
    type_exo_subm = 'bar'
    exo_subm_data = []
    exo_subm_labels = []
    
    min10 = 'False'
    
    if request.args.get('min10') is not None:
        min10 = request.args.get('min10')
    
    if request.args.get('main') is not None:
        main = request.args.get('main')
        if main == 'exercices_subm':
            if min10 == 'True':
                global lepl1402_exo_subm_min10
                if len(lepl1402_exo_subm_min10) == 0:
                    lepl1402_exo_subm_min10 = exercise_submissions('LEPL1402', 'True')
                exo_subm_data = lepl1402_exo_subm_min10[1]
                exo_subm_labels = lepl1402_exo_subm_min10[0]
            else:
                global lepl1402_exo_subm
                if len(lepl1402_exo_subm) == 0:
                    lepl1402_exo_subm = exercise_submissions('LEPL1402')
                exo_subm_data = lepl1402_exo_subm[1]
                exo_subm_labels = lepl1402_exo_subm[0]
    
    #######
    # graph des heures d'activité
    #######
    
    titre_active_hours = "Heures d'activité"
    type_active_hours = 'bar'
    active_hours_data = []  # le % de soumissions
    active_hours_labels = []  # les heures
    
    if request.args.get('main') is not None:
        main = request.args.get('main')
        if main == 'active_hours':
            global lepl1402_active_hours
            if len(lepl1402_active_hours) == 0:
                lepl1402_active_hours = active_hours('LEPL1402')
            active_hours_data = lepl1402_active_hours[1]
            active_hours_labels = lepl1402_active_hours[0]
    
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
    elif main == 'exercices_subm':  # graph des pourcentage de soumissions valides par exercices
        titre_graph = titre_exo_subm
    elif main == 'active_hours':  # graph des pourcentage de soumissions valides par exercices
        titre_graph = titre_active_hours
    
    return render_template('graphs/graphs.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
    
                           titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                           min = min, max = max, form_min = form_min, form_max = form_max, real_min = real_min, real_max = real_max, unit = unit,
                           
                           titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                           min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                           
                           titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype,
                           
                           titre_exo_subm = titre_exo_subm, type_exo_subm = type_exo_subm, exo_subm_data = exo_subm_data, exo_subm_labels = exo_subm_labels, min10 = min10,
                           
                           titre_active_hours = titre_active_hours, type_active_hours = type_active_hours, active_hours_data = active_hours_data, active_hours_labels = active_hours_labels,
                           
                           helpMessage = helpMessage, theme = theme, calendar = calendar)


@app.route('/lepl1402/exercices_list')
def lepl1402_exercices_list():
    
    # on doit importer les variables globales ici sinon elles ne s'actualisent pas
    from . import(theme, helpMessage, calendar)
    
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
    titre_subm = 'Soumissions par jour'
    type_subm = 'line'  # le type de graphique
    
    if len(subm_dates) > 0:
        min = subm_dates[0]
        max = subm_dates[-1]
    else:  # des valeurs bidon
        min = '2018-01-01'
        max = '2020-06-01'
    
    real_min = min
    real_max = max
        
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
    
    titre_subm_M = 'Soumissions par mois'
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
    # graph des réussites
    #######
    
    lepl1402_data_successes = successes('LEPL1402', task)
        
    labels_successes = lepl1402_data_successes[0]
    data_successes = lepl1402_data_successes[1]
    pourcentage_successes = lepl1402_data_successes[2]
    
    titre_successes = 'Réussites'
    type_successes = 'doughnut'
    datatypeS = 'nombre'
    
    if request.args.get('datatype') is not None:
        datatypeS = request.args.get('datatype')
        if datatypeS == 'pourcentage':
            data_successes = pourcentage_successes
    
    #######
    # graph des réussites cumulées
    #######
    
    lepl1402_data_successesByTime = successesByTime('LEPL1402', task)
    
    # dates et nombres de réussites (cumulées)
    successes_dates = lepl1402_data_successesByTime[0]
    successes_nbr_cumulative = lepl1402_data_successesByTime[1]
    
    # graphique par defaut (courbe soumissions par jour)
    titre_successesByTime = 'Réussites Cumulées'
    type_successesByTime = 'line'  # le type de graphique
    
    if len(successes_dates) > 0:
        min_S = successes_dates[0]
        max_S = successes_dates[-1]
    else:  # des valeurs bidon
        min_S = '2018-01-01'
        max_S = '2020-06-01'
    real_min_S = min_S
    real_max_S = max_S
        
    if request.args.get('min_S') is not None:
        min_S = request.args.get('min_S')
    if request.args.get('max_S') is not None:
        max_S = request.args.get('max_S')
    
    # les dates affichées dans les formulaires
    form_min_S = min_S
    form_max_S = max_S
    
    # réglage de l'unité du graphique
    minD_S = datetime.datetime.strptime(min_S, "%Y-%m-%d")
    maxD_S = datetime.datetime.strptime(max_S, "%Y-%m-%d")
    difference_S = maxD_S - minD_S
    if difference_S < datetime.timedelta(days=20): # si il y a moins de 20 jours représentés, on affiche les unités en jours
        unit_S = 'day'
    elif difference_S < datetime.timedelta(days=90): # si il y a moins de de 90 jours représentés, on affiche les unités en semaines
        unit_S = 'week'
    elif difference_S < datetime.timedelta(days=720):
        unit_S = 'month'
    else:
        unit_S = 'year'
    
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
    elif main == 'successes':  # graph des résultats (pie chart)
        titre_graph = titre_successes
    elif main == 'successesByTime':  # graph des résultats (pie chart)
        titre_graph = titre_successesByTime
    
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
    
    search = ""
    if request.args.get('search') is not None:
        search = request.args.get('search')
        tasks_name_search = []
        tasks_tried_search = []
        tasks_succeeded_search = []
        percentage_search = []
        for i in range(len(tasks_name)):
            if search.lower() in tasks_name[i].lower():
                tasks_name_search.append(tasks_name[i])
                tasks_tried_search.append(tasks_tried[i])
                tasks_succeeded_search.append(tasks_succeeded[i])
                percentage_search.append(percentage[i])
        tasks_name = tasks_name_search
        tasks_tried = tasks_tried_search
        tasks_succeeded = tasks_succeeded_search
        percentage = percentage_search
    
    return render_template('graphs/graphs-exercices-list.html', cours = cours, titre = titre_page, titre_graph = titre_graph, size = size, main = main,
    
                           titre_subm = titre_subm, type_subm = type_subm, dates = subm_dates, data = subm_nbr, datesV = subm_dates_valid, dataV = subm_nbr_valid,
                           min = min, max = max, form_min = form_min, form_max = form_max, real_min = real_min, real_max = real_max, unit = unit,
                           
                           titre_subm_M = titre_subm_M, type_subm_M = type_subm_M, dates_M = subm_dates_M, data_M = subm_nbr_M, datesV_M = subm_dates_M_valid, dataV_M = subm_nbr_M_valid,
                           min_M = min_M, max_M = max_M, form_min_M = form_min_M, form_max_M = form_max_M, unit_M = unit_M,
                           
                           titre_results = titre_results, data_results = data_results, labels_results = labels_results, type_results = type_results, datatype = datatype,
                           
                           titre_successes = titre_successes, data_successes = data_successes, labels_successes = labels_successes, type_successes = type_successes, datatypeS = datatypeS,
                           
                           titre_successesByTime = titre_successesByTime, type_successesByTime = type_successesByTime, dates_S = successes_dates, data_S = successes_nbr_cumulative,
                           min_S = min_S, max_S = max_S, form_min_S = form_min_S, form_max_S = form_max_S, real_min_S = real_min_S, real_max_S = real_max_S, unit_S = unit_S,
                           
                           task = task, tasks_name = tasks_name, tasks_tried = tasks_tried, tasks_succeeded = tasks_succeeded, percentage = percentage, sort = sort, search = search,
                           
                           helpMessage = helpMessage, theme = theme, calendar = calendar)