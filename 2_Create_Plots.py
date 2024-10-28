import pandas as pd #dataframe
import matplotlib.pyplot as plt #graphics
import numpy as np #calculation
from math import pi
import os #data structure

folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__))+"\Test2\Code_mirco\data", "")
input_file = open(f"{folder_path}Spielerdetails.csv", "r")
df = pd.read_csv(f"{folder_path}Spielerdetails.csv")

print(df.head())

df.plot()
plt.show()
