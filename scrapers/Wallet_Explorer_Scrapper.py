import time
import requests
from bs4 import BeautifulSoup

#Scrape data from wallet explorer
link = 'https://www.walletexplorer.com/wallet/SilkRoadMarketplace/addresses?page='
nb_page = 3729
file = 'DNM_SR.csv' #file where the addresses will be stored
with open(file, 'w') as f:
    for i in range(1, nb_page+1):
        url = link + str(i)
        time.sleep(1)
        page = requests.get(url)
        while page.status_code != 200:
            print('error: ', i)
            time.sleep(10)
            page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all('a'):
            #only get addresses
            if link.get('href').startswith('/address/'):
                f.write("%s\n" % (link.get('href')[9:]))