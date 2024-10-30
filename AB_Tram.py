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

#Welche Nr. Welches Tram
#Visualisierung
#Bemerkung zur Datenbank. Input vom Disponent.

#Verbindungsaufbau Sqlite3 und erstellen von Datenbank AB_Tram
connection = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "AB_Tram.db"))
cursor = connection.cursor()

#Erstellen von Tabellen
#eventuell Datum einbauen (Störungsbeginn Datum)
cursor.execute("CREATE TABLE IF NOT EXISTS `trams`(`id` INT AUTO_INCREMENT PRIMARY KEY,`Tramtyp` VRCAHAR(200),`TechnischerPlatz` VRCAHAR(200),`Störungsbeginn` INT,`Auftragsnummer` INTEGER, `Beschreibung` VRCAHAR(200), `Bemerkung` VRCAHAR(200));")

#Aktueller Ordnerpfad
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__))+"""\Ablag_Exports""","")

#Nimmt das aktuellste Excel im Pfad "folder_path"
Liste_Dateien = os.listdir(folder_path)
df = pd.read_excel(folder_path + Liste_Dateien[-1])

df_T =df["Technischer Platz"]
df_Z =df["Störungsbeginn"].dt.date
df_M =df["Meldungsnummer"]
df_B =df["Beschreibung"]

c_com = 0
c_cor = 0
c_awnf = 0
c_f_l = 0
c_f_k = 0
#Datenbank mit Daten aus Excel schreiben
for i, y, z, w in zip(df_T, df_Z, df_M, df_B):
    x = dt.date.today()
    xy = x-y
    s_1 = i.split("TB")[2]
    s_2 = int(s_1[:4])
    if s_2 >= 301 and s_2 <= 399:
        cursor.execute(f"INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`) VALUES ( 'Combino','{i}','{xy.days}','{z}', '{w}');")
        c_com +=1
    elif s_2 >= 478 and s_2 <= 599:
         cursor.execute(f"INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`) VALUES ( 'Cornichon','{i}','{xy.days}','{z}', '{w}');")
         c_cor +=1
    elif s_2 >= 1449 and s_2 <= 1599:
         cursor.execute(f"INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`) VALUES ( 'AWNF (Anhänger)','{i}','{xy.days}','{z}', '{w}');")
         c_awnf +=1
    elif s_2 >= 5001 and s_2 <= 5998:
         cursor.execute(f"INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`) VALUES ( 'Flexity lang','{i}','{xy.days}','{z}', '{w}');")
         c_f_l +=1
    elif s_2 >= 6001 and s_2 <= 6300:
         cursor.execute(f"INSERT INTO `trams`(`Tramtyp`,`TechnischerPlatz`,`Störungsbeginn`,`Auftragsnummer`, `Beschreibung`) VALUES ( 'Flexity kurz','{i}','{xy.days}','{z}', '{w}');")
         c_f_k +=1
    else:
        pass

# F_Dis = input("Bei welcher Tramnummer bzw Technischer Platz soll der Eintrag erfolgen?")
# I_Dis = input("Bemerkung Disponent: ")

# cursor.execute(f"UPDATE trams SET Bemerkung = '{I_Dis}' WHERE '{F_Dis}' = TechnischerPlatz;")

#Zeige alle Zeilen
cursor.execute("Select * from 'trams';")
for row in cursor.fetchall():
     lenth = len(row)
     print("*"*lenth)
     print(f"{row}")
    
    
df_2 = pd.read_sql_query("Select * from 'trams';", connection)


connection.commit()
connection.close()


fig, ax = plt.subplots(figsize=(15, 6))

ax.scatter(x=df_2['Störungsbeginn'], y=df_2['Tramtyp'], s=df_2['Störungsbeginn'])
#annotate https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html
ax.set(xlabel="Anzahl Tage Tram Ausserbetrieb", title=f"Scatter Plot: {Liste_Dateien[-1]}")
plt.show()

fig, ax = plt.subplots(figsize=(14, 7), subplot_kw=dict(aspect="equal"))

tram = [f"{c_com} Combino",
          f"{c_cor} Cornichon",
          f"{c_awnf} Anhänger",
          f"{c_f_l} Flexity-lang",
          f"{c_f_k} Flexity-kurz"]

data = [float(x.split()[0]) for x in tram]
tramtyp = [x.split()[-1] for x in tram]
c_max = sum([c_com, c_cor, c_awnf, c_f_k, c_f_l])

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d} stk)"


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))


ax.legend(wedges, tramtyp,
          title=f"Datum: {x}" +" " *20 +"\n" + f"Insgesamt Tram Ausserbetrieb: {c_max} \nLegende:",
          loc="center",
          bbox_to_anchor=(1, 0, 0.5, 1))


plt.setp(autotexts, size=8, weight="bold")

ax.set_title(f"Ausserbetriebsliste: {Liste_Dateien[-1]}")

plt.show()