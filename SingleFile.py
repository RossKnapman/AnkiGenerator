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

englishWords = []
foreignWords = []


inputLanguage = 'de'
targetLanguage = 'en'

words = []

f = codecs.open("My Clippings.txt", 'r', 'utf-8')

lines = f.read().splitlines()

for i in range(len(lines)):
    if lines[i] == "==========":
#        word = re.sub(r'[^a-zA-Z]', "", lines[i-1])
        word = lines[i-1]
        words.append(word)

# Now remove any duplicates
words = list(set(words))

# word = 'schieben'

for word in words:

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.deepl.com/translator#' + inputLanguage + '/' + targetLanguage + '/' + word)


    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "tag_wordtype"))
        )
    except TimeoutException:  # Word unavailable
        print('Failed to find word:', word)

    pageHTML = driver.page_source
    soup = BS(pageHTML, 'html.parser')

    featured = soup.findAll("div", {"class": "lemma featured"})
    print(len(featured))

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
            print(gender)

            if 'masculine' in gender:
                englishWords.append('the ' + englishWord)
                foreignWords.append('der ' + foreignWord)

            elif 'feminine' in gender:
                englishWords.append('the ' + englishWord)
                foreignWords.append('die ' + foreignWord)

            elif 'neuter' in gender:
                englishWords.append('the ' + englishWord)
                foreignWords.append('das ' + foreignWord)

            else:  # E.g. plural
                pass

        else:
            englishWords.append(englishWord)
            foreignWords.append(foreignWord)

    print(englishWords, foreignWords)

    driver.close()

assert(len(englishWords) == len(foreignWords))
