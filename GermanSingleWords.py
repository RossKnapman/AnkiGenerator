# -*- coding: utf-8 -*-
import codecs
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv
import sys


language = 'de'

words = []

# Need to have chromedriver installed
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# For my simple list
f = codecs.open('My Clippings.txt', 'r', 'utf-8')
lines = f.read().splitlines()

for i in range(len(lines)):
    words.append(lines[i])

# f = codecs.open("My Clippings.txt", 'r', 'utf-8')
#
# lines = f.read().splitlines()
#
# for i in range(len(lines)):
#     if lines[i] == "==========":
# #        word = re.sub(r'[^a-zA-Z]', "", lines[i-1])
#         word = lines[i-1]
#         words.append(word)
#
# # Now remove any duplicates
# words = list(set(words))

for word in words:

    if word != '':

        try:

            csvfile = open('words.csv', 'a+')
            writer = csv.writer(csvfile, delimiter=";")

            driver = webdriver.Chrome(options=options)
            driver.get('https://www.deepl.com/translator')
            driver.find_element_by_tag_name('textarea').send_keys(word)

            driver.find_element_by_xpath('//div[@dl-test="translator-source-lang"]').click()
            inLangButton = driver.find_element_by_xpath('//div[@dl-test="translator-source-lang"]').find_element_by_xpath('//button[@dl-test="translator-lang-option-' + language + '"]')

            inLangButton.click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "tag_wordtype"))
                )
            except TimeoutException:  # Word unavailable
                print('Failed to find word:', word)
                failedCSV = open('failed.csv', 'a+')
                failedWriter = csv.writer(failedCSV)
                failedWriter.writerow([word])

            pageHTML = driver.page_source
            soup = BS(pageHTML, 'html.parser')

            featured = soup.findAll("div", {"class": "lemma featured"})

            # word = featured[0]

            for featuredWord in featured:

                foreignWord = featuredWord.find("span", {"class": "tag_lemma"}).find("a")
                try:
                    foreignWord.span.decompose()
                except AttributeError:  # There is no text in a "span" tag to remove
                    pass
                foreignWord = foreignWord.text

                englishWord = featuredWord.find("a", {"class": "dictLink featured"})
                try:
                    englishWord.span.decompose()
                except AttributeError:  # There is no text in a "span" tag to remove
                    pass
                englishWord = englishWord.text

                type = featuredWord.find("span", {"class": "tag_wordtype"}).text

                if 'noun' in type:
                    gender = type.split(',')[1]

                    if 'masculine' in gender:
                        # englishWords.append('the ' + englishWord)
                        # foreignWords.append('der ' + foreignWord)
                        writer.writerow(['the ' + englishWord, 'der ' + foreignWord])
                        writer.writerow(['der ' + foreignWord, 'the ' + englishWord])

                    elif 'feminine' in gender:
                        # englishWords.append('the ' + englishWord)
                        # foreignWords.append('die ' + foreignWord)
                        writer.writerow(['the ' + englishWord, 'die ' + foreignWord])
                        writer.writerow(['die ' + foreignWord, 'the ' + englishWord])


                    elif 'neuter' in gender:
                        # englishWords.append('the ' + englishWord)
                        # foreignWords.append('das ' + foreignWord)
                        writer.writerow(['the ' + englishWord, 'das ' + foreignWord])
                        writer.writerow(['das ' + foreignWord, 'the ' + englishWord])


                    else:  # E.g. plural
                        pass

                else:
                    # englishWords.append(englishWord)
                    # foreignWords.append(foreignWord)
                    writer.writerow([englishWord, foreignWord])
                    writer.writerow([foreignWord, englishWord])


            # print(englishWords, foreignWords)

            driver.close()

        except Exception as e:
            print("Exception:", e)
            print(word)
            continue

# assert(len(englishWords) == len(foreignWords))

# with open("words.csv", "w") as csvfile:
#     writer = csv.writer(csvfile, delimiter=";")
#     for i in range(len(englishWords)):
#         writer.writerow([englishWords[i], foreignWords[i]])
#         writer.writerow([foreignWords[i], englishWords[i]])
