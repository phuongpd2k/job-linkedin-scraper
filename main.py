import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
print('Finish import')
options = Options()
options.add_argument('--headless')
driver=webdriver.Chrome(options=options)
def login():
    with open('login.txt') as f:
        lines=f.readlines()
    loginUrl = 'https://www.linkedin.com/login'
    driver.get(loginUrl)
    sleep(1)
    txtEmail = driver.find_element(By.ID,"username")
    txtEmail.send_keys(lines[0])
    txtPassword = driver.find_element(By.ID,"password")
    txtPassword.send_keys(lines[1])
    txtPassword.send_keys(Keys.RETURN)
    print('Login sucessful')
    sleep(1)
def getJobCard():
    allCards = driver.find_elements(By.CLASS_NAME,'job-card-container--clickable')
    listData=[]
    for card in allCards:
        jobTitle = card.find_element(By.CLASS_NAME,'job-card-list__title')
        companyName = card.find_element(By.CLASS_NAME,'job-card-container__company-name')
        locationDiv = card.find_element(By.CLASS_NAME,'job-card-container__metadata-wrapper')
        location= locationDiv.find_element(By.TAG_NAME,'li')
        dateTime = card.find_element(By.TAG_NAME,'time')
        linkCard = card.find_element(By.TAG_NAME,'a')
        listData.append([jobTitle.text,companyName.text,location.text,dateTime.get_attribute('datetime'),linkCard.get_attribute('href')])
    return listData
def getDetail(jobLink):
    listData=[]
    try:
        driver.get(jobLink)
        sleep(2.5)
        btnSeeAll = driver.find_element(By.PARTIAL_LINK_TEXT,'See all jobs')
        checkExist = len(btnSeeAll.text)
        if(checkExist>0):
            eleSeeAll = btnSeeAll.get_attribute('href')
            driver.get(eleSeeAll)
            sleep(1)
            listData.extend(getJobCard()) 
            masterPage = driver.find_element(By.CLASS_NAME,'artdeco-pagination__pages--number')
            allPages = masterPage.find_elements(By.TAG_NAME,'li')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.5)
            for index,page in enumerate(allPages):
                if(index==0): 
                    page.click()
                    continue
                if(index>0):
                    masterPage1 = driver.find_element(By.CLASS_NAME,'artdeco-pagination__pages')
                    allPages1 = masterPage1.find_elements(By.TAG_NAME,'li')
                    page = allPages1[index]
                page.click()
                sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                listData.extend(getJobCard())
                sleep(1)
            print("Inserted: "+str(len(listData))+"rows")    
            return listData        
    except:
        print("Inserted: "+str(len(listData))+"rows")    
        return listData
login()
with open('jobLink.txt') as f:
        jobLinks=f.readlines()
listDataFinal=[]
for link in jobLinks:
    print('Crawl this: '+link)
    listDataFinal.extend(getDetail(link))
with open('output.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    headers=['Title','Company Name','Location','Date','URL']
    writer.writerow(headers)
    writer.writerows(listDataFinal)
driver.quit()