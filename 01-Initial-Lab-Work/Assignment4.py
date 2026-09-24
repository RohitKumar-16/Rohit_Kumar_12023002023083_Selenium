from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

radio_button = driver.find_element(By.CSS_SELECTOR,"#radio-btn-example > fieldset > label:nth-child(3) > input")
print("Radio button found:", radio_button.get_attribute("value"))
radio_button.click()

time.sleep(5)

driver.quit()