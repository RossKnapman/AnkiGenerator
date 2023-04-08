# -*- coding: utf-8 -*-
import time
import random
import csv
import codecs
import re
import requests
import urllib
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS

### Write to file as going, not at the end!

words = []

# language = 'german'
language = 'french'

f = codecs.open("My Clippings.txt", 'r', 'utf-8')

lines = f.read().splitlines()

for i in range(len(lines)):
    if lines[i] == "==========":
#        word = re.sub(r'[^a-zA-Z]', "", lines[i-1])
        word = lines[i-1]
        words.append(word)

# Now remove any duplicates
words = list(set(words))

# sentences = []
# translations = []
# failed = []


## Get a random proxy (taken from https://codelike.pro/create-a-crawler-with-rotating-ip-proxy-in-python/)

ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

def random_proxy():
  return random.randint(0, len(proxies) - 1)

# Retrieve latest proxies
def retrieveProxies():
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BS(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
      proxies.append({
        'ip':   row.find_all('td')[0].string,
        'port': row.find_all('td')[1].string
  })

    return proxies

# Choose a random proxy
proxies = retrieveProxies()
proxy_index = random_proxy()
proxy = proxies[proxy_index]


for i in range(len(words)):
    word = words[i]

    page = None

    while page is None:

        proxiesDict = {
            "http": "http://" + proxy["ip"] + ":" + proxy["port"],
            "https": "http://" + proxy["ip"] + ":" + proxy["port"],
        }

        try:

            page = requests.get("https://www.linguee.com/english-" + language + "/search?source=auto&query=" + word, proxies=proxiesDict)

        except:
            proxies = retrieveProxies()
            print("Lost connection, changing proxy...")
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]


    print("Creating soup...")
    soup = BS(page.text, "html.parser")

    print("Finding lines...")
    lines = soup.find_all(class_="tag_e")

    # Get all examples

    #for line in lines:
    #    sentence = line.find(class_="tag_s")
    #    print(sentence.contents[0])
    #    translation = line.find(class_="tag_t")
    #    print(translation.contents[0])


    # Just get the first example
    try:
        sentence = lines[0].find(class_="tag_s").contents[0]
        translation = lines[0].find(class_="tag_t").contents[0]

        print(word)
        print(sentence)
        print(translation)
        print("\n")

        csvfile = open('phrases.csv', 'a+')
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow([sentence, translation])

        # sentences.append(sentence)
        # translations.append(translation)


    except IndexError:
        print("Word failed:", word)
        print("\n")
        # failed.append(word)

    # time.sleep(0.5)

    # Generate new proxy every 10 requests
    if i % 10 == 0:
        proxy_index = random_proxy()
        proxy = proxies[proxy_index]
