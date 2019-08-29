from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup
import csv #don't know how to use just as yet

#setting default headers
# headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
items=[] #maintaining a list of Amazon ASIN codes

#sites[] is the list of bestseller pages...did it this way because I don't know mechanize just as yet
sites=["https://www.amazon.in/gp/bestsellers/books/","https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=2"]
for site in sites:
    # r=requests.get(site,verify=False) #GET request sent
    # html=r.content #after 200 OK, text of the request is stored in html
    r=urlopen(site)
    html=r.read()
    soup=BeautifulSoup(html,'html.parser') #html parser employed
    r.close()
    # tags=soup('a') #searches all <a> tags
    # print(soup)
    # print (tags)
    table=soup.findAll("div",{"class":"a-section a-spacing-none aok-relative"})
    # table=soup.findAll("div",{"class":"p13n-sc-truncated"})
    # print(table)
    # items=[]
    for item in table:
        final={}
        final["URL"]="https://amazon.in"+item.a["href"]
        try:
            final["Title"]=item.find("div",{"class":"p13n-sc-truncate p13n-sc-line-clamp-1"}).string.strip()
        except Exception:
            final["Title"]=item.find("div",{"class":"p13n-sc-truncate p13n-sc-line-clamp-2"}).string.strip()
        except AttributeError:
            final["Title"]="Not Available"
        
        try:
            final["Author"]=item.find("a",{"class":"a-size-small a-link-child"}).string.strip()
        except AttributeError:
            final["Author"]="Not Available"
        
        try:
            final["Rating"]=item.find("span",{"class":"a-icon-alt"}).string.strip()
        except AttributeError:
            final["Rating"]="Not Available"
        if final["Rating"]=="Prime":
            final["Rating"]="Not Available"
        
        try:
            final["Reviews"]=item.find("a",{"class":"a-size-small a-link-normal"}).string.strip()
        except AttributeError:
            final["Reviews"]="Not Available"
        
        try:
            final["Price"]=item.find("span",{"class":"p13n-sc-price"}).string.strip()
            # Price=""
            # for ch in temp:
            #     if (temp!="\"" or temp!=" ")
            #         Price+=ch
        except AttributeError:
            final["Price"]="Not Available"
        items.append(final)
f=open("amazon_bestsellers.csv","w")
w=csv.DictWriter(f,["URL","Title","Author","Rating","Reviews","Price"])
w.writeheader()
for item in items:
    w.writerow(item)
f.close()
