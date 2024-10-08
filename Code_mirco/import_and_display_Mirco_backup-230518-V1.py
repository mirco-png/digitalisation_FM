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
import colorama
from colorama import Fore, Style
import openpyxl

from itertools import filterfalse


# Q Is more data available? maybe also for attack players?
# I made the code more flixible so the code will co through all playertypes

# specify the folder path where your CSV files are located
#folder_path = "./data/own_data/Midfield"
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
    # Q i don't get the number manualy and i don't know why the excel list has many none values
    for file in csv_files:
        file_path = os.path.join(folder_path+"/"+type, file)
        df = pd.read_csv(file_path,encoding="utf-8")
        # Normalize MV to MV at 20 years (if not available take 19, 21 or 18, in that order)
        if (df.age==20).any():
            #print("found")
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==20].iloc[0,4]
        elif (df.age==19).any():
            #print("found")
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==19].iloc[0,4]
        elif (df.age==21).any():
            #print("found")
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==21].iloc[0,4]
        elif (df.age==18).any():
            #print("found")
            df["normalized MV"]=df["marketValueUnformatted"]/df[df.age==18].iloc[0,4]
        else:
            df["normalized MV"]=df["marketValueUnformatted"]/df["marketValueUnformatted"].iloc[0]
        df_list.append(df)
    #print(csv_files)

    # Concatenate all dataframes into a single dataframe
    df_merged = pd.concat(df_list, axis=0, ignore_index=True)

    # Save into csv
    data_path=os.path.join(os.path.dirname(os.path.abspath(__file__))+"\data", "")
    df_merged.to_csv(data_path+""+type+"mv.csv",sep=";")


    # Get unique list of player names
    players=list(set(df_merged["Name"]))

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

    # Fit a normal distribution to the data
    def f(x, mu, sigma,A):
        return A/(np.sqrt(np.pi)*sigma)*np.exp(-0.5*((x-mu)/sigma)**2)
    x=np.linspace(18,40,22) #Q how do you define the number for the fitting curve?
    y=means
    # fit the function to the data p0=initial guesses
    popt, pcov, = curve_fit(f, x, y, p0=[28,3,90]) #Q how do you define the number for the fitting curve?
    a, b, c = popt
    ls_model = []
    x_model = np.linspace(min(x), max(x), 100)
    y_model = f(x_model, a, b, c)
    ls_model.append(x_model)
    ls_model.append(y_model)

    # # plot the data and fitted function
    # plt.title(f"Fitting curve of {type} player in the Bundesliga", fontsize=15)
    # plt.scatter(x, y, data=y_model)
    # plt.plot(x_model, y_model)
    # plt.show()

    #Abweichung von der Normalverteilung der Marktwertentwicklung
    df_merged["Div from normal distr"]=df_merged["normalized MV"]-f(df_merged["age"],*popt)
    #sort by age for deviations normalized MV
    devnorm=[]
    for ages in range(18,40):
        if type == "Attack":
            addmvage=df_merged[df_merged.age==ages].iloc[:,7].values
            if not addmvage.any():
                devnorm.append([0])
            else:
                devnorm.append(addmvage)          
        else:
            addmvage=df_merged[df_merged.age==ages].iloc[:,14].values
            if not addmvage.any():
                devnorm.append([0])
            else:
                devnorm.append(addmvage)
    devmeans=[]
    for i in devnorm:
        devmeans.append((np.mean(i)))
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

    # Get median of Div to calculate over- or underperformers
    divvals=[]
    df_merged["performer"]=""

    for iplayer in players:
        if type == "Attack":
            divvalplayer=df_merged[df_merged.Name==iplayer].iloc[:,7].values
            mask=df_merged.Name==iplayer
            if np.median(divvalplayer)>0:
                divvals.append("Over")
                df_merged["performer"]
                df_merged.loc[mask,"performer"]="Over"
            else:
                divvals.append("Under")
                df_merged.loc[mask,"performer"]="Under"
        else:
            divvalplayer=df_merged[df_merged.Name==iplayer].iloc[:,14].values
            mask=df_merged.Name==iplayer
            if np.median(divvalplayer)>0:
                divvals.append("Over")
                df_merged["performer"]
                df_merged.loc[mask,"performer"]="Over"
            else:
                divvals.append("Under")
                df_merged.loc[mask,"performer"]="Under"

    df_merged.to_csv(folder_path+"/"+"total"+type+".csv",encoding="utf-8",sep=";")
    #Show over- and underperformers
    # fig,ax=plt.subplots()
    # ax.plot(players, divvals)
    # fs = 10  # fontsize

    # fig, axs = plt.subplots()

    # axs.violinplot(normmvinage, range(18,40), points=22, widths=0.7,
    #                     showmeans=True, showextrema=True, showmedians=True,bw_method=0.5)
    # axs.set_title(f"market developement of {type} player in the Bundesliga", fontsize=20)
    # axs.set_ylabel('relative market value')
    # axs.set_xlabel('age in years')
    # plt.show()
input_file = open(f"{folder_path}Spielerdetails.csv", "r")

df = pd.read_csv(f"{folder_path}Spielerdetails.csv")
#df.to_csv(f"{folder_path}Spielerdetails.csv", index=False)
ls_d = []
ls_m = []
ls_a = []
ls_d_a = []
ls_m_a = []
ls_s_a = []
ls_d_n = []
ls_m_n = []
ls_s_n = []
dic_squad = {}
counter_3 = 0
d = datetime.datetime.now().date()

df_list_2 = []
for i in input_file:
    s = i.split(",")
    for y in s:
        if y == "Position":
            index_p = counter_3
        elif y == "2022 Market value":
            index_m = counter_3
            index_v = counter_3
        if y == "Geboren":
            index_b = counter_3
        if y == "Nachname":
            index_n = counter_3
        if y == "Vorname":
            index_vn = counter_3
        counter_3 +=1
    if i.split(",")[index_b] != "Geboren":
        d2 = datetime.datetime.strptime(i.split(",")[index_b], '%Y-%m-%d').date()
        d3 = (d-d2)/365
        age = d3.days
        if i.split(",")[index_p] == "Abwehr":
            if i.split(",")[index_n] != "Nachname" and i.split(",")[index_vn] != "Vorname":
                ls_d_n.append(i.split(",")[index_n] + "" +i.split(",")[index_vn])
            ls_d_a.append(age)
            ls_d.append(int(i.split(",")[index_m]))
            dic_squad.update({"defense_age": ls_d_a})
            dic_squad.update({"defense_name": ls_d_n})
        elif i.split(",")[index_p] == "Mittelfeld":
            if i.split(",")[index_n] != "Nachname" and i.split(",")[index_vn] != "Vorname":
                ls_m_n.append(i.split(",")[index_n] + "" +i.split(",")[index_vn])
            ls_m_a.append(age)
            ls_m.append(int(i.split(",")[index_m]))
            dic_squad.update({"midfield_age": ls_m_a})
            dic_squad.update({"midfield_name": ls_m_n})
        elif i.split(",")[index_p] == "Sturm":
            if i.split(",")[index_n] != "Nachname" and i.split(",")[index_vn] != "Vorname":
                ls_s_n.append(i.split(",")[index_n] + "" +i.split(",")[index_vn])
            ls_s_a.append(age)
            ls_a.append(int(i.split(",")[index_m]))
            dic_squad.update({"attack_age": ls_s_a})
            dic_squad.update({"attack_name": ls_s_n})
        dic_squad.update({"defense": ls_d})
        dic_squad.update({"midfield": ls_m})
        dic_squad.update({"attack": ls_a})
 # Concatenate all dataframes into a single dataframe
#df_merged = pd.concat(df_list_2, axis=0, ignore_index=True)

# Save into csv
#data_path=os.path.join(os.path.dirname(os.path.abspath(__file__))+"\data", "")
#df_merged.to_csv(data_path+""+"Spielerdetails.csv",sep=";")
# p = input("which position has your player? (defense, midfield or attacker?): ")
# #c = input("how long is the contract duration?")
# age = round(int(input("please enter the age of the player: ")))
# mv =  round(int(input("please enter the market value of the player (USD $): ")))
# print("thank you for entering the values. the model will calculate the estimated market value of the next 3 years:")
# d = datetime.date.today()
count_1 = (len(ls_relevant_d)/2)
count = (len(ls_relevant_m)/2)
count_2 = len(dic_squad["defense_age"])
count_3 = len(dic_squad["midfield_age"])
count_4 = len(dic_squad["attack_age"])
total_m_1 = 0
total_m_2 = 0
total_m_3 = 0
total_s = 0


print("{:^126}".format("-"*124))
print(Style.BRIGHT + "|{:^124}|".format("Borussia Dortmund | BVB")+ Style.RESET_ALL)
print("|{}|".format("-"*124))
print(Style.BRIGHT + "|{:^124}|".format("Position: "+LS_playertype[0]) + Style.RESET_ALL)
print("|{}|".format("-"*124))
print("| {:10}".format("Back-Nr.")  + "| " +"{:<21}".format("Player name")+ "| " +"{:<19}".format("Contract duration")+ "| "+ "{:<4}".format("age")+"| "+ "MV {:<11}".format(str(d.year) +"/"+str(d.year+1)) +"| " +"MV {:<11}".format(str(d.year+1) +"/"+str(d.year+2)) +"| " + "MV {:<11}".format(str(d.year+2) +"/"+str(d.year+3))+"| "+ "{:<13}".format("Contract end") + "| " )
print("|{}|".format("-"*124))

ls_x1 = []
ls_x2 =[]
ls_x3=[]
ls_y = []
ls_mv = []
count = 0
for a in dic_squad["defense_age"]:
    len_mv = 0
    counter=0
    for i in ls_relevant_d[:23]:
        if round(i) == a:
            r_nr = df["Rücken-Nr."][count]
            name_v = df["Vorname"][count]
            name_n = df["Nachname"][count]
            name = f"{name_v} " + f"{name_n}"
            x1 = df["2022 Market value"][count] * ls_relevant_d[23+counter+1]/ls_relevant_d[23+counter]
            total_m_1 += round(x1)
            duration = df["Vertragslaenge"][count]
            x2 = df["2022 Market value"][count] * ls_relevant_d[23+counter+2]/ls_relevant_d[23+counter]
            total_m_2 += round(x2)
            x3 = df["2022 Market value"][count] * ls_relevant_d[23+counter+3]/ls_relevant_d[23+counter]
            total_m_3 += round(x3)
            ls_x1.append("{:,}".format(round(x1)))
            ls_x2.append("{:,}".format(round(x2)))
            ls_x3.append("{:,}".format(round(x3)))
            mv = "{:<15}".format(round(x2))
            dif_c_year = df["V-Jahr"][count] + duration
            dif_year = dif_c_year - d.year
            ls_y.append(dif_c_year)
            if dif_year == 1:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(a)+"| "+ Fore.YELLOW + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            elif dif_year == 2:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(a)+"| " + Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.YELLOW +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            elif dif_year == 3:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(a)+"| " + Fore.GREEN +"{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " +Fore.YELLOW+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            elif dif_year <= 0:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(a)+"| "+ Fore.RED + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            else:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+ "| "+ "{:<4}".format(a)+"| "+ Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN +"{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x3))+Style.RESET_ALL + "| "  +"{:<13}".format(dif_c_year) + "| " )
            a1 = df["Geboren"][count]
            # d2 = datetime.datetime.strptime(a1.split(",")[index_b], '%Y-%m-%d').date()
            # d3 = (d-d2)/365
            # age = d3.days
            count +=1
        counter +=1
print("|{}|".format("-"*124))
print(Style.BRIGHT + "|{:^124}|".format("Position: "+LS_playertype[1]) + Style.RESET_ALL)
print("|{}|".format("-"*124))
# print("Nr.    " + "| " +"{:<21}".format("Player name") + "| " +"{:<21}".format("Contract duration")+""+"| "+ "MV {:<11}".format(d.year+1) +"| " +"MV {:<11}".format(d.year+2) +"| " + "MV {:<11}".format(d.year+3)+"| " + "{:<13}".format("Contract end") + "| " )
# print("-{}-".format("-"*115))

for m in dic_squad["midfield_age"]:
    counter = 0
    for y in ls_relevant_m[:23]:
        if round(y) == m:
            mv = df["2022 Market value"]
            ls_mv.append(mv)
            r_nr = df["Rücken-Nr."][count]
            name_v = df["Vorname"][count]
            name_n = df["Nachname"][count]
            name = f"{name_v} " + f"{name_n}"
            x1 = df["2022 Market value"][count] * ls_relevant_m[23+counter+1]/ls_relevant_m[23+counter]
            total_m_1 += round(x1)
            duration = df["Vertragslaenge"][count]
            #print(f"{name}     | {duration} |{d.year+1}: " + "{:,}".format(round(x1)) +" USD $")
            x2 = df["2022 Market value"][count] * ls_relevant_m[23+counter+2]/ls_relevant_m[23+counter]
            total_m_2 += round(x2)
            #print(f"Market value of {name} in year {d.year+2}: " + "{:,}".format(round(x2)) +" USD $")
            x3 = df["2022 Market value"][count] * ls_relevant_m[23+counter+3]/ls_relevant_m[23+counter]
            total_m_3 += round(x3)
            ls_x1.append("{:,}".format(round(x1)))
            ls_x2.append("{:,}".format(round(x2)))
            ls_x3.append("{:,}".format(round(x3)))
            dif_c_year = df["V-Jahr"][count] + duration
            dif_year = dif_c_year - d.year
            ls_y.append(dif_c_year)
            if dif_year == 1:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(m)+"| "+ Fore.YELLOW + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            elif dif_year == 2:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(m)+"| " + Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.YELLOW +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            elif dif_year == 3:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(m)+"| " + Fore.GREEN +"{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " +Fore.YELLOW+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            elif dif_year <= 0:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(m)+"| "+ Fore.RED + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
            else:
                print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(m)+"| "+ Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN +"{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x3)) +Style.RESET_ALL +"| "+ "{:<13}".format(dif_c_year) + "| " )
            #print(f"Nr. {count+1}" + " "*c3+f" | {name} " +" "*c+f" | {duration}" +" "*17 +"| "+ "{:^14,}".format(round(x1)) +"| " +"{:^14,}".format(round(x2)) +"| " + "{:^14,}".format(round(x3))+"| " )
            folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__))+"\data", "")            
            count +=1
        counter += 1
print("|{}|".format("-"*124))
print(Style.BRIGHT + "|{:^124}|".format("Position: "+LS_playertype[2]) + Style.RESET_ALL)
print("|{}|".format("-"*124))
for a in dic_squad["attack_age"]:
    counter = 0
    for z in ls_relevant_a[:23]:
        if count == len(df.index):
            pass
        else:
            if round(z) == a:
                r_nr = df["Rücken-Nr."][count]
                name_v = df["Vorname"][count]
                name_n = df["Nachname"][count]
                name = f"{name_v} " + f"{name_n}"
                x1 = df["2022 Market value"][count] * ls_relevant_a[23+counter+1]/ls_relevant_a[23+counter]
                total_m_1 += round(x1)
                duration = df["Vertragslaenge"][count]
                x2 = df["2022 Market value"][count] * ls_relevant_a[23+counter+2]/ls_relevant_a[23+counter]
                total_m_2 += round(x2)
                x3 = df["2022 Market value"][count] * ls_relevant_a[23+counter+3]/ls_relevant_a[23+counter]
                total_m_3 += round(x3)
                ls_x1.append("{:,}".format(round(x1)))
                ls_x2.append("{:,}".format(round(x2)))
                ls_x3.append("{:,}".format(round(x3)))
                dif_c_year = df["V-Jahr"][count] + duration
                dif_year = dif_c_year - d.year
                if dif_year == 1:
                    print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(a)+"| "+ Fore.YELLOW + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
                elif dif_year == 2:
                    print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(a)+"| " + Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.YELLOW +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
                elif dif_year == 3:
                    print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(a)+"| " + Fore.GREEN +"{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " +Fore.YELLOW+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
                elif dif_year <= 0:
                    print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| " +"{:<19}".format(duration)+"| "+ "{:<4}".format(a)+"| "+ Fore.RED + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| "+Fore.RED +"{:<14,}".format(round(x2)) + Style.RESET_ALL +"| " +Fore.RED+ "{:<14,}".format(round(x3)) + Style.RESET_ALL + "| " + "{:<13}".format(dif_c_year) + "| " )
                else:
                    print("| Nr. {:<6}".format(r_nr)+ "| " +"{:<21}".format(name) + "| "  +"{:<19}".format(duration)+"| "+ "{:<4}".format(a)+"| "+ Fore.GREEN + "{:<14,}".format(round(x1)) + Style.RESET_ALL +"| " + Fore.GREEN +"{:<14,}".format(round(x2)) +Style.RESET_ALL +"| " + Fore.GREEN + "{:<14,}".format(round(x3)) +Style.RESET_ALL +"| "+ "{:<13}".format(dif_c_year) + "| " )
                #print(f"Nr. {count+1}" + " "*c3+f" | {name} " +" "*c+f" | {duration}" +" "*17 +"| "+ "{:^14,}".format(round(x1)) +"| " +"{:^14,}".format(round(x2)) +"| " + "{:^14,}".format(round(x3))+"| " )
                ls_y.append(dif_c_year)
                count +=1
            counter += 1

counter=0
c = 1
ls =[]
for s, c in zip(df["Gehalt/Jahr"], df["Vertragslaenge"]):
    dif_c_year = df["V-Jahr"][[counter]] + c
    dif_year = dif_c_year - d.year
    total_s += int(s) * dif_year[counter]
    w = int(s) * dif_year[counter]
    ls.append("{:,}".format(w))
    counter +=1
    c +=1
df["wage"] = ls
df["2023 Market value"] = ls_x1
df["2024 Market value"] = ls_x2
df["2025 Market value"] = ls_x3
df["Contract end"] = ls_y
df.to_excel(f"{folder_path}squad_results.xlsx", index=False)
print("|{}|".format("-"*118))
print(Style.BRIGHT + "| {:<54}".format("Total Market Value") + "| {:<14,}".format(total_m_1)+ "| {:<14,}".format(total_m_2)+ "| {:<29,}|".format(total_m_3) + Style.RESET_ALL)
print("|{}|".format("-"*118))
print(Style.BRIGHT + "| {:<54}".format("Total salary per year") + "| {:<61,}".format(total_s)+ "|")
print("{:^120}".format("-"*120))
# for loop for attacker
# #Vertragsdauer
# #flexibler bei den jahre

