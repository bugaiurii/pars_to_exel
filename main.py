import json
import xlsxwriter
import requests
from bs4 import BeautifulSoup

PAGES_COUNT = 1
OUT_FILENAME = 'out.json'
OUT_XLSX_FILENAME = 'out.xlsx'


def dump_to_json(filename, data, **kwargs):
    kwargs.setdefault('ensure_ascii', False)
    kwargs.setdefault('indent', 1)

    with open(OUT_FILENAME, 'w') as f:
        json.dump(data, f, **kwargs)


def dump_to_xlsx(filename, data):

    with xlsxwriter.Workbook(filename) as workbook:
        ws = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        headers = [' Имя', 'Город', 'Номер телефона']

        for col, h in enumerate(headers):
            ws.write_string(0, col, h, cell_format=bold)

        for row, item in enumerate(data, start=1):
            ws.write_string(row, 0, item['name'])
            try:
                ws.write_string(row, 1, item['city'])
            except:
                pass
            try:
                ws.write_string(row, 2, item['phone_number'])
            except:
                pass


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
    dump_to_json(OUT_FILENAME, data)
    dump_to_xlsx(OUT_XLSX_FILENAME, data)




if __name__ == '__main__':
    main()