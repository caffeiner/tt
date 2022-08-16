#! /usr/local/bin/python3
import os
import time
from urllib.parse import urlparse

import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# for use pyinstaller, you need to add in crawling.spec file, hidden imports >> 'selenium','selenium.webdriver.common.by','selenium.webdriver.common.keys'
chrome_options = Options()
chrome_options.add_argument('--headless')  # 크롬창을 켜지 않고 백그라운드에서 크롤링
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(chrome_options=chrome_options)
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
    images = driver.find_elements(By.CSS_SELECTOR,
                                  "#Main > section:nth-child(1) > div.grid.gutter-bottom > div > div > div > div.photo-tile > button")

    sql = "INSERT INTO picture (filepath, tag, publicFlag, isPicture, id) VALUES (%s, %s, %s, %s, %s)"
    file_name_list = []
    # root = "./img/"
    saveRoot = "/var/www/html/crawling/img/"
    root = "/var/www/html/S07P12A707/BackEnd/src/main/resources/static/img/"

    for image in images:
        url = image.get_attribute('data-modal-image-url')
        print('url: ' + url)
        parsed_file = urlparse(url)
        file_name = saveRoot + os.path.basename(parsed_file.path)
        file = requests.get(url)
        file_name_list.append(file_name)
        open(file_name, 'wb').write(file.content)

    length = len(images)
    for i in range(len(images)):
        imageClick = driver.find_element(By.CSS_SELECTOR,
                                         "#Main > section:nth-child(1) > div.grid.gutter-bottom > div > div:nth-child(" + str(
                                             i + 1) + ") > div > div.photo-tile > a > div > img")

        file_name = file_name_list[i]
        print('file_name: ' + file_name)
        imageClick.click()

        # crawlTags
        tags = driver.find_elements(By.CLASS_NAME, "nowrap")
        tagSql = ""
        for tag in tags:
            tagSql += tag.get_attribute('innerText') + ", "
        tagSql = tagSql[:-2]  # 맨 마지막 콤마 제거
        time.sleep(2)
        driver.back()  # 뒤로가기

        cur = conn.cursor()
        cur.execute(sql, (file_name, tagSql, 1, 1, 'manager'))
        print(str(i + 1) + "/" + str(length) + " End of One Cycle & Execute")
    conn.commit()


crawlImage()
driver.close()
