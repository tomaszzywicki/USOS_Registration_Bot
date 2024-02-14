from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime

class Driver_Logic:
    def __init__(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def login_to_usos(self, username, password):
        self.driver.get("https://usosweb.usos.pw.edu.pl/kontroler.php?_action=logowaniecas/index")
        username_element = self.driver.find_element(By.ID, "username")
        password_element = self.driver.find_element(By.ID, "password")
        username_element.send_keys(username)
        password_element.send_keys(password)
        login_element = self.driver.find_element(By.CLASS_NAME, "form-button")
        login_element.send_keys(Keys.ENTER)


    def select_wf(self, link, group_nr):
        self.driver.get(link)
        class_button_element = self.driver.find_element(By.CSS_SELECTOR, f'input.group-input[name="zajecia[474186][]"][value="{group_nr}"]') #TODO set to custom group
        class_button_element.click()
        submit_button_element = self.driver.find_element(By.CSS_SELECTOR, 'input.submit.semitransparent[value="Rejestruj"][onclick="return isAnyGroupChecked();"]') #TODO check if that is ok

        clicks = 0
        while True:
            current_time = datetime.datetime.now().time()
            if current_time.hour == 8 and current_time.minute == 0:  #TODO set to custom time
                while clicks <= 5:
                    submit_button_element.click()
                    clicks += 1
                    time.sleep(1)
                break
            time.sleep(0.01)
    

    def loop_driver(self):
        while True:
            pass

