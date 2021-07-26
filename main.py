from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup as Bs
from dotenv import load_dotenv
from selenium import webdriver
from typing import Dict, List
from upload import upload_csv
import pandas as pd
import os

load_dotenv()

# ========== SETUP ========== #

URL = 'https://sigaa.unifei.edu.br/'
my_username = os.getenv('MY_USERNAME')
my_password = os.getenv('MY_PASSWORD')
driver_path = os.getenv('DRIVER_PATH')
csv_output = os.getenv('CSV_OUTPUT')

options = Options()
options.headless = True
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options, executable_path=driver_path)

driver.get(URL)

# ========== LOGIN ========== #
# xPaths
login_xpath = '/html/body/div/div/div[1]/div[2]/div/ul/li[2]/a'
user_xpath = '/html/body/div[2]/div[2]/div[4]/form/table/tbody/tr[1]/td/input'
password_xpath = '/html/body/div[2]/div[2]/div[4]/form/table/tbody/tr[2]/td/input'
submit_xpath = '/html/body/div[2]/div[2]/div[4]/form/table/tfoot/tr/td/input'

# Driver
login = driver.find_element_by_xpath(login_xpath)
login.click()

user = driver.find_element_by_xpath(user_xpath)
user.send_keys(my_username)

password = driver.find_element_by_xpath(password_xpath)
password.send_keys(my_password)

submit = driver.find_element_by_xpath(submit_xpath)
submit.click()

# ========== FIND GRADES TABLES ========== #
# xPaths
dashboard_xpath = '/html/body/div[2]/div[1]/div[2]/div[1]/ul/li[3]/a'
menu_learning_xpath = '/html/body/div[2]/div[2]/div[1]/div[1]/div/form/div/table/tbody/tr/td[1]'
grades_page_xpath = '/html/body/div[2]/div[2]/div[1]/div[1]/div/form/div/div[1]/table/tbody/tr[1]/td[2]'
grades_table_xpath = '/html/body/div/div[2]/div/table'

# Driver
dashboard = driver.find_element_by_xpath(dashboard_xpath)
dashboard.click()

action = ActionChains(driver)
menu_learning = driver.find_element_by_xpath(menu_learning_xpath)
action.move_to_element(menu_learning).perform()

grades_page = driver.find_element_by_xpath(grades_page_xpath)
grades_page.click()

grades_table = driver.find_element_by_xpath(grades_table_xpath).get_attribute('outerHTML')

# ========== EXTRACT DATA ========== #
# Columns
soup = Bs(grades_table, 'html.parser')

thead = soup.find('thead')
ths = thead.findChildren('th')
columns = []

for th in ths:
    columns.append(''.join(th.text.split()))

# Rows
tbody = soup.find('tbody')
trs = tbody.findChildren('tr')
rows = []

for tr in trs:
    rows.append(tr.find_all('td'))

codes = []
unity_1 = []
unity_2 = []
results = []
absences = []

for i in range(len(rows)):
    codes.append(''.join(rows[i][0].text.split()))
    unity_1.append(''.join(rows[i][2].text.split()))
    unity_2.append(''.join(rows[i][3].text.split()))
    results.append(''.join(rows[i][5].text.split()))
    absences.append(''.join(rows[i][6].text.split()))

d: Dict[str, List[str]] = {
    columns[0]: codes,
    columns[2]: unity_1,
    columns[3]: unity_2,
    columns[5]: results,
    columns[6]: absences,
}

# Create Dataframe
df = pd.DataFrame(data=d)

# Export CSV
df.to_csv(csv_output, index=False, encoding='utf-8')

# Upload CSV to G Drive
upload_csv()

# Print results and stop the driver
print(df)
driver.close()
