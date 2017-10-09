from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from data import USERNAME, PASSWORD


def automate():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("http://www.pythonanywhere.com/")
    driver.find_element_by_id("id_login_link").click()
    username = driver.find_element_by_id("id_auth-username")
    username.send_keys(USERNAME)
    password = driver.find_element_by_id("id_auth-password")
    password.send_keys(PASSWORD)
    driver.find_element_by_id("id_next").click()
    driver.find_element_by_css_selector("#id_files_link").click()
    driver.find_element_by_css_selector("#id_row_directory_5 > td.first_column > a").click()
    driver.find_element_by_css_selector("#id_row_directory_1 > td.first_column > a").click()
    upload = driver.find_element_by_id("id_upload_filename").send_keys("C:\\Users\\Puocci\\Documents\\LuckycloverBot\\obj\\listaSf.pkl")
    upload = driver.find_element_by_id("id_upload_filename").send_keys("C:\\Users\\Puocci\\Documents\\LuckycloverBot\\obj\\listaFi.pkl")
    web = driver.find_element_by_id("id_web_app_link").click()
    reload_app = driver.find_element_by_css_selector("#id_eyedema_pythonanywhere_com > form > div:nth-child(1) > div > button").click()
    driver.quit()
