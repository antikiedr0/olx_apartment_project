from scrape import Scrapper
from scrape_data import ScrapeData
from link_scraper import save_links
from clean_data import clean_run
from db import push
citys = [
    'warszawa',
    'gdansk',
    'krakow',
    'poznan',
    'wroclaw',
    'bydgoszcz',
    'szczecin',
    'lublin'
]

# pipeline stages executed in order by the state machine
STATES = [
    'GET_OGLOSZENIA',
    'GET_LINKS',
    'SCRAPE_DATA',
    'CLEAN_DATA',
    'PUSH_TO_DB',
    'DONE',
]

# state machine that runs the full scraping pipeline step by step
class Scraper:

    def __init__(self):
        self.state = STATES[0]

    def next_state(self):
        # move to the next stage in the pipeline
        idx = STATES.index(self.state)
        self.state = STATES[idx + 1]

    def clear_files(self):
        # wipe all data files before starting a fresh run
        files = ['data/oferty.txt', 'data/linki.txt', 'data/dane.txt', 'data/dane.json', 'data/dane_clean.json']
        for f in files:
            open(f, 'w').close()
        print("-------------------Pliki wyczyszczone---------------------\n")

    def run(self):
        self.clear_files()
        while self.state != 'DONE':
            print(f'Stan: {self.state}')
            if self.state == 'GET_OGLOSZENIA':
                print('---------------Downloading Listing------------------\n')
                for city in citys:
                    links = Scrapper(f'https://www.olx.pl/nieruchomosci/mieszkania/{city}/?page=')
                    links.main()
            elif self.state == 'GET_LINKS':
                print("-------------------Getting links---------------------\n")
                save_links()
            elif self.state == 'SCRAPE_DATA':
                print("-------------------Starting data scraping---------------------\n")
                data = ScrapeData('data/linki.txt')
                data.run()
            elif self.state == 'CLEAN_DATA':
                print("-------------------Cleaning data---------------------\n")
                clean_run()
            elif self.state == 'PUSH_TO_DB':
                print("-------------------Pushing data to database---------------------\n")
                push()
            self.next_state()
        print("ALL DONE!")

if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
