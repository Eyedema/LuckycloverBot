from selenium import webdriver
from data import USERNAME, PASSWORD


def automate():
    driver = webdriver.Chrome()
    driver.get("http://www.pythonanywhere.com/")
    login = driver.find_element_by_id("id_login_link")
    login.click()
    username = driver.find_element_by_id("id_auth-username")
    username.click()
    username.send_keys(USERNAME)
    password = driver.find_element_by_id("id_auth-password")
    password.click()
    password.send_keys(PASSWORD)
    nextBtn = driver.find_element_by_id("id_next")
    nextBtn.click()
    files = driver.find_element_by_id("id_files_link")
    files.click()
    directory_bot = driver.find_element_by_id("id_row_directory_4")
    directory_bot.click()
    directory_obj = driver.find_element_by_xpath("//*[@id='id_row_directory_1']/td[1]/a")
    directory_obj.click()
    upload = driver.find_element_by_id("id_upload_filename")
    upload.send_keys("D:\\Progetti\\clover2.0\\obj\\listaSf.pkl")
    upload = driver.find_element_by_id("id_upload_filename")
    upload.send_keys("D:\\Progetti\\clover2.0\\obj\\listaFi.pkl")
    web = driver.find_element_by_id("id_web_app_link")
    web.click()
    reload_app = driver.find_element_by_xpath("//*[@id='id_eyedema_pythonanywhere_com']/form/div[1]/div/button")
    reload_app.click()
    import time
    time.sleep(30)
    driver.close()

