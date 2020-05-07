import sqlite3

conn = sqlite3.connect('user.sqlite')

cursor = conn.cursor()

# creation de la table
"""
cursor.execute('''CREATE TABLE user_settings
(
  ID        INT PRIMARY KEY     NOT NULL,
  INFOS     TEXT                NOT NULL,
  THEME     TEXT                NOT NULL,
  COVID     TEXT                NOT NULL,
  CALENDAR  TEXT                NOT NULL
);''')
"""


# ajout de contenu
"""
ID = 1
infos = "True"
theme = "blue"
covid = "False"
calendar = "True"

cursor.execute('''INSERT INTO user_settings (ID, INFOS, THEME, COVID, CALENDAR)
                VALUES (?, ?, ?, ?, ?)''',
               (ID, infos, theme, covid, calendar) )
"""

conn.commit()

conn.close()
