# -*- coding: utf-8 -*-
import time
import random
import csv
import codecs
import re
import requests
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

noRequests = 0

sentences = []
translations = []

for i in range(len(words)):

    word = words[i]

    page = requests.get("https://www.linguee.com/english-german/search?source=auto&query=" + word)


    noRequests += 1
    soup = BS(page.text, "html.parser")

    isBlocked = soup.find(text="You have sent too many requests causing Linguee to block your computer")
    if isBlocked:
        print("Blocked for sending too many requests after " + str(noRequests) + " requests :(")

        # Write what we have so far to the file
        assert len(sentences) == len(translations)

        print(sentences)
        print(translations)

        with open("sentences.csv", "wb") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            for i in range(len(sentences)):
                writer.writerow([sentences[i], translations[i]])
        break

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

    time.sleep(random.randrange(10, 20))


assert len(sentences) == len(translations)

with open("sentences.csv", "wb") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    for i in range(len(sentences)):
        writer.writerow([sentences[i], translations[i]])