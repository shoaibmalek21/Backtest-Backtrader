import os.path
import sys  
import pandas as pd


df = pd.read_csv('trade_list.csv')
# df = pd.read_csv('test_data.csv') # Trading data(1994-95) 

# If Date with AM & PM format then it's helpful to you.

df.loc[df["Date"].str.contains("|".join(['AM', 'PM'])), 'NEWDT'] = pd.to_datetime(
	df.loc[df["Date"].str.contains("|".join(['AM', 'PM'])), "Date"]
)

df.loc[~df["Date"].str.contains("|".join(['AM', 'PM'])), 'NEWDT'] = pd.to_datetime(
	df.loc[~df["Date"].str.contains("|".join(['AM', 'PM'])), "Date"]
)

del df['Date']
df = df.rename({'NEWDT': 'Date'}, axis=1)
df = df.set_index('Date').sort_index()
print(df)
