import requests
import bs4

lst = []
url = 'https://www.fbi.gov/news/press-releases/fbi-confirms-lazarus-group-cyber-actors-responsible-for-harmonys-horizon-bridge-currency-theft'
res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
soup.find_all('ul')

fbi_addresses = []
for ul in soup.find_all('ul'):
    for li in ul.find_all('li'):
        if li.text != '' and (li.text.startswith('bc') or li.text.startswith('0x')):
            fbi_addresses.append(li.text)

#write to file
with open('FBI_BTC_wallets.csv', 'w') as f:
    for address in fbi_addresses:
        f.write(address + '\n')