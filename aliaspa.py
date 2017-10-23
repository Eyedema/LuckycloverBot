from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, time, timedelta
from dateutil.relativedelta import relativedelta


prima_data = date.today()
fine_data = date.today() + relativedelta(months=+1)
delta = fine_data - prima_data
for i in range(delta.days + 1):
	print (prima_data + timedelta(days=i)).strftime('%d/%m/%Y')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get("https://www.aliaspa.it/puliziastrade/")
	driver.find_element_by_css_selector("body > div > div.row > div > div > div.panel-heading > ul > li:nth-child(2) > a").click()
	Select(driver.find_element_by_css_selector('#comunedata')).select_by_value("FIRENZE")
	driver.find_element_by_css_selector("#datatratti").send_keys((prima_data + timedelta(days=i)).strftime("%d/%m/%Y"))
	driver.find_element_by_css_selector("#calcoladataall").click()
	element = WebDriverWait(driver, 10).until(
	    EC.presence_of_element_located((By.CSS_SELECTOR, "#calcoladataall-content > div.modal-body"))
	)
	html = driver.page_source
	soup = BeautifulSoup(html, "lxml")
	table = driver.find_element_by_css_selector("#calcoladataall-content > div.modal-body")
	rows = table.find_elements_by_tag_name("tr")
	for row in rows:
		print row.text
	driver.quit()
	