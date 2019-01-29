from selenium import webdriver
import config


url = "https://www.cryptopanic.com"
chromedriver_path = os.path.join(config.ROOT_DIR, "chromedriver")

options = webdriver.ChromeOptions()

# initialize headless mode
options.add_argument('headless')

# set the window size
options.add_argument('window-size=1200x600')

# initialize the driver
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver_path)

driver.get(url)

# wait up to 10 seconds for the elements to become available
driver.implicitly_wait(10)

# use css selectors to grab the login inputs
email = driver.find_element_by_css_selector('input[type=email]')
password = driver.find_element_by_css_selector('input[type=password]')
login = driver.find_element_by_css_selector('input[value="Log In"]')

driver.get_screenshot_as_file('main-page.png')
