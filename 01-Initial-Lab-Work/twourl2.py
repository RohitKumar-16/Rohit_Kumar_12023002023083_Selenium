from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver=webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
parent_window=driver.current_window_handle
print(parent_window)
driver.maximize_window()

driver.switch_to.new_window("tab")

driver.get("https://testautomationpractice.blogspot.com/#")
new_tab=driver.find_element(By.XPATH,'//*[@id="post-body-1307673142697428135"]/div[3]/div[1]').click()
windows=driver.window_handles
print(windows)

time.sleep(5)

driver.quit()