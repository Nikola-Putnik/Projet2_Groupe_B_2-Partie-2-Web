import sqlite3

# Accès à la base de données
conn = sqlite3.connect('inginious.sqlite')

# Le curseur permettra l'envoi des commandes SQL
cursor = conn.cursor()


for row in cursor.execute("SELECT status, username from submissions"):
    print(row[0], row[1])


# Toujours fermer la connexion quand elle n'est plus utile
conn.close()
