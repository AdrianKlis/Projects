import requests
from datetime import datetime, timedelta
import json
import os
import random

def pobierz_dostepne_waluty():  #Pobiera dostępne waluty na stronie api nbp
    url = "http://api.nbp.pl/api/exchangerates/tables/A/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Błąd sieciowy: {e}")
        return None

    dane = json.loads(response.text)
    waluty = [pozycja["code"] for pozycja in dane[0]["rates"]]
    return waluty
def pobierz_dane_z_bazy(waluta, data):  #Patrzy kurs danej waluty na dany dzień
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

def wczytaj_najwieksze_id():
    if not os.path.exists('faktury.json'):
        with open('faktury.json', 'w') as plik:
            plik.write('[]')  # Utwórz pusty plik JSON
    else:
        try:
            with open("faktury.json", "r") as plik:
                faktury = json.load(plik) 
                return max([faktura['Faktura']['id'] for faktura in faktury])
        except (ValueError):
            return 0
    
def wyswietl_fakture_po_id(id):
    if not os.path.exists('faktury.json'): #jezeli nie istnieje, utworz go
        with open('faktury.json','w') as plik:
            plik.write('[]') #utworz pusty plik JSON
        print("Plik z fakturami nie istniał, został utworzony, proszę dodaj fakturę do pliku, aby wyczytać po ID.")
    else:    
        with open("faktury.json", 'r') as plik:
            faktury = json.load(plik)
            for faktura in faktury:
                if faktura["Faktura"]["id"] == id:
                    print("Faktura:")
                    print(faktura["Faktura"])
                    print("Płatność:")
                    print(faktura["Platnosc"])
                    return
            print("Nie znaleziono faktury o podanym ID.")

def wczytaj_plik_wsadowy_i_zapis_do_pliku():
    """
    Funkcja wczytuje dane z pliku wsadowego, przypisuje unikalne id fakturze na podstawie największego id w pliku faktury.json,
    a następnie zapisuje te dane do pliku faktury.json.

    Jeśli plik wsadowy nie istnieje, funkcja wyświetla komunikat o błędzie i kończy działanie.
    Jeśli wystąpi błąd podczas wczytywania pliku wsadowego, funkcja wyświetla komunikat o błędzie i kończy działanie.
    Jeśli plik faktury.json nie istnieje, funkcja tworzy pusty plik JSON.
    Jeśli wystąpi błąd podczas zapisywania do pliku faktury.json, funkcja wyświetla komunikat o błędzie.
    """
    if not os.path.exists('plik_wsadowy.json'):
        print("Plik wsadowy nie istnieje.")
        return
    try:
        with open("plik_wsadowy.json", "r") as plik:
            faktury = json.load(plik)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd podczas wczytywania pliku wsadowego: {e}")
        return
    najwieksze_id = wczytaj_najwieksze_id()
    for faktura in faktury:
        faktura['Faktura']['id'] = najwieksze_id + 1
        najwieksze_id += 1
    if not os.path.exists('faktury.json'):
        with open('faktury.json', 'w') as plik:
            plik.write('[]')  # Utwórz pusty plik JSON
    try:
        with open("faktury.json", "r") as plik:
            istniejace_faktury = json.load(plik)
    except (FileNotFoundError, json.JSONDecodeError):
        istniejace_faktury = []
    istniejace_faktury.extend(faktury)
    try:    
        with open("faktury.json", "w") as plik:
            json.dump(istniejace_faktury, plik)
    except IOError as e:
        print(f"Błąd podczas zapisywania do pliku: {e}")

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
    zapisz_do_pliku(platnosc): Zapisuje dane faktury i płatności do pliku 'faktury.json'.
    """
    def __init__(self,id):
        self.id = id
        self.kwota = None
        self.waluta = None
        self.data_wystawienia = None
        self.data_wystawienia_weekend = None
        self.status = None
    def wprowadz_dane(self, dostepne_waluty):
        while True:
            try:
                self.kwota = float(input("Podaj kwotę faktury: "))
                if self.kwota < 0:
                    raise ValueError("Kwota nie może być ujemna.")
            except ValueError as e:
                print(e)
                continue  # Kontynuuj pętlę, aby poprosić użytkownika o ponowne wprowadzenie danych
            break
        while True:
            print("Dostępne waluty: ", ', '.join(dostepne_waluty))
            self.waluta = input("Podaj walutę faktury (lub zostaw puste dla PLN): ")
            if self.waluta.strip() == "":
                self.waluta = "PLN"
                break
            elif self.waluta not in dostepne_waluty:
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
                        self.data_wystawienia_weekend = data.strftime('%Y-%m-%d')
                        break
            except ValueError as e:
                print(e)

    def zapisz_do_pliku(self, platnosc):
        dane_faktury = {
            "id": self.id,
            "kwota": self.kwota,
            "waluta": self.waluta,
            "data_wystawienia": self.data_wystawienia,
            "status": self.status,
        }
        dane_platnosci = {
            "id": platnosc.id_faktury,
            "kwota": platnosc.kwota,
            "waluta": platnosc.waluta,
            "data_platnosci": platnosc.data_platnosci,
        }
        if not os.path.exists('faktury.json'):
            with open('faktury.json', 'w') as plik:
                plik.write('[]')  # Utwórz pusty plik JSON
        try:
            with open("faktury.json", "r") as plik:
                faktury = json.load(plik)
        except (FileNotFoundError, json.JSONDecodeError):
            faktury = []
            faktury.append({"Faktura": dane_faktury, "Platnosc": dane_platnosci})
            try:    
                with open("faktury.json", "w") as plik:
                    json.dump(faktury, plik)
            except IOError as e:
                print(f"Błąd podczas zapisywania do pliku: {e}")

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
        self.data_platnosci_piatek = None

    def wprowadz_dane(self, dostepne_waluty):
        oplata = str(input("Czy istnieje płatność do faktury? (Tak/Nie)"))
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
                self.waluta = input("Podaj walutę płatności (lub zostaw puste dla PLN): ")
                if self.waluta.strip() == "":
                            self.waluta = "PLN"
                            break
                elif self.waluta not in dostepne_waluty:
                    print("Podana waluta nie jest dostępna. Wybierz jedną z dostępnych walut.")
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
                        self.data_platnosci_piatek = data.strftime('%Y-%m-%d')
                        break
                except ValueError as e:
                    print(e)

def menu():
    while True:
        print("Wybierz tryb działania programu:")
        print("1. Tryb interaktywny")
        print("2. Wyswietl fakturę po ID")
        print("3. Wyjdź")

        wybor = input("Wybierz opcję: ")

        if wybor == "1":
            dostepne_waluty = pobierz_dostepne_waluty()
            if dostepne_waluty is not None:
                najwieksze_id = wczytaj_najwieksze_id()
                faktura = Faktura(najwieksze_id+1)
                faktura.wprowadz_dane(dostepne_waluty)
                platnosc = Platnosc(faktura.id)
                platnosc.wprowadz_dane(dostepne_waluty)
                
                # Pobieranie kursów walut

                if faktura.waluta == "PLN":
                    kurs_faktura = 1
                else:
                    if faktura.data_wystawienia_weekend is not None:


                    else:    
                        dane_faktura, kurs_faktura = pobierz_dane_z_bazy(faktura.waluta, faktura.data_wystawienia)

                if platnosc.waluta == "PLN":
                    kurs_platnosc = 1
                else:
                    dane_platnosc, kurs_platnosc = pobierz_dane_z_bazy(platnosc.waluta, platnosc.data_platnosci)
                faktura.status = "Nie można pobrać kursu waluty."
                if kurs_platnosc is not None and kurs_faktura is not None:
                    # Przeliczanie kwoty faktury i płatności w tych samych walutach
                    if faktura.waluta == platnosc.waluta:
                        if faktura.kwota == platnosc.kwota:
                            faktura.status = "Opłacona w całości"
                        elif faktura.kwota > platnosc.kwota:
                            do_zaplaty = faktura.kwota - platnosc.kwota
                            faktura.status = "Do zapłaty: " + str(do_zaplaty)+ " " + str(faktura.waluta)
                        else:   
                            nadplata = platnosc.kwota - faktura.kwota
                            faktura.status = "Nadpłata: " + str(nadplata) + " " + str(faktura.waluta)
                    # Konwersja na zlotowki walut faktury oraz platnosci, poniewaz strona api podaje kursy danych walut własnie w tej walucie.
                    else:
                        kwota_faktury_w_PLN = faktura.kwota * kurs_faktura
                        kwota_platnosci_w_PLN = platnosc.kwota * kurs_platnosc
                        # Porównanie kwoty faktury i płatności w PLN oraz konwersja do waluty domyślnej
                        if kwota_faktury_w_PLN == kwota_platnosci_w_PLN:
                            faktura.status = "Opłacona w całości"
                        elif kwota_faktury_w_PLN > kwota_platnosci_w_PLN:
                            do_zaplaty_w_PLN = kwota_faktury_w_PLN - kwota_platnosci_w_PLN
                            # Przeliczanie kwoty do zapłaty z powrotem na walutę faktury
                            do_zaplaty = do_zaplaty_w_PLN / kurs_faktura
                            faktura.status = "Do zapłaty: " + str(do_zaplaty)+ " " + str(faktura.waluta)
                        else:   
                            nadplata_w_PLN = kwota_platnosci_w_PLN - kwota_faktury_w_PLN
                            # Przeliczanie kwoty nadpłaty z powrotem na walutę faktury
                            nadplata = nadplata_w_PLN / kurs_platnosc
                            faktura.status = "Nadpłata: " + str(nadplata)+ " " + str(faktura.waluta)
                else:
                    print("Nie można pobrać kursu waluty.")
            # Aktualizacja statusu w pliku i wyswietlenie
            faktura.zapisz_do_pliku(platnosc)
            wyswietl_fakture_po_id(faktura.id)
        elif wybor == "2":
            max = wczytaj_najwieksze_id()
            szukane_id = int(input("Podaj id szukanej faktury od 0 do " + str(max) +": "))
            wyswietl_fakture_po_id(szukane_id)
        elif wybor == "3":
            # Wyjście z programu
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")
#uruchamianie menu
menu()