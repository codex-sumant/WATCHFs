import 	numpy as np 
import pandas as pd 
import re

df = pd.read_csv("train.csv",low_memory=False)

df.drop(['Name'], axis=1, inplace=True)
df['ELFVersion'] = df['ELFVersion'].apply(lambda x: str(x)[2:])
df['Flags'] = df['Flags'].apply(lambda x: str(x)[2:])

req_col = [a for a in df.columns if '_size' in a]
req_col.extend([a for a in df.columns if 'entsize' in a])

for i in req_col:
    df[i] = df[i].apply(lambda x: str(x).replace(".0", ''))
for i in req_col:
    df[i] = df[i].apply(lambda x: int(str(x), 16) if x != "nan" and "E" not in str(x).upper() else x)
    df[i] = df[i].apply(lambda x: np.NaN if x != "nan" and "E" in str(x).upper() else x)
    df[i] = df[i].apply(lambda x: np.NaN if x == "nan" else x)
    df[i] = pd.to_numeric(df[i])

attr_list = []
with open('weka_features_toremove.txt', 'r') as f:
    for l in f:
        attr_list.append(l[27:].strip())

df.drop(attr_list, axis=1, inplace=True)

from sklearn.preprocessing import LabelEncoder

lb_make = LabelEncoder()
df["Identification_l"] = lb_make.fit_transform(df["Identification"])
print(df.dtypes)

df.to_csv("final_train.csv", index=False)
