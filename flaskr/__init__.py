from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #premier graphique sur le covid19
    @app.route('/graph0')
    def graph():
        fileCSV = open('data/total_cases.csv','r')
        
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

    return app
