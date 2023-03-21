from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

'''
    Link für Volleyball Buchung:
    https://buchung.hsz.rwth-aachen.de/angebote/Wintersemester_2022_23/_Volleyball_Spielbetrieb.html
'''

KURS_ID = "11432933"
LINK = "https://buchung.hsz.rwth-aachen.de/angebote/Wintersemester_2022_23/_Tischtennis_Spielbetrieb.html"


def click_geschlecht_radio_box(driver):
    geschlecht_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Geschlecht:*')]")
    parent = geschlecht_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@value = 'M']").click()


def write_vorname(driver):
    vorname_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Vorname:*')]")
    parent = vorname_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'vorname']").send_keys("Leon")


def write_nachname(driver):
    nachname_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Familienname:*')]")
    parent = nachname_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'name']").send_keys("Kamke")


def write_strasse(driver):
    strasse_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Strasse Nr:*')]")
    parent = strasse_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'strasse']").send_keys("Grosskölnstraße 29")


def write_stadt(driver):
    stadt_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'PLZ Ort:*')]")
    parent = stadt_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'ort']").send_keys("52062 Aachen")


def click_status(driver):
    status_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Status:*')]")
    parent = status_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//option[@value = 'S-RWTH']").click()


def write_matrikelnummer(driver):
    matr_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Matrikel-Nr.:*')]")
    parent = matr_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'matnr']").send_keys("451973")


def write_email(driver):
    email_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'E-Mail:*')]")
    parent = email_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'email']").send_keys("l.kamke@web.de")


def write_phonenr(driver):
    phonenr_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Telefon:*')]")
    parent = phonenr_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'telefon']").send_keys("015157753920")


def write_iban(driver):
    iban_tag = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'IBAN:*')]")
    parent = iban_tag.find_element(by=By.XPATH, value="..")
    parent.find_element(by=By.XPATH, value="//input[@name = 'iban']").send_keys("DE23560614720007246070")


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
    # kostenpflichtig_buchen_tag.click()
    print("Kostenpflichtig gebucht!")
    # print(kostenpflichtig_buchen_tag.get_attribute("title"))


def click_termin_auswaehlen(driver):
    driver.find_element(by=By.XPATH, value="//input[@type = 'submit']").click()
    print("Termin ausgewählt")


def isBookingForm(driver):
    try:
        x = driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Bitte wählen Sie einen Termin aus:')]")
        return False
    except:
        return True


if __name__ == '__main__':
    # Chrome webdriver starten
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(0.2)

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

            print("Button clicked!")
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
        click_termin_auswaehlen(driver)
        # ----------------- new page ------------------------------

    # click geschlecht
    click_geschlecht_radio_box(driver)

    # write vorname
    write_vorname(driver)

    # write nachname
    write_nachname(driver)

    # write Adresse
    write_strasse(driver)

    # write Stadt
    write_stadt(driver)

    # click Status
    click_status(driver)

    # write Matrikelnummer
    write_matrikelnummer(driver)

    # write Email
    write_email(driver)

    # write phonenr
    write_phonenr(driver)

    # write iban
    write_iban(driver)

    # accept teilnahmebedingungen
    accept_bedingungen(driver)

    # click "weiter zur buchung"
    click_buchung(driver)

    # ----------------- new page ------------------------------

    click_kostenpflichtig_buchen(driver)
