import requests
from bs4 import BeautifulSoup as bs


class Scrapper: 
    
    def __init__(self, page):
        self.urls = []
        self.city = page.split('/')[5]  # extract city name from URL
        for i in range(1,15):
            self.urls.append(page + str(i))

    def main(self):
        for url in self.urls:
            try:
                # pretend to be a browser so OLX doesn't block us
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                response = requests.get(url, headers=headers)
                soup = bs(response.text, 'html.parser')

                # find all listing cards on the page
                ogloszenia = soup.find_all('div', attrs={'data-testid': 'l-card'})

                with open("data/oferty.txt", "a") as file:
                    for ogloszenie in ogloszenia:
                        tytul_elem = ogloszenie.find('a', attrs={'data-testid': 'card-title-link'})
                        link = tytul_elem['href']
                        if 'otodom' not in link:
                            link = 'https://www.olx.pl/' + link
                        cena_elem = ogloszenie.find('p', attrs={'data-testid': 'ad-price'})

                        tytul = tytul_elem.text.strip() if tytul_elem else "Brak tytułu"
                        cena = cena_elem.text.strip() if cena_elem else "Brak ceny"
                        cena = cena.split(" ")
                        # remove trailing currency or "do negocjacji" label
                        if cena[-1] == "negocjacji":
                            cena.pop()
                            cena.pop()
                        else:
                            cena.pop()
                        intcena = ""
                        for i in cena:
                            intcena += i
                        try:
                            intcena = int(intcena)
                            wartosc = 0
                            # skip listings below 50 000 PLN to filter out rooms and garages
                            if intcena > 50000:
                                wartosc = intcena
                            if wartosc > 0:
                                print(f"Tytuł: {tytul}")
                                print(f"Cena:  {wartosc}")
                                print(f"Link: {link}")
                                print("-" * 30)
                                file.write(f"Tytuł: {tytul}\n")
                                file.write(f"Cena:  {wartosc}\n")
                                file.write(f"Link: {link}|{self.city}\n")
                                file.write("-"*30 + "\n")
                        except ValueError as err:
                            print(err)
                        
            except requests.exceptions.RequestException as err:
                print("Błąd połączenia:", err)

if __name__ == "__main__":
    app = Scrapper("https://www.olx.pl/nieruchomosci/mieszkania/warszawa/?page=")
    app.main()