import sqlite3
conn=sqlite3.connect("inginious.sqlite")
cursor=conn.cursor()
listecours=[]
liste_exo=[]
listemoyenne=[]
for row in cursor.execute("SELECT DISTINCT(course) FROM submissions"):  #Je crée une liste avec les cours 
    listecours.append(row[0])
for row in cursor.execute("SELECT DISTINCT(task) FROM submissions WHERE course ='LSINF1101-PYTHON'"):
    liste_exo.append(row[0])
x=0
for i in liste_exo:
    for row in cursor.execute("SELECT avg(grade) FROM submissions WHERE task='{}'".format(i)):
        listefin.append(round(row[0],2))
print(listefin)