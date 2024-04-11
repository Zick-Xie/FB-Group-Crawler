url=input("請輸入社團連結")
userat=input("請輸入臉書帳號")
userpw=input("請輸入臉書密碼")

import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd 

options = FFOptions()
driver = webdriver.Firefox(options=options)

driver.get("https://www.facebook.com/")
time.sleep(1)

usernameInput=driver.find_element(By.ID, "email")
passwordInput=driver.find_element(By.ID, "pass")

usernameInput.send_keys(userat)
time.sleep(0.5)
passwordInput.send_keys(userpw) 
time.sleep(1)

signinBtn=driver.find_element(By.CSS_SELECTOR, "[data-testid=royal_login_button]")
signinBtn.send_keys(Keys.ENTER)
time.sleep(2)

# clubifo

driver.get((url))
soup = BeautifulSoup(driver.page_source, 'html.parser')        
cbnfind = soup.find_all('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv x1xlr1w8')
cbflist = []
for i in cbnfind:
    cbflist.append(i.text)

clubname=cbflist[0]
clubID=url.split("groups/")[1]

soup = BeautifulSoup(driver.page_source, 'html.parser')        
cbmNfind = soup.find_all('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xi81zsa x1s688f')
cbmNlist = []
for i in cbmNfind:
    cbmNlist.append(i.text)
cbmN=cbmNlist[0][:-4]

# main
cleaned_links=[]
target=0
while target != clubname:
    post_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/posts/']")
    for i in post_links:
        href = i.get_attribute("href")
        cleaned_href = href.split("?", 1)[0]
        cleaned_links.append(cleaned_href)
    y = driver.execute_script("return window.scrollY")
    driver.execute_script(f"window.scrollTo(0, {y+300})")
    dt = driver.find_elements(By.CSS_SELECTOR, "span.x4k7w5x > a")
    for i in dt:
        try:
            ActionChains(driver).move_to_element(i).perform()
        except:
            pass
    soup = BeautifulSoup(driver.page_source, 'html.parser')         
    scctfind = soup.find_all('h3', class_='x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz x1gslohp x1yc453h')
    scct = []
    for i in scctfind:
        scct.append(i.text)
    # postN=len(scct)
    lastone=scct[-1]
    xtn=len(lastone)-3-(len(clubname))
    target=lastone[xtn:-3]


# link

post_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/posts/']")
for i in post_links:
    href = i.get_attribute("href")
    cleaned_href = href.split("?", 1)[0]
    cleaned_links.append(cleaned_href)

distinct_links = []
for x in cleaned_links:
    if x in distinct_links:
        continue
    else:
        distinct_links.append(x)

TOtalPostURL=[]
for b in distinct_links:
    TOtalPostURL.append(b)
Changelist=[]
clubIDN=len(clubID)+20
for i in range(len(TOtalPostURL)):
    if TOtalPostURL[i].split("//www.")[1][:clubIDN] != f"facebook.com/groups/{clubID}":
        TOtalPostURL[i]="ErVurl"
        Changelist.append(str(i))
ErvToBeRemoved1="ErVurl"
try:
    while True:
        TOtalPostURL.remove(ErvToBeRemoved1)
except ValueError:
    pass

dict = {"Post URL": TOtalPostURL
       }

allresult = pd.DataFrame(dict)
csvname=f"{clubname}url.csv"
allresult.to_csv(csvname)
