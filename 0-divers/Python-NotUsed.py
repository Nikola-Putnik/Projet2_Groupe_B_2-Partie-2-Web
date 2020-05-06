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