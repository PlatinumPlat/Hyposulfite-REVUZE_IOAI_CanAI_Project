from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from keybert import KeyBERT
import pandas as pd


def review_analysis(result_set):
    rev_dict = {'Review Name': [],
                'Review Text': []}
    total = 0
    count = 0

    for result in result_set:
        review_name = result.find(class_='d4r55').text
        try:
            review_text = result.find('span', class_='wiI7pd').text
        except Exception as e:
            continue
        rev_dict['Review Name'].append(review_name)
        rev_dict['Review Text'].append(review_text)
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(review_text)

        total += list(vs.values())[3]
        count += 1
    return pd.DataFrame(rev_dict), total / count

def address_Addition(address1, new_df):
    address_list = address1.split(',')
    new_df['address'] = address_list[0]
    new_df['city'] = address_list[1]
    return new_df

url = []
bool = True

print("Hello USER, visit our website ---- for details about this program. Note that --saftey concerns here--- and copyright licesne here...")
#add systems for checking url, etc.
while bool != False:
    a = input("Insert full url: ")
    url.append(a)

    q = input("Stop input? (Answer y/n): ")
    if (q== 'y'):
        bool=False

c = 0
for i in range(0, len(url)):
    c = c + 1
    driver = webdriver.Chrome()
    driver.get(url[i])
    time.sleep(30)

    # Finding the address of the location
    response = BeautifulSoup(driver.page_source, 'html.parser')
    address_element = driver.find_element(By.CLASS_NAME, 'rogA2c')
    address = address_element.text
    if address_element:
        address = address_element.text
    else:
        print("CAPTCHA appeared, which is blocking the page.")
        address = "Address Not Found"
    print("The address of the business is " + address + ".")

    review_button = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div/button[2]/div[2]')
    review_button.click()

    time.sleep(5)
    driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]').click()
    time.sleep(10)

    SCROLL_PAUSE_TIME = 5

    last_height = driver.execute_script("return document.body.scrollHeight")

    number = 0
    while True:
        number = number + 1

        ele = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
        driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

        time.sleep(SCROLL_PAUSE_TIME)
        ele = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')

        new_height = driver.execute_script("return arguments[0].scrollHeight", ele)

        if number == 5:
            break
        if new_height == last_height:
            break
        last_height = new_height
    next_item = driver.find_elements('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
    time.sleep(5)

    for i in next_item:
        button = i.find_elements(By.TAG_NAME, 'button')
        for m in button:
            if m.text == "More":
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", m)
                    time.sleep(5)
                    m.click()
                except Exception as e:
                    print("Encountered popup/modal which is blocking the more button. Program will wait until button is available to be clicked.")
        time.sleep(5)

    response = BeautifulSoup(driver.page_source, 'html.parser')
    next_2 = response.find_all('div', class_='jftiEf')

<<<<<<< HEAD
    df, avg = review_analysis(next_2)
=======
    def get_review_summary(result_set):
        rev_dict = {'Review Name': [],
                    'Review Text': []}
        total = 0
        count = 0
        reviewsDataSet = ""

        for result in result_set:
            review_name = result.find(class_='d4r55').text
            try:
                review_text = result.find('span', class_='wiI7pd').text
            except Exception as e:
                continue
            rev_dict['Review Name'].append(review_name)
            rev_dict['Review Text'].append(review_text)
            reviewsDataSet = reviewsDataSet + review_text
            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(review_text)

            total += list(vs.values())[3]
            count += 1
        return pd.DataFrame(rev_dict), total/count, reviewsDataSet


    df, avg, reviewsData = get_review_summary(next_2)
    
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(reviewsData, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=30, top_n=8)
>>>>>>> 358787485bcfa0669d577807f6a79078d1ac00fa

    if c == 1:
        df1 = df.copy()
        final_df = address_Addition(address, df1)
    else:
        df2 = df.copy()
        final_df = address_Addition(address, df2)
        final_df1 = pd.concat([df1, final_df], axis=0)

    print(df)
    avg = round(5+(avg/2)*10)

    print("After running sentiment analysis on the reviews, this program discovered that the average sentiment score (from zero to ten) for the business was", avg, "out of 10.")
    if avg<-8:
        print("In other words, the CONTENT of the reviews was often strongly negative.")
    elif avg <-4:
        print("In other words, the CONTENT of the reviews was often negative.")
    elif avg<0:
        print("In other words, the CONTENT of the reviews was often somewhat negative.")
    elif avg<4:
        print("In other words, the CONTENT of the reviews was often somewhat positive.")
    elif avg<8:
        print("In other words, the CONTENT of the reviews was often positive.")
    else:
        print("In other words, the CONTENT of the reviews was often extremely positive.")
    KeyWORDS = "Furthermore, the key words used in the the reviews were: "
    for element, index in keywords:
        if index % 2 != 0:
            if element == keywords[-2]:
                KeyWORDS = KeyWORDS + "and " + element + "."
            else:
                KeyWORDS = KeyWORDS + element + ", "
    print(KeyWORDS.replace("\n", ""))