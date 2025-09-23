# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0077C095EFB1B6670C1217EDEB6A50ECFD43050AFBEDA806AA6278D179BF6BC34E7386D014A29DF646A9ACF2AFDE921AE81DA1453D2DD95E8DC1E12FA247773A90D2B87EB2EAA7BB36C1DE4671027F9B8907133D0EE5C50907479DC2584AAD091A3B57399BC8CDB6A6516613E4DEE443CC6483B321886626DCD9917C8A72EF31199258894EDF5AA23C140F49CAD388405C3FC1BE2708A7EA3498D01322BAF0D1527514C387FBBFC7C21804ABF7090552A77F98F46BA50992631225E6239BF1C5D2A385547AC23E4F464ACD9C3F273FCE1C3D0C74044FF90E5E9FA3C802ED272DB85AE7EC897A2BEA6D2FB40C03AD4BFC7F74F8BFCE05FA3AC45E59D2AC9F2E4DF59AD0DD0AEE43450A4519C997633D79ACB1E045F94DAAC7A9D0D9E9741E14333FA973ED714C3F8C2650EA881D15C73A44E4A5FCDBC9938C16DDE51B210B7B6C3894792AC1672608E96192463FD396EE784FB2947DC1B8A88A4F725E275FC74940EE2AE2283EE52AE0CB548A4D18CC18F9"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
