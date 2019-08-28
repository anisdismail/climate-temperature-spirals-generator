"""This is the class to be used for generating the visualization. It prompts the user to
enter the url to the data file and will create the visualization in html format 
in the user's working directory."""

#prompt the user to get the most recent data file url
print("Please refer to https://www.metoffice.gov.uk/hadobs/hadcrut4/data/current/time_series \
 and paste the link to most recent data file here:")

url=input()
from urllib.parse import quote
#encode the url
urlenc=quote(url)
#load the data into a Pandas dataframe and return a
#cleaned version
from loading_data import load_data
hadcrut=load_data(url)

#create the visualization
from loading_viz import load_viz
result=load_viz(hadcrut)
print(result)