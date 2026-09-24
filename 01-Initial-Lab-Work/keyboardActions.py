from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
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
driver.get("https://text-compare.com/")
driver.maximize_window()

left_text=driver.find_element(By.CSS_SELECTOR,"textarea:first-of-type")
left_text.send_keys("Welcome to Selenium")

act = ActionChains(driver)
 
act.click(left_text)
act.key_down(Keys.CONTROL)
act.send_keys("a")
act.key_up(Keys.CONTROL)
 
act.key_down(Keys.CONTROL)
act.send_keys("c")
act.key_up(Keys.CONTROL)
 
right_text = driver.find_element(By.CSS_SELECTOR, "textarea:nth-of-type(2)")
act.click(right_text)
 
act.key_down(Keys.CONTROL)
act.send_keys("v")
act.key_up(Keys.CONTROL)

act.perform()

driver.quit()