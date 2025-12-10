from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
def extract_chapters (button):
    yield chapter #generator

driver = webdriver.Firefox()
driver.get("https://www.bible.com/bible/3438/GEN.1.MYE?parallel=93")
button = driver.find_element(By.ID,"headlessui-popover-button-:r0:").click()
options = driver.find_elements(By.XPATH,"//div/div[2]/main/div[1]/div/div[1]/div[1]/div/div[1]/div/div/div[2]/ul/li")
time.sleep(3)
books = [x.text for x in options]
buttons = [x.get_attribute('button') for x in options]
print(books)
print(buttons)

driver.close()

books_chapters = {book: [] for book in books}
print(books)
