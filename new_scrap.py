from selenium import *
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

Keyword = input()
Keyword_data = Keyword.replace(" ", "+")

url = "https://www.youtube.com/results?search_query="+Keyword_data
driver = webdriver.Chrome(options= options)
driver.maximize_window()
driver.get(url)
time.sleep(10)

def videos():

    # driver.execute_script("window.scrollBy(0,10000)","")

    def convert_to_list_of_lists(flat_list, sublist_length):
        return [flat_list[i:i+sublist_length] for i in range(0, len(flat_list), sublist_length)]

    sublist_length = 1

    soup = BeautifulSoup(driver.page_source,'html.parser')
    videos = soup.select('#video-title yt-formatted-string')
    video_list = [x.text.encode('utf-8') for x in videos]
    video_list_final = convert_to_list_of_lists(video_list,sublist_length)

    with open('videolist.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        # for value1, value2 in zip(uname_list_final,comment_list_final):
        #     thewriter.writerow([value1,value2])
        thewriter.writerows(video_list_final)



def comments():

    driver.find_element(By.XPATH, '//yt-formatted-string[@class="style-scope ytd-video-renderer"]').click()

    previous_height = 0

    while True:
        height = driver.execute_script("""
                function getActualHeight(){
                    return Math.max(
                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                    );
                }
                return getActualHeight()
            """)
        
        driver.execute_script(f"window.scrollTo({previous_height},{previous_height+300})")
        time.sleep(1)
        previous_height += 300

        if previous_height >= height:
            break

        soup = BeautifulSoup(driver.page_source, 'html.parser')

    driver.quit()

    title_text = soup.select_one('#container h1')
    print(title_text.text.encode('utf-8'))

    def convert_to_list_of_lists(flat_list, sublist_length):
        return [flat_list[i:i+sublist_length] for i in range(0, len(flat_list), sublist_length)]

    sublist_length = 1

    comments = soup.select("#content #content-text")
    comment_list = [x.text.encode('utf-8') for x in comments]
    comment_list_final = convert_to_list_of_lists(comment_list,sublist_length)

    #uname = soup.findAll('span',{"class":"style-scope ytd-comment-renderer"})
    uname = soup.select("#header-author #author-text span")
    uname_list = []

    for i in uname:
        uname_list.append(i.text.encode('utf-8'))

    uname_list_final = convert_to_list_of_lists(uname_list,sublist_length)

    print(uname_list_final)
    print(comment_list_final)

    with open('commentlist.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        for value1, value2 in zip(uname_list_final,comment_list_final):
            thewriter.writerow([value1,value2])

videos()
comments()
