import psycopg2
import json

# loads clean data into PostgreSQL
def push():
    conn = psycopg2.connect(
        dbname="mieszkania", user="user", password="password", host="localhost", port=5433
    )
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS oferty (
            id SERIAL PRIMARY KEY,
            miasto VARCHAR(50),
            cena_m2_pln FLOAT,
            powierzchnia FLOAT,
            liczba_pokoi INT,
            poziom VARCHAR(20),
            umeblowane VARCHAR(10),
            rynek VARCHAR(20),
            rodzaj_zabudowy VARCHAR(50)
        )
    ''')

    # clear old data before each run
    cur.execute('TRUNCATE TABLE oferty RESTART IDENTITY')

    with open('data/dane_clean.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for oferta in data:
        cur.execute('''
            INSERT INTO oferty (miasto, cena_m2_pln, powierzchnia, liczba_pokoi, poziom, umeblowane, rynek, rodzaj_zabudowy)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            oferta.get('miasto'),
            oferta.get('cena_m2_pln'),
            oferta.get('powierzchnia'),
            oferta.get('liczba_pokoi'),
            oferta.get('poziom'),
            oferta.get('umeblowane'),
            oferta.get('rynek'),
            oferta.get('rodzaj_zabudowy'),
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Wstawiono {len(data)} rekordów")

push()