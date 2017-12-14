from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
import string

browser = webdriver.Firefox()  
#browser.get('https://www.walmart.com/store/444/springfield-mo/search?query=744476384164')  
#browser.get('https://www.walmart.com/store/4381/branson-mo/search?query=848061038828')
browser.get('https://www.walmart.com/store/1009/republic-mo/search?query=848061038828')
html_source = browser.page_source  
browser.quit()

soup=BeautifulSoup(html_source,'html.parser')

comment1 = soup.findAll('div',{'class':'stockStatus'})
comment2 = soup.findAll('div',{'class':'Price-block'})
Dollars = soup.findAll('span', attrs={'class':'Price-characteristic'})
Cents = soup.findAll('span', attrs={'class':'Price-mantissa'})

#comments = soup.findAll("Out")
#print (comment1)
#print ()
#print (Dollars)
#print ()


for item in soup.findAll('div',{'class':'stockStatus'}):
	print (item.string)

for item in soup.findAll('span', attrs={'class':'Price-characteristic'}):
	Dollars = item.string
	
for item in soup.findAll('span', attrs={'class':'Price-mantissa'}):
	Cents = item.string

#Check for nulls

Cost = Dollars + "." + Cents
print (Cost)

