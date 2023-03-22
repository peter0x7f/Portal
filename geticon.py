import sys
import requests
import os.path
from bs4 import BeautifulSoup

def download_favicon(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        icon_tag = soup.find('link', rel='shortcut icon')
        if not icon_tag:
            icon_tag = soup.find('link', rel='icon')
        if icon_tag:
            icon_url = icon_tag['href']
            if 'http' not in icon_url:
                icon_url = url + '/' + icon_url
            response = requests.get(icon_url, headers=headers, stream=True)
            if response.status_code == 200:
                icon_file = os.path.basename(url) + '.ico'
                with open(icon_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print('Favicon downloaded successfully')
            else:
                print('Failed to download favicon')
        else:
            print('Favicon not found')
    else:
        print('Invalid website URL')


