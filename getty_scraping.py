import os
import requests
from bs4 import BeautifulSoup
import urllib.request

if __name__ == "__main__":
    search_terms = ['no smile', 'smile']
    pages = 100

    for term in search_terms:
        counter = 0

        file_path = f'../project_capstone/{term}'
        os.makedirs(file_path)

        for page in range(1, pages+1):
            try:
                base_url = f'https://www.gettyimages.ca/photos/{term}'
                headers = {'User-Agent': 'My User Agent 1.0'}
                params = {
                    'page': f'{page}',
                    'numberofpeople': 'one',
                    'phrase': term,
                    'recency': 'anydate',
                    'sort': 'best',
                    'license': 'rf,rm',
                    'suppressfamilycorrection': 'true'
                    }
                r = requests.get(base_url, headers = headers, params = params)
            except:
                print('An error occurred')

            soup = BeautifulSoup(r.content, 'lxml')
            for img in soup.find_all('img', {'class':'gallery-asset__thumb gallery-mosaic-asset__thumb'}):
                img_url = img['src']
                urllib.request.urlretrieve(img_url, f'{file_path}/{counter}.jpg')
                counter += 1
            print(f'Scraped {term}: Page {page}')
