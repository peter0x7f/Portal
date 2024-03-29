import sys
import requests
import os
import os.path
from bs4 import BeautifulSoup
from PIL import Image

# MM start


def download_favicon(url, name):
    #includes relavant headers
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    #gets response
    response = requests.get(url, headers=headers)

    #double checks valid response
    if response.status_code == 200:

        # MM end
        # TG start
        # checks if file already exists.
        if os.path.isfile(os.getcwd() + "/Icons/" + str(name) + '.ico'):
            return "Icons/" + str(name) + '.ico'
        #TG end
        # MM start
        soup = BeautifulSoup(response.content, 'html.parser')

        #checks for ico image
        icon_tag = soup.find('link', rel='shortcut icon')

        #  checks alternate tag for icon
        if not icon_tag:
            icon_tag = soup.find('link', rel='icon')
        if icon_tag:
            icon_url = icon_tag['href']
            if 'http' not in icon_url:
                icon_url = url + '/' + icon_url

            response = requests.get(icon_url, headers=headers, stream=True)
            #checks if ico link is valid
            if response.status_code == 200:
                # generates full filepath for new icon file
                icon_file = os.getcwd() + "/Icons/" + str(name) + '.ico'
                #writes content to file
                with open(icon_file, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print('Favicon downloaded successfully')
                im = Image.open(icon_file)
                new_im = im.resize((150, 150))
                new_im.save(icon_file)
                return icon_file

            else:
                #sets icon to default
                print('Failed to download favicon')
                return "Icons/Default.png"

        else:
            print('Favicon not found')
            return "Icons/Default.png"

    else:
        print('Invalid website URL')
        return "Icons/Default.png"

    response.close()


# MM end
