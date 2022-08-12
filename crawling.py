#! /usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
#crawling.spec file hidden imports >> 'selenium','selenium.webdriver.common.by','selenium.webdriver.common.keys'
driver = webdriver.Chrome()
#executable_path="/home/ubuntu/jenkins-backend/BackEnd/crawling/tt/chromedriver.exe"
driver.get("https://burst.shopify.com/")
elem = driver.find_element(By.CSS_SELECTOR, "#search_search")
elem.send_keys("cat")
elem.send_keys(Keys.RETURN)

def crawlImage():
    images = driver.find_elements(By.CSS_SELECTOR, "#Main > section:nth-child(1) > div.grid.gutter-bottom > div > div > div > div.photo-tile > button")
    for image in images:
        try:
            image.click()
            print(image)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "#CloseModal").click()
        except:
            pass


def crawlTags():
    tags = driver.find_elements(By.CSS_SELECTOR, "#Main > section:nth-child(1) > div.grid.gutter-bottom > div > div:nth-child(1) > div > div.photo-tile > a")
    #Main > section:nth-child(1) > div.grid.gutter-bottom > div > div:nth-child(1) > div > div.photo-tile > a
    #Main > section:nth-child(1) > div.grid.gutter-bottom > div > div:nth-child(2) > div > div.photo-tile > a

    for tag in tags:
        tag.click()
        print(tag)
        print(driver.find_elements(By.CSS_SELECTOR,"#Main > section:nth-child(1) > div > div > div > div.photo__details > p:nth-child(5) > a"))


def changeName(path):
    count = 1
    filenames = [filename for filename in os.listdir(path) if filename.endswith("jpg")]
    for filename in filenames:
        print(filename)
        print(path+filename)
        os.rename(path+filename, path+ str(count)+ ".jpg")
        count += 1

#changeName("C:\\Users\\SSAFY\\Downloads\\")
#HOME/Downloads
#crawlTags()
crawlImage()
driver.close()