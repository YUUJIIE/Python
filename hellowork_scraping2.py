#Selenium、ChromeDriver、Pandas、BeautifulSoupのインストールが必要
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.hellowork.mhlw.go.jp/index.html' #ハローワークインターネットサービスのURL

#GoogleChromeのバージョンに合ったChromeDriverをダウンロードしてください
DRIVER_PATH = 'chromedriver.exe' #ChromeDriverのファイルパスを記述してください
driver = webdriver.Chrome(executable_path = DRIVER_PATH)
driver.get(url)
time.sleep(3)

#「求人情報検索」をクリック
driver.find_element_by_class_name('retrieval_icn').click()
time.sleep(3)

#「東京都」を選択
element = driver.find_element_by_id('ID_tDFK1CmbBox')
Select(element).select_by_value('13')
time.sleep(3)

#市区町村の選択ボタンをクリック
driver.find_element_by_id("ID_Btn").click()
time.sleep(3)

#「千代田区」を選択
element = driver.find_element_by_id("ID_rank1CodeMulti")
Select(element).select_by_value("13101")
time.sleep(3)

driver.find_element_by_id("ID_ok").click()
time.sleep(3)

#検索ワードに「在宅勤務」を入力
element = driver.find_element_by_id('ID_freeWordInput')
element.clear()
element.send_keys('在宅勤務')
time.sleep(3)

#検索ボタンを押す
element = driver.find_element_by_id('ID_searchBtn').click()
time.sleep(3)

#BeautifulSoupでページ情報を取得
soup = BeautifulSoup(driver.page_source, 'html.parser')

#「kyujin」テーブルの情報を取得
jobs = soup.find_all('table', class_='kyujin')

#「職種」、「会社名」、「就業場所」、「仕事内容」、「求人票URL」の情報を取得し、配列に格納する
job_name_list = []
company_list = []
location_list = []
work_list = []
job_posting_list = []
job_posting_url = 'https://www.hellowork.mhlw.go.jp/kensaku'

for i, job in enumerate(jobs):
    job_name = job.find('td', class_='m13').text.strip()
    job_name_list.append(job_name)
    
    company = job.find_all('tr', class_='border_new')[1].text[7:-2]
    company_list.append(company)
    
    location = job.find_all('tr', class_='border_new')[2].text[7:-2]
    location_list.append(location)
    
    work = job.find_all('tr', class_='border_new')[3].text[8:-2]
    work_list.append(work)  
    
    job_posting = job.find('a', id='ID_kyujinhyoBtn').get('href')
    job_posting = job_posting_url + job_posting[1:]
    job_posting_list.append(job_posting)

#検索結果のページ数を取得
page_num = soup.find_all('li')

#ページ番号を取得
page_num_list = []

for i in page_num:
    page_num_list.append(str(i)[30])

page_number = int(max(page_num_list[-2]))

#検索結果が31件以上だったとき、次ページに遷移して情報を取得する
if page_number != 1:
    for i in range(2, page_number+1):
        element = driver.find_element_by_name('fwListNaviBtn' + str(i)).click()
        time.sleep(3)
        for i, job in enumerate(jobs):
            job_name = job.find('td', class_='m13').text.strip()
            job_name_list.append(job_name)
            company = job.find_all('tr', class_='border_new')[1].text[7:-2]
            company_list.append(company)
    
            location = job.find_all('tr', class_='border_new')[2].text[7:-2]
            location_list.append(location)
    
            work = job.find_all('tr', class_='border_new')[3].text[8:-2]
            work_list.append(work)
            
            job_posting = job.find('a', id='ID_kyujinhyoBtn').get('href')
            job_posting = job_posting_url + job_posting[1:]
            job_posting_list.append(job_posting)

#取得した情報をデータフレームにまとめる
result = {
    '職種': job_name_list,
    '事業所名': company_list,
    '就業場所': location_list,
    '仕事の内容': work_list,
    '求人票URL': kyujinhyo_list
    }

df = pd.DataFrame(result)

#データフレームをCSVファイルに保存する
df.to_csv('hellowork.csv', index = False, encoding='utf_8_sig')

#ブラウザを閉じる
driver.close()

#検索結果が7ページ以上あるときは対応出来てません。
#参考サイト：https://www.geek.sc/archives/2975