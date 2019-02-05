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
    print("Initializing chromedriver.\n")
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)

    print("Navigating to %s\n" % url)
    driver.get(url)

    # wait up to 10 seconds for the elements to become available
    driver.implicitly_wait(2)

    return driver, filter


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
        print("Total rows loaded: %s\n" % len(elements))
        return False


def getData():
    data = dict()
    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')

    total_rows = len(elements) - 7  # elements being returned are appended by 7 of the first rows.
    print("Downloading Data...\n")
    start = datetime.datetime.today()
    print("Time Start: %s\n" % start.ctime())
    for i in range(total_rows):
        # print("Downloading Row %s of %s" % (i + 1, total_rows))

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

        data[i] = {"Date": date_time,
                   "Title": title,
                   "Currencies": currencies,
                   "Votes": votes}
        print("Downloaded %s of %s\nTitle: %s\nPublished: %s\n" % (i + 1,
                                                                   total_rows,
                                                                   data[i]['Title'],
                                                                   data[i]["Date"]))

    print("Finished gathering %s rows of data\n" % len(data))
    print("Time End: %.19s" % datetime.datetime.now())
    print("Elapsed Time Gathering Data: %.7s\n" % (datetime.datetime.now() - start))

    return data


def saveData(data):
    # Save the website data
    file_name = "cryptopanic_{}_{:.10}->{:.10}.pickle".format(filter.lower(),
                                                              str(data[len(data) - 1]['Date']),
                                                              str(data[0]['Date']))
    print("Saving data to %s\n" % file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def tearDown():
    print("Exiting Headless Chrome Driver\n")
    driver.quit()


driver, filter = setUp()

print("Scrolling and Loading News Feed. ;)")
while True:

    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')

    if loadMore(len(elements)):
        continue
    else:
        data = getData()
        saveData(data)
        tearDown()
        break


def loadData():

    # Save the website data
    file_name = "cryptopanic_hot_2019-02-03 11:10:04->2019-02-04 15:00:46.pickle"
    with open(file_name, 'rb') as f:
        return pickle.load(f)
# data = loadData()
# print(data[len(data)-8]['Date'])
# print(data[2]['Date'])
# file_name = "cryptopanic_{}_{:.10}->{:.10}.pickle".format(filter.lower(),
#                                                   str(data[len(data) - 8]['Date']),
#                                                   str(data[0]['Date']))
# file_name
# for i in range(len(data)):
#     print(i, data[i]["Date"])
