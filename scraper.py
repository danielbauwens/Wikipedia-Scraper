# Imports all necessary libraries.
from bs4 import BeautifulSoup
import requests
import re

# Defines the function to retrieve the first paragraph from each individual wiki-Page
def get_first_paragraph(wikipedia_url):
    client = requests.session()
    wiki = client.get(wikipedia_url)
    soup = BeautifulSoup(wiki.text, "html.parser")
    first_paragraph = ""

    # A for loop that checks the parent classes of "p"(paragraphs) that don't contain the first paragraph and skips those.
    for p in soup.find_all("p"):
        if p.find_parent(class_="bandeau-cell") or p.find_parent(class_="plainlist"):
            continue   

        # Removing html elements from the text.
        p = p.text.strip()

        # Defining the first paragraph and cleaning up left over text so it's easy to read.
        if p != "":
            first_paragraph = p
            first_paragraph = re.sub(r'\(\/.*?\;', '(', str(first_paragraph))
            first_paragraph = re.sub(r'\(.*?\;.*?\;', '(', str(first_paragraph))
            first_paragraph = re.sub(r'\[.*?\]', '', str(first_paragraph))
            first_paragraph = re.sub(r'\xa0', '', str(first_paragraph))

            # Breaking out of the loop checking for "p"(paragraphs). We only want the first one (relevant to us).
            break

    return first_paragraph

# Defines the function to retrieve the leaders per country info + wikipedia link, which then calls the above function
# and adds the newly gathered first paragraph data in to a newly made category in the info dictionary. 
def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    cookie_url = root_url+ "/cookie"
    client = requests.session()

    # Calling the cookies once on initialization to be able to get the countries list.
    cookies = client.get(cookie_url).cookies
    countries_url = root_url+ "/countries"

    # Countries is now defined and can be used later.
    countries = requests.get(countries_url, cookies=cookies).json()
    leaders_url = root_url+ "/leaders"
    leaders_per_country = {}

    # A for loop that iterates over the given countries to retrieve their respective data on its country leaders.
    for entry in countries:
        cname = "country="+entry

        # Every time it iterates over a new country a new cookie is called.
        cookies = client.get(cookie_url).cookies

        # Retrieves and stores the json data in a dictionary; 'leaders_per_country'.
        leaders_per_country[entry] = client.get(leaders_url, params=cname, cookies=cookies).json()

        # This for loop adds a new section in the dictionary; 'Summary'. It stores the 'first_paragraph' data retrieved in
        # the above function 'get_first_paragraph'.
        for i in range(len(leaders_per_country[entry])):
            leaders_per_country[entry][i]['Summary']  = get_first_paragraph(leaders_per_country[entry][i]["wikipedia_url"])

            # For readability I only print the leaders first and last name and their first paragraph. 
            print(leaders_per_country[entry][i]['first_name']+ " "+ leaders_per_country[entry][i]['last_name']+":\n"+ leaders_per_country[entry][i]['Summary'] + "\n")
