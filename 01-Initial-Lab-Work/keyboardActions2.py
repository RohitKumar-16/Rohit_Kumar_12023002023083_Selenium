from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.maximize_window()

driver.get("https://text-compare.com/")

# Task 1
input1 = driver.find_element(By.XPATH, "//*[@id='inputText1']")
input1.send_keys("Welcome to Selenium.")

time.sleep(2)

# Task 2 - Copy left panel to right panel
input2 = driver.find_element(By.XPATH, "//*[@id='inputText2']")

act = ActionChains(driver)

# Select all
act.click(input1)
act.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL)

# Copy
act.key_down(Keys.CONTROL).send_keys("c").key_up(Keys.CONTROL)

# Click right panel
act.click(input2)

# Paste
act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL)

act.perform()

time.sleep(3)

driver.quit()