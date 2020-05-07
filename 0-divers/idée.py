"""
Ce code affiche les moyennes de chaque cours et la moyenne générale 
"""

import sqlite3

# Accès à la base de données
conn = sqlite3.connect('inginious.sqlite')

# Le curseur permettra l'envoi des commandes SQL
cursor = conn.cursor()
données = {}
l1=[]
moyenne = 0
for row in cursor.execute("SELECT course, avg(grade)from user_tasks GROUP BY course"): # Je choisis la moyenne pour chaque cours
    l1.append(row) #j'insère le tuple( cours,moyenne) dans une liste. chaque element est un tuple
for i in l1:
    x,y = i      #je parcours ma liste et j'assigne x au cours et y a sa moyenne
    données[x] =y    # chaque element de ma liste transormé est ajouté dans mon dictionnaire données 
for row in cursor.execute("SELECT avg(grade) from user_tasks"): # je calcule la moyenne générale 
    moyenne = row     
for key,value in données.items():
    print("le cours {} à une moyenne de {} ´%".format(key,value))
print("{} ´% ceci est la moyenne générale".format(moyenne))
 

# Toujours fermer la connexion quand elle n'est plus utile
conn.close()