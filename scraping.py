from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

url="https://www.imdb.com/india/top-rated-indian-movies/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=f299869f-a183-4a64-a887-6491356429b6&pf_rd_r=BK6RXMS0G4NHMK17JTVQ&pf_rd_s=right-4&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_india_tr_rhs_1"

my_url=urlopen(url)
html=my_url.read()
soup=BeautifulSoup(html,"html.parser")
my_url.close()

movies=[]
table=soup.findAll("tr")
for item in table:
    movie={}
    try:
        movie["Poster"]=item.find("td",{"class":"posterColumn"}).img["src"]
    except AttributeError:
        movie["Poster"]="Not Available"
    
    try:
        movie["Info"]=item.find("td",{"class":"titleColumn"})
    except AttributeError:
        # movie["Rank"]="Not Available"
        # movie["Title"]="Not Available"
        # movie["Year"]="Not Available"
        movie["Info"]="Not Available"
    
    try:
        movie["Rating"]=item.find("td",{"class":"ratingColumn imdbRating"}).string.strip()
    except AttributeError:
        movie["Rating"]="Not Available"
    
    movies.append(movie)

f=open("imdb_india.csv","w")
# w=csv.DictWriter(f,["Poster","Rank","Title","Year","Rating"])
w=csv.DictWriter(f,["Poster","Info","Rating"])
w.writeheader()
for movie in movies:
    w.writerow(movie)
f.close()
