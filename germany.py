from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

from time import sleep
from datetime import datetime
import os

load_dotenv("germany.env")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
url = os.environ.get('URL')
#url = "https://www.ch-edoc-reservation.admin.ch/#/session?token=fvBcvvne&locale=en-US"
deadline = "05.08.2024"

def schedule_appointment():
    driver.get(url)
    
    sleep(10)
    flag = 0
    
    
    try:   
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "bookingListBtn")))
        driver.find_element(By.ID, "bookingListBtn").click()
    except:
        pass
    
    xpath = "//*[@id='content']/app-booking-search/app-proposal-table/div/table/tbody/tr[1]/td[1]"
    # driver.find_element(By.CLASS_NAME, "ui-button ui-corner-all ui-widget ui-button-icon-only ui-dialog-titlebar-close").click()
    sleep(5)
    
    try:
        # Wait for the element to be present in the DOM
        # Wait for the "Vancouver" element to be present in the DOM
        appointment_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Find the following sibling <td> element with class "text-right"
        #appointment_elem_sample = appointment_elem.find_element(By.XPATH, "./following-sibling::td[@class='text-right']")
        # elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="paymentOptions"]/div[2]/table/tbody/tr[7]/td[2]')))
        appointment_date = appointment_elem.get_attribute('innerHTML').split()[-1]
        print(appointment_date)
        if datetime.strptime(appointment_date, "%d.%m.%Y").date() < datetime.strptime(deadline, "%d.%m.%Y").date():
            appointment_elem.click()
            sleep(10)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "bookBtn")))
            driver.find_element(By.ID, "bookBtn").click()
            print("Appointment scheduled")
            flag = 1
        # Do something with elem
    except:
        print("Element not found or took too long to load.")
    return flag

if __name__ == "__main__":
    while True:
        current_time = datetime.now()
        
        print("Current time:", current_time)
        scheduled = schedule_appointment()
        if scheduled:
            break
        sleep(1800)
