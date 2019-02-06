from selenium import webdriver
import os
import time
import datetime
import sys
import re
import pickle
import urllib


ROOT_DIR = os.path.dirname(os.getcwd())
abs_path_data = "/Users/pAulse/Documents/Projects/Python Projects/Webscraping/robobrowser/cryptopanic/cryptopanic_scraper/data/"
SCROLL_PAUSE_TIME = 1


def setUp():
    try:
        filter = sys.argv[1]
    except Exception as e:
        # print(e)
        filter = 'All'

    url = "https://www.cryptopanic.com/news?filter={}".format(filter)
    chromedriver_path = os.path.join(ROOT_DIR, "chromedriver")

    options = webdriver.ChromeOptions()

    # initialize headless mode
    options.add_argument('headless')

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
    return False
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
        title = elements[i].find_element_by_css_selector("span.title-text span:nth-child(1)").text
        if title == '':
            driver.execute_script("arguments[0].scrollIntoView();",
                                  elements[i].find_element_by_css_selector("span.title-text"))
            title = elements[i].find_element_by_css_selector("span.title-text span:nth-child(1)").text

        # Get Source URL
        elements[i].find_element_by_css_selector("a.news-cell.nc-title").click()
        source_name = elements[i].find_element_by_css_selector("span.si-source-name").text
        source_link = driver.find_element_by_xpath("//div/h1/a[2]").get_property('href')
        source_url = re.sub(".*=", '', urllib.parse.unquote(source_link))
        driver.back()

        #  Get Currency Tags
        currencies = []
        currency_elements = elements[i].find_elements_by_class_name("colored-link")
        for currency in currency_elements:
            currencies.append(currency.text)

        votes = dict()
        nc_votes = elements[i].find_elements_by_css_selector("span.nc-vote-cont")
        for nc_vote in nc_votes:
            vote = nc_vote.get_attribute('title')
            value = vote[:2]
            action = vote.replace(value, '').replace('votes', '').strip()
            votes[action] = int(value)

        data[i] = {"Date": date_time,
                   "Title": title,
                   "Currencies": currencies,
                   "Votes": votes,
                   "Source": source_name,
                   "URL": source_url}
        print("Downloaded %s of %s\nPublished: %s\nTitle: %s\nSource: %s\nURL: %s\n" % (i + 1,
                                                                                        total_rows,
                                                                                        data[i]["Date"],
                                                                                        data[i]["Title"],
                                                                                        data[i]["Source"],
                                                                                        data[i]["URL"]))

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
    with open(abs_path_data + file_name, 'wb') as f:
        pickle.dump(data, f)


def tearDown():
    print("Exiting Chrome Driver")
    driver.quit()


driver, filter = setUp()
if __name__ == "__main__":
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
