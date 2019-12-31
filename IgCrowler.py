from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import re
import pandas as pd

# %% Initialize driver and enter info
url = 'https://www.instagram.com/accounts/login/'
email = "jcratebo703@gmail.com"
psd = "psd123678"

driverPath = "/Users/caichengyun/PycharmProjects/NOSQL-FinalProject_NLP/geckodriver"
driver = webdriver.Firefox(executable_path=driverPath)
driver.maximize_window()
driver.get(url)

driver.implicitly_wait(20)

driver.find_element_by_xpath("//div[@class='-MzZI'][1]/div[@class='_9GP1n   ']/label[@class='f0n8F ']/input["
                             "@class='_2hvTZ pexuQ zyHYP']").send_keys(email)
driver.find_element_by_xpath("//div[@class='-MzZI'][2]/div[@class='_9GP1n   ']/label[@class='f0n8F ']/input["
                             "@class='_2hvTZ pexuQ zyHYP']").send_keys(psd)
driver.find_element_by_xpath("//button[@class='sqdOP  L3NKy   y3zKF     ']").click()

# %%
driver.get("https://www.instagram.com/tsai_ingwen/?hl=zh-tw")
driver.implicitly_wait(20)
Urls = []
postUrl = []

for i in range(0, 5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)

    page_1_source = driver.page_source
    soup = BeautifulSoup(page_1_source, "html.parser")

    for link in soup.find_all('a'):
        Urls.append(link.get('href'))

regex = re.compile(r'^/p/')
postUrl = list(filter(regex.search, Urls))
uniqueUrls = list(set(postUrl))
# print(uniqueUrls)

fullPostUrls = []

for i in range(len(uniqueUrls)):
    fullPostUrls.append("https://www.instagram.com" + uniqueUrls[i])

print(fullPostUrls)

# %% First Layer
firstLayerPosts = pd.DataFrame(columns=("PostUrl", "Poster", "Date", "Time", "Post", "Tag", "TagPeople"))
firstLayerAllTags = []

for i in range(len(fullPostUrls)):
    driver.get(fullPostUrls[i])
    tagPeople = []
    sleep(1)
    postSource = driver.page_source
    soup = BeautifulSoup(postSource, "html.parser")
    for link in soup.find_all('a', class_="JYWcJ"):
        # print(link.get('href'))
        tagPeople.append(link.get('href'))
        tagPeople = [i.strip('/') for i in tagPeople]

    if not tagPeople:
        continue

    print(tagPeople)
    firstLayerAllTags = firstLayerAllTags + tagPeople

    oneUrl = fullPostUrls[i]

    for x in soup.find_all('a', class_="nJAzx"):
        onePoster = x.get('title')

    for x in soup.find_all('time', class_="FH9sR Nzb55"):
        oneDate = x.get('title')
        oneTime = x.get('datetime')

    for x in soup.find_all('div', class_="C7I1f X7jCj"):
        allSpan = x.find_all('span')
        onePost = allSpan[len(allSpan)-1].text

    firstLayerPosts.loc[-1] = [oneUrl, onePoster, oneDate, oneTime, onePost, len(tagPeople), tagPeople]
    firstLayerPosts.index = firstLayerPosts.index + 1
    firstLayerPosts = firstLayerPosts.sort_index()

pd.set_option('display.max_columns', None)
firstLayerPosts
print(firstLayerAllTags)

# %% Second Layer
tags = list(set(firstLayerAllTags))

for k in range(len(tags)):
    print(tags[k])
    driver.get("https://www.instagram.com/"+tags[k])
    secondUrls = []
    secondPostUrl = []
    for i in range(0, 5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)

        page_1_source = driver.page_source
        soup = BeautifulSoup(page_1_source, "html.parser")

        for link in soup.find_all('a'):
            secondUrls.append(link.get('href'))

    secondPostUrl = list(filter(regex.search, secondUrls))
    secondUniqueUrls = list(set(secondPostUrl))

    secondFullPostUrls = []

    for i in range(len(secondUniqueUrls)):
        secondFullPostUrls.append("https://www.instagram.com" + secondUniqueUrls[i])

    firstLayerAllTags = []

    for i in range(len(secondFullPostUrls)):
        driver.get(secondFullPostUrls[i])
        tagPeople = []
        sleep(1)
        postSource = driver.page_source
        soup = BeautifulSoup(postSource, "html.parser")
        for link in soup.find_all('a', class_="JYWcJ"):
            # print(link.get('href'))
            tagPeople.append(link.get('href'))
            tagPeople = [i.strip('/') for i in tagPeople]

        if not tagPeople:
            continue

        print(tagPeople)
        firstLayerAllTags = firstLayerAllTags + tagPeople

        oneUrl = fullPostUrls[i]

        for x in soup.find_all('a', class_="nJAzx"):
            onePoster = x.get('title')

        for x in soup.find_all('time', class_="FH9sR Nzb55"):
            oneDate = x.get('title')
            oneTime = x.get('datetime')

        for x in soup.find_all('div', class_="C7I1f X7jCj"):
            allSpan = x.find_all('span')
            onePost = allSpan[len(allSpan)-1].text

        firstLayerPosts.loc[-1] = [oneUrl, onePoster, oneDate, oneTime, onePost, len(tagPeople), tagPeople]
        firstLayerPosts.index = firstLayerPosts.index + 1
        firstLayerPosts = firstLayerPosts.sort_index()

firstLayerPosts

#%%
from pymongo import MongoClient

hostname = '52.54.130.90'
port = 27017
username = 'admin'
password = 'admin'
databaseName = 'admin'

client = MongoClient(hostname, port)
db = client[databaseName]
db.authenticate(username, password)

db = client['FinalProject']
mycol = db["20200101"]

records = firstLayerPosts.to_dict('records')
mycol.insert_many(records)
#%%
# driver.get("https://www.instagram.com/p/B6Aw0ltl4Ue/")
# tagPeople = []
# sleep(1)
# postSource = driver.page_source
# soup = BeautifulSoup(postSource, "html.parser")
# for link in soup.find_all('a', class_="JYWcJ"):
#     # print(link.get('href'))
#     tagPeople.append(link.get('href'))
#     tagPeople = [i.strip('/') for i in tagPeople]
#
# print(tagPeople)
#
# for x in soup.find_all('div', class_="C7I1f X7jCj"):
#     allSpan = x.find_all('span')
#     onePost = allSpan[len(allSpan)-1].text
#
# print(onePost)
#
#
