from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

driver=webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

try:
    driver.get("https://testautomationpractice.blogspot.com/")
    parent_menu=driver.find_element(By.XPATH,"//button[contains(text(),'Point Me')]")
    sub_option=driver.find_element(By.XPATH,"//a[contains(text(),'Mobiles')]")
    act=ActionChains(driver)
    act.move_to_element(parent_menu).move_to_element(sub_option).click().perform()
    print("Howered over menu and selected Mobile successfully.")
    time.sleep(5)

finally:
    driver.quit()