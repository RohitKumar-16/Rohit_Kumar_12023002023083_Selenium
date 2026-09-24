from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://testautomationpractice.blogspot.com/#")
driver.maximize_window()

# Find all links on the webpage
links = driver.find_elements(By.TAG_NAME, "a")

print("Total number of links:", len(links))

# Print the text of each link
for link in links:
    print(link.text)
time.sleep(10)

driver.quit()