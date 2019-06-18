# This script scrapes 100 pages each from Getty Images for the search terms
# 'no smile' and 'smile' and saves the images

import os
import requests
from bs4 import BeautifulSoup
import urllib.request

if __name__ == "__main__":

    # Define image search terms and pages to scrape
    search_terms = ['no smile', 'smile']
    pages = 100

    # Iterate through each search_terms
    for term in search_terms:

        # Variable to increment for image naming
        img_no = 0

        # Create new folder
        file_path = f'./images/{term}'
        os.makedirs(file_path)

        # Iterate through each page
        for page in range(1, pages+1):
            # Get response from each page with specific parameters
            base_url = f'https://www.gettyimages.ca/photos/{term}'
            headers = {'User-Agent': 'My User Agent 1.0'}
            # params filters for images with only one person
            params = {
                    'page': f'{page}',
                    'numberofpeople': 'one',
                    'recency': 'anydate',
                    'sort': 'best',
                    'license': 'rf,rm'
                }
            r = requests.get(base_url, headers=headers, params=params)

            soup = BeautifulSoup(r.content, 'lxml')

            # Search and find image url from HTML
            for img in soup.find_all('img', {'class': 'gallery-asset__thumb gallery-mosaic-asset__thumb'}):

                img_url = img['src']
                # Save image
                urllib.request.urlretrieve(img_url, f'{file_path}/{img_no}.jpg')
                img_no += 1

            # Print scrapping status update
            print(f'Scraped {term}: Page {page}')

    # Rename no smile directory according to snake case
    os.rename('./images/no smile', './images/no_smile')
