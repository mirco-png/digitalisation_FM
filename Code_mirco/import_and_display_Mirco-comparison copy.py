import pandas as pd #dataframe
import matplotlib.pyplot as plt #graphics
import numpy as np #calculation
from math import pi
import os #data structure
import csv
from scipy.stats import norm
from scipy.optimize import curve_fit #normal distribution
from math import isnan
import datetime as datetime
from colorama import Fore, Style
import openpyxl
from pathlib import Path


# Select folder path data within the existing path
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__))+"\data", "")

# Choose which player typ: defense, midfield, attack
LS_playertype=["Defence", "Midfield", "Attack"]

# Get a list of all CSV files in the folder
# Loop through list of types to investiged different types
for type in LS_playertype:
    file_list = os.listdir(folder_path+"/"+type)
    csv_files = [file for file in file_list if file.endswith('.csv')]

    # Create an empty list to store the dataframes
    df_list = []

    # Loop through the CSV files and append the dataframes to the list
    for file in csv_files:
        file_path = os.path.join(folder_path+"/"+type, file)
        df = pd.read_csv(file_path,encoding="utf-8")
        # Normalize MV to MV at 20 years (if not available take 19, 21 or 18, in that order)
        if (df.age==20).any():
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==20].iloc[0,4]
        elif (df.age==19).any():
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==19].iloc[0,4]
        elif (df.age==21).any():
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==21].iloc[0,4]
        elif (df.age==18).any():
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==18].iloc[0,4]
        else:
            df["normalized MV"]=df["marketValueUnformatted"]/df["marketValueUnformatted"].iloc[0]
        df_list.append(df)

    # Concatenate all dataframes into a single dataframe
    df_merged = pd.concat(df_list, axis=0, ignore_index=True)

    # Save into csv
    data_path=os.path.join(os.path.dirname(os.path.abspath(__file__))+"\data", "")
    df_merged.to_csv(data_path+""+type+"mv.csv",sep=";")

    #sort by age for normalized MV
    normmvinage=[]
    for ages in range(18,40):
        if type == "Attack":
            addmvage=df_merged[df_merged.age==ages].iloc[:,6].values
            if not addmvage.any():
                normmvinage.append([0])
            else:
                normmvinage.append(addmvage)
        else:
            addmvage=df_merged[df_merged.age==ages].iloc[:,13].values
            if not addmvage.any():
                normmvinage.append([0])
            else:
                normmvinage.append(addmvage)
    means=[]
    for i in normmvinage:
        means.append(np.mean(i))
    stdiv=[]
    for i in normmvinage:
        stdiv.append(np.std(i))

    # Fit a normal distribution to the data / np.pi *2
    def f(x, mu, sigma,A):
        return A/(np.sqrt(np.pi)*sigma)*np.exp(-0.5*((x-mu)/sigma)**2)
    x=np.linspace(18,40,22) #Q how do you define the number for the fitting curve?
    y=means
    # fit the function to the data p0=initial guesses
    popt, pcov, = curve_fit(f, x, y, p0=[28,3,90])
    a, b, c = popt
    ls_pmodel = []
    x_model = np.linspace(min(x), max(x), 100)
    y_model = f(x_model, a, b, c)
    ls_pmodel.append(x_model)
    ls_pmodel.append(y_model)

    if type == "Defence":
        ls_relevant_d = []
        for i in ls_pmodel:
            ls_relevant_d.append(i[0])
            ls_relevant_d.append(i[5])
            ls_relevant_d.append(i[9])
            ls_relevant_d.append(i[14])
            ls_relevant_d.append(i[18])
            ls_relevant_d.append(i[23])
            ls_relevant_d.append(i[27])
            ls_relevant_d.append(i[32])
            ls_relevant_d.append(i[36])
            ls_relevant_d.append(i[41])
            ls_relevant_d.append(i[45])
            ls_relevant_d.append(i[50])
            ls_relevant_d.append(i[54])
            ls_relevant_d.append(i[59])
            ls_relevant_d.append(i[63])
            ls_relevant_d.append(i[68])
            ls_relevant_d.append(i[72])
            ls_relevant_d.append(i[77])
            ls_relevant_d.append(i[81])
            ls_relevant_d.append(i[86])
            ls_relevant_d.append(i[90])
            ls_relevant_d.append(i[95])
            ls_relevant_d.append(i[99])

    elif type == "Midfield":
        ls_relevant_m = []
        for i in ls_pmodel:
            ls_relevant_m.append(i[0])
            ls_relevant_m.append(i[5])
            ls_relevant_m.append(i[9])
            ls_relevant_m.append(i[14])
            ls_relevant_m.append(i[18])
            ls_relevant_m.append(i[23])
            ls_relevant_m.append(i[27])
            ls_relevant_m.append(i[32])
            ls_relevant_m.append(i[36])
            ls_relevant_m.append(i[41])
            ls_relevant_m.append(i[45])
            ls_relevant_m.append(i[50])
            ls_relevant_m.append(i[54])
            ls_relevant_m.append(i[59])
            ls_relevant_m.append(i[63])
            ls_relevant_m.append(i[68])
            ls_relevant_m.append(i[72])
            ls_relevant_m.append(i[77])
            ls_relevant_m.append(i[81])
            ls_relevant_m.append(i[86])
            ls_relevant_m.append(i[90])
            ls_relevant_m.append(i[95])
            ls_relevant_m.append(i[99])
        
    elif type == "Attack":
        ls_relevant_a = []
        for i in ls_pmodel:
            ls_relevant_a.append(i[0])
            ls_relevant_a.append(i[5])
            ls_relevant_a.append(i[9])
            ls_relevant_a.append(i[14])
            ls_relevant_a.append(i[18])
            ls_relevant_a.append(i[23])
            ls_relevant_a.append(i[27])
            ls_relevant_a.append(i[32])
            ls_relevant_a.append(i[36])
            ls_relevant_a.append(i[41])
            ls_relevant_a.append(i[45])
            ls_relevant_a.append(i[50])
            ls_relevant_a.append(i[54])
            ls_relevant_a.append(i[59])
            ls_relevant_a.append(i[63])
            ls_relevant_a.append(i[68])
            ls_relevant_a.append(i[72])
            ls_relevant_a.append(i[77])
            ls_relevant_a.append(i[81])
            ls_relevant_a.append(i[86])
            ls_relevant_a.append(i[90])
            ls_relevant_a.append(i[95])
            ls_relevant_a.append(i[99])



input_file = open(f"{folder_path}Spielerdetails.csv", "r")
df = pd.read_csv(f"{folder_path}Spielerdetails.csv")
d = datetime.datetime.now().date()


counter=0
c = 1
ls =[]
for s, c in zip(df["wage per year"], df["contract duration"]):
    dif_c_year = df["c-year"][[counter]] + c
    dif_year = dif_c_year - d.year
    year = d.year
    if int(dif_c_year) == d.year and s >0:
        s = int(s) * 0.5
        ls.append("{:,}".format(s))
    else:
        s = int(s) * dif_year[counter]
        ls.append("{:,}".format(s))
    counter +=1
    c +=1

df.to_excel(f"{folder_path}squad_results_c.xlsx", index=False)


c = 0
ls_age_t =      []
ls_tm_t =       []
ls_pm_t =       []
ls_dif_t =      []
ls_difp_t =     []
ls_pm3_t =      []
ls_dif3_t =     []
ls_difp3_t =    []
for i in df["Vorname"]:
    x=  0
    xc = 0
    x2= 0
    x3= 0
    ls_tm =     []
    ls_pm =     []
    ls_age =    []
    ls_dif =    []
    ls_difp =   []
    ls_pm3 =    []
    ls_dif3 =   []
    ls_difp3 =  []
    while x < 15:
        d2 = datetime.datetime.strptime(df["Born"][c], '%Y-%m-%d').date()
        d3 = (d-d2)/365
        age = int(d3.days)
        age = age-15+x
        if age >= 18:
            xc +=1
        string = f"{2007+x} "+ "Market value"
        tm = df[string][c] /1000
        pm = int(df[string][c] * ls_relevant_d[23+xc+1]/ls_relevant_d[23+xc]) /1000
        dif = tm - pm
        if tm !=0:
            difp = abs(dif)*100/tm
        else:
            difp = 0
        ls_difp.append(difp)
        ls_dif.append(dif)
        ls_tm.append(round(tm))
        ls_age.append(age)
        ls_pm.append(round(pm))
        x += 1
    while x3 < 5:
        string1 = f"{2007+x2} "+ "Market value"
        string2 = f"{2007+x2+1} "+ "Market value"
        string3 = f"{2007+x2+2} "+ "Market value"
        tm1 = df[string1][c] /1000
        tm2 = df[string2][c] /1000
        tm3 = df[string3][c] /1000
        pm1 = int(df[string1][c] * ls_relevant_d[23+x2+1]/ls_relevant_d[23+x2])
        pm2 = int(pm1 * ls_relevant_d[23+x2+2]/ls_relevant_d[23+x2+1])
        pm3 = int(pm2 * ls_relevant_d[23+x2+3]/ls_relevant_d[23+x2+2])
        dif1 = tm1 - pm1
        dif2 = tm2 - pm2
        dif3 = tm3 - pm3
        ls_pm3.append(round(pm1/1000))
        ls_pm3.append(round(pm2 /1000))
        ls_pm3.append(round(pm3 /1000))
        ls_dif3.append(round(dif1))
        ls_dif3.append(round(dif2))
        ls_dif3.append(round(dif3))
        x3 += 1
        x2 += 3
    ls_pm_t.append(ls_pm)
    ls_tm_t.append(ls_tm)
    ls_age_t.append(ls_age) 
    ls_dif_t.append(ls_dif)
    ls_pm3_t.append(ls_pm3)
    ls_dif3_t.append(ls_dif3)
    ls_difp_t.append(ls_difp)
    c +=1

t = 0
tt = 0
ls_t = []
ls_tt = []
for i, ii in zip(ls_difp_t, ls_dif_t):
    c = 0
    cc = 0
    for y in i:
        if y != 0:
            t += y
            c += 1
        else:
            t = 0
            c += 1
    ls_t.append(int(t/c))
    for yy in ii:
        if yy != 0:
            tt += yy
            cc+=1
    ls_tt.append(tt/cc)

co =    0
d =     {}
c =     0
for a, t, p, i, p3, i3, pp in zip(ls_age_t, ls_tm_t, ls_pm_t, ls_dif_t, ls_pm3_t, ls_dif3_t, ls_difp_t):
    v = df["Vorname"][co]
    n = df["Nachname"][co]
    d[f"age for {v} {n}"] = a
    d[f"deviation market value for {v} {n}"] =      i
    d[f"deviation market value in % for {v} {n}"] = pp
    d[f"deviation market value (3) for {v} {n}"] =  i3
    d[f"predicted market value (3) for {v} {n}"] =  p3
    d[f"predicted market value for {v} {n}"] =      p
    d[f"transfermarkt market value for {v} {n}"] =  t
    
    
    co +=1
co =0

df_new = pd.DataFrame(d)
c = 0

#Error handling if folder doesn't exist creating folder for saving graphics
try:
    os.stat(f"{folder_path}/graphics_1-year_prediction")
    os.stat(f"{folder_path}/graphics_1-year_deviation")
    os.stat(f"{folder_path}/graphics_3-year_prediction")
    os.stat(f"{folder_path}/graphics_3-year_deviation")
except:
    os.mkdir(f"{folder_path}/graphics_1-year_prediction")
    os.mkdir(f"{folder_path}/graphics_1-year_deviation")
    os.mkdir(f"{folder_path}/graphics_3-year_prediction")
    os.mkdir(f"{folder_path}/graphics_3-year_deviation")


#Creating graphics
for n, v in zip(df["Vorname"], df["Nachname"]):
    df_new.plot(y=[f"predicted market value for {n} {v}", f"transfermarkt market value for {n} {v}"], x=f"age for {n} {v}" , figsize=(14, 7))
    plt.title(f"Comparison market value development for {n} {v} with an average forecast error of {ls_t[c]}%")
    plt.xlabel("age", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.ylabel("Market value in Tsd Euro", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.savefig(f"{folder_path}/graphics_1-year_prediction/{c} {n} {v}.png")
    df_new.plot(y=[f"deviation market value for {n} {v}"], x=f"age for {n} {v}" , figsize=(14, 7))
    plt.xlabel("age", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.ylabel("deviation Market value in Tsd Euro", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.savefig(f"{folder_path}/graphics_1-year_deviation/{c} d {n} {v}.png")
    df_new.plot(y=[f"deviation market value in % for {n} {v}"], x=f"age for {n} {v}" , figsize=(14, 7))
    plt.title(f"deviation market value in % and forecaste error of {ls_t[c]}% for {n} {v}")
    plt.xlabel("age", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.ylabel("deviation Market value in %", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.savefig(f"{folder_path}/graphics_1-year_deviation/ d in % {n} {v}.png")
    df_new.plot(y=[f"predicted market value (3) for {n} {v}", f"transfermarkt market value for {n} {v}"], x=f"age for {n} {v}" , figsize=(14, 7))
    plt.title(f"3-year market value comparison for {n} {v}")
    plt.xlabel("age", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.ylabel("Market value in Tsd Euro", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.savefig(f"{folder_path}/graphics_3-year_prediction/{c} (3) {n} {v}.png")
    df_new.plot(y=[f"deviation market value (3) for {n} {v}"], x=f"age for {n} {v}" , figsize=(14, 7))
    plt.xlabel("age", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.ylabel("deviation Market value in Tsd Euro", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 16,
            labelpad = 6)
    plt.savefig(f"{folder_path}/graphics_3-year_deviation/{c} (3) d {n} {v}.png")
    c +=1