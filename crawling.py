#! /usr/local/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import pymysql
import glob
from selenium.webdriver.chrome.options import Options

#for use pyinstaller, you need to add in crawling.spec file, hidden imports >> 'selenium','selenium.webdriver.common.by','selenium.webdriver.common.keys'
chrome_options = Options()
chrome_options.add_argument('--headless') #크롬창을 켜지 않고 백그라운드에서 크롤링
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome("/var/www/html/crawling/chromedriver", chrome_options=chrome_options)
driver.get("https://burst.shopify.com/")
elem = driver.find_element(By.CSS_SELECTOR, "#search_search")
elem.send_keys("cat")
elem.send_keys(Keys.RETURN)

'''     picture table column
`pictureIdx` int NOT NULL AUTO_INCREMENT,
`filepath` varchar(100) NOT NULL,
`tag` varchar(50) NOT NULL,
`publicFlag` tinyint(1) DEFAULT '1',
`isPicture` tinyint(1) DEFAULT '1',         #사진인지 동영상인지, 1이면 사진
`id` varchar(30) DEFAULT NULL,
`updateTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP'''

conn = pymysql.connect(host='i7a707.p.ssafy.io',
                       port=9888,
                       user='root',
                       password='a707!1402',
                       db='miru',
                       charset='utf8')

def crawlImage():
    images = driver.find_elements(By.CSS_SELECTOR, "#Main > section:nth-child(1) > div.grid.gutter-bottom > div > div > div > div.photo-tile > button")

    print("다운로드 할 사진 갯수")
    print(len(images))
    for i in range(len(images)):
        try:
            images[i].click()
            print(images[i])
            driver.find_element(By.CSS_SELECTOR, "#CloseModal").click()
        except:
            pass
        imageClick = driver.find_element(By.CSS_SELECTOR,
                                          "#Main > section:nth-child(1) > div.grid.gutter-bottom > div > div:nth-child("+str(i+1)+") > div > div.photo-tile > a > div > img")
        imageClick.click()

        #crawlTags
        tags = driver.find_elements(By.CLASS_NAME, "nowrap")
        tagSql = ""
        for tag in tags:
            tagSql += tag.get_attribute('innerHTML') +","
        tagSql = tagSql[:-1] #맨 마지막 콤마 제거
        print("---------tagSql---------")
        print(tagSql)
        driver.back() #뒤로가기

        list_of_files = glob.glob('//var/www/html/crawling/img/*')
        print("현재 폴더 내에 있는 파일들 중에")
        print(list_of_files)
        latest_file = max(list_of_files, key=os.path.getctime)
        print("방금 다운로드 받은 파일 경로")
        print(latest_file)

        #insert into user (id, password, email, recommendFlag, salt) values ('manager','a707!1402','kmj9247@naver.com', 1, 'salt');
        #insert into picture (filepath, tag, isPicture, id) values ('/test/path/filename.jpg','cat,animal',1,'manager');

        sql = "INSERT INTO picture (filepath, tag, isPicture, id) VALUES (%s, %s, %s, %s)"

        cur = conn.cursor()
        cur.execute(sql, (latest_file, tagSql, 1, 'manager'))
        print("execute 끝, 한사이클 끝")
    conn.commit()

crawlImage()
driver.close()