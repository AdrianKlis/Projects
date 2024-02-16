# Projekt programu do fakturowania i opłacania faktur

Projekt Faktury to aplikacja do generowania i zarządzania fakturami. Umożliwia tworzenie faktur w różnych walutach, przeliczanie kwot na PLN oraz zapisywanie faktur do pliku JSON.

## Wymagania

- Python 3.6 lub nowszy
- Moduły:
   *requests: Jest to biblioteka Pythona używana do wysyłania żądań HTTP. Jest to kluczowe narzędzie do interakcji z API internetowymi.
   *datetime i timedelta z modułu datetime: Są to klasy używane do manipulowania datami i czasem.
   *json: Jest to moduł używany do pracy z danymi JSON. Można go użyć do parsowania danych JSON do słowników Pythona i odwrotnie. 
   *os: Jest to moduł, który dostarcza funkcje do interakcji z systemem operacyjnym, takie jak czytanie zmiennych środowiskowych, manipulowanie ścieżkami plików itp.
   *unittest: Jest to wbudowany moduł Pythona do tworzenia i uruchamiania testów jednostkowych.
   *patch z modułu unittest.mock: Jest to funkcja używana do zastępowania części kodu innymi wartościami lub zachowaniami podczas testowania. Jest to często używane do symulowania odpowiedzi z zewnętrznych usług lub API.

## Instalacja

1. Sklonuj repozytorium na swój komputer.
2. Zainstaluj wymagane moduły za pomocą polecenia `pip install -r requirements.txt`.

## Uruchomienie

Uruchom program za pomocą polecenia `python zadanie.py`.

## Opis funkcji

- `pobierz_dostepne_waluty()`: Pobiera dostępne waluty z API NBP.
- `pobierz_dane_z_bazy(waluta, data)`: Pobiera kurs danej waluty na dany dzień z API NBP.
- `wczytaj_najwieksze_id()`: Wczytuje największe ID faktury z pliku JSON.
- `wyswietl_fakture_po_id(id)`: Wyświetla fakturę o podanym ID.
- `zapisz_do_pliku(platnosci)`: Zapisuje wygenerowane faktury i platności do pliku JSON.
- `Faktura`: Klasa reprezentująca fakturę.
- `Platnosc`: Klasa reprezentująca płatność.

## Autor

Adrian Kliś 52709
