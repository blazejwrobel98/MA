import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


def create_internal_static_dns_a_record(options, user):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get("https://infoblox.ad.global/ui/")
    while True:
        try:
            driver.find_element(By.NAME, "username")
            driver.find_element(By.NAME, "password")
            time.sleep(1)
            break
        except Exception as e:
            pass
    driver.find_element(By.NAME, "username").send_keys(user.username)
    driver.find_element(By.NAME, "password").send_keys(user.password)
    driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
    time.sleep(10)
    for elem in driver.find_elements(By.XPATH, "//a[@class='childmenu']"):
        if elem.text == "Data Management":
            elem.click()
            break
    time.sleep(4)
    for elem in driver.find_elements(By.XPATH, "//a[@class='childmenu']"):
        if elem.text == "DNS":
            elem.click()
            break
    time.sleep(8)
    driver.find_element(By.LINK_TEXT, "Show Filter").click()
    time.sleep(2)

    sel = driver.find_elements(By.XPATH, '//select')
    for elem in sel:
        if "Choose Filter" in elem.text:
            select = Select(elem)
            for index in range(len(select.options)):
                select = Select(elem)
                select.select_by_value("13")
                break
    time.sleep(1)
    sel = driver.find_elements(By.XPATH, '//select')
    for elem in sel:
        if "begins with" in elem.text:
            select = Select(elem)
            for index in range(len(select.options)):
                select = Select(elem)
                select.select_by_value("2")
                break
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@name="filters:1:userFilter:valueTextWidget"]').send_keys(options['Domain'])
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@name="filters:1:userFilter:valueTextWidget"]').send_keys(Keys.ENTER)
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, '//span[@class="ib-grid-link"]').click()
        time.sleep(5)
    except NoSuchElementException:
        driver.quit()
        return [False, "Domain not found"]
    driver.find_element(By.XPATH, '//button[@class=" x-btn-text ib_h_icon_add"]').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//input[@name="view:arecord:fqdn_fake"]').send_keys(options['Host'])
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@name="view:arecord:address"]').send_keys(options['IP Address'])
    time.sleep(1)
    driver.find_element(By.XPATH, '//textarea[@name="view:arecord:comment"]').send_keys(options['Task'])

    input("Press Enter to continue...")
