from urllib.request import urlopen
import re
import requests
from bs4 import BeautifulSoup
import csv

items = [] # maintaining a list of Amazon ASIN codes

# sites[] is the list of bestseller pages...did it this way because I don't know mechanize just as yet
sites = ["https://www.amazon.in/gp/bestsellers/books/","https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_2?ie=UTF8&pg=2"]

for site in sites:
    r = urlopen(site)
    html = r.read()
    soup = BeautifulSoup(html,'html.parser') #html parser employed
    r.close()
    table = soup.findAll("div",{"class":"a-section a-spacing-none aok-relative"})
    for item in table:
        final = {}
        final["URL"] = "https://amazon.in"+item.a["href"]
        try:
            final["Title"] = item.find("div",{"class":"p13n-sc-truncate p13n-sc-line-clamp-1"}).string.strip()
        except Exception:
            final["Title"] = item.find("div",{"class":"p13n-sc-truncate p13n-sc-line-clamp-2"}).string.strip()
        except AttributeError:
            final["Title"] = "Not Available"
        
        try:
            final["Author"] = item.find("a",{"class":"a-size-small a-link-child"}).string.strip()
        except AttributeError:
            final["Author"] = "Not Available"
        
        try:
            final["Rating"] = item.find("span",{"class":"a-icon-alt"}).string.strip()
        except AttributeError:
            final["Rating"] = "Not Available"
        if final["Rating"] == "Prime":
            final["Rating"] = "Not Available"
        
        try:
            final["Reviews"] = item.find("a",{"class":"a-size-small a-link-normal"}).string.strip()
        except AttributeError:
            final["Reviews"] = "Not Available"
        
        try:
            final["Price"] = item.find("span",{"class":"p13n-sc-price"}).string.strip()
        except AttributeError:
            final["Price"] = "Not Available"
        items.append(final)
        
f = open("amazon_bestsellers.csv","w")
w = csv.DictWriter(f,["URL","Title","Author","Rating","Reviews","Price"])
w.writeheader()
for item in items:
    if 1 == 1:
        w.writerow(item)
f.close()
