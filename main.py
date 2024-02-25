import requests
from datetime import datetime, timedelta
import json
import os
import random

def wczytaj_i_wyswietl_faktury(plik):
    """
    Funkcja wczytuje i wyświetla faktury z pliku JSON.

    Parametry:
    plik (str): Ścieżka do pliku JSON.

    Funkcja wykonuje następujące kroki:
    1. Otwiera plik JSON.
    2. Wczytuje i wyświetla każdą linię pliku jako fakturę.
    3. W przypadku błędów podczas wczytywania pliku, funkcja wyświetla odpowiedni komunikat o błędzie.
    """
    try:
        with open(plik, 'r', encoding='UTF-8') as f:
            for linia in f:
                faktura = json.loads(linia)
                print(faktura)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd podczas wczytywania pliku: {e}")

def wczytaj_plik():
    """
    Funkcja wczytuje dane z pliku 'faktury.json'.

    Funkcja wykonuje następujące kroki:
    1. Otwiera plik 'faktury.json'.
    2. Wczytuje dane z pliku.
    3. Zwraca wczytane dane.
    4. W przypadku błędów podczas wczytywania pliku, funkcja wyświetla odpowiedni komunikat o błędzie i zwraca None.
    """
    try:
        with open("faktury.json", "r", encoding='UTF-8') as plik:
            faktury = json.load(plik)
            return faktury
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd podczas wczytywania pliku wsadowego: {e}")
        return
def pobierz_dostepne_waluty():

    """
    Funkcja pobiera dostępne waluty z API Narodowego Banku Polskiego.

    Zwraca:
    list: Lista dostępnych walut. Każda waluta jest reprezentowana przez swój trzyliterowy kod ISO.
    """
      
    url = "http://api.nbp.pl/api/exchangerates/tables/A/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Błąd sieciowy: {e}")
        return None

    dane = json.loads(response.text)
    waluty = [pozycja["code"] for pozycja in dane[0]["rates"]]
    waluty.append("PLN")
    return waluty
def pobierz_dane_z_bazy(waluta, data):  #Patrzy kurs danej waluty na dany dzień
  
    """
    Funkcja pobiera kurs danej waluty na dany dzień z API Narodowego Banku Polskiego.

    Parametry:
    waluta (str): Trzyliterowy kod ISO waluty.
    data (str): Data w formacie 'RRRR-MM-DD'.

    Zwraca:
    tuple: Para zawierająca dane JSON z API oraz kurs waluty. Jeśli wystąpi błąd, zwraca (None, None).
    """
  
    print(f"Waluta: {waluta}, Data: {data}")  # Debugging
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{waluta}/{data}/"
    response = requests.get(url)
    print(f"URL: {url}")  # Debugging
    
    if response.status_code == 200:
        dane = json.loads(response.text)
        kurs = dane['rates'][0]['mid']
        return dane, kurs
    else:
        print(f"Błąd podczas pobierania danych: {response.status_code}")
        return None, None
    
def wyswietl_fakture_po_id(id):
    if not os.path.exists('faktury.json'): 
        with open('faktury.json','w') as plik:
            plik.write('[]') 
        print("Plik z fakturami nie istniał, został utworzony, proszę dodaj fakturę do pliku, aby wyczytać po ID.")
    else:    
        with open("faktury.json", 'r') as plik:
            for linia in plik:
                faktura = json.loads(linia)
                if faktura["faktura"]["id"] == id:
                    print("faktura:")
                    print(faktura["faktura"])
                    print("platnosc:")
                    if "platnosc" not in faktura or len(faktura["platnosc"]) == 0:
                        print("Faktura nie posiada żadnej płatności.")
                    else:
                        for platnosc in faktura["platnosc"]:
                            print(platnosc)
                    return
            print("Nie znaleziono faktury o podanym ID.")

def wczytaj_najwieksze_id():

    """
    Funkcja wczytuje plik 'faktury.json' i zwraca największe ID faktury.

    Jeśli plik 'faktury.json' nie istnieje, funkcja tworzy pusty plik JSON i zwraca 0.
    Jeśli wystąpi błąd podczas wczytywania pliku 'faktury.json', funkcja zwraca 0.

    Zwraca:
    int: Największe ID faktury lub 0, jeśli plik 'faktury.json' jest pusty lub nie istnieje.
    """

    if not os.path.exists('faktury.json'):
        with open('faktury.json', 'w') as plik:
            plik.write('[]')  # Utwórz pusty plik JSON
            return 0
    else:
        try:
            ids = []
            with open("faktury.json", "r", encoding='UTF-8') as plik:
                try:
                    for linia in plik: 
                        faktura = json.loads(linia)
                        ids.append(faktura['faktura']['id'])
                except:
                    return 0
            return max(ids)
        except (ValueError, json.JSONDecodeError):
            return 0

def wczytaj_najmniejsze_id(): #Funkcja tylko i wylacznie do opcji wyswietl fakture po id

    """
    Funkcja wczytuje plik 'faktury.json' i zwraca najmniejsze ID faktury.

    Ta funkcja jest używana tylko do opcji wyświetlania faktury po ID.

    Jeśli plik 'faktury.json' nie istnieje, funkcja tworzy pusty plik JSON i zwraca 0.
    Jeśli wystąpi błąd podczas wczytywania pliku 'faktury.json', funkcja zwraca 0.

    Zwraca:
    int: Najmniejsze ID faktury lub 0, jeśli plik 'faktury.json' jest pusty lub nie istnieje.
    """

    if not os.path.exists('faktury.json'):
        with open('faktury.json', 'w') as plik:
            plik.write('[]')  # Utwórz pusty plik JSON
    else:
        try:
            ids = []
            with open("faktury.json", "r", encoding='UTF-8') as plik:
                try:
                    for linia in plik:
                        faktura = json.loads(linia)
                        ids.append(faktura['faktura']['id'])
                except:
                    return 0
            return min(ids)
        except (ValueError, json.JSONDecodeError):
            return 0


def wczytaj_plik_wsadowy_i_zapis_do_pliku(plik_wsadowy):
    """
    Funkcja wczytuje dane z pliku wsadowego, przetwarza je i zapisuje do pliku.

    Parametry:
    plik_wsadowy (str): Ścieżka do pliku wsadowego.

    Funkcja wykonuje następujące kroki:
    1. Sprawdza, czy plik wsadowy istnieje.
    2. Wczytuje dane z pliku wsadowego.
    3. Przetwarza dane, sprawdzając poprawność danych wejściowych.
    4. Zapisuje przetworzone dane do pliku.

    W przypadku błędów podczas wczytywania lub przetwarzania danych, funkcja wyświetla odpowiedni komunikat o błędzie.
    """
    if not os.path.exists(plik_wsadowy):
        print("Plik wsadowy nie istnieje.")
        return
    try:
        with open(plik_wsadowy, "r", encoding='UTF-8') as plik:
            faktury = json.load(plik)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd podczas wczytywania pliku wsadowego: {e}")
        return
    najwieksze_id = wczytaj_najwieksze_id()
    dostepne_waluty = pobierz_dostepne_waluty()
    for faktura in faktury:
        try:
            data_wystawienia = datetime.strptime(faktura['faktura']['data_wystawienia'], '%Y-%m-%d')
        except ValueError:
            print("Data wystawienia faktury nie jest w prawidłowym formacie (powinna być w formacie RRRR-MM-DD).")
            continue
        if faktura['faktura']['kwota_faktury'] < 0:
            print("Kwota nie może być ujemna.")
            break
        if faktura['faktura']['waluta'] not in dostepne_waluty:
            print("Podana waluta nie jest dostępna.")
            break
        if 'kwota_po_odliczeniu_platnosci' not in faktura:
            faktura['kwota_po_odliczeniu_platnosci'] = faktura['faktura']['kwota_faktury']
        if 'faktura' not in faktura or 'data_wystawienia' not in faktura['faktura'] or faktura['faktura']['data_wystawienia'] == "":
            print("Data wystawienia faktury nie jest podana.")
            break
        if 'data_pobrania_kursu' not in faktura or faktura['faktura']['data_pobrania_kursu'] == "":
            data_wystawienia = datetime.strptime(faktura['faktura']['data_wystawienia'], '%Y-%m-%d')
            if data_wystawienia.weekday() > 4:  # Jeśli to weekend
                piątek = data_wystawienia - timedelta(days=data_wystawienia.weekday() - 4)
                faktura['faktura']['data_pobrania_kursu'] = piątek.strftime('%Y-%m-%d')
            else:
                faktura['faktura']['data_pobrania_kursu'] = faktura['faktura']['data_wystawienia']
        najwieksze_id = najwieksze_id + 1
        faktura['faktura']['id'] = najwieksze_id 
        zapisz_do_pliku(faktura['faktura'],None)
        platnosci = faktura['platnosc']  # Teraz 'platnosc' jest listą
        if platnosci is not None:
            for platnosc in platnosci:
                if platnosc['kwota'] < 0:
                    print("Kwota nie może być ujemna.")
                    break
                if platnosc['waluta'] not in dostepne_waluty:
                    print("Podana waluta nie jest dostępna.")
                    break
                if 'data_platnosci' not in platnosc or platnosc['data_platnosci'] == "":
                    print("Data płatności nie jest podana.")
                    break
                try:
                    platnosc['data_platnosci'] = datetime.strptime(faktura['data_wystawienia'], '%Y-%m-%d')
                except ValueError:
                    print("Data wystawienia faktury nie jest w prawidłowym formacie (powinna być w formacie RRRR-MM-DD).")
                    continue
                if 'data_pobrania_kursu' not in platnosc or platnosc['data_pobrania_kursu'] == "":
                    data_platnosci = datetime.strptime(platnosc['data_platnosci'], '%Y-%m-%d')
                    if data_platnosci.weekday() > 4:  # Jeśli to weekend
                        piątek = data_platnosci - timedelta(days=data_platnosci.weekday() - 4)
                        platnosc['data_pobrania_kursu'] = piątek.strftime('%Y-%m-%d')
                    else:
                        platnosc['data_pobrania_kursu'] = platnosc['data_platnosci']
                faktura['status'],faktura['kwota_po_odliczeniu_platnosci']=porownaj_kursy(faktura,platnosc)
                zapisz_do_pliku(faktura,platnosc)
        else:
            break

        # Sprawdź, czy waluta jest dostępna

def zapisz_do_pliku(faktura, platnosc):
    """
    Funkcja zapisuje dane faktury i płatności do pliku JSON.

    Parametry:
    faktura (dict lub Faktura): Słownik lub obiekt Faktura zawierający dane faktury.
    platnosc (dict lub Platnosc): Słownik lub obiekt Platnosc zawierający dane płatności.

    Funkcja wykonuje następujące kroki:
    1. Sprawdza, czy plik 'faktury.json' istnieje. Jeśli nie, tworzy pusty plik JSON.
    2. Wczytuje dane z pliku 'faktury.json'.
    3. Dodaje dane faktury i płatności do wczytanych danych.
    4. Zapisuje aktualizowane dane z powrotem do pliku 'faktury.json'.

    W przypadku błędów podczas wczytywania lub zapisywania danych, funkcja wyświetla odpowiedni komunikat o błędzie.
    """
    if not os.path.exists('faktury.json'):
        with open('faktury.json', 'w') as plik:
            plik.write('[]')  # Utwórz pusty plik JSON
    dane = []
    with open('faktury.json', 'r',encoding='UTF-8') as f:
        try:
            dane = json.load(f)
        except json.JSONDecodeError as e:
            if str(e) == 'Expecting value: line 1 column 1 (char 0)':
                faktura_data = None
                print('Plik jest pusty. Utworzony zostanie nowy plik.')
                if faktura:
                    faktura_data = { "faktura":{
                        "id": 0,
                        "kwota_faktury": faktura['kwota_faktury'],
                        "kwota_po_odliczeniu_platnosci": faktura['kwota_po_odliczeniu_platnosci'],
                        "waluta": faktura['waluta'],
                        "data_wystawienia": faktura['data_wystawienia'],
                        "data_pobrania_kursu": faktura['data_pobrania_kursu'],
                        "status": faktura['status'],
                        "platnosc": []  # Teraz 'platnosc' jest listą wewnątrz 'faktura'
                    }}
                elif isinstance(faktura,Faktura):
                    faktura_data = { "faktura":{
                        "id": 0,
                        "kwota_faktury": faktura.kwota_faktury,
                        "kwota_po_odliczeniu_platnosci": faktura.kwota_po_odliczeniu_platnosci,
                        "waluta": faktura.waluta,
                        "data_wystawienia": faktura.data_wystawienia,
                        "data_pobrania_kursu": faktura.data_pobrania_kursu,
                        "status": faktura.status,
                        "platnosc": []  # Teraz 'platnosc' jest listą wewnątrz 'faktura'
                    }}
                if faktura_data is not None:
                    print('ok')
                    dane.append(faktura_data)
                    with open('faktury.json', 'w') as f:
                        json.dump(dane, f, indent=4)
            else:
                raise

    if platnosc is not None:
        if isinstance(platnosc,Platnosc):
            platnosc_data = {"platnosc":{
                "id": platnosc.id_faktury,
                "kwota": platnosc.kwota,
                "waluta": platnosc.waluta,
                "data_platnosci": platnosc.data_platnosci,
                "data_pobrania_kursu:": platnosc.data_pobraniu_kursu
            }}
        else: 
            platnosc_data = {"platnosc":{
                "id": faktura['id'],
                "kwota": platnosc['kwota'],
                "waluta": platnosc['waluta'],
                "data_platnosci": platnosc['data_platnosci'],
                "data_pobrania_kursu": platnosc['data_pobrania_kursu']
            }}
        for faktury in dane:
            if faktury['faktura']['id'] == id_faktury:
                if faktury['faktura']['id'] != faktura['status']:
                    faktury['faktura']['status'] = faktura['status']
                faktury['faktura']['platnosc'].append(platnosc_data)
                break
            else:
                # Jeśli faktura nie istnieje, przygotuj dane faktury i dodaj całe dane faktury
                if isinstance(faktura,Faktura):
                    faktura_data = {"faktura":{
                        "id": faktura.id,
                        "kwota_faktury": faktura.kwota_faktury,
                        "kwota_po_odliczeniu_platnosci": faktura.kwota_po_odliczeniu_platnosci,
                        "waluta": faktura.waluta,
                        "data_wystawienia": faktura.data_wystawienia,
                        "data_pobrania_kursu": faktura.data_pobrania_kursu,
                        "status": faktura.status,
                        "platnosc": [platnosc_data]  # Teraz 'platnosc' jest listą wewnątrz 'faktura'
                    }}
                else:
                    faktura_data = {"faktura":{
                        "id": faktura['id'],
                        "kwota_faktury": faktura['kwota_faktury'],
                        "kwota_po_odliczeniu_platnosci": faktura['kwota_po_odliczeniu_platnosci'],
                        "waluta": faktura['waluta'],
                        "data_wystawienia": faktura['data_wystawienia'],
                        "data_pobrania_kursu": faktura['data_pobrania_kursu'],
                        "status": faktura['status'],
                        "platnosc": [platnosc_data]  # Teraz 'platnosc' jest listą wewnątrz 'faktura'
                    }}
                dane.append(faktura_data)
        with open('faktury.json', 'w',encoding="UFT-8") as f:
            json.dump(dane, f, indent=4)
    else:
        return
        

def porownaj_kursy(faktura,platnosci):
    """
    Funkcja porównuje kursy walut dla faktury i płatności.

    Parametry:
    faktura (dict lub Faktura): Słownik lub obiekt Faktura zawierający dane faktury.
    platnosci (list): Lista słowników lub obiektów Platnosc zawierających dane płatności.

    Funkcja wykonuje następujące kroki:
    1. Przetwarza dane faktury i płatności.
    2. Pobiera kursy walut dla faktury i płatności.
    3. Porównuje kwoty faktury i płatności w tych samych walutach.
    4. Konwertuje kwoty na złotówki, jeśli waluty faktury i płatności są różne.
    5. Porównuje kwoty faktury i płatności w złotówkach i konwertuje wynik z powrotem na walutę faktury.
    6. Zwraca status płatności i kwotę do zapłaty lub nadpłatę.

    W przypadku błędów podczas pobierania kursów walut, funkcja zwraca komunikat o błędzie.
    """
    nadplata = None
    do_zaplaty = None
    if isinstance(faktura, Faktura):
        id = faktura.id
        kwota = faktura.kwota_po_odliczeniu_platnosci
        waluta = faktura.waluta
        data_wystawienia = faktura.data_wystawienia
        data_pobrania_kursu = faktura.data_pobrania_kursu
    else:  # faktura jest słownikiem
        id = faktura['id']
        kwota = faktura['kwota_po_odliczeniu_platnosci']
        waluta = faktura['waluta']
        data_wystawienia = faktura['data_wystawienia']
        data_pobrania_kursu = faktura['data_pobrania_kursu']
        

    if waluta == "PLN":
        kurs_faktura = 1
    else:
        if data_pobrania_kursu is not None:
            dane_faktura, kurs_faktura = pobierz_dane_z_bazy(waluta, data_pobrania_kursu)
        else:    
            dane_faktura, kurs_faktura = pobierz_dane_z_bazy(waluta, data_wystawienia)
    kwota_platnosci_w_PLN = 0
    for platnosc in platnosci:
        if isinstance(platnosc, Platnosc):
            kwota_platnosci = platnosc.kwota
            waluta_platnosc = platnosc.waluta
            data_platnosci = platnosc.data_platnosci
            data_pobrania_kursu_platnosci= platnosc.data_pobrania_kursu
        else:  # platnosc jest słownikiem
            kwota_platnosci = platnosc['kwota']
            waluta_platnosc = platnosc['waluta']
            data_platnosci = platnosc['data_platnosci']
            data_pobrania_kursu_platnosci = platnosc['data_pobrania_kursu']
        if waluta_platnosc == "PLN":
            kurs_platnosc = 1
        else:
            if data_pobrania_kursu_platnosci is not None:
                dane_platnosc, kurs_platnosc = pobierz_dane_z_bazy(waluta, data_pobrania_kursu_platnosci)
            else:
                dane_platnosc, kurs_platnosc = pobierz_dane_z_bazy(waluta, data_platnosci)
        status = "Nie można pobrać kursu waluty."
        if kurs_platnosc is not None and kurs_faktura is not None:
        # Przeliczanie kwoty faktury i płatności w tych samych walutach
            if waluta == waluta_platnosc:
                if kwota == kwota_platnosci:
                    status = "Opłacona w całości"
                elif kwota > platnosc.kwota:
                    do_zaplaty = kwota - kwota_platnosci
                    status = "Do zapłaty: " + str(do_zaplaty)+ " " + str(waluta)
                else:   
                    nadplata = kwota_platnosci - kwota
                    status = "Nadpłata: " + str(nadplata) + " " + str(waluta)
        # Konwersja na zlotowki walut faktury oraz platnosci, poniewaz strona api podaje kursy danych walut własnie w tej walucie.
            else:
                kwota_faktury_w_PLN = kwota * kurs_faktura
                kwota_platnosci_w_PLN = kwota_platnosci * kurs_platnosc
                # Porównanie kwoty faktury i płatności w PLN oraz konwersja do waluty domyślnej
                if kwota_faktury_w_PLN == kwota_platnosci_w_PLN:
                    status = "Opłacona w całosci"
                elif kwota_faktury_w_PLN > kwota_platnosci_w_PLN:
                    do_zaplaty_w_PLN = kwota_faktury_w_PLN - kwota_platnosci_w_PLN
                    # Przeliczanie kwoty do zapłaty z powrotem na walutę faktury
                    do_zaplaty = do_zaplaty_w_PLN / kurs_faktura
                    status = "Do zapłaty: " + str(do_zaplaty)+ " " + str(waluta)
                else:   
                    nadplata_w_PLN = kwota_platnosci_w_PLN - kwota_faktury_w_PLN
                    # Przeliczanie kwoty nadpłaty z powrotem na walutę faktury
                    nadplata = nadplata_w_PLN / kurs_platnosc
                    status = "Nadpłata: " + str(nadplata)+ " " + str(waluta)
    if do_zaplaty is not None:
        kwota = -kwota              
    return status,kwota
            
class Faktura: 
    """
    Klasa reprezentująca fakturę.

    Atrybuty:
    id (int): Unikalny identyfikator faktury.
    kwota (float): Kwota faktury.
    waluta (str): Waluta, w której wystawiona jest faktura.
    data_wystawienia (str): Data wystawienia faktury w formacie 'YYYY-MM-DD'.
    data_wystawienia_weekend (str): Data wystawienia faktury przesunięta na ostatni piątek, jeśli data wystawienia przypada na weekend, jest to zmienna ukryta, wykorzystywana tylko i wylacznie do pobrania kursu na piatek przed weekendem..
    status (str): Status faktury.

    Metody:
    wprowadz_dane(dostepne_waluty): Prosi użytkownika o wprowadzenie danych faktury.
    """
    def __init__(self,id):
        self.id = id
        self.kwota_faktury = None
        self.kwota_po_odliczeniu_platnosci = None
        self.waluta = None
        self.data_wystawienia = None
        self.data_pobrania_kursu = None
        self.status = None
        self.platnosc = None
    def wprowadz_dane(self, dostepne_waluty):
        while True:
            try:
                self.kwota_faktury = float(input("Podaj kwotę faktury: "))
                self.kwota_po_odliczeniu_platnosci = self.kwota_faktury
                if self.kwota_faktury < 0:
                    raise ValueError("Kwota nie może być ujemna.")
            except ValueError as e:
                print(e)
                continue  # Kontynuuj pętlę, aby poprosić użytkownika o ponowne wprowadzenie danych
            break
        while True:
            print("Dostępne waluty: ", ', '.join(dostepne_waluty))
            self.waluta = input("Podaj walutę faktury: ")
            if self.waluta not in dostepne_waluty:
                print("Podana waluta nie jest dostępna. Wybierz jedną z dostępnych walut.")
                continue  # Kontynuuj pętlę, aby poprosić użytkownika o ponowne wprowadzenie danych
            else: 
                break
        while True:
            data_wystawienia = input("Podaj datę wystawienia faktury (YYYY-MM-DD): ")
            try:
                data = datetime.strptime(data_wystawienia, '%Y-%m-%d')
                self.data_wystawienia = data.strftime('%Y-%m-%d')
                if data.date() > datetime.now().date():
                    raise ValueError("Data nie może być późniejsza niż dzisiejsza data.")
                if data.weekday() > 4:
                        while data.weekday() > 4: # Jeśli data przypada na sobotę lub niedzielę, cofnij do ostatniego piatku
                            data -= timedelta(days=1)
                        self.data_pobrania_kursu = data.strftime('%Y-%m-%d')
                break
            except ValueError as e:
                print(e)

class Platnosc:
    """
    Klasa reprezentująca płatność za fakturę.

    Atrybuty:
    id_faktury (int): Identyfikator faktury, do której odnosi się płatność.
    kwota (float): Kwota płatności.
    waluta (str): Waluta, w której dokonano płatności.
    data_platnosci (str): Data płatności w formacie 'YYYY-MM-DD'.
    data_platnosci_piatek (str): Data płatności przesunięta na ostatni piątek, jeśli data płatności przypada na weekend.

    Metody:
    wprowadz_dane(dostepne_waluty): Prosi użytkownika o wprowadzenie danych płatności.
    """
    def __init__(self, id_faktury):
        self.id_faktury = id_faktury
        self.kwota = None
        self.waluta = None
        self.data_platnosci = None
        self.data_pobrania_kursu = None

    def wprowadz_dane(self, dostepne_waluty):
        oplata = str(input("Czy istnieje płatność do faktury? (Tak/Nie): "))
        if oplata.lower() == "tak":
            while True:
                try:
                    self.kwota = float(input("Podaj kwotę płatności: "))
                    if self.kwota < 0:
                        raise ValueError("Kwota nie może być ujemna.")
                    break
                except ValueError as e:
                    print(e)

            print("Dostępne waluty: ", ', '.join(dostepne_waluty))
            while True:
                self.waluta = input("Podaj walutę płatności: ")
                if self.waluta not in dostepne_waluty:
                    print("Podana waluta nie jest dostępna. Wybierz jedną z dostępnych walut.")
                    continue
                else:
                    break

            while True:
                data_platnosci = input("Podaj datę wystawienia Płatności (YYYY-MM-DD): ")
                try:
                    data = datetime.strptime(data_platnosci, '%Y-%m-%d')
                    self.data_platnosci = data.strftime('%Y-%m-%d')
                    if data.date() > datetime.now().date():
                        raise ValueError("Data nie może być późniejsza niż dzisiejsza data.")
                    if data.weekday() > 4:
                        while data.weekday() > 4: # Jeśli data przypada na sobotę lub niedzielę, cofnij do ostatniego piatku
                            data -= timedelta(days=1)
                        self.data_platnosci_weekend = data.strftime('%Y-%m-%d')
                    break
                except ValueError as e:
                    print(e)
        else:
            print("Faktura została dodana pomyślnie")
    def dodaj_platnosc_do_faktury(self):
        """
        Dodaje płatność do faktury o danym ID.
        Parametry:
        faktury (list): Lista faktur, do której należy dodać płatność.
        """
        faktury = wczytaj_plik()
        for faktura in faktury:
            if faktura['id'] == self.id_faktury:
                if 'platnosci' not in faktura:
                    faktura['platnosci'] = []
                faktura['platnosci'].append(self)
                print(f"Dodano płatność do faktury o ID {self.id_faktury}.")
                faktura['status'] = porownaj_kursy(faktura, self)  # Aktualizacja statusu faktury
                return
            else:
                print(f"Nie znaleziono faktury o ID {self.id_faktury}.")

def menu():
    while True:
        print("Wybierz tryb działania programu:")
        print("1. Tryb interaktywny")
        print("2. Dodaj płatność do istniejącej faktury po ID")
        print("3. Wyswietl fakturę po ID")
        print("4. Uruchom plik wsadowy")
        print("5. Wyjdź z programu.")

        wybor = input("Wybierz opcję: ")

        max = wczytaj_najwieksze_id()
        min = wczytaj_najmniejsze_id()

        if wybor == "1":
            dostepne_waluty = pobierz_dostepne_waluty()
            if dostepne_waluty is not None:
                najwieksze_id = wczytaj_najwieksze_id()
                faktura = Faktura(najwieksze_id+1)
                faktura.wprowadz_dane(dostepne_waluty)
                platnosc = Platnosc(faktura.id)
                platnosc.wprowadz_dane(dostepne_waluty)
                porownaj_kursy(faktura,platnosc)
                zapisz_do_pliku(faktura,platnosc)
                wyswietl_fakture_po_id(faktura.id)
            else:
                print("Nie można pobrać kursu waluty.")
            # Aktualizacja statusu w pliku i wyswietlenie
        elif wybor == "2":
            wczytaj_i_wyswietl_faktury('faktury.json')
            id_szukanej_faktury = input("Wprowadź ID faktury do ktorej probujesz dokonac płatność (od "+str(min)+" do "+str(max)+"):")
            platnosc = Platnosc(id_szukanej_faktury)
            platnosc.wprowadz_dane(dostepne_waluty)
            platnosc.dodaj_platnosc_do_faktury()
        elif wybor == "3":
            szukane_id = int(input("Podaj id szukanej faktury od " + str(min) + " do " + str(max) +": "))
            wyswietl_fakture_po_id(szukane_id)
        elif wybor == "4":
            """
            plik_wsadowy = input("Nazwa pliku wsadowego (Ważne, żeby plik był w formacie JSON): ")
            if not plik_wsadowy.endswith('.json'):
                plik_wsadowy += '.json'
            """
            plik_wsadowy = "plik_wsadowy.json"
            wczytaj_plik_wsadowy_i_zapis_do_pliku(plik_wsadowy)
            break
        elif wybor == "5":
            exit()
        else:
            print("Nieznana opcja, spróbuj ponownie.")
#uruchamianie menu
menu()
