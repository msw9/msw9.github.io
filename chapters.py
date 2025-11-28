from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def extract chapters (button):
    yield chapter #generator

driver = webdriver.Firefox()
driver.get("https://www.bible.com/bible/3438/GEN.1.MYE?parallel=93")
elem = driver.find_element(By.NAME, "q")
driver.close()
