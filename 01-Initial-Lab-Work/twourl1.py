from selenium import webdriver
import time

driver=webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

driver.switch_to.new_window("tab")

driver.get("https://testautomationpractice.blogspot.com/#")

time.sleep(5)

driver.quit()