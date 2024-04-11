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


TOtalPostURL= []
TOtalPostID = []
TOtalauthor = []
TOtalPostcontent = []
TOtalReaction = []
TOtalReactionList = []
TOtalSeenbyN = []
TOtalSeenbyList = []
TOtalCommentN = []
TOtalCommentList = []

cbvne=f"{clubname}.csv"
test=pd.read_csv(cbvne)
TOtalPostURL = test['Post URL'].tolist()


start=0
for p in range(len(TOtalPostURL)-int(start)):
    kp=int(p)+int(start)
    # postID
    postid=TOtalPostURL[kp].split("/posts/")[1].rstrip("/")
    driver.get(TOtalPostURL[kp])
    time.sleep(2)
    TOtalPostID.append(postid)
    
    # Author name
    soup = BeautifulSoup(driver.page_source, 'html.parser')         
    authnornfind = soup.find('h3', class_='x1heor9g x1qlqyl8 x1pd3egz x1a2a7pz x1gslohp x1yc453h')
    TOtalauthor.append(authnornfind.text)
    
    # Postcontent
    try:
        if driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[3]/div[1]") != None:
            postcontent=driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[3]/div[1]").text
    except:
        postcontent="no content"

    picfind=[]
    try:
        if driver.find_elements(By.XPATH, '//img[@class="xz74otr x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3"]')[0] != None:
            picetfind = driver.find_elements(By.XPATH, '//img[@class="xz74otr x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3"]')
            picfind=[]
            picct=0
            for i in picetfind:
                picct+=1
                pngname=f"圖片{picct}:"
                picfind.append(pngname+i.get_attribute("src"))
    except:
        pass

    try:
        if driver.find_element(By.XPATH, '//img[@class="x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r"]') != None:
            picetfind = driver.find_element(By.XPATH, '//img[@class="x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r"]')
            picfind=[]
            pngname="圖片:"
            picfind.append(pngname+picetfind.get_attribute("src"))  
    except:
        pass

    try:
        if driver.find_element(By.XPATH, '//video[@class="x1lliihq x5yr21d xh8yej3"]') != None:
            picetfind = driver.find_element(By.XPATH, '//video[@class="x1lliihq x5yr21d xh8yej3"]')
            picfind=[]
            pngname="影片:"
            picfind.append(pngname+picetfind.get_attribute("src"))  
    except:
        pass

    if picfind != []:
        picfind2="\n".join(map(str, picfind))
    else:
        picfind2="no pictures or video"
    
    mixedcontent=postcontent+"\n"+picfind2
    TOtalPostcontent.append(mixedcontent)
    
    # Seen 
    soup = BeautifulSoup(driver.page_source, 'html.parser')        
    seen = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa')
    slist = []
    for i in seen:
        slist.append(i.text)
    
    try:
        if slist[0][-8:]=="回應了這張相片。":
                slist.pop(0)
    except:
        pass

    if slist!=[]:
        if len(slist) != 1:
            commentN=(slist[0]).rstrip("則留言")
        else:
            commentN="no comment"

        if len(slist) != 1 and slist[1]=="所有人都已看過":
            seenN=str(int(cbmN)-2)
        elif len(slist) == 1 and slist[0]=="所有人都已看過":
            seenN=str(int(cbmN)-2)
        elif len(slist) != 1 :
            seenN=str(int((slist[1]).rstrip("人已看過"))-1)
        else:    
            seenN=str(int((slist[0]).rstrip("人已看過"))-1)
    else:
        commentN="no comment"
        seenN="此貼文未顯示看過人數"

    driver.find_element(By.XPATH, '//span[contains(text(),"已看過")]').click()
    time.sleep(1)
    ct=0
    while ct < int(seenN):
        pane = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')  
        sbname = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')
        ct=int(len(sbname))

    sbnamelist = []
    for i in sbname:
        sbnamelist.append(i.text)

    sbclose=driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/i").click()
    seebylistjoint = "、".join(map(str, sbnamelist))

    TOtalSeenbyN.append(seenN)
    TOtalCommentN.append(commentN)
    TOtalSeenbyList.append(seebylistjoint)
    
    # reaction
    idt=0
    try:
        while driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span")[0] != None:
            driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span")[0].click()
            idt=1
            time.sleep(0.5)
    except :
        pass
    
    try:
        while driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[5]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span")[0] != None:
            driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[5]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span")[0].click()
            idt=1
            time.sleep(0.3)
    except :
        pass


    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')        
    rtlist = soup.find_all('div', class_='x1i10hfl xe8uvvx xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct xjbqb8w x18o3ruo x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g x1ypdohk xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg x1vjfegm x3nfvp2 xrbpyxo xng8ra x16dsc37')
    rt = "".join(map(str, rtlist))
    rt = rt.split("aria-label=")
    rt.pop(0)

    rt2=[]
    for i in range(len(rt)):
        rt[i]=(rt[i].split("aria-selected="))[0]
        rt2.append(rt[i])

    if idt != 0:
        rtresult=rt2
    else:
        rtresult="no reaction"

    rtnamelist = []

    if rtresult !="no reaction" and len(rtresult) > 1 :    
        for i in range((len(rtresult))-1):
            rtag=f'//div[@aria-label={rtresult[i+1]}]'
            driver.find_element(By.XPATH, rtag).click()
            time.sleep(3)
            rtct=0
            rtype=rtresult[i+1].split(",")[0][1:]
            rtnbr=(rtresult[i+1].split(" "))[1][:-1]
            rtttyp=f"按{rtype}的有{rtnbr}人:"
            rtnamelist.append(rtttyp)
            time.sleep(0.8)
            soup = BeautifulSoup(driver.page_source, 'html.parser')  
            rtname = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')
            rtct=int(len(rtname))
            for j in rtname:
                rtnamelist.append(j.text+"、")
    elif rtresult !="no reaction" and len(rtresult) == 1:
        rtag=f'//div[@aria-label={rtresult[0]}]'
        driver.find_element(By.XPATH, rtag).click()
        time.sleep(3)
        rtct=0
        rtype=rtresult[0].split(",")[0][1:]
        rtnbr=(rtresult[0].split(" "))[1][:-1]
        rtttyp=f"按{rtype}的有{rtnbr}人:"
        rtnamelist.append(rtttyp)
        time.sleep(0.8)
        soup = BeautifulSoup(driver.page_source, 'html.parser')  
        rtname = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')
        rtct=int(len(rtname))
        for j in rtname:
            rtnamelist.append(j.text+"、")
    else:
        rtnamelist.append("no reaction")

    time.sleep(1)
    try:
        while driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div")[0] != None:
            driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div")[0].click()
            time.sleep(0.3)
    except :
        pass

    rtrt2= "".join(map(str, rtresult))
    if rtrt2 !="no reaction":
        rtresult2=f"這篇貼文的互動：{rtrt2}"
    else:
        rtresult2="no reaction"

    if rtnamelist[0] !="no reaction":
        rtnamelist2=" ".join(map(str, rtnamelist))
    else:
        rtnamelist2="no reaction"
    
    TOtalReaction.append(rtresult2)
    TOtalReactionList.append(rtnamelist2)

    # TOtalReaction.append("系統錯誤,暫時無法獲得此資訊")
    # TOtalReactionList.append("系統錯誤,暫時無法獲得此資訊")

    if commentN != "no comment":
        try:
            cmt1=driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[4]/div/div/div[2]/div[2]/div/div/span").click()
            time.sleep(0.8)
            cmt2=driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/span").click()
            time.sleep(0.8)
        except:
            pass
        
        y = driver.execute_script("return window.scrollY")
        driver.execute_script(f"window.scrollTo(0, {y + 600})")
        time.sleep(0.8)
        
        # 點擊查看更多貼文
        try:
            while driver.find_elements(By.XPATH, '//span[contains(text(),"查看更多留言")]')[0] != None:
                driver.find_elements(By.XPATH, '//span[contains(text(),"查看更多留言")]')[0].click()
                y = driver.execute_script("return window.scrollY")
                driver.execute_script(f"window.scrollTo(0, {y + 600})")
                time.sleep(1)
        except :
            pass
        
        try:
            while driver.find_elements(By.XPATH, '//span[contains(text(),"檢視")]')[0] != None:
                driver.find_elements(By.XPATH, '//span[contains(text(),"檢視")]')[0].click()
                y = driver.execute_script("return window.scrollY")
                driver.execute_script(f"window.scrollTo(0, {y + 600})")
                time.sleep(1)
        except :
            pass

                
        try:
            while driver.find_elements(By.XPATH, '//span[contains(text(),"查看另")]')[0] != None:
                driver.find_elements(By.XPATH, '//span[contains(text(),"查看另")]')[0].click()
                y = driver.execute_script("return window.scrollY")
                driver.execute_script(f"window.scrollTo(0, {y + 600})")
                time.sleep(1)
        except :
            pass
        
        # 點開回覆
        try:
            while driver.find_elements(By.XPATH, '//div[contains(text(),"已回覆")]')[0] != None:
                driver.find_elements(By.XPATH, '//div[contains(text(),"已回覆")]')[0].click()
                time.sleep(0.3)
        except :
            pass

        # 點開所有留言(查看更多)
        try:
            while driver.find_elements(By.XPATH, '//div[contains(text(),"查看更多")]')[0] != None:
                driver.find_elements(By.XPATH, '//div[contains(text(),"查看更多")]')[0].click()
                time.sleep(0.3)
        except :
            pass
        
        # 抓取留言
        soup = BeautifulSoup(driver.page_source, 'html.parser')        

        # 抓取留言者姓名
        allcmtname = soup.find_all('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv')
        allcmtnamelist = []
        for i in allcmtname:
            allcmtnamelist.append(i.text)
        allcmtnamelist.pop(0)

        # 處理重複留言者的姓名
        counts={}
        for index, key in enumerate(allcmtnamelist):
            if key in counts:
                counts[key]+=1
                allcmtnamelist[index]=f"{key}_.{counts[key]}"
            else:
                counts[key]=0

        # 抓取留言本體
        allcmtct = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u')
        allcmtctlist = []
        for i in allcmtct:
            allcmtctlist.append(i.text)


        # 處理其他值
        valueToBeRemoved="Facebook"
        try:
            while True:
                allcmtctlist.remove(valueToBeRemoved)
        except ValueError:
            pass
    else:
        allcmtctlist="no comment"
        allcmtnamelist="no comment"

    commentjointlist=[]
    if commentN != "no comment":
        try:
            for i in range(int(commentN)):
                commentjointlist.append(allcmtnamelist[i]+":"+allcmtctlist[i])
            commentjoint = "\n".join(map(str, commentjointlist))
        except:
            commentjoint="留言中含有純圖片的回覆"
    else:
        commentjoint="no comment"

    TOtalCommentList.append(commentjoint)
    time.sleep(2)

dict = {"PostID": TOtalPostID, 
        "author": TOtalauthor, 
        "Post content": TOtalPostcontent, 
        "Reaction": TOtalReaction,   
        "Reaction List": TOtalReactionList, 
        "SeenbyN": TOtalSeenbyN,
        "Seenby List": TOtalSeenbyList, 
        "CommentN": TOtalCommentN,
        "Comment List": TOtalCommentList,
        "Post URL": TOtalPostURL
       }

allresult = pd.DataFrame(dict)
csvname=f"{clubname}.csv"
allresult.to_csv(csvname)

driver.close()
