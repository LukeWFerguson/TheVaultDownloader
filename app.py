import os
import time
import requests

from bs4 import BeautifulSoup
from pathlib import Path
from selenium.webdriver import Chrome
from string import ascii_uppercase

BASE_URL = 'https://vimm.net'
CONSOLE_URL = BASE_URL + '/vault/GameCube/'
DOWNLOAD_FOLDER = os.environ['USERPROFILE'] + '/Downloads'


def is_download_finished(temp_folder):
    firefox_temp_file = sorted(Path(temp_folder).glob('*.part'))
    chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    downloaded_files = sorted(Path(temp_folder).glob('*.*'))

    if (len(firefox_temp_file) == 0) and (len(chrome_temp_file) == 0) and (len(downloaded_files) >= 1):
        return True
    else:
        return False


def download_files(url):
    try:
        print('Downloading games from: ' + url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', class_='rounded centered cellpadding1 hovertable')
        rows = table.find_all('tr')

        for row in rows:
            print('\tDownloading: ' + str(row.find('a').string))
            game_url = BASE_URL + row.find('a')['href']
            driver = Chrome(executable_path='resources/chromedriver_win32/chromedriver.exe')
            driver.get(game_url)
    
            # Click on `Download` button.
            driver.find_element_by_name("download").click()
    
            # Wait for download to start.
            time.sleep(10)
    
            # Wait for download to finish.
            while True:
                if is_download_finished(DOWNLOAD_FOLDER):
                    break
                else:
                    time.sleep(10)
    
            driver.close()
    except AttributeError:
        print("No games found here: " + url)


def main():
    # Have to do the number one separately.
    number_url = BASE_URL + '/vault/?p=list&system=GameCube&section=number'
    download_files(number_url)

    # Iterate through each letter of the alphabet.
    for letter in ascii_uppercase:
        download_files(CONSOLE_URL + letter)


if __name__ == "__main__":
    main()
