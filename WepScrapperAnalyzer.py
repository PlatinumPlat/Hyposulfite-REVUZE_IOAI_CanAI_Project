import sys

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.devtools.v134.css import add_rule
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as BC
import pandas as pd

def address_Addition(address1, new_df):
    address_list = address1.split(',')
    new_df['address'] = address_list[0]
    new_df['city'] = address_list[1]
    return new_df


driver = webdriver.Chrome()

url = []
bool = True

print("Hello USER, visit our website ---- for details about this program. Note that --saftey concerns here--- and copyright licesne here...")
#add systems for checking url, etc.
while bool != False:
    a = input("Insert full url: ")
    xPATH = input("Insert review link's path: ")
    b = [a, xPATH]

    url.append(b)

    q = input("Stop input? (Answer y/n): ")
    if (q== 'y'):
        bool=False

c = 0
for i in range(0, len(url)):
    c = c + 1
    driver.get(url[i][0])
    time.sleep(5)

    # Finding the address of the location
    response = BeautifulSoup(driver.page_source, 'html.parser')
    address_element = driver.find_element(By.CLASS_NAME, 'rogA2c')
    address = address_element.text
    if address_element:
        address = address_element.text
    else:
        print("CAPTCHA appeared, which is blocking the page.")
        address = "Address Not Found"
    print(address)

    driver.find_element('xpath',url[i][1]).click()
    time.sleep(3)

    SCROLL_PAUSE_TIME = 5

    last_height = driver.execute_script("return document.body.scrollHeight")

    number = 0
    while True:
        number = number + 1

        ele = driver.find_element('xpath', url[i][1])
        driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

        time.sleep(SCROLL_PAUSE_TIME)
        ele = driver.find_element('xpath', url[i][1])

        new_height = driver.execute_script("return arguments[0].scrollHeight", ele)

        if number == 5:
            break
        if new_height == last_height:
            break
        last_height = new_height
    next_item = driver.find_elements('xpath', url[i][1])
    time.sleep(3)

    for i in next_item:
        button = i.find_elements(By.TAG_NAME, 'button')
        for m in button:
            if m.text == "More":
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", m)
                    time.sleep(1)
                    m.click()
                except Exception as e:
                    print("Encountered popup/modal which is blocking the more button. Program will wait until button is available to be clicked.")
                    #print(f"Skipping this 'More' button due to: {e}")
        time.sleep(5)

    response = BeautifulSoup(driver.page_source, 'html.parser')
    next_2 = response.find_all('div', class_='jftiEf')


    def get_review_summary(result_set):
        rev_dict = {'Review Name': [],
                    'Review Text': []}

        for result in result_set:
            review_name = result.find(class_='d4r55').text
            review_text = result.find('span', class_='wiI7pd').text
            rev_dict['Review Name'].append(review_name)
            rev_dict['Review Text'].append(review_text)

        return pd.DataFrame(rev_dict)

    df = get_review_summary(next_2)

    if c == 1:
        df1 = df.copy()
        final_df = address_Addition(address, df1)
    else:
        df2 = df.copy()
        final_df = address_Addition(address, df2)
        final_df1 = pd.concat([df1, final_df], axis=0)

print(df)
#address, etc. in other files.
#instead, use google api for ethical factor