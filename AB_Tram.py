# IMPORT BIBLIOTHEKEN

import pandas as pd #dataframe
import matplotlib.pyplot as plt #graphics
import numpy as np #calculation
from math import pi
import os #data structure
from scipy.stats import norm
from scipy.optimize import curve_fit #normal distribution
from math import isnan
import datetime as dt
import sqlite3

#-----------------------------------------------------------------------------------------------------------------
# NOTIZEN

#Bemerkung zur Datenbank. Input vom Disponent.

#-----------------------------------------------------------------------------------------------------------------
# BESPRECHUNG OOP:

# class Datanalysis(object):
#      def __init__(self, x): 
#         self.X = x
#      def conn(self, path, sql):
#           pass
#      def query(self, xy):
#           pass

# class Visualisation(object):
#      def __init__(self, x): 
#         self.X = x
#      def scatter(self, x, y):
#           pass
#      def pie(self, x, y):
#           pass

# Datanalysis()
# Visualisation()

#-----------------------------------------------------------------------------------------------------------------
# DATENANALYSE

#Löscht die Datenbank AB_Tram.db
f_path =os.path.join(os.path.dirname(os.path.abspath(__file__))+"""\AB_Tram.db""")
os.remove(f_path)

#Verbindungsaufbau Sqlite3 und erstellen von Datenbank AB_Tram
connection = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "AB_Tram.db"))

#Definition "cursor" zum Schreiben in die Datenbank
cursor = connection.cursor()

#Erstellt Tabelle "trams"
cursor.execute("""
     CREATE TABLE IF NOT EXISTS `trams`(
          `id` INT AUTO_INCREMENT PRIMARY KEY,
          `Tramtyp` VRCAHAR(200),
          `TechnischerPlatz` VRCAHAR(200),
          `Störungsbeginn` INT,
          `Auftragsnummer` INTEGER,
          `Beschreibung` VRCAHAR(200),
          `Bemerkung` VRCAHAR(200),
          `Abk_TechnischerPlatz` SMALLINT);
""")

#Aktueller Ordnerpfad
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__))+"""\Ablag_Exports""","")
#Nimmt das aktuellste Excel im Pfad "folder_path"
list_dir = os.listdir(folder_path)
df = pd.read_excel(folder_path + list_dir[-1])


#Data frames
df_t =df["Technischer Platz"]
df_2 =df["Störungsbeginn"].dt.date
df_m =df["Meldungsnummer"]
df_b =df["Beschreibung"]

#l_df = [df["Technischer Platz"], df["Störungsbeginn"].dt.date, df["Meldungsnummer"], df["Beschreibung"]]

#Zähler
c_com = 0
c_cor = 0
c_awnf = 0
c_f_l = 0
c_f_k = 0
counter = -1
l_co = []
l_c = []

#Datenbank SQLite3 mit Daten aus Excel schreiben
for i, y, z, w in zip(df_t, df_2, df_m, df_b):
     l_df_it = df_t.tolist()
     x = dt.date.today()
     xy = x-y
     s_1 = i.split("TB")[2]
     s_2 = int(s_1[:4])
     co = 0
     for x, txt in enumerate(df_t):
         if i == txt:
              co += 1
     if i != l_df_it[counter]:
          l_co.append(f"{i} :"f"{co}")
          if s_2 >= 301 and s_2 <= 399:
               cursor.execute("INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`, `Abk_TechnischerPlatz`) VALUES ( ?,?,?,?,?,?)", ('Combino', i, xy.days, z, w, s_2))
               c_com +=1
               
          elif s_2 >= 478 and s_2 <= 599:
               cursor.execute("INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`, `Abk_TechnischerPlatz`) VALUES ( ?,?,?,?,?,?)", ('Cornichon', i, xy.days, z, w, s_2))
               c_cor +=1
               
          elif s_2 >= 1449 and s_2 <= 1599:
               cursor.execute("INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`, `Abk_TechnischerPlatz`) VALUES ( ?,?,?,?,?,?)", ('AWNF (Anhänger)', i, xy.days, z, w, s_2))
               c_awnf +=1
          
          elif s_2 >= 5001 and s_2 <= 5998:
               cursor.execute("INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`, `Abk_TechnischerPlatz`) VALUES ( ?,?,?,?,?,?)", ('Flexity lang', i, xy.days, z, w, s_2))
               c_f_l +=1
          
          elif s_2 >= 6001 and s_2 <= 6300:
               cursor.execute("INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`, `Abk_TechnischerPlatz`) VALUES ( ?,?,?,?,?,?)", ('Flexity kurz', i, xy.days, z, w, s_2))
               c_f_k +=1
               
     counter +=1


#Bemerkungen der Datenbank hinzufügen
# F_Dis = input("Bei welcher Tramnummer bzw Technischer Platz soll der Eintrag erfolgen?")
# I_Dis = input("Bemerkung Disponent: ")
# cursor.execute(f"UPDATE trams SET Bemerkung = '{I_Dis}' WHERE '{F_Dis}' = TechnischerPlatz;")

#Data frame 2 aus der Datenbank SQLite3
df_2 = pd.read_sql_query("Select * from 'trams';", connection)

connection.commit()
connection.close()

#-----------------------------------------------------------------------------------------------------------------
#VISUALISIERUNG


fig, ax = plt.subplots(figsize=(14, 6))

x = df_2['Störungsbeginn'].tolist()
y = df_2['Tramtyp'].tolist()
s = df_2['Störungsbeginn']
annotations = df_2['Abk_TechnischerPlatz'].tolist()
ax.scatter(x, y, s=s)

# BESPRECHUNG Label zu nah aufeinander:
for xi, yi, txt in zip(x, y, annotations):
     print(xi, yi)
     for i in y:
        pass  
     ax.annotate(txt,
                xy=(xi, yi), xycoords='data',)
#                xytext=(0.8, 0.8), textcoords='data',
#                arrowprops=dict(arrowstyle="->", connectionstyle="arc3")

ax.set(xlabel="Anzahl Tage Tram Ausserbetrieb", title=f"Scatter Plot: {list_dir[-1]}")

fig, ax = plt.subplots(figsize=(14, 7), subplot_kw=dict(aspect="equal"))

l_l_co = len(l_co)

size = [c_com, c_cor, c_awnf, c_f_l, c_f_k]
tram = ['Combino', 'Cornichon', 'Anhänger', 'Flexity-lang', 'flexity-kurz']
label = [
     'Combino / \nInsg. 28stk.',
     'Cornichon / \nInsg. 26stk.',
     'Anhänger / \nInsg. 20stk.',
     'Flexity-lang / \nInsg. 44stk.',
     'Flexity-kurz / \nInsg. 17stk'
     ]

data = [x for x in size]
tramtyp = [x for x in tram]

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}% ({absolute:d} stk.)"

ax.pie(size, labels=label, autopct=lambda pct: func(pct, size))

ax.legend(tramtyp,
          title=f"Datum: {dt.date.today()}" +" " *20 +"\n" + f"Insgesamt Tram Ausserbetrieb: {l_l_co} \nLegende:",
          loc="center",
          bbox_to_anchor=(1, 0.25, 0.5, 1))


ax.set_title(f"Ausserbetriebsliste: {list_dir[-1]}")

plt.show()