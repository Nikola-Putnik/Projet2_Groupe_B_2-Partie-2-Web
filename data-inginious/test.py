import sqlite3
import datetime


date_format = "%Y-%m-%dT%H:%M:%S"
b = "2020-02-16T22:57:05.482+0100"
b = b[:-9] # on remove les micro secondes et le +0100
x = datetime.datetime.strptime(b, date_format)
year = x.strftime("%Y")
print("year:", year)

date_time = x.strftime("%m-%d-%Y, %H:%M:%S")
print("date and time:",date_time)

a = datetime.datetime(2008, 9, 26, 1, 51, 42)
print(a)

"2020-01-12T17:02:42.623+0100" > "2020-02-02T16:20:02.989+0100"

# Accès à la base de données
conn = sqlite3.connect('inginious.sqlite')

# Le curseur permettra l'envoi des commandes SQL
cursor = conn.cursor()

"""
submissions_dates = []
submissions_nbr = [] # nombre de submissions par jours
for row in cursor.execute("SELECT submitted_on from submissions WHERE course = 'LSINF1101-PYTHON' AND submitted_on >= '2020-02-02T16:20:02.989+0100'"):
    current_date = row[0][:-9] # '2020-02-16T22:57:05'
    current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
    current_dayDate = current_date_formated.strftime("%m-%d-%Y") # '02-16-2020'
    if current_dayDate not in submissions_dates:
        submissions_dates.append(current_dayDate)

    
print("len :",len(submissions_dates))
print(submissions_dates)
print(submissions_nbr)
"""



"""
xy = {}

for row in cursor.execute("SELECT submitted_on from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
    current_date = row[0][:-9] # '2020-02-16T22:57:05'
    current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
    current_dayDate = current_date_formated.strftime("%d-%m-%Y") # '02-16-2020'
    if current_dayDate not in xy:
        xy[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
    else:
        xy[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1

submissions_dates = list(xy.keys())
submissions_nbr = list(xy.values())
"""


def nbr_to_month_fr(n):
    if n == 1:
        mois = "janvier"
    elif n == 2:
        mois = "février"
    elif n == 3:
        mois = "mars"
    elif n == 4:
        mois = "avril"
    elif n == 5:
        mois = "mai"
    elif n == 6:
        mois = "juin"
    elif n == 7:
        mois = "juillet"
    elif n == 8:
        mois = "aout"
    elif n == 9:
        mois = "septembre"
    elif n == 10:
        mois = "octobre"
    elif n == 11:
        mois = "novembre"
    elif n == 12:
        mois = "décembre"
    else:
        mois = "coronavirus"
    return mois


xy = {}

for row in cursor.execute("SELECT submitted_on from submissions WHERE course = 'LSINF1101-PYTHON' ORDER BY submitted_on"):
    current_date = row[0][:-9] # '2020-02-16T22:57:05'
    current_date_formated = datetime.datetime.strptime(current_date, date_format) # datetime.datetime(2020, 2, 16, 22, 57, 5)
    current_dayDate = current_date_formated.strftime("%B %Y") # '02-16-2020'
    if current_dayDate not in xy:
        xy[current_dayDate] = 1 # si la date est pas dans le dico, on l'ajoute avec une valeur de 1
    else:
        xy[current_dayDate] += 1 # si elle y est déjà, on augmente sa valeur de 1

submissions_dates = list(xy.keys())
submissions_nbr = list(xy.values())





# Toujours fermer la connexion quand elle n'est plus utile
conn.close()
