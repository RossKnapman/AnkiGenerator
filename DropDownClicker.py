from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.deepl.com/translator')
driver.find_element_by_tag_name('textarea').send_keys('merde')

driver.find_element_by_xpath('//div[@dl-test="translator-source-lang"]').click()
testIn = driver.find_element_by_xpath('//button[@dl-value="FR"]')
testIn.click()

targetDropdown = driver.find_element_by_xpath('//div[@dl-test="translator-target-lang"]')
targetDropdown.click()
print(targetDropdown.get_attribute('outerHTML'))
testOut = targetDropdown.find_element_by_xpath('//button[@dl-value="EN"]')
highlight(testOut)
# testOut.click()

# driver.find_element_by_xpath('//button[@dl-value="DE"]').click()
