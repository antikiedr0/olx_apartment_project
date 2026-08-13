import json

# normalizes raw scraped data and removes duplicates
def clean_run():
    with open('data/dane.json', 'r', encoding='utf-8') as jfile:
        data = json.load(jfile)

    def clean_cena_m2(value):
        # handle both PLN and EUR, remove non-breaking spaces
        return float(value.replace('zł/m²', '').replace('€/m²', '').replace(',', '.').replace('\xa0', '').strip())

    def clean_powierzchnia(value):
        return float(value.replace('m²', '').replace(',', '.').replace('\xa0', '').strip())

    def clean_liczba_pokoi(value):
        # extract only digits from strings like "2 pokoje"
        return int(''.join(filter(str.isdigit, value)))

    clean_data = []
    seen = []

    for oferta in data:
        # OLX and Otodom use different key names for the same fields
        rodzaj = oferta.get('rodzajzabudowy') or oferta.get('rodzaj_zabudowy', '')
        liczba = oferta.get('liczbapokoi') or oferta.get('liczba_pokoi', '0')

        item = {
            'miasto': oferta.get('miasto', None),
            'cena_m2_pln': clean_cena_m2(oferta['cena_m2_pln']) if 'cena_m2_pln' in oferta else None,
            'powierzchnia': clean_powierzchnia(oferta['powierzchnia']) if 'powierzchnia' in oferta else None,
            'liczba_pokoi': clean_liczba_pokoi(liczba) if liczba else None,
            'poziom': oferta.get('poziom', None),
            # check wyposazenie as fallback if umeblowane is not set
            'umeblowane': oferta.get('umeblowane') or ('tak' if 'meble' in oferta.get('wyposażenie', '') else None),
            'rynek': oferta.get('rynek', None),
            'rodzaj_zabudowy': rodzaj or None,
        }

        if item not in seen:
            seen.append(item)
            clean_data.append(item)

    with open('data/dane_clean.json', 'w', encoding='utf-8') as jfile:
        json.dump(clean_data, jfile, ensure_ascii=False, indent=2)

    print(f"Zapisano {len(clean_data)} ogłoszeń (usunieto {len(data) - len(clean_data)} duplikatów)")

clean_run()