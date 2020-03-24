import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def prepare_driver(url):
    # options = Options()
    # options.add_argument('-headless')
    driver = webdriver.Chrome(executable_path="hotelm/drivers/chromedriver.exe")
    driver.get(url)
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'destinationAddress.destination')))
    return driver

def fill_form(driver, location, cInDate, cOutDate):
    print("fill_form start")
    # input location
    search_location = driver.find_element_by_name('destinationAddress.destination')
    print("found destination address input field")
    search_location.click()
    search_location.send_keys(location)
    time.sleep(2)
    # input check-in date
    search_checkin = driver.find_element_by_class_name('ccheckin')
    search_checkin.click()
    search_checkin.send_keys(Keys.CONTROL + "a")
    search_checkin.send_keys(Keys.BACKSPACE)
    search_checkin.send_keys(cInDate)
    search_checkin.send_keys(Keys.ESCAPE)
    # input check-out date
    search_checkout = driver.find_element_by_class_name('ccheckout')
    search_checkout.click()
    search_checkout.send_keys(Keys.CONTROL + "a")
    search_checkout.send_keys(Keys.BACKSPACE)
    search_checkout.send_keys(cOutDate)
    search_checkout.send_keys(Keys.ESCAPE)
    # input special rates
    search_special = driver.find_element_by_class_name('js-special-rates-header')
    search_special.click()
    time.sleep(1)
    search_special2 = driver.find_element_by_xpath("//label[contains(text(),'Corporate')]")
    search_special2.click()
    driver.find_element_by_name("corporateCode").send_keys("MMP")
    # find search button and click it
    driver.find_element_by_css_selector("div.l-hsearch-find button").click()
    # wait until next page has loaded before running next function
    wait = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'l-property-name')))
    print("fill_form Success")

def scrape_results(driver):
    print("scrape results start")
    hotel_names = list()
    hotel_links = list()
    hotel_address = list()
    hotel_price = list()
    dist = list()
    hotel_names_driver = driver.find_elements_by_class_name("l-property-name")
    print("Hotel names start")
    for hotel in hotel_names_driver:
        hotel_names.append(hotel.text)
    hotel_links_driver = driver.find_elements_by_class_name("js-hotel-quickview-link")
    print("hotel links start")
    for hotel in hotel_links_driver:
        hotel_links.append(hotel.get_attribute('href'))
    print("hotel address start")
    hotel_address_driver = driver.find_elements_by_class_name("m-hotel-address")
    for hotel in hotel_address_driver:
        hotel_address.append(hotel.text)
    print("hotel price start")
    hotel_price_driver = driver.find_elements_by_xpath("//a[contains(@class,'js-view-rate-btn-link analytics-click t-price-btn t-no-hover-link is-price-link-disable')]//span[contains(@class,'m-display-block')]")
    for hotel in hotel_price_driver:
        hotel_price.append(hotel.text)
    print(hotel_names, hotel_links, hotel_address, hotel_price)
    return hotel_names, hotel_links, hotel_address, hotel_price

# def combine_data(names, links, address, price):

if __name__ == '__main__':
    try:
        url = "https://www.marriott.com/search/default.mi"
        driver = prepare_driver(url)
        fill_form(driver, 'Las Vegas, NV', '7-10-20', '7-13-20')
        time.sleep(1)
        scrape_results(driver)
        print("main.py successfully completed")
    except:
        print("Fail")
