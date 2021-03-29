import requests
from bs4 import BeautifulSoup

from time import sleep

import pandas as pd


class parsing:
    def __init__(self, path):
        self.page_url = 'https://kazakhstan.travel'

        result = []
        for region in self.__get_url_regions():
            sleep(1)
            print(region)
            for place in self.__get_url_places(region.replace('en', 'kk')):
                result.append(self.__get_places_information(place.replace('en', 'kk')))
                sleep(1)
        pd.DataFrame(result, columns=['title', 'url', 'hour', 'price', 'location', 'subtitle', 'text']).to_csv(path, index=False)
        print('Successfully parsed and saved!')
 
    def __get_url_regions(self):
        page = requests.get(self.page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_find = soup.find_all(class_='clearlist submenu-list submenu-list--columns')[0]
        results = []
        for job_elem in soup_find.find_all('a'):
            title_elem = job_elem.get('href')
            results.append(self.page_url + title_elem)
        return results
        
    def __get_url_places(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        soup_find = soup.find_all(class_='map-with-attractions-list-items-item')
        results = []
        for job_elem in soup_find:
            title_elem = job_elem.a.get('href')
            results.append(self.page_url + title_elem)
        return results

    def __get_places_information(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        spot_info = soup.find_all(class_='spot-info-item')
        hour = ''
        price = ''
        location = ''
        for spot in spot_info:
            if spot.h4.text == "Time to visit":
                hour = spot.p.text
            elif spot.h4.text == "Visit cost":
                price = spot.p.text
            elif spot.h4.text == "Location":
                location = spot.p.text
        title = soup.find(class_='content-title').text
        subtitle = soup.find(class_='content-subtitle content-subtitle--line').text
        text = soup.find(class_='content-text').text[:-36]
        return [title, url, hour, price, location, subtitle, text]

if __name__ == '__main__':
    parse = parsing('dataset/kazakhstan_travel_kz.csv')