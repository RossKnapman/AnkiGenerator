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

# To do: write a separate file for the words that failed

words = []

f = codecs.open("My Clippings.txt", 'r', 'utf-8')

lines = f.read().splitlines()

for i in range(len(lines)):
    if lines[i] == "==========":
#        word = re.sub(r'[^a-zA-Z]', "", lines[i-1])
        word = lines[i-1]
        words.append(word)

#print(words)

# Now remove any duplicates
words = list(set(words))

sentences = []
translations = []
failed = []


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

print(len(proxies))

# Choose a random proxy
proxies = retrieveProxies()
proxy_index = random_proxy()
proxy = proxies[proxy_index]



for i in range(len(words)):
    print(i)
    word = words[i]



    # req = Request("https://www.linguee.com/english-german/search?source=auto&query=" + word)
    # req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
    # soup = BS(urlopen(req).read(), "html.parser")

    page = None

    while page is None:

        proxiesDict = {
            "http": "http://" + proxy["ip"] + ":" + proxy["port"],
            "https": "http://" + proxy["ip"] + ":" + proxy["port"],
        }

        try:

            print("Proxy:", proxy["ip"])
            page = requests.get("https://www.linguee.com/english-german/search?source=auto&query=" + word, proxies=proxiesDict)

        except:
            proxies = retrieveProxies()
            print("Lost connection, changing proxy...")
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]
            print("New proxy:", proxy["ip"])


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

        sentences.append(sentence)
        translations.append(translation)


    except IndexError:
        print("Word failed:", word)
        print("\n")
        failed.append(word)

    # time.sleep(0.5)

    # Generate new proxy every 10 requests
    if i % 10 == 0:
        proxy_index = random_proxy()
        proxy = proxies[proxy_index]


assert len(sentences) == len(translations)

print(sentences)
print(translations)
print(failed)

with open("sentences.csv", "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    for i in range(len(sentences)):
        writer.writerow([sentences[i], translations[i]])
