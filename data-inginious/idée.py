import sqlite3

# Accès à la base de données
conn = sqlite3.connect('inginious.sqlite')

# Le curseur permettra l'envoi des commandes SQL
cursor = conn.cursor()
données ={}
listecours=[]
for row in cursor.execute("SELECT DISTINCT course from user_tasks"):
    row =str(row).split()
    listecours.append(row)
    print(listecours)
taille = len(listecours)
i=0
while i<= taille-1:
    print(listecours[i])
    i+=1
        
    
print(données)    
# Toujours fermer la connexion quand elle n'est plus utile
conn.close()