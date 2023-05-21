import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import pandas as pd
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import chardet
import csv

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#options.add_experimental_option("excludeSwitches",["enable-automation"])
#options.add_experimental_option('useAutomationExtension',False)
#options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("window-size=1280,800")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")


kv = """
<MyBoxLayout>:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    canvas.before:
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

<MyLabel>:
    size_hint_y: None
    height: 50
    background_color: 0, 0, 1, 1

<MyButton>:
    size_hint_y: None
    height: 50
    background_color: 0, 1, 0, 1

<MyTextInput>:
    multiline: False
    size_hint_y: None
    height: 50
    background_color: 1, 1, 0, 1
"""
class textinp(Widget):
    def close_app(self):
        App.get_running_app().stop()
        Window.close()

class SearchApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.search_input = TextInput(hint_text='Enter keyword', multiline=False)
        layout.add_widget(self.search_input)
        
        self.from_input = TextInput(hint_text='From', multiline=False)
        layout.add_widget(self.from_input)
        
        self.to_input = TextInput(hint_text='To', multiline=False)
        layout.add_widget(self.to_input)
        
        btn = Button(text='Submit')
        btn.bind(on_release=self.search_keyword)
        layout.add_widget(btn)
        return layout

       
    def search_keyword(self, instance):
        keyword = self.search_input.text
        fromm=self.from_input.text
        to=self.to_input.text
        
        
        url = "https://nitter.net/search?f=tweets&q="+keyword+"&since="+fromm+"&until="+to+"&near="
        pages = 4
    
        
        driver = webdriver.Chrome(options= options)
        driver.maximize_window()
        driver.get(url)
        time.sleep(15)

        previous_height = 0
        for i in range(pages):
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
                previous_height += 600

                if previous_height >= height:
                    break
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            #driver.quit()

            #print(soup.encode('utf-8'))
            timestamps=[]

            username = soup.findAll('div',{"class":"fullname-and-username"})
            timestamp = soup.findAll('span',{"class":"tweet-date"})        
            tweets = soup.findAll('div',{"class":"tweet-content media-body"})
            
            tweet_df=pd.DataFrame()
            for i in timestamp:
                timestamp_a = i.find('a')
                timestamp_data = timestamp_a['title']
                timestamps.append(timestamp_data)
            
            tweet_list = [[x.text.encode('utf-8')] for x in tweets]
            username_list = [[x.text.encode('utf-8')] for x in username]
            times=[x for x in timestamps]

            #tweet_df['usernames']=username_list
            #tweet_df['tweets']=tweet_list
            #tweet_df['timestamp']=times
            with open('tweets.csv','w',newline='') as f:
                thewriter=csv.writer(f)
                thewriter.writerow(['Time','UserName','Tweet'])

            with open('tweets.csv', 'a', newline='') as f:
                thewriter = csv.writer(f)
                for value1, value2, value3 in zip(times,username_list,tweet_list):
                    thewriter.writerow([value1,value2,value3])
            driver.find_element(By.XPATH,'//div[@class="show-more"]/a').click()

            previous_height = 0
            
            
            #with open('tweetlist.csv', 'w', newline='') as f:
                #thewriter = csv.writer(f)
                #for value in zip(tweet_list):
                                    
                    #thewriter.writerow[value.decode('utf-8')]
                    #thewriter.writerows(tweet_list)

            #driver.find_element(By.XPATH, "//a[@href='?f=tweets&q=modiji&cursor=DAADDAABCgABFwUZfpsaUAMKAAIXBRLmsppAAAAIAAIAAAACCAADAAAAAAgABAAAAAEKAAUXBRmBNIAnEAoABhcFGYE0f7HgAAA']").click()

            #for tweet in tweets:
            #    print(tweet.text.encode('utf-8'))
        df=pd.read_csv('tweets.csv')


if __name__ == '__main__':
        SearchApp().run()
