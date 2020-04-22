import requests
from bs4 import BeautifulSoup


url = "https://remoteintech.company/"
html = requests.get(url)
bs = BeautifulSoup(html.text, "lxml")


def get_all_companies_links():
    """ Return a list of the companies url that accept remote jobs """
    companies = bs.select('#companies-table tr')
    links = []

    for item in companies:
        if item.find('td', class_='company-name'):
            links.append(''.join([url[:-1], item.find('td', class_='company-name').find('a').get('href')]))

    return links


def search_for_technology(key_word):
    """ Return companies using the given technology """
    links = get_all_companies_links()
    results = []

    for link in links:
        print('finding on ...', link.split('/')[-2])
        _html = requests.get(link)
        bs = BeautifulSoup(_html.text, "lxml")
        div = bs.find('div', class_='section-companyTechnologies')
        text = div.find('p').text if div and div.find('p') else ''
        if key_word.lower() in text.lower():
            results.append(link)
            print('** technology found! **', '\n')
    
    return results


if __name__ == "__main__":

    tech = input('Type a technology to be found: ')
    result = search_for_technology(tech)
    print('\n', '*** Results ***', '\n')
    print('\n'.join([f'{idx}. {link}' for idx, link in enumerate(result)]))
    print('\n','*** End ***')

    pass