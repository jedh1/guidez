import selenium
import time
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def prepare_driver(url):
    #Chrome options
    options = Options()
    # options.add_argument('--window-size=1920,1080')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--headless')
    #load Chrome driver
    driver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")

    # Selenium for herokuapp
    # https://www.andressevilla.com/running-chromedriver-with-python-selenium-on-heroku/
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--window-size=1920,1080')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'destinationAddress.destination')))
    print('prepare driver completed')
    return driver

def test_fields(driver):
    print('test_fields start')
    time.sleep(1)
    t1 = driver.find_element_by_class_name('js-special-rates-header')
    print('found special rates box')
    t1.click()
    print('click success')
    time.sleep(1)
    driver.find_element_by_xpath("//label[contains(text(),'CAA')]").click()
    print('found AAA/CAA')
    time.sleep(1)

    driver.find_element_by_class_name('js-brands-header').click()
    time.sleep(1)

    t2 = driver.find_element_by_class_name('js-special-rates-header')
    t2.click()
    time.sleep(1)
    driver.find_element_by_xpath("//label[contains(text(),'Senior')]").click()
    time.sleep(1)

    driver.find_element_by_class_name('js-brands-header').click()
    time.sleep(1)

    driver.find_element_by_class_name('js-special-rates-header').click()
    time.sleep(1)
    driver.find_element_by_xpath("//label[contains(text(),'Military')]").click()
    time.sleep(1)


def fill_form(driver, location, cInDate, cOutDate):
    print("fill_form start")
    # input location
    search_location = driver.find_element_by_name('destinationAddress.destination')
    print("found destination address input field")
    search_location.click()
    print("search_location click success")
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
    # if special_rates:
    #     search_special = driver.find_element_by_class_name('js-special-rates-header')
    #     search_special.click()
    #     time.sleep(1)
    #     search_special2 = driver.find_element_by_xpath("//label[contains(text(),'Corporate')]")
    #     search_special2.click()
    # if special_rates_code:
    #     driver.find_element_by_name("corporateCode").send_keys(str(special_rates_code))
    # find search button and click it
    driver.find_element_by_css_selector("div.l-hsearch-find button").click()
    print('Clicked search button')
    # wait until next page has loaded before running next function
    wait = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'l-property-name')))
    # Sort by price
    driver.find_element_by_xpath("//span[contains(text(),'Distance')]").click()
    print('Clicked sort menu')
    time.sleep(1)
    driver.find_element_by_xpath("//li[contains(text(),'Price')]").click()
    print('Clicked sort by price')
    time.sleep(10)
    #wait = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'l-property-name')))
    print("fill_form Success")

def scrape_results(driver):
    # print("scrape results start")
    hotel_names = list()
    hotel_links = list()
    hotel_address = list()
    hotel_price = list()
    dist = list()
    hotel_names_driver = driver.find_elements_by_class_name("l-property-name")
    # print("Hotel names start")
    for hotel in hotel_names_driver:
        hotel_names.append(hotel.text)
    hotel_links_driver = driver.find_elements_by_class_name("js-hotel-quickview-link")
    # print("hotel links start")
    for hotel in hotel_links_driver:
        hotel_links.append(hotel.get_attribute('href'))
    # print("hotel address start")
    hotel_address_driver = driver.find_elements_by_class_name("m-hotel-address")
    for hotel in hotel_address_driver:
        hotel_address.append(hotel.text)
    # print("hotel price start")
    hotel_price_driver = driver.find_elements_by_xpath("//a[contains(@class,'js-view-rate-btn-link analytics-click t-price-btn t-no-hover-link is-price-link-disable')]//span[contains(@class,'m-display-block')]")
    for hotel in hotel_price_driver:
        hotel_price.append(hotel.text)
    # print(hotel_names, hotel_links, hotel_address, hotel_price)
    driver.close()
    return hotel_names, hotel_links, hotel_address, hotel_price

def email_marriott_results(res, recipient):
    # def takePrice(lst):
    #     return lst[3]
    # res.sort(key=takePrice)
    subject = 'Marriott Search Results - Have a Great Day!'
    txt_message = 'Have a great day!'
    html_body = render_to_string('hotelm/results_email.html', {'res': res})
    msg = EmailMultiAlternatives(
        subject = subject,
        body = txt_message,
        from_email = 'csprojects200220@gmail.com',
        to = [recipient],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()
# def combine_data(names, links, address, price):

if __name__ == '__main__':
    try:
        url = "https://www.marriott.com/search/default.mi"
        driver = prepare_driver(url)
        test_fields(driver)
        print("main.py successfully completed")
    except:
        print("Fail")
