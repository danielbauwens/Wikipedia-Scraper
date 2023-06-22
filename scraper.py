import requests
import re
from bs4 import BeautifulSoup

def get_first_paragraph(wikipedia_url):
    client = requests.session()
    wiki = client.get(wikipedia_url)
    soup = BeautifulSoup(wiki.text, "html.parser")
    first_paragraph = ""
    for p in soup.find_all("p"):
        if p.find_parent(class_="bandeau-cell") or p.find_parent(class_="plainlist"):
            continue   
        p = p.text.strip()
        if p != "":
            first_paragraph = p
            break
    return first_paragraph

def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    cookie_url = root_url+ "/cookie"
    client = requests.session()
    cookies = client.get(cookie_url).cookies
    countries_url = root_url+ "/countries"
    countries = client.get(countries_url, cookies=cookies).json()
    leaders_url = root_url+ "/leaders"
    leaders_per_country = {}
    
    for entry in countries:
            try:
                cname = "country="+entry
                leaders_per_country[entry] = client.get(leaders_url, params=cname, cookies=cookies).json()
                for i in range(len(leaders_per_country[entry])):
                    leaders_per_country[entry][i]['Summary']  = get_first_paragraph(leaders_per_country[entry][i]["wikipedia_url"])
                    return leaders_per_country[entry][i], leaders_per_country[entry][i]['Summary']
            except KeyError: 
                cookies = client.get(cookie_url).cookies
                continue
get_leaders()