from selenium import webdriver
import config
import os

def getProperties():
    properties = driver.execute_script('return window.getComputedStyle(arguments[0], null);', element)

    for property in properties:
        print(element.value_of_css_property(property))


def setUp():

    url = "https://www.cryptopanic.com"
    chromedriver_path = os.path.join(config.ROOT_DIR, "chromedriver")

    options = webdriver.ChromeOptions()

    # initialize headless mode
    # options.add_argument('headless')
    # webdriver.ChromeOptions().extensions
    # webdriver.ChromeOptions().add_extension()

    # Set the window size
    options.add_argument('window-size=1200x800')

    # initialize the driver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)

    driver.get(url)

    # wait up to 10 seconds for the elements to become available
    driver.implicitly_wait(2)

    return driver


def getData():
    data = dict()

    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')
    print(len(elements))

    # count = 0
    for i in range(len(elements)):
        print(i)
        print(len(elements))

        #  Debug
        # if count == 2:
        #     count = 0
        #     break
        elements[i].find_element_by_css_selector('time')
        #  Get date posted
        date_time = elements[i].find_element_by_css_selector('time').get_attribute('datetime')
        # print(date_time)

        #  Get Title of News
        # title = element.find_element_by_class_name("title-text").text
        title = elements[i].find_element_by_css_selector("span.title-text").text
        if title == '':
            print("Empty title below")
            print(title)
            print("Scrolling")
            scrollCenter()
            title = elements[i].find_element_by_css_selector("span.title-text").text
            print("Not empty")
            print(title)


        # TODO Get Link Source

        #  Get Currency Tags
        currency_elements = elements[i].find_elements_by_class_name("colored-link")
        currencies = []
        for currency in currency_elements:
            currencies.append(currency.text)

        nc_votes = elements[i].find_elements_by_css_selector("span.nc-vote-cont")
        votes = []
        for nc_vote in nc_votes:
            votes.append(nc_vote.get_attribute('title'))
        try:
            data[i] = {"Date": date_time,
                       "Title": title,
                       "Currencies": currencies,
                       "Votes": votes}
        except Exception as e:
            print(e)
            print("Element index is %s" % i)
            print("Length of elements is %s" % len(elements))
            break

        # count += 1

    return len(elements), data


def loadMore():
    # Load More News
    load_more = driver.find_element_by_class_name('btn-outline-primary')
    driver.execute_script("arguments[0].scrollIntoView();", load_more)


def scrollCenter():
    #  Scrolls to Center
    scroll = driver.find_element_by_class_name('ps__rail-y')
    scroll.click()
    # driver.get_window_position()
    # scroll.get_attribute('offsetTop')
    # scroll.get_attribute('style')


def tearDown():
    driver.quit()


driver = setUp()

import time
SCROLL_PAUSE_TIME = 1
count = 0
while count < 10:
    print(count)
    lenData, data = getData()
    loadMore()
    print(lenData, data)
    count += 1
    time.sleep(SCROLL_PAUSE_TIME)

print("finished!")
print(lenData, data)
tearDown()

getData()
