from selenium import webdriver
from selenium.webdriver.common.by import By

try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.primark.com/en-gb")
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    men = driver.find_element(By.XPATH, "//*[@data-testautomation-id = 'home-page-categories']//*[@data-testautomation-id='typography'][text()='Men']/ancestor::a")
    men.click()
    driver.find_element(By.XPATH,
                        "//*[@data-testautomation-id = 'categories-carousel']//*[@data-testautomation-id='hero-banner-item-title']").click()

finally:
    driver.quit()
