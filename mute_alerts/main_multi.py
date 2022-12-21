import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process

# open "mute.csv" file and read the data into a list
with open("mute.csv", "r") as f:
    mute_list = f.read().splitlines()
open('failed.csv', 'w').close()


def mute_func(element):
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # open "https://solarwinds.ad.global/Orion/Login.aspx" in chrome incognito mode

    failed = []
    driver.get("https://solarwinds.ad.global/Orion/Login.aspx")
    driver.get("https://solarwinds.ad.global/Orion/Login.aspx")
    username = driver.find_element(By.ID, "ctl00_BodyContent_Username")
    username.send_keys("ad\sa-blawro")
    password = driver.find_element(By.ID, "ctl00_BodyContent_Password")
    password.send_keys("JECyf4yhdpWgsX7c3COF")
    password.send_keys(Keys.RETURN)
    print(f"Muting alerts for {element} ...")
    try:
        driver.get("https://solarwinds.ad.global/Orion/Nodes/Default.aspx")
        search_input = driver.find_element(By.ID, "search")
        search_input.send_keys(element)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)
        select_all = driver.find_element(By.ID, "selectAll")
        select_all.click()
        schedule = driver.find_element(By.XPATH, "//li[@class='submenu']")
        schedule.click()
        schedule = driver.find_element(By.XPATH, "//a[@id='scheduleMaintenanceLink']")
        schedule.click()
        time.sleep(1)
        date = driver.find_element(By.NAME,
                                   "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodFrom$txtDatePicker")
        date.clear()
        date.send_keys("18.09.2022")
        time_start = driver.find_element(By.NAME,
                                         "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodFrom$txtTimePicker")
        time_start.clear()
        time_start.send_keys("07:30")
        date = driver.find_element(By.NAME,
                                   "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodUntil$txtDatePicker")
        date.clear()
        date.send_keys("18.09.2022")
        time_end = driver.find_element(By.NAME,
                                       "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodUntil$txtTimePicker")
        time_end.clear()
        time_end.send_keys("12:30")
        time.sleep(1)
        submit = driver.find_element(By.ID,
                                     "ctl00_ctl00_ctl00_BodyContent_ContentPlaceHolder1_adminContentPlaceholder_MaintenanceSchedulerDialog_buttonSchedule")
        submit.click()
        time.sleep(1)
    except Exception as e:
        failed.append(element)
        pass
    print(f"Failed to mute alerts for {failed}")
    with open("failed.csv", "a") as f:
        for line in failed:
            f.write(line + "\n")


if __name__ == '__main__':
    procs = []
    for name in mute_list:
        proc = Process(target=mute_func, args=(name,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
