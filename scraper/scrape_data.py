import requests
from bs4 import BeautifulSoup as bs
import json

# scrapes detailed data from each individual listing
class ScrapeData:

    def __init__(self, file):
        with open(file) as f:
            self.links = []
            self.dane = []
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = line.split("\n")
                self.links.append(line[:6])

    def scrape_data_from_links(self, link):
        # city is appended to the link with | separator
        url, city = link.rsplit('|', 1) if '|' in link else (link, None)

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers)
        soup = bs(response.text, 'html.parser')
        print('Link: '+ url)
        result = 'Link' + url
        post = {'miasto': city}

        if 'www.otodom.pl' in url:
            main_price = soup.find('div', attrs={'data-sentry-element':"MainPriceWrapper"})
            additional_price = soup.find('div', attrs = {'data-sentry-element':"AdditionalPriceWrapper"})
            try:
                main_price = main_price.find('strong', attrs={'data-cy':"adPageHeaderPrice"})
                additional_price = additional_price.find('div', attrs={"aria-label":"Cena za metr kwadratowy"})
                if main_price:
                    # each property attribute is in its own ItemGridContainer div
                    args = soup.find_all('div', attrs={'data-sentry-element':"ItemGridContainer"})
                    print(main_price.text.strip())
                    print(additional_price.text.strip())
                    result += "\nCena: " +  main_price.text.strip() + '\n'
                    result += "Cena za m2: " + additional_price.text.strip() + '\n'
                    post['cena_m2_pln'] = additional_price.text.strip().replace(' ', '')
                    for arg in args:
                        print(arg.text.strip())
                        result += arg.text.strip() + '\n'
                        text = arg.text.strip()
                        if ':' in text:
                            key, value = text.split(':', 1)
                            key = key.replace(' ', '_').lower()
                            value = value.replace(' ', '').lower()
                            post[key.strip()] = value.strip()
            except:
                # listing was removed or unavailable
                print("Ogloszenie zamkniete")
                return 0

        elif "www.olx.pl" in url:
            args_of_olx = soup.find('div', attrs = {'data-nx-name': "ListContainer"})

            if args_of_olx:
                # each attribute is a <p> tag inside the ListContainer
                args = args_of_olx.find_all('p', attrs={'data-nx-name': 'P3'})
                for arg in args:
                    print(arg.text.strip())
                    result += arg.text.strip() + '\n'
                    text = arg.text.strip()
                    if ':' in text:
                        key, value = text.split(':', 1)
                        if key == "Cena za m²":
                            key = 'cena_m2_pln'
                        key = key.replace(' ', '').lower()
                        value = value.replace(' ', '').lower()
                        post[key.strip()] = value.strip()

        self.dane.append(post)
        return result

    def run(self):
        with open("data/dane.txt", "w") as file, open('data/dane.json', 'w') as jfile:
            for link in self.links:
                # strip the "Link: " prefix
                link = link[0][6:]
                result = self.scrape_data_from_links(link)
                if result != 0:
                    file.write(result)
                    file.write(("\n"+"-"*20+"\n"))

            json.dump(self.dane, jfile, ensure_ascii=False, indent=2)       

if __name__ == "__main__":
    app = ScrapeData('data/linki.txt')
    app.run()