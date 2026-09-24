from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time

browsername="chrome"

if browsername.lower()=="chrome":
    driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
elif browsername.lower()=="firefox":
    driver=webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
else:
    raise Exception("Invalid browser name. Please choose 'chrome' or 'firefox'.")
driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()
#locating the element on webpage through XPATH and selecting the value from the dropdown
'''dropdown=Select(driver.find_element(By.XPATH,"//input[@id='autocomplete']"))
dropdown.select_by_value('Germany')
time.sleep(2)
'''

#locaating the element on webpage through CSS selector and selecting the value from the dropdown
driver.find_element(By.ID,"autocomplete").send_keys("Germany")
options=driver.find_elements(By.CSS_SELECTOR,".ui-menu-item")
for option in options:
    if option.text=="Germany":
        option.click()
        break
time.sleep(2)