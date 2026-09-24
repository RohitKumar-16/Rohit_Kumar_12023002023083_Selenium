from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver=webdriver.Chrome()

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

driver.maximize_window()

button=driver.find_element(By.CSS_SELECTOR,"button")

button.click()

time.sleep(10)

time.sleep(10)

driver.quit()