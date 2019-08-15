from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime, time, json, os
from bs4 import BeautifulSoup

# declare arival date and calculate return date with a little arithmatic
depart = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%m/%d/%Y')
returning = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime('%m/%d/%Y')

# create driver instance, in this case using headless chrom browsing and using a custom argument
# user-agent to make the webpage think we are running in a normal browser
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver/chromedriver', options=options)
# driver = webdriver.Chrome(executable_path='/Users/sam/Devel/airfair-scraper/chromedriver/chromedriver')
driver.implicitly_wait(10)
driver.get("")

# go to the flights tab on the expedia landing page
flights_button = driver.find_element_by_id("tab-flight-tab-hp")
flights_button.click()

# enter your departing airport
flight_from = driver.find_element_by_id("flight-origin-hp-flight")
flight_from.send_keys("Chicago (CHI-All Airports)")

# enter your destination
flight_to = driver.find_element_by_id("flight-destination-hp-flight")
flight_to.send_keys("San Francisco, CA (SFO-San Francisco Intl.)")

# enter a departure date
departing = driver.find_element_by_id("flight-departing-hp-flight")
departing.send_keys(depart)
departing.send_keys(Keys.ESCAPE)

# enter a return date
return_date = driver.find_element_by_id("flight-returning-hp-flight")
for i in range(0,10,1):
    return_date.send_keys(Keys.BACK_SPACE)

return_date.send_keys(returning)
return_date.send_keys(Keys.ESCAPE)

# try div[7] but sometimes the page renders the search button under div[8] should probably look into this
try:
    search_button = driver.find_element_by_xpath("//*[@id=\"gcw-flights-form-hp-flight\"]/div[7]/label/button")
    search_button.click()
except:
    search_button = driver.find_element_by_xpath("//*[@id=\"gcw-flights-form-hp-flight\"]/div[8]/label/button")
    search_button.click()


time.sleep(20)
try:
    if driver.find_element_by_css_selector('.basic-economy-toggle-link'):
        rules_and_restrictions = driver.find_element_by_css_selector('.basic-economy-toggle-link')
        rules_and_restrictions.click()
        time.sleep(1)
        select_trip_to = driver.find_element_by_css_selector('button.btn-secondary:nth-child(3)')
        select_trip_to.click()
except:
    try:
        driver.find_element_by_xpath("//*[@id=\"flight-module-wl_\"]/div[1]/div/div[1]/div/div[2]/div")
        try:
            select_trip_to = driver.find_element_by_xpath("//*[@id=\"flightModuleList\"]/li[2]/div[1]/div[1]/div[2]/div/div[2]/button")
            select_trip_to.click()
        except NoSuchElementException:
            select_trip_to = driver.find_element_by_xpath("//*[@id=\"flightModuleList\"]/li[2]/div[1]/div[1]/div[2]/div/div[2]/button")
            select_trip_to.click()
        except:
            print("you're xpath is bad again")
    except NoSuchElementException:
        try:
            select_trip_to = driver.find_element_by_xpath("//*[@id=\"flightModuleList\"]/li[1]/div[1]/div[1]/div[2]/div/div[2]/button")
            select_trip_to.click()
        except NoSuchElementException:
                select_trip_to = driver.find_element_by_xpath("//*[@id=\"flightModuleList\"]/li[2]/div[1]/div[1]/div[2]/div/div[2]/button")
                select_trip_to.click()
        except:
            print("you're xpath is bad again")


try:
    # select flight back
    time.sleep(10)
    select_trip_return = driver.find_element_by_xpath("//*[@id=\"flightModuleList\"]/li[1]/div[2]/button[1]")
    select_trip_return.click()
    time.sleep(10)
    select_trip_return_final = driver.find_element_by_xpath("//*[@id=\"basic-economy-tray-content-1\"]/div/div/div[1]/button")
    select_trip_return_final.click()
    # no thanks response to "do we want a hotel"
    time.sleep(3)
    no_thanks = driver.find_element_by_css_selector("#forcedChoiceNoThanks")
    no_thanks.send_keys(Keys.ENTER)
except NoSuchElementException as e:
    print(e)

# soup it
time.sleep(15)
handle = driver.window_handles
currentHandle = driver.current_window_handle
# switch driver focus to new tab based on the above fetched window handle
driver.switch_to.window(handle[1])

# soup time
url = driver.current_url
soup = BeautifulSoup(driver.page_source, 'lxml')
driver.quit()

# DEPARTURE TRIP INFO

departureAirline = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5)')[0].get_text() # departing airline
departureCity = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)')[0].get_text() # departing city
departureDate = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')[0].get_text() # departing date
departureTime = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > span:nth-child(1)')[0].get_text() # departing time
arrivalCity = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(4)')[0].get_text() # arrival city
arrivalTime = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(3) > span:nth-child(1)')[0].get_text() # arrival time
stopsTo = soup.select('div.flex-card:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(4) > span:nth-child(2)')[0].get_text() # nonstop?

# RETURN TRIP INFO

departureAirlineB = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5)')[0].get_text() # airline home
departureCityB = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)')[0].get_text() # departing city
departureDateB = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')[0].get_text() # departing date
departureTimeB = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > span:nth-child(1)')[0].get_text() # departing time
arrivalCityB = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(4)')[0].get_text() # arrival city
arrivalTimeB = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(3) > span:nth-child(1)')[0].get_text() # arrival time
stopsFrom = soup.select('div.flex-card:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(4) > span:nth-child(2)')[0].get_text() # nonstop?

# RETURN DICT

info = {
    "scrapeDate": datetime.datetime.now().strftime("%m/%d/%Y"),
    "scrapeTime": datetime.datetime.now().strftime("%H:%M:%S"),
    "totalPrice": soup.find("span", attrs={"class": "packagePriceTotal"}).get_text(),
    "urlToBook": url,
    "flightInfo": {
        "departure": {
            "airline": departureAirline,
            "date": departureDate,
            "departCity": departureCity,
            "departTime": departureTime,
            "arriveCity": arrivalCity,
            "arriveTime": arrivalTime,
            "stops": stopsTo
        },
        "returning": {
            "airline": departureAirlineB,
            "date": departureDateB,
            "departCity": departureCityB,
            "departTime": departureTimeB,
            "arriveCity": arrivalCityB,
            "arriveTime": arrivalTimeB,
            "stops": stopsFrom
        }
    }
}
print(json.dumps(info, sort_keys=True, indent=4))
