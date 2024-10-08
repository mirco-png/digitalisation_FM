import pandas as pd #dataframe
import matplotlib.pyplot as plt #graphics
import numpy as np #calculation
from math import pi
import os #data structure
import csv
from scipy.stats import norm
from scipy.optimize import curve_fit #normal distribution
import datetime as datetime
from colorama import Fore, Style
import openpyxl as xl #for financial bilanz

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
    # MV = market value
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
        #The data for type attack has another order than midfield and defence
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
    #Calculate the means and standard deviations for the fitting data
    means=[]
    for i in normmvinage:
        means.append(np.mean(i))
    stdiv=[]
    for i in normmvinage:
        stdiv.append(np.std(i))

    # Fit a normal distribution to the data
    def f(x, mu, sigma,A):
        return A/(np.sqrt(np.pi)*sigma)*np.exp(-0.5*((x-mu)/sigma)**2)
    x=np.linspace(18,40,22) #Q how do you define the number for the fitting curve?
    y=means
    # fit the function to the data p0=initial guesses
    popt, pcov, = curve_fit(f, x, y, p0=[28,3,90])
    a, b, c = popt
    # Create list to get the data of the fitting curve
    ls_model = []
    x_model = np.linspace(min(x), max(x), 100)
    y_model = f(x_model, a, b, c)
    ls_model.append(x_model)
    ls_model.append(y_model)

    # plot the data and fitted function
    plt.title(f"Fitting curve of {type} player in the Bundesliga", fontsize=15)
    plt.scatter(x, y, data=y_model)
    plt.xlabel("age", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 12,
            labelpad = 6)
    plt.ylabel("normalized market value", 
            family='serif', 
            color='r', 
            weight='normal', 
            size = 12,
            labelpad = 6)
    plt.plot(x_model, y_model)
    plt.show()

    #Take the relevant values for each age from 18-40 for each position to calculate the market value in future
    if type == "Defence":
        ls_relevant_d = []
        for i in ls_model:
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
        for i in ls_model:
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
        for i in ls_model:
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
total_m_1 = 0
total_m_2 = 0
total_m_3 = 0
total_s = 0

print("{:^138}".format("-"*136))
print(Style.BRIGHT + "|{:^136}|".format("Borussia Dortmund | BVB")+ Style.RESET_ALL)
print("|{}|".format("-"*136))
print(Style.BRIGHT + "|{:^136}|".format("Position: "+LS_playertype[0]) + Style.RESET_ALL)
print("|{}|".format("-"*136))
print("| {:10}".format("Back-Nr.")  + "| " +"{:<21}".format("Player name")+ "| " + "{:<10}".format("Position")+ "| " +"{:<19}".format("Contract duration")+ "| "+ "{:<4}".format("age")+"| "+ "MV {:<11}".format(str(d.year) +"/"+str(d.year+1)) +"| " +"MV {:<11}".format(str(d.year+1) +"/"+str(d.year+2)) +"| " + "MV {:<11}".format(str(d.year+2) +"/"+str(d.year+3))+"| "+ "{:<13}".format("Contract end") + "| " )
print("|{}|".format("-"*136))

ls_x1 = []
ls_x2 =[]
ls_x3=[]
ls_y = []
ls_mv = []
count = 0
for a, p, v, n, r_nr, in zip(df["Born"], df["Position"], df["Vorname"], df["Nachname"], df["Ruecken-Nr."] ):
    name = f"{v} " + f"{n}"
    counter=0
    d2 = datetime.datetime.strptime(a, '%Y-%m-%d').date()
    d3 = (d-d2)/365
    age = int(d3.days)
    duration = df["contract duration"][count]
    dif_c_year = df["c-year"][count] + duration
    if age >= 18: #parameter settings for scenarios
        if p == "defence":
            for i in ls_relevant_d[:23]:
                if round(i) == age:
                    x1 = df["2022 Market value"][count] * ls_relevant_d[23+counter+1]/ls_relevant_d[23+counter]
                    x2 = df["2022 Market value"][count] * ls_relevant_d[23+counter+2]/ls_relevant_d[23+counter]
                    x3 = df["2022 Market value"][count] * ls_relevant_d[23+counter+3]/ls_relevant_d[23+counter]
                    count +=1
                counter +=1
        elif p == "midfield":
            for i in ls_relevant_m[:23]:
                if round(i) == age:
                    x1 = df["2022 Market value"][count] * ls_relevant_m[23+counter+1]/ls_relevant_m[23+counter]
                    x2 = df["2022 Market value"][count] * ls_relevant_m[23+counter+2]/ls_relevant_m[23+counter]
                    x3 = df["2022 Market value"][count] * ls_relevant_m[23+counter+3]/ls_relevant_m[23+counter]
                    count +=1
                counter +=1
        elif p == "attack":
            for i in ls_relevant_a[:23]:
                if round(i) == age:
                    x1 = df["2022 Market value"][count] * ls_relevant_a[23+counter+1]/ls_relevant_a[23+counter]
                    x2 = df["2022 Market value"][count] * ls_relevant_a[23+counter+2]/ls_relevant_a[23+counter]
                    x3 = df["2022 Market value"][count] * ls_relevant_a[23+counter+3]/ls_relevant_a[23+counter]
                    count +=1
                counter +=1
        dif_year = dif_c_year - d.year
        if dif_year == 1:
            print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " + "{:<10}".format(p) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(age)+"| "+ Fore.YELLOW + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
        elif dif_year == 2:
            print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " + "{:<10}".format(p) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(age)+"| " + Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.YELLOW +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
        elif dif_year == 3:
            print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " + "{:<10}".format(p) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(age)+"| " + Fore.GREEN +"{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " +Fore.YELLOW+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
        elif dif_year <= 0:
            print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " + "{:<10}".format(p) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(age)+"| "+ Fore.RED + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
        else:
            print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " + "{:<10}".format(p) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(age)+"| "+ Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN +"{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x3))+Style.RESET_ALL + "| "  +"{:<13}".format(dif_c_year) + "| " )
    else:
        x1 = 0
        x2 = 0
        x3 = 0
        x11 = 0
        x12 = 0
        x33 = 0
        print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " + "{:<10}".format(p) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(age)+"| "+ Fore.YELLOW + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
        count +=1
    ls_y.append(dif_c_year)
    total_m_1 += round(x1)
    total_m_2 += round(x2)
    total_m_3 += round(x3)
    ls_x1.append("{}".format(round(x1)))
    ls_x2.append("{}".format(round(x2)))
    ls_x3.append("{}".format(round(x3)))
    counter +=1


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
    total_s +=s
    counter +=1
    c +=1
df["wage"] = ls
df["2024 Market value"] = pd.Series(ls_x1)
df["2025 Market value"] = pd.Series(ls_x2)
df["2026 Market value"] = pd.Series(ls_x3)
df["Contract end"] = pd.Series(ls_y)
df.to_excel(f"{folder_path}squad_results.xlsx", index=False)
print("|{}|".format("-"*136))
print(Style.BRIGHT + "| {:<72}".format("Total Market Value") + "| {:<14,}".format(total_m_1)+ "| {:<14,}".format(total_m_2)+ "| {:<29,}|".format(total_m_3) + Style.RESET_ALL)
print("|{}|".format("-"*136))
print(Style.BRIGHT + "| {:<72}".format("Total salary per year") + "| {:<61,}".format(total_s)+ "|")
print("{:^138}".format("-"*136))



total_m_11 = 0
total_m_22 = 0
total_m_33 = 0
total_s2 = 0

ls_x11 = []
ls_x22 =[]
ls_x33=[]
ls_y = []
ls_mv = []
df2 = pd.read_excel(f"{folder_path}squad_results-scenario.xlsx")
df3 = pd.read_excel(f"{folder_path}squad_results.xlsx")
workbook = xl.load_workbook(f"{folder_path}ka-gesamtergebnisrechnung-bvb-gb2122.xlsx")
excel_sheet = workbook['ka-gesamtergebnisrechnung']
value = excel_sheet['C18'].value

sheet = workbook.active
x=0
xw = 0
for i, y, m, w in zip(df2["Vorname"], df["Vorname"], df3["2024 Market value"], df3["wage per year"]):
    if i != y:
        x += m
        value += w /1000
sheet["C11"] = round(int(x)/1000)
sheet["C18"] = round(int(value))

workbook.save(f"{folder_path}ka-gesamtergebnisrechnung-bvb-gb2122.xlsx")

#-------------------------start parameters to optimize the model----------------------------------------------
    #Abweichung von der Normalverteilung der Marktwertentwicklung
    # df_merged["Div from normal distr"]=df_merged["normalized MV"]-f(df_merged["age"],*popt)
    # #sort by age for deviations normalized MV
    # devnorm=[]
    # for ages in range(18,40):
    #     if type == "Attack":
    #         addmvage=df_merged[df_merged.age==ages].iloc[:,7].values
    #         if not addmvage.any():
    #             devnorm.append([0])
    #         else:
    #             devnorm.append(addmvage)          
    #     else:
    #         addmvage=df_merged[df_merged.age==ages].iloc[:,14].values
    #         if not addmvage.any():
    #             devnorm.append([0])
    #         else:
    #             devnorm.append(addmvage)
    # devmeans=[]
    # for i in devnorm:
    #     devmeans.append((np.mean(i)))


    # # Get median of Div to calculate over- or underperformers
    # divvals=[]
    # df_merged["performer"]=""

    # for iplayer in players:
    #     if type == "Attack":
    #         divvalplayer=df_merged[df_merged.Name==iplayer].iloc[:,7].values
    #         mask=df_merged.Name==iplayer
    #         if np.median(divvalplayer)>0:
    #             divvals.append("Over")
    #             df_merged["performer"]
    #             df_merged.loc[mask,"performer"]="Over"
    #         else:
    #             divvals.append("Under")
    #             df_merged.loc[mask,"performer"]="Under"
    #     else:
    #         divvalplayer=df_merged[df_merged.Name==iplayer].iloc[:,14].values
    #         mask=df_merged.Name==iplayer
    #         if np.median(divvalplayer)>0:
    #             divvals.append("Over")
    #             df_merged["performer"]
    #             df_merged.loc[mask,"performer"]="Over"
    #         else:
    #             divvals.append("Under")
    #             df_merged.loc[mask,"performer"]="Under"

    # df_merged.to_csv(folder_path+"/"+"total"+type+".csv",encoding="utf-8",sep=";")
#-------------------------end parameters to optimize the model----------------------------------------------