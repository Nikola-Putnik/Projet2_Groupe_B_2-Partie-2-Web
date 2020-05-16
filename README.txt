################################################

Installation de l'application FLask du Groupe B2

################################################

BASE DE DONNÉES:
------------------------------------------------

Placer la db dans le dossier 'data-inginious'
La db doit être nommée 'inginious.sqlite'


WINDOWS
------------------------------------------------

1) Décompresser l'archive

2) Ouvrir le terminal (cmd.exe) et insérer les commandes suivantes:

>>> choisissez la bonne directory si vous n'y êtes pas encore
cd [EMPLACEMENT DE VOTRE DOSSIER, ex: 'cd Projet2/flask-app']

>>> installation de flask
py -m venv venv

>>>
venv\Scripts\activate

>>>
pip install flask

>>>
set FLASK_APP=flaskr

>>>
set FLASK_ENV=development

>>>
flask run


FINI =====> ouvrez l'url: http://127.0.0.1:5000


Chaque fois que vous relancerez l'application il faudra réutiliser les commandes suivantes:

cd [EMPLACEMENT DE VOTRE DOSSIER]
venv\Scripts\activate
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run


################################################


MAC (testé par un externe)
------------------------------------------------

>>> choisissez la bonne directory si vous n'y êtes pas encore
cd [EMPLACEMENT DE VOTRE DOSSIER, ex: 'cd Projet2/flask-app']

>>> installation de flask
py -m venv venv

>>>
. venv\bin\activate

>>>
pip install flask

>>>
export FLASK_APP=flaskr

>>>
export FLASK_ENV=development

>>>
flask run


FINI =====> ouvrez l'url: http://127.0.0.1:5000


################################################


LINUX (non testé)
------------------------------------------------

1) Décompresser l'archive

2) Ouvrir le terminal dans le dossier du projet et insérer les commandes suivantes:

>>>
virtualenv -p python3 venv ### Pour créer le virtualenv, à ne faire qu'une fois (et il faut avoir installé python3-virtualenv)

>>>
source venv/bin/activate

>>>
pip install Flask

>>>
flask run


FINI =====> ouvrez l'url: http://127.0.0.1:5000


Si cela ne marche pas, essayez peut etre les commandes: (avant d'effectuer 'flask run')

export FLASK_APP=flaskr

export FLASK_ENV=development