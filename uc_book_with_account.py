import time
import pause
from datetime import datetime

from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

TEST = False
KURS_ID = "11531829"
LINK = "https://buchung.hsz.rwth-aachen.de/angebote/Sommersemester_2023/_Volleyball_Spielbetrieb.html"


def read_account():
    f = open("account.txt", "r")
    email = f.readline()[:-1]
    password = f.readline()
    f.close()
    return email, password


def click_have_password(driver):
    driver.find_element(by=By.ID, value="bs_pw_anmlink").click()


def write_email_and_password(driver):
    tag = driver.find_element(by=By.ID, value="bs_pw_anm")
    tag.find_element(by=By.XPATH, value="//input[@type = 'text']").send_keys("l.kamke@web.de")
    tag.find_element(by=By.XPATH, value="//input[@type = 'password']").send_keys("Karaganda69!")
    tag.find_element(by=By.XPATH, value="//input[@value = 'weiter zur Buchung']").click()


def write_iban(driver):
    iban_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'IBAN:*')]")
    parent = iban_tag.find_element(by=By.XPATH, value="..")
    parent = parent.find_element(by=By.XPATH, value="//input[@name = 'iban']")
    parent.clear()
    parent.send_keys("DE23560614720007246070")


def accept_bedingungen(driver):
    tbn_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Anmelde- und Teilnahmebedingungen')]")
    parent = tbn_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'tnbed']").click()


def click_buchung(driver):
    tbn_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Anmelde- und Teilnahmebedingungen')]")
    parent = tbn_tag.find_element(by=By.XPATH, value="../../..")
    clicked_weiter_zur_buchung = False
    while not clicked_weiter_zur_buchung:
        try:
            parent.find_element(by=By.XPATH, value="//input[@id = 'bs_submit']").click()
            print("clicked weiter zur Buchung")
            clicked_weiter_zur_buchung = True
        except:
            print("wait on Weiter zur Buchung Button")


def click_kostenpflichtig_buchen(driver):
    kostenpflichtig_buchen_tag = driver.find_element(by=By.XPATH, value="//input[@value = 'kostenpflichtig buchen']")
    if not TEST:
        kostenpflichtig_buchen_tag.click()
        print("Kostenpflichtig gebucht!")
    else:
        print(kostenpflichtig_buchen_tag.get_attribute("title"))


def click_termin_auswaehlen(driver):
    driver.find_element(by=By.XPATH, value="//input[@type = 'submit']").click()
    print("Termin ausgewählt")


def isBookingForm(driver):
    try:
        driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Bitte wählen Sie einen Termin aus:')]")
        return False
    except:
        return True


if __name__ == '__main__':
    # pause.until(datetime(2023, 3, 27, 0, 5))
    print("lets go")
    # Passwort und Email auslesen
    EMAIL, PASSWORD = read_account()

    # Chrome webdriver starten
    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    driver = uc.Chrome()
    driver.implicitly_wait(0.008)

    found_button = False
    counter = 0
    while not found_button:
        try:
            # HSZ Volleyball Spielbetrieb Wintersemester Buchen Webseite laden
            driver.get(LINK)

            # Buchen-Button finden
            a_element = driver.find_element(by=By.ID, value="K" + KURS_ID)

            # Get the parent of the <a id="xxxx"><a/> element, which is from type <td></td>
            td_element = a_element.find_element(by=By.XPATH, value="..")

            # get the button element
            input_element = td_element.find_element(by=By.TAG_NAME, value="input")

            # click on the button -> new page with form
            input_element.click()

            print("Buchen button appeared and clicked")
            found_button = True
        except:
            counter += 1
            print("------ " + str(counter) + " ------")

    # switch driver to new page
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    # ----------------- new page ------------------------------

    if not isBookingForm(driver):
        # Termin auswählen
        try:
            click_termin_auswaehlen(driver)
        except:
            print("Error in Termin auswählen")
        # ----------------- new page ------------------------------

    # here the driver has to be on the "form page"
    counter = 0
    finished = False
    while not finished:
        try:
            # click ich habe ein Passwort
            click_have_password(driver)

            # type email
            tag = driver.find_element(by=By.ID, value="bs_pw_anm")
            tag.find_element(by=By.XPATH, value="//input[@type = 'text']").send_keys(EMAIL)
            # type password
            tag.find_element(by=By.XPATH, value="//input[@type = 'password']").send_keys(PASSWORD)
            # click on weiter zur Buchung
            tag.find_element(by=By.XPATH, value="//input[@value = 'weiter zur Buchung']").click()

            write_iban(driver)

            accept_bedingungen(driver)

            click_buchung(driver)

            # ----------------- new page ------------------------------

            click_kostenpflichtig_buchen(driver)
            finished = True
        except:
            counter += 1
            print("---- Waiting for form page " + str(counter) + " ----")

    # Sleep 10 minutes
    time.sleep(600)
