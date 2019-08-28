""" This function will prepare the dataset to be ready for visualization.
It takes as input the url to the data file and returns a cleaned Pandas dataframe """


def load_data(url):
	try:
		#import libraries needed
		import pandas as pd
		import numpy as np
		from urllib.request import Request,urlopen

		#download most recent HadCrut dataset
		req=Request(url,headers={'User-Agent': 'Mozilla/5.0'})
		content=urlopen(req).read()
		file=open("HadCrut.txt","wb")
		file.write(content)
		file.close()

		#read the data into a Pandas dataframe
		hadcrut=pd.read_csv(file.name,delim_whitespace=True,usecols=[0,1],header=None)
		#split the first column into month and year columns
		hadcrut["month"]=hadcrut[0].str.split("/").str[1].astype(int)
		hadcrut["year"]=hadcrut[0].str.split("/").str[0].astype(int)
		#rename the 1 column to value
		hadcrut.rename(columns={1:"value"},inplace=True)
		#select and save all but the first column (0)
		hadcrut=hadcrut[["value","month","year"]].copy()

		#print("before",hadcrut["year"].value_counts(ascending=True).head())
		#check if the most recent year has complete data recordings
		recent=hadcrut["year"].value_counts(ascending=True).head(1)
		if recent.values < [12] :
			#if not complete remove the most recent year
			hadcrut=hadcrut.drop(hadcrut[hadcrut["year"]==(recent.index.values[0])].index)
		#print("after",hadcrut["year"].value_counts(ascending=True).head())

		#create a multiindex using the year and month columns
		hadcrut=hadcrut.set_index(["year","month"])
		# compute the mean of the global temperatures from 1850 to 1900 and subtract that value from the entire dataset
		hadcrut -= hadcrut.loc[1850:1900].mean()

		#return the column names
		hadcrut=hadcrut.reset_index()
	except Exception as e:
		print("Problem in loading the data, reason",e)
	else:
		return hadcrut

