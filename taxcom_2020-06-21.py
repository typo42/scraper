import time
import re
import csv
# import unicodecsv as csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

options = Options()

DRIVER_PATH = '/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://taxcom.ru/proverka-kontragentov/search/?query=%D1%81%D1%82%D1%80%D0%BE%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D1%81%D1%82%D0%B2%D0%BE+%D1%80%D0%B5%D0%BA%D0%BE%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F+%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B9+%D0%B8+%D1%81%D0%BE%D0%BE%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9")

companies = {}

links = []

emails = []

total = 0

n = 0

def scrape_page(q):
    time.sleep(2)

    boxes = driver.find_elements_by_class_name('bl')

    print('\n')

    x = 1
    for box in boxes:

        company_details = {'Название':'unknown','ИНН':'unknown', 'КПП':'unknown'}

        title_element = driver.find_element_by_xpath(f'//*[@id="content"]/div/div/section[2]/div/div[2]/div[1]/div/div[{x}]/a')

        driver.execute_script("arguments[0].scrollIntoView()", title_element)
        title = title_element.text
        company_details['Название'] = title

        INN_element = driver.find_element_by_xpath(f'//*[@id="content"]/div/div/section[2]/div/div[2]/div[1]/div/div[{x}]/div[2]/div[1]')
        INN = INN_element.text
        INN = re.findall('\d+', INN)
        INN = INN.pop()
        company_details['ИНН'] = INN

        KPP_element = driver.find_element_by_xpath(f'//*[@id="content"]/div/div/section[2]/div/div[2]/div[1]/div/div[{x}]/div[2]/div[2]')
        KPP = KPP_element.text
        KPP = re.findall('\d+', KPP)
        KPP = KPP.pop()
        company_details['КПП'] = KPP

        link = 'https://sbis.ru/contragents/' + str(INN) + '/' + str(KPP)
        links.append(link)

        n = len(boxes) * q + x - 10
        company = {n:company_details}
        companies.update(company)

        [print(key, value) for key, value in company.items()]
        x += 1


    next = driver.find_element_by_xpath('//*[@id="content"]/div/div/section[2]/div/div[3]/div/div/ul/li[6]/a')
    next.click()
    del next


a = list(range(5))
q = 0
for item in a:
    q += 1
    scrape_page(q)

with open('taxcom.csv', 'w') as output:
    writer = csv.writer(output, delimiter='\t')
    n = 1
    for value in companies.values():
        a = list(value.values())
        row = [n, a]
        writer.writerow(row)
        n += 1

x = 0
for link in links:
    # print(links[x])
    # print('\n')
    driver.get(links[x])
    try:
        # email_element = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div[2]/div[2]/a')
        email_element = driver.find_element_by_class_name("cCard__Contacts-site-element")
        email = email_element.get_attribute('title')
        emails.append(email)
        # email = email.upper()
        print('\n', email)
    except:
        pass
    x += 1

# print(emails)


# LINK = links[19]

# driver.get(LINK)

# email_element = driver.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div[2]/div[1]/div[3]/div[1]/div[2]/div[2]/div[2]/a')
# email = email_element.get_attribute('title')
# print(email)

# def add_company(title):
#     companies.update('title':'ИНН','КПП','статус','отрасль','регион')

# companies = {}
# # company_INNs = []

# for element in company_elements:
#     driver.execute_script("arguments[0].scrollIntoView()", element)
#     company_title = element.text
#     # company_titles.append(company_title)
#     INN_element = driver.find_element_by_class_name("inn")
#     company_INN = INN_element.text
#     # company_INNs.append(company_INN)
#     KPP_element = driver.find_element_by_class_name("kpp")
#     company_KPP = KPP_element.text
#     companies.update('Название компании':'company_title', 'ИНН':'company_INN', 'КПП':'company_KPP')

# print(companies)




# print(company_titles)
# print(company_INNs)

# driver.execute_script("arguments[0].scrollIntoView()", byRegionsLink)

# time.sleep(1)

# byRegionsLinkMore = driver.find_element_by_name("byRegionsLinkMore")
# byRegionsLinkMore.click()

# time.sleep(1)

# # region = driver.find_element_by_link_text("client-tree-item-108")
# # driver.execute_script("arguments[0].scrollIntoView()", region)

# region = driver.find_element_by_xpath("//form[@name='contragentsRegionListGridView']/data-id='86'")

# driver.execute_script("arguments[0].scrollIntoView()", region)

# print(region)

# time.sleep(1)

# region.click()

# time.sleep(5)

# # driver.quit()

driver.close()
quit()
