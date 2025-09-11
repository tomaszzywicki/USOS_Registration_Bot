import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logging import getLogger

logger = getLogger(name="driver_logic_logger")

LOGIN_LINKS = {
    "Politechnika Warszawska": "https://usosweb.usos.pw.edu.pl/kontroler.php?_action=logowaniecas/index",
    "Uniwersytet Warszawski": "https://logowanie.uw.edu.pl/cas/login",
}


class DriverLogic:
    def __init__(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)

    def login_to_usos(self, username: str, password: str, university: str):
        try:
            self.driver.get(LOGIN_LINKS.get(university))
            username_element = self.driver.find_element(By.ID, "username")
            password_element = self.driver.find_element(By.ID, "password")
            username_element.send_keys(username)
            password_element.send_keys(password)
            login_element = self.driver.find_element(
                By.CLASS_NAME,
                (
                    "form-button"
                    if university == "Politechnika Warszawska"
                    else "btn-submit"
                ),
            )
            login_element.send_keys(Keys.ENTER)
            logger.info("Successfully logged")
        except Exception as e:
            logger.error(f"Error during logging: {e}")

    def select_course(
        self, university, group_nr, hour, minute, link=None, course_name=None
    ):
        if university == "Politechnika Warszawska":
            self.select_course_pw(link, group_nr=group_nr, hour=hour, minute=minute)
        elif university == "Uniwersystet Warszawski":
            self.select_course_uw(
                course_name=course_name, group_nr=group_nr, hour=hour, minute=minute
            )

    def select_course_pw(self, link, group_nr, hour, minute):
        self.driver.get(link)
        class_button_element = self.driver.find_element(
            By.XPATH, f'//input[@class="group-input" and @value="{group_nr}"]'
        )
        class_button_element.click()
        submit_button_element = self.driver.find_element(
            By.CSS_SELECTOR,
            'input.submit.semitransparent[value="Rejestruj"][onclick="return isAnyGroupChecked();"]',
        )

        while True:
            current_time = datetime.datetime.now().time()
            if current_time.hour == hour and current_time.minute == minute:
                clicks = 0
                while clicks <= 1:
                    submit_button_element.click()
                    clicks += 1
                    time.sleep(1)
                time.sleep(5)

                submit_button_element.click()  # if USOS and device time synchronization is fucked up
                break
            time.sleep(0.01)

    def select_course_uw(self, course_name, group_nr, hour, minute):
        course_name = course_name.lower().title()
        self.driver.get(
            "https://usosweb.uw.edu.pl/kontroler.php?_action=dla_stud/zetony/index#!/registration/4023-2025Z-WF"
        )

        try:
            print("[INFO] Oczekiwanie na załadowanie strony...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.course-row"))
            )

            time.sleep(3)

            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "Liczba wyświetlanych przedmiotów" not in page_text:
                print("[WARNING] Strona może nie być w pełni załadowana")
                time.sleep(5)

            course_rows = self.driver.find_elements(By.CSS_SELECTOR, "div.course-row")
            print(f"[DEBUG] Znaleziono {len(course_rows)} kursów")

            if len(course_rows) == 0:
                print(
                    "[ERROR] Nie znaleziono żadnych kursów - sprawdź czy jesteś zalogowany"
                )
                return False

            # with open("file.txt", "w", encoding="utf-8") as file:
            #     for row in course_rows:
            #         html = row.get_attribute("outerHTML")
            #         file.write(html)
            #         file.write("\n\n")

            for row in course_rows:
                try:
                    label_element = row.find_element(By.TAG_NAME, "label")
                    label_text = label_element.text.strip()
                    print(f"[DEBUG] Label znaleziony: '{label_text}'")

                    if course_name.lower() in label_text.lower():
                        pin_checkbox = row.find_element(
                            By.XPATH, ".//input[@type='checkbox']"
                        )

                        if not pin_checkbox.is_selected():
                            self.driver.execute_script(
                                "arguments[0].click();", pin_checkbox
                            )
                            print(
                                f"[INFO] Kliknięto 'przypnij' dla kursu: {course_name}"
                            )
                        else:
                            print(f"[INFO] Kurs {course_name} już przypięty.")

                        time.sleep(1)
                        break

                except Exception as e:
                    print(f"[DEBUG] Błąd przy przetwarzaniu wiersza kursu: {e}")
                    continue
            print(f"[WARN] Nie znaleziono kursu o nazwie: {course_name}")
        except:
            print("Błąd")
        print(f"[INFO] Oczekiwanie na załadowanie grup dla kursu: {course_name}")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//tbody//tr[td[@class='col-md-1']]")
                )
            )
            time.sleep(1)
            print("[INFO] Grupy załadowane.")
        except Exception as e:
            print(f"[ERROR] Nie udało się załadować grup: {e}")
            return False

        group_xpath = f"//tbody//tr[td[@class='col-md-1']/div[text()='{group_nr}']]"
        register_button_xpath = ".//div[@class='cart want-register']"

        print(f"[INFO] Oczekiwanie na godzinę rejestracji: {hour:02d}:{minute:02d}")

        while True:
            current_time = datetime.datetime.now().time()

            if current_time.hour == hour and current_time.minute == minute:
                print(
                    f"[INFO] Rozpoczynanie rejestracji o {current_time.strftime('%H:%M:%S')}"
                )

                clicks = 0
                max_clicks = 5

                while clicks < max_clicks:
                    try:
                        group_row = self.driver.find_element(By.XPATH, group_xpath)

                        register_button = group_row.find_element(
                            By.XPATH, register_button_xpath
                        )

                        self.driver.execute_script(
                            "arguments[0].click();", register_button
                        )
                        print(
                            f"[INFO] Klik #{clicks + 1} - Kliknięto rejestrację w grupie {group_nr}"
                        )

                        clicks += 1
                        time.sleep(0.1)

                    except Exception as e:
                        print(f"[ERROR] Błąd podczas kliknięcia #{clicks + 1}: {e}")
                        clicks += 1
                        time.sleep(0.1)

                print(
                    f"[INFO] Zakończono próby rejestracji. Wykonano {clicks} kliknięć."
                )
                return True

            time.sleep(0.05)
