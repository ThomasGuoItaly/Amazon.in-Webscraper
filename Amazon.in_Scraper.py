# import dateutil.utils
import requests
from bs4 import BeautifulSoup
# import pandas as pd
import csv
from lxml import html
from datetime import *
import time
# from dateutil import relativedelta

dat= date.today()
with open('AmazonCrawler_'+str(dat)+'.csv','a',newline='',encoding='UTF-8') as fp:
    writer=csv.writer(fp)
    writer.writerow(['PageNumber','Record_no','Website','ProductName','ProductDescription','ProductUrl'])


headers = {
    'accpet':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language':'en-US,en;q=0.9'
}
recordno = 0
for x in range(1,11):
    try:
        url = f'https://www.amazon.in/s?k=mobile&i=electronics&rh=n%3A1389401031&page={x}&qid=1629409220&ref=sr_pg_2'
        time.sleep(5)
        source = requests.get(url,headers=headers,timeout=30)
        soup = html.fromstring(source.text)
        try:
            article = soup.xpath('//div[@class="s-expand-height s-include-content-margin s-latency-cf-section s-border-bottom"]')
        except:
            article=''
        for i, item in enumerate(article):
            global description
            recordno = recordno + 1
            print('Pagenumber :{}'.format(x))
            print('ItemScraped :{}'.format(recordno))
            try:
                name = item.xpath(".//div[@class='a-section a-spacing-none']//h2//a/span//text()")[0].strip()
            except:
                name= ''
            print(name)
            try:
                producturl = item.xpath(".//div[@class='a-section a-spacing-none']//h2//a//@href")[0]
                finalurl= f'https://www.amazon.in{producturl}'
                print(finalurl)
                source2 = requests.get(finalurl, headers=headers, timeout=30)
                soup2 = html.fromstring(source2.text)
                try:
                    article2 =soup2.xpath('//div[@id="productDescription_feature_div"]')
                except:
                    article2=''
                for item2 in article2:
                    try:
                        description=item2.xpath(".//div[@id='productDescription']//p//text()")[0].strip()
                    except:
                        description= ''
                    print(description)
                    print()
            except:
                finalurl= ''

            with open('AmazonCrawler_'+str(dat)+'.csv','a',newline='',encoding='UTF-8') as fp:
                writer=csv.writer(fp)
                writer.writerow([x,recordno,'https://www.amazon.in/',name,description,finalurl])
    except Exception as e:
        with open('AmazonCrawler_Error'+str(dat)+'.csv','a',newline='',encoding='UTF-8') as fp:
            writer=csv.writer(fp)
            writer.writerow([url,str(e)])

print('TaskComplete')