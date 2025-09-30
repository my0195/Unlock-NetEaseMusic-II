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
    browser.add_cookie({"name": "MUSIC_U", "value": "000E60FF58E1D3697718C7B0DF9A4EAF3004A89DEC4BEBE0983946D1927354605142E6E351CFB36EFCAB4D882036235FC7C4AE1D1D0069760E33CBAD740C40D6E097327BB7BFFA1A77D828BC0C42D1D68330136C79E729F0681DB6FFB90C6BE76F1FA9E2BF4BB36A1FA7A08FFBD1C51AE1739771E1B13418D1D85751D652C3A9D560194B120C39A924E5F16A8D840D215260A2E260F01F5508BB617956C2E07756981E718644DF161AD22BFDB0E938B31C68857B7C01C7A713A5126D9B4A6664B000B69713327B3EF5F2FEF0D5823355D79594F21561A52162F2E2AD9DC45D1FDFB9FF70DF58FD509067D044C7CF6A93B4145DCE51B60E7EBE836297D4846796CD66EDCB1E290FB893B4B62D0EC04FC2AED4FA465FCD3054DE06ED68CF2056B4C91DC9EA1D7916C5626B18A4D275848A73AF031439768A064CB93C1D4F02B65398DB76A436989C1FDF3A587A4DD11992DF8F328A4BE687767402FDF73DEC65634A7CE5B644BEADBF7EACE0E01C13E849DF"})
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
