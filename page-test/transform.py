# on ouvre le fichier html d'origine
fileIn = open('empty-page.html','r')
htmlCode = fileIn.read()

# on ouvre le fichier csv
fileCSV = open('data/total_cases.csv','r')



# afficher le nombre de cas par pays le dernier jour

pays0 = fileCSV.readline().replace('\n','') # on lit la 1ere ligne (liste des pays)
pays1 = pays0.split(',')
nombre_pays = len(pays1)-2 # nombre de pays
liste_pays = pays1[2:nombre_pays+2] # liste de tous les pays


last_day = fileCSV.readlines()[-1].replace('\n','') # on lit la derniere ligne
liste_last_day = last_day.split(',')
nombre_pays_infecte = len(liste_last_day)-2 # nombre de pays infectes le dernier jour
liste_cas_last_day = liste_last_day[2:nombre_pays_infecte+2] # liste du nombre de cas par pays le dernier jour

graphique = 'bar'



# afficher l'evolution du nombre de cas

for .readline()




# transformation

htmlCode = htmlCode.replace('{type}', graphique)
htmlCode = htmlCode.replace('{labels}', str(liste_pays))
htmlCode = htmlCode.replace('{data}', str(liste_cas_last_day))
print(str(liste_pays))
print(str(liste_cas_last_day))
print(htmlCode)

fileOut = open('final-page.html','w')
fileOut.write(htmlCode)
fileOut.close()
