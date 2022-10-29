import requests
from bs4 import BeautifulSoup

PAGES_COUNT = 1

def get_soup(url, **kwargs):
    response = requests.get(url, **kwargs)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features='html.parser')
    else:
        soup = None
    return soup

def crawl_products(page_count):
    urls = []
    fmt = 'https://www.inmyroom.ru/profi/page/{page}'

    for page_n in range(1, 1 + page_count):
        print('page: {}'.format(page_n))

        page_url = fmt.format(page=page_n)
        #print(page_url)
        soup = get_soup(page_url)
        #print(soup)
        if soup is None:
            break

        for tag in soup.find_all("a", class_='user-preview_name'):
            href = tag.get('href')
            urls.append(href)

    return urls


def parse_products(urls):
    data = []
    for url in urls:
        print('\tproduct: {}'.format(url))
        soup = get_soup(url)
        if soup is None:
            break
        name = soup.find("h1", class_='s-UserProfile_b-Header_title').text.strip()
        try:
            city = soup.find("p", class_='s-UserProfile_b-Header_subtitle').text.strip()
            city = city.split('/ ')[1]
        except:
            city = None
        try:
            phone_number = soup.find("a", class_='__withIcon __phone')['data-active-text']
        except:
            phone_number = None
        print(name)
        print(city)
        print(phone_number)

        item = {
            'name': name,
            'city': city,
            'phone_number': phone_number,
        }
        data.append(item)
    return data



def main():
    urls = crawl_products(PAGES_COUNT)
    data = parse_products(urls)



if __name__ == '__main__':
    main()