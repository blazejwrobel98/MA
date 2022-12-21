import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# open "mute.csv" file and read the data into a list
with open("mute.csv", "r") as f:
    mute_list = f.read().splitlines()

chrome_options = Options()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# open "https://solarwinds.ad.global/Orion/Login.aspx" in chrome incognito mode
mute_range = {
    "from": {
        "date": "10.11.2022",
        "time": "8:30"
    },
    "to": {
        "date": "10.11.2022",
        "time": "15:00"
    }
}
failed = []
driver.get("https://solarwinds.ad.global/Orion/Login.aspx")
driver.get("https://solarwinds.ad.global/Orion/Login.aspx")
username = driver.find_element(By.ID, "ctl00_BodyContent_Username")
username.send_keys("ad\sa-blawro")
password = driver.find_element(By.ID, "ctl00_BodyContent_Password")
password.send_keys("JECyf4yhdpWgsX7c3COF")
password.send_keys(Keys.RETURN)
i = 0
time.sleep(2)
print("Opening node manager...")
driver.get("https://solarwinds.ad.global/Orion/Nodes/Default.aspx")
for element in mute_list:
    print(f"Muting alerts for {element} ... {i + 1}/{len(mute_list)}")
    i += 1
    try:
        time.sleep(2)
        search_input = driver.find_element(By.ID, "search")
        time.sleep(1)
        search_input.clear()
        search_input.send_keys(element)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)
        select_all = driver.find_element(By.ID, "selectAll")
        select_all.click()
        if len(driver.find_elements(By.XPATH, "//tr[@class='row-alt'][td]")) > 1:
            print("More than one node found, skipping...")
            failed.append(element)
            continue
        schedule = driver.find_element(By.XPATH, "//li[@class='submenu']")
        schedule.click()
        schedule = driver.find_element(By.XPATH, "//a[@id='scheduleMaintenanceLink']")
        schedule.click()
        time.sleep(1)
        date = driver.find_element(By.NAME,
                                   "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodFrom$txtDatePicker")
        date.clear()
        date.send_keys(mute_range["from"]["date"])
        time_start = driver.find_element(By.NAME,
                                         "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodFrom$txtTimePicker")
        time_start.clear()
        time_start.send_keys(mute_range["from"]["time"])
        date = driver.find_element(By.NAME,
                                   "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodUntil$txtDatePicker")
        date.clear()
        date.send_keys(mute_range["to"]["date"])
        time_end = driver.find_element(By.NAME,
                                       "ctl00$ctl00$ctl00$BodyContent$ContentPlaceHolder1$adminContentPlaceholder$MaintenanceSchedulerDialog$periodUntil$txtTimePicker")
        time_end.clear()
        time_end.send_keys(mute_range["to"]["time"])
        time.sleep(1)
        submit = driver.find_element(By.ID,
                                     "ctl00_ctl00_ctl00_BodyContent_ContentPlaceHolder1_adminContentPlaceholder_MaintenanceSchedulerDialog_buttonSchedule")
        time.sleep(1)
        submit.click()
        time.sleep(1)
    except Exception as e:
        failed.append(element)
        pass
print(f"Failed to mute alerts for {failed}")
with open("failed.csv", "w") as f:
    for line in failed:
        f.write(line + "\n")

input("Press Enter to exit ...")
