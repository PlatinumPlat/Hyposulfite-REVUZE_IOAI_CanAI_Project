from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from keybert import KeyBERT
import pandas as pd

def review_analysis(result_set):
    # Collect review text and corresponding usernames
    rev_dict = {'Review Name': [],
                'Review Text': []}
    total = 0
    count = 0
    reviewsData = ""

    for result in result_set:
        review_name = result.find(class_='d4r55').text
        try:
            review_text = result.find('span', class_='wiI7pd').text
        except Exception as e: #Handle exception for reviews which only contain ratings
            continue
        rev_dict['Review Name'].append(review_name)
        rev_dict['Review Text'].append(review_text)
        # Add review text to a string in preparation for keyword extraction
        reviewsData += review_text

        # Perform sentiment analysis on each review
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(review_text)
        # Add sentiment score to universal counter for the calculation of the sentiment averages
        total += list(vs.values())[3]
        count += 1

    # return data table, sentiment average, collection of all the review text (respectively)
    return pd.DataFrame(rev_dict), total / count, reviewsData

# Initial Messages
print("Hello User, this program has been submitted to the IOAI CANAI 2025 competition and it is for educational purposes only. Note that bypassing CAPTCHA is unethical, and our program should not require such an act.")
print("For the program's input, paste the google maps link of your business; go to google.com/maps, search for your business in the sidebar, and then click it.")

# Receiving Input
url = input("Insert full url: ")

driver = webdriver.Chrome()
driver.get(url)
time.sleep(20)

# Finding the address of the location
response = BeautifulSoup(driver.page_source, 'html.parser')
address_element = driver.find_element(By.CLASS_NAME, 'rogA2c')
address = address_element.text
if address_element:
    address = address_element.text
    print("The address of the business is " + address + ".")
else:
    print("Program could not find the address of the business.")

# Enter extensive reviews page
review_button = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div/button[2]/div[2]')
review_button.click()

time.sleep(5)
# Find reviews container and click on the object to ensure focus
driver.find_element('xpath','//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]').click()
time.sleep(10)

last_height = driver.execute_script("return document.body.scrollHeight")
number = 0
while True:
    # Scroll down reviews container to load more reviews
    number += 1

    ele = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
    driver.execute_script('arguments[0].scrollBy(0, 5000);', ele)

    time.sleep(5)
    ele = driver.find_element('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
    new_height = driver.execute_script("return arguments[0].scrollHeight", ele)

    if number == 5:
        #THIS
        break
    if new_height == last_height:
        # Prevent endless scrolling when program reaches the end of the page
        break
    last_height = new_height

# Find individual review boxes
next_item = driver.find_elements('xpath', '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
time.sleep(5)

for i in next_item:
    # Click the more button to enable full extraction of the reviews
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

# Get updated and loaded review container
response = BeautifulSoup(driver.page_source, 'html.parser')

# Find review text in review containers
next_2 = response.find_all('div', class_='jftiEf')

analysis, avg, reviewsData = review_analysis(next_2)

# Initialize keybert model for keyword extraction
kw_model = KeyBERT()

# Search for top 8 reoccurring 1-2 word phrases and maintain diversity and relevance
keywords = kw_model.extract_keywords(reviewsData, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=30, top_n=8)

print(analysis)

# Sentiment analysis results
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

# Keyword extraction
KeyWORDS = "Furthermore, the key words used in the the reviews were: "
for element, index in keywords:
    if index % 2 != 0:
        if element == keywords[-2]:
            KeyWORDS = KeyWORDS + "and " + element + "."
        else:
            KeyWORDS = KeyWORDS + element + ", "
string_keywords = [value[0] for value in keywords]
for i, element in enumerate(string_keywords):
    if i == len(string_keywords) - 1:
        KeyWORDS = KeyWORDS + "and " + element + "."
    else:
        KeyWORDS = KeyWORDS + element + ", "

print(KeyWORDS.replace("\n", ""))

# Final messages
print("\nThank you for using REVUZE! This program was created by Sophia and Olivia Pu in the hopes of improving businesses around the world with easily accessible customer feedback analysis, including YOURS.")