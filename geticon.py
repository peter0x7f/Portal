import sys
import requests
import os
import os.path
from bs4 import BeautifulSoup

def download_favicon(url, name):
    #includes relavant headers 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    #gets response
    response = requests.get(url, headers=headers)
    #double checks that 
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #checks for ico image
        icon_tag = soup.find('link', rel='shortcut icon')
        if not icon_tag:
            icon_tag = soup.find('link', rel='icon')
        if icon_tag:
            icon_url = icon_tag['href']
            if 'http' not in icon_url:
                icon_url = url + '/' + icon_url
            response = requests.get(icon_url, headers=headers, stream=True)
            #checks if ico link is valid
            if response.status_code == 200:
                icon_file = os.getcwd() + "/Icons/" + name + '.ico'
                #writes content to file
                with open(icon_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print('Favicon downloaded successfully')
                return os.getcwd() + "/" + name + '.ico'
            else:
                #sets icon to default
                print('Failed to download favicon')
                return os.path.getcwd()+"/Icons/"+"default.ico"
        else:
            print('Favicon not found')
            return os.path.getcwd()+"/Icons/"+"default.ico"
    else:
        print('Invalid website URL')
        return os.path.getcwd()+"/Icons/"+"default.ico"
    response.close()
