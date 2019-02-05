from selenium import webdriver
import config
import os
import time
import datetime
import sys
import re
import pickle


SCROLL_PAUSE_TIME = 1


def setUp():
    try:
        filter = sys.argv[1]
    except Exception as e:
        print(e)
        filter = 'All'

    url = "https://www.cryptopanic.com/news?filter={}".format(filter)
    chromedriver_path = os.path.join(config.ROOT_DIR, "chromedriver")

    options = webdriver.ChromeOptions()

    # initialize headless mode
    options.add_argument('headless')
    # webdriver.ChromeOptions().extensions
    # webdriver.ChromeOptions().add_extension()

    # Set the window size
    options.add_argument('window-size=1200x800')

    # initialize the driver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)

    driver.get(url)

    # wait up to 10 seconds for the elements to become available
    driver.implicitly_wait(2)

    return driver, filter


def getData():
    data = dict()
    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')

    print("Gathering Data...")
    start = datetime.datetime.today()
    print("Time Start: %s" % start.ctime())
    for i in range(len(elements)):

        #  Get date posted
        date_time = elements[i].find_element_by_css_selector('time').get_attribute('datetime')
        string_date = re.sub('-.*', '', date_time)
        date_time = datetime.datetime.strptime(string_date, "%a %b %d %Y %H:%M:%S %Z")

        #  Get Title of News
        title = elements[i].find_element_by_css_selector("span.title-text").text
        if title == '':
            driver.execute_script("arguments[0].scrollIntoView();",
                                  elements[i].find_element_by_css_selector("span.title-text"))
            title = elements[i].find_element_by_css_selector("span.title-text").text

        # TODO Get Link Source

        #  Get Currency Tags
        currencies = []
        currency_elements = elements[i].find_elements_by_class_name("colored-link")
        for currency in currency_elements:
            currencies.append(currency.text)

        votes = []
        nc_votes = elements[i].find_elements_by_css_selector("span.nc-vote-cont")
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

    print("Finished gathering %s rows of data" % len(elements))
    print("Time End: %.19s" % datetime.datetime.now())
    print("Elapsed Time Gathering Data: %.7s" % (datetime.datetime.now() - start))

    return data


def loadMore(len_elements):
    # Load More News
    load_more = driver.find_element_by_class_name('btn-outline-primary')
    driver.execute_script("arguments[0].scrollIntoView();", load_more)

    time.sleep(SCROLL_PAUSE_TIME)

    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')
    if len_elements < len(elements):
        print("Loading %s more rows" % (len(elements) - len_elements))
        return True
    else:
        print("No more rows to load :/")
        print("Max rows loaded: %s" % len(elements))
        return False


def saveData(data):
    # Save the website data
    file_name = "cryptopanic_{}_{}->{}.pickle".format(filter.lower(),
                                                      str(data[len(data) - 1]['Date']),
                                                      str(data[0]['Date']))
    print("Saving data to %s" % file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def tearDown():
    driver.quit()


driver, filter = setUp()

while True:
    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')
    if loadMore(len(elements)):
        continue
    else:
        print("Total Rows loaded:%s" % len(elements))
        data = getData()
        saveData(data)
        tearDown()
        break
