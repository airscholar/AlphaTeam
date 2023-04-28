import bs4
import requests


def scrape(url):
    """
    :Function: Scrape the addresses from the FBI website
    :param url: the URL of the website
    :type url: str
    :return: None
    """
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    soup.find_all('ul')

    fbi_addresses = []
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            # scraping addresses that are 30+ characters long and have no spaces
            if len(li.text) > 30 and ' ' not in li.text:
                fbi_addresses.append(li.text)

    # write to file
    with open('../datasets/FBI_BTC_wallets.csv', 'w') as f:
        for address in fbi_addresses:
            f.write(address + '\n')


url = 'https://www.fbi.gov/news/press-releases/fbi-confirms-lazarus-group-cyber-actors-responsible-for-harmonys-horizon-bridge-currency-theft'

# uncomment to run
# scrape(url)
