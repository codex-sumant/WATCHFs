# coding: utf-8

import pandas as pd
import numpy as np
import re
import subprocess

def postprocessing():
	df = pd.read_csv('final.csv')

	df.drop(['Name'], axis=1, inplace=True)
	df['ELFVersion'] = df['ELFVersion'].apply(lambda x: x[2:])
	df['Flags'] = df['Flags'].apply(lambda x: x[2:])

	req_col = [a for a in df.columns if '_size' in a]
	req_col.extend([a for a in df.columns if 'entsize' in a])

	for i in req_col:
		  df[i] = df[i].apply(lambda x: str(x).replace(".0", ''))
	for i in req_col:
		if(not df[i].empty):
			df[i] = df[i].apply(lambda x: int(str(x), 16) if x != "nan" and "E" not in str(x).upper() else x)
		df[i] = df[i].apply(lambda x: np.NaN if x != "nan" and "E" in str(x).upper() else x)
		df[i] = df[i].apply(lambda x: np.NaN if x == "nan" else x)
		df[i] = pd.to_numeric(df[i])


	attr_list = []
	with open('weka_features_toremove.txt', 'r') as f:
		  for l in f:
		      attr_list.append(l[27:].strip())

	df.drop(attr_list, axis=1, inplace=True)
	df['label'] = '?'

	df.to_csv('final_1.csv', index=False)
	
	subprocess.call('java -cp .:./weka.jar weka.core.converters.CSVLoader final_1.csv > final.arff' , shell=True)





