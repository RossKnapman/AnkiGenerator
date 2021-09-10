# -*- coding: utf-8 -*-
import codecs
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv


language = 'fr'

words = []

options = webdriver.FirefoxOptions()
options.headless = True

f = codecs.open("My Clippings.txt", 'r', 'utf-8')

lines = f.read().splitlines()

for i in range(len(lines)):
    if lines[i] == "==========":
        word = lines[i-1]
        words.append(word)

# Now remove any duplicates
words = list(set(words))

for word in words:

    if word != '':

        print(word)

        try:

            csvfile = open('words.csv', 'a+')
            writer = csv.writer(csvfile, delimiter=";")

            driver = webdriver.Firefox(options=options)
            driver.set_window_size(1920, 1080)  # Prevents cookies banner from obscuring buttons
            driver.get('https://www.deepl.com/translator')

            driver.find_element_by_tag_name('textarea').send_keys(word)

            try:
                WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "lmt__language_container"))
                )
            except:
                print('Page failed to load:')

            driver.find_element_by_xpath('//div[@dl-test="translator-source-lang"]').click()
            inLangButton = driver.find_element_by_xpath('//div[@dl-test="translator-source-lang"]').find_element_by_xpath('//button[@dl-test="translator-lang-option-' + language + '"]')
            inLangButton.click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "tag_wordtype"))
                )
            except TimeoutException:  # Word unavailable
                print('Failed to find word:', word)

            pageHTML = driver.page_source
            soup = BS(pageHTML, 'html.parser')

            featured = soup.findAll("div", {"class": "lemma featured"})

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

                        if foreignWord[0] in 'bcdfghjklmnpqrstvwxyz':
                            writer.writerow(['the ' + englishWord, 'le ' + foreignWord])
                            writer.writerow(['le ' + foreignWord, 'the ' + englishWord])

                        # If begins with vowel, start with l' instead of le/la
                        else:
                            writer.writerow(['the ' + englishWord, 'l\'' + foreignWord + ' (m)'])
                            writer.writerow(['l\'' + foreignWord + ' (m)', 'the ' + englishWord])

                    elif 'feminine' in gender:

                        if foreignWord[0] in 'bcdfghjklmnpqrstvwxyz':
                            writer.writerow(['the ' + englishWord, 'la ' + foreignWord])
                            writer.writerow(['la ' + foreignWord, 'the ' + englishWord])

                        else:
                            writer.writerow(['the ' + englishWord, 'l\'' + foreignWord + ' (f)'])
                            writer.writerow(['l\'' + foreignWord + ' (f)', 'the ' + englishWord])

                    else:  # E.g. plural
                        pass

                else:
                    writer.writerow([englishWord, foreignWord])
                    writer.writerow([foreignWord, englishWord])


            driver.close()

        except Exception as e:
            print("Exception:", e)
            continue
