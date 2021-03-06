import requests
import csv
from bs4 import BeautifulSoup

res = requests.get('https://www.marketsandmarkets.com/telecom-and-IT-market-research-113.html')
soup = BeautifulSoup(res.text, 'html.parser')
titles = soup.select('.alt')


def custom_table(title):
    ct = []
    for idx, item in enumerate(title):
        ti = str(title[idx].select('h3'))
        a = ti.find('>', 74, 120)
        de = str(title[idx].select('p'))
        b = de.find('>')
        href = str(title[idx].select('a'))
        cs = href.find('=')
        ce = href.find('"', 60, 100)
        date = str(title[idx].select('.displaynone')[0])
        us = de.find('USD')
        ue = de.find('illion', us, us+50)
        vs = de.find('%')
        das = date.find('>')
        ct.append({'Report_Title': ti[a + 1:-10], 'Report_Description': de[b + 1:-5], 'Link': href[cs + 1:ce],
                   'USD_Value': de[us+4:ue+6], '%_Val': de[vs-3:vs+1], 'Date_Published': date[das+1:-5].strip()})
    return ct


q = custom_table(titles)

filename = "web_scrapping.csv"
fields = ['Report_Title', 'Date_Published', 'Link', 'Report_Description', 'USD_Value', '%_Val']
with open(filename, 'w',newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(q)