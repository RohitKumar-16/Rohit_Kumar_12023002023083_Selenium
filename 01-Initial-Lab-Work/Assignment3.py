from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

# CSS Selector: ID starts with a specific value
elements = driver.find_elements(By.CSS_SELECTOR, "input[id^='name']")

print("Number of matching elements:", len(elements))

for element in elements:
    print("Element ID:", element.get_attribute("id"))
    print("Element Type:", element.get_attribute("type"))

driver.quit()