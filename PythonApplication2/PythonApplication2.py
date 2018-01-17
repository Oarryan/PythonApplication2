from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
import string
import gspread
import time
 

from oauth2client.service_account import ServiceAccountCredentials
#use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('C:\client_secret.json',scope)
client = gspread.authorize(creds)

wks = client.open("Spyder Test").get_worksheet(3)

store_list = [sl for sl in wks.col_values(1) if sl]
print (store_list)
moniker_list = [ml for ml in wks.col_values(2) if ml]
print (moniker_list)
wks2=client.open("Spyder Test").get_worksheet(2)
upc_list = [ul for ul in wks2.col_values(1) if ul]
print (upc_list)

row = 80 #Header Row for Store ID - Should be 1 after done experimenting

for upc in upc_list:
        client = gspread.authorize(creds) # Keep Authorizing so Token doesn't expire and throw and exception -- apparently this is NOT enough

#for store in store_list:
    #for moniker in moniker_list:
        #wks2=client.open("Spyder Test").get_worksheet(2)
        #upc_list = [ul for ul in wks2.col_values(1) if ul]
        #print (store_list)
        #print (moniker_list)
        #print (upc_list)
        
        row=row+1
        column = 3 # Start putting data in Column 3 Incrementing in the upc_list loop
       
        #for upc in upc_list:
        for store in store_list:
                browser = webdriver.Firefox() 
                ndex = ((store_list).index(store))
                moniker=(moniker_list[ndex])
                print (moniker)
                url="https://www.walmart.com/store/"+ store + "/" + moniker + "/search?query="+str(upc)
                
                status = "" # Start the status off as a blank -- concatenate all to this. If nothing, should remain blank, right?
                

                Dollars = "No"
                Cents = "Results"   
                #browser.get('https://www.walmart.com/store/444/springfield-mo/search?query=744476384164')  
                #browser.get('https://www.walmart.com/store/4381/branson-mo/search?query=848061038828')
                #browser.get('https://www.walmart.com/store/1009/republic-mo/search?query=848061038828')
                #browser.get('https://www.walmart.com/store/845/buffalo-mo/search?query=027242272903')
                #browser.get('https://www.walmart.com/store/1009/republic-mo/search?query=072179224945')
                page = ''
                while page =='':
                    try:
                        browser.get(url)
                        page = browser.get(url)
                    except:                             #Catches Exceptions like Proxy failures or Connection Refusals
                        print('Connection refused')
                        time.sleep(5)
                        continue
                                    
                html_source = browser.page_source  
                browser.quit()
                soup=BeautifulSoup(html_source,'html.parser')

                #comment1 = soup.findAll('div',{'class':'stockStatus'})
                #comment2 = soup.findAll('div',{'class':'Price-block'})
                #Dollars = soup.findAll('span', attrs={'class':'Price-characteristic'})
                #Cents = soup.findAll('span', attrs={'class':'Price-mantissa'})

                #comments = soup.findAll("Out")
                #print (comment1)
                #print ()
                #print (Dollars)
                #print ()

                # Apparently need to check for Out of Stock / Limited Stock / and whatever "I've never heard of that item is" (nul)

                wks1=client.open("Spyder Test").get_worksheet(1)

                for item in soup.findAll('div', attrs={'class':'stockStatus'}):
	                #print ("stockStatus", item.string)
                    status = status + str(item.string)
                    
                for item in soup.findAll('strong', attrs={'class':'stockStatus-available'}):
                    print("stockStatus-available", item.string)
                    status = status + str(item.string)

                for item in soup.findAll('strong', attrs={'class':'stockStatus-limitedStock'}):
	                #print ("stockStatus-limitedStock" , item.string)
                    status = status + str(item.string)

                for item in soup.findAll('span', attrs={'class':'Price-characteristic'}):
	                Dollars = item.string
	
                for item in soup.findAll('span', attrs={'class':'Price-mantissa'}):
	                Cents = item.string

#Check for nulls

                Cost = Dollars + "." + Cents
                print (url)
                print (Cost)

                wks1.update_cell(row,column,status)
                column=column+1
                wks1.update_cell(row,column,Cost)

                column=column+1

                

