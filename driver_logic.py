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


    def select_course(self, link, group_nr, hour, minute):
        self.driver.get(link)
        class_button_element = self.driver.find_element(By.XPATH, f'//input[@class="group-input" and @value="{group_nr}"]')
        class_button_element.click()
        submit_button_element = self.driver.find_element(By.CSS_SELECTOR, 'input.submit.semitransparent[value="Rejestruj"][onclick="return isAnyGroupChecked();"]')

        while True:
            current_time = datetime.datetime.now().time()
            if current_time.hour == hour and current_time.minute == minute:
                clicks = 0
                while clicks <= 1:
                    submit_button_element.click()
                    clicks += 1
                    time.sleep(1)
                time.sleep(5)

                clicks = 0
                while clicks <= 1: # if usos and computers clock are not synchronized it makes sure that button will be clicked
                    submit_button_element.click()
                    clicks += 1
                    time.sleep(1)

                break
            time.sleep(0.01)

