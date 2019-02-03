from selenium import webdriver
import config
import os
import time
import datetime
SCROLL_PAUSE_TIME = 1


def getProperties():
    properties = driver.execute_script('return window.getComputedStyle(arguments[0], null);', element)

    for property in properties:
        print(element.value_of_css_property(property))


def setUp():

    url = "https://www.cryptopanic.com"
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

    return driver


# def getData():
#
#     data = dict()
#     elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')
#     try:
#         for i in range(len(elements)):
#
#             #  Get date posted
#             date_time = elements[i].find_element_by_css_selector('time').get_attribute('datetime')
#
#             #  Get Title of News
#             title = elements[i].find_element_by_css_selector("span.title-text").text
#             if title == '':
#                 driver.execute_script("arguments[0].scrollIntoView();",
#                                       elements[i].find_element_by_css_selector("span.title-text"))
#                 title = elements[i].find_element_by_css_selector("span.title-text").text
#
#             # TODO Get Link Source
#
#             #  Get Currency Tags
#             currencies = []
#             currency_elements = elements[i].find_elements_by_class_name("colored-link")
#             for currency in currency_elements:
#                 currencies.append(currency.text)
#
#             votes = []
#             nc_votes = elements[i].find_elements_by_css_selector("span.nc-vote-cont")
#             for nc_vote in nc_votes:
#                 votes.append(nc_vote.get_attribute('title'))
#             try:
#                 data[i] = {"Date": date_time,
#                            "Title": title,
#                            "Currencies": currencies,
#                            "Votes": votes}
#             except Exception as e:
#                 print(e)
#                 print("Element index is %s" % i)
#                 print("Length of elements is %s" % len(elements))
#                 break
#     except Exception as e:
#         print(e)
#     return len(elements), data

def getData():

    data = dict()
    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')

    for i in range(len(elements)):

        #  Get date posted
        date_time = elements[i].find_element_by_css_selector('time').get_attribute('datetime')

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

    return len(elements), data


def loadMore(len_elements):
    # Load More News
    load_more = driver.find_element_by_class_name('btn-outline-primary')
    driver.execute_script("arguments[0].scrollIntoView();", load_more)

    time.sleep(SCROLL_PAUSE_TIME)

    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')
    if len_elements < len(elements):
        print("loaded %s more rows" % (len(elements) - len_elements))
        return True
    else:
        print("No more rows to load :/")
        print("Max rows loaded: %s" % len(elements))
        return False


def tearDown():
    driver.quit()
tearDown()

driver = setUp()


while True:
    elements = driver.find_elements_by_css_selector('div.news-row.news-row-link')
    print("Total Rows loaded:%s" % len(elements))
    # time.sleep(SCROLL_PAUSE_TIME)
    if loadMore(len(elements)):
        continue
    else:
        print("Gathering Data...")
        len_data, data = getData()
        print(len_data, data)
        print("finished!")
        tearDown()
        break

print(data)
# Save the website data
import pickle
file_name = "cryptopanic_all_%s.pickle" % datetime.datetime.utcnow().date()
file_name
with open(file_name, 'wb') as f:
          pickle.dump(data, f)
