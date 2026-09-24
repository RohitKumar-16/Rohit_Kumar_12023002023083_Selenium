from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
driver.maximize_window()

# 1. By.ID
name = driver.find_element(By.ID, "name")
name.send_keys("Rohit")

# 2. By.NAME
radio = driver.find_element(By.NAME, "radioButton")
radio.click()

# 3. By.TAG_NAME
heading = driver.find_element(By.TAG_NAME, "h1")
print("Heading:", heading.text)

# 4. By.LINK_TEXT
latest_news = driver.find_element(By.LINK_TEXT, "Latest News")
print(latest_news.text)

# 5. By.CLASS_NAME
login_button = driver.find_element(By.CLASS_NAME, "btn-primary")
print("Button:", login_button.text)
time.sleep(10)

driver.quit()