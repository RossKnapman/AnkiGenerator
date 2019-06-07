# -*- coding: utf-8 -*-
import codecs
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

test = 'Schloss'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.deepl.com/translator#' + inputLanguage + '/' + targetLanguage + '/' + test)

# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, "//div[@dl-test='translator-source']"))
# )
# inputLanguage = driver.find_element_by_xpath("//div[@dl-test='translator-source']")
# dropDownButton = driver.find_element_by_xpath("//button[@dl-test='translator-source-lang-btn']")
# dropDownButton.click()
# # WebDriverWait(driver, 30).until(
# #     EC.element_to_be_clickable((By.XPATH, "//button[@dl-value='FR']"))
# # )
# driver.implicitly_wait(2)
# inputButton = inputLanguage.find_element_by_xpath("//button[@dl-value='FR']")
# print(inputButton.text)
# inputButton.click()

# input = driver.find_element_by_tag_name('textarea')
# input.send_keys(test)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "tag_wordtype"))
)

pageHTML = driver.page_source
soup = BS(pageHTML, 'html.parser')

featured = driver.find_elements_by_xpath('//div[@class="lemma featured"]')

word = featured[1]

# for word in featured:

lemmaTag = word.find_element_by_class_name('tag_lemma')
foreignWord = lemmaTag.find_element_by_class_name('dictLink').text
print(foreignWord)

translationTag = word.find_element_by_class_name('tag_trans')

englishWord = translationTag.find_element_by_xpath('//a[@class="dictLink featured"]').text
print("Translation tag:", translationTag.get_attribute('innerHTML'))
print("English:", englishWord)

type = word.find_element_by_class_name('tag_wordtype').text

if 'noun' in type:
    englishWords.append('the ' + englishWord)
    gender = type.split(', ')[1]

    if gender == 'masculine':
        foreignWords.append('der ' + foreignWord)

    elif gender == 'feminine':
        foreignWords.append('die ' + foreignWord)

    elif gender == 'neuter':
        foreignWords.append('das ' + foreignWord)

else:
    englishWords.append(englishWord)
    foreignWords.append(foreignWord)

print(englishWords, foreignWords)
assert(len(englishWords) == len(foreignWords))

driver.close()
