def pokaz_komendy():
    print("\nDostępne komendy:")
    print("saldo - zmiana salda konta")
    print("sprzedaż - sprzedaż produktu")
    print("zakup - zakup produktu")
    print("konto - pokaż stan konta")
    print("lista - pokaż stan magazynu")
    print("magazyn - pokaż konkretny produkt")
    print("przegląd - przegląd operacji")
    print("koniec - zakończ program")

def main():
    saldo = 0
    magazyn = {}  # nazwa_produktu: (ilość, cena)
    historia = []

    while True:
        pokaz_komendy()
        komenda = input("\nWprowadź komendę: ").strip().lower()

        if komenda == "saldo":
            try:
                kwota = float(input("Podaj kwotę (może być ujemna): "))
                opis = input("Opis operacji: ")
                saldo += kwota
                historia.append(("saldo", kwota, opis))
                print(f"Zmieniono saldo o {kwota}. Nowe saldo: {saldo:.2f}")
            except ValueError:
                print("Błąd: nieprawidłowa kwota.")

        elif komenda == "sprzedaż":
            nazwa = input("Nazwa produktu: ")
            if nazwa not in magazyn or magazyn[nazwa][0] <= 0:
                print("Błąd: Produkt niedostępny w magazynie.")
                continue
            try:
                cena = float(input("Cena sprzedaży za sztukę: "))
                sztuk = int(input("Liczba sztuk do sprzedaży: "))
                if sztuk > magazyn[nazwa][0]:
                    print("Błąd: Brak wystarczającej ilości towaru.")
                    continue
                magazyn[nazwa] = (magazyn[nazwa][0] - sztuk, cena)
                saldo += cena * sztuk
                historia.append(("sprzedaż", nazwa, cena, sztuk))
                print(f"Sprzedano {sztuk} szt. '{nazwa}' za {cena * sztuk:.2f}")
            except ValueError:
                print("Błąd: nieprawidłowe dane.")

        elif komenda == "zakup":
            nazwa = input("Nazwa produktu: ")
            try:
                cena = float(input("Cena zakupu za sztukę: "))
                sztuk = int(input("Liczba sztuk do zakupu: "))
                koszt = cena * sztuk
                if cena < 0 or sztuk <= 0:
                    print("Błąd: cena lub ilość nie może być ujemna.")
                    continue
                if saldo < koszt:
                    print("Błąd: niewystarczające środki na koncie.")
                    continue
                saldo -= koszt
                if nazwa in magazyn:
                    magazyn[nazwa] = (magazyn[nazwa][0] + sztuk, cena)
                else:
                    magazyn[nazwa] = (sztuk, cena)
                historia.append(("zakup", nazwa, cena, sztuk))
                print(f"Zakupiono {sztuk} szt. '{nazwa}' za {koszt:.2f}")
            except ValueError:
                print("Błąd: nieprawidłowe dane.")

        elif komenda == "konto":
            print(f"Aktualne saldo: {saldo:.2f}")

        elif komenda == "lista":
            if not magazyn:
                print("Magazyn jest pusty.")
            else:
                print("\nStan magazynu:")
                for produkt, (ilosc, cena) in magazyn.items():
                    print(f"- {produkt}: {ilosc} szt., cena jednostkowa: {cena:.2f}")

        elif komenda == "magazyn":
            nazwa = input("Podaj nazwę produktu: ")
            if nazwa in magazyn:
                ilosc, cena = magazyn[nazwa]
                print(f"{nazwa}: {ilosc} szt., cena: {cena:.2f}")
            else:
                print("Produkt nie znajduje się w magazynie.")

        elif komenda == "przegląd":
            if not historia:
                print("Brak historii operacji.")
                continue
            try:
                od = input("Od którego indeksu? (Enter - od początku): ")
                do = input("Do którego indeksu? (Enter - do końca): ")
                od = int(od) if od else 0
                do = int(do) + 1 if do else len(historia)
                if od < 0 or do > len(historia):
                    print(f"Błąd: Zakres poza historią (0–{len(historia)-1})")
                    continue
                for i in range(od, do):
                    print(f"{i}: {historia[i]}")
            except ValueError:
                print("Błąd: nieprawidłowe indeksy.")

        elif komenda == "koniec":
            print("Zakończono program.")
            break

        else:
            print("Nieznana komenda. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
    if __name__ == "__main__":
    main()

def wczytaj_dane():
    try:
        with open('magazyn.txt', 'r') as f:
            saldo = float(f.readline().strip())
            stan_magazynu = {line.split()[0]: int(line.split()[1]) for line in f.readlines()}
    except FileNotFoundError:
        saldo = 0.0
        stan_magazynu = {}
    return saldo, stan_magazynu

def zapisz_dane(saldo, stan_magazynu):
    with open('magazyn.txt', 'w') as f:
        f.write(f"{saldo}\n")
        for kod, ilosc in stan_magazynu.items():
            f.write(f"{kod} {ilosc}\n")

from datetime import datetime

def dodaj_do_histori(kod_produktu, ilosc, typ_operacji):
    with open('historia.txt', 'a') as f:
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{data} {typ_operacji} {kod_produktu} {ilosc}\n")

def przyjmij_towar(kod_produktu, ilosc, saldo, stan_magazynu):
    if saldo >= ilosc * 10:  # Zakładając, że cena jednostkowa to 10
        saldo -= ilosc * 10
        stan_magazynu[kod_produktu] = stan_magazynu.get(kod_produktu, 0) + ilosc
        dodaj_do_histori(kod_produktu, ilosc, 'Przyjęcie')
        zapisz_dane(saldo, stan_magazynu)
        print(f"Przyjęto {ilosc} sztuk produktu {kod_produktu}.")
    else:
        print("Brak wystarczających środków na koncie.")

def wydaj_towar(kod_produktu, ilosc, saldo, stan_magazynu):
    if stan_magazynu.get(kod_produktu, 0) >= ilosc:
        stan_magazynu[kod_produktu] -= ilosc
        saldo += ilosc * 10  # Zakładając, że cena jednostkowa to 10
        dodaj_do_histori(kod_produktu, ilosc, 'Wydanie')
        zapisz_dane(saldo, stan_magazynu)
        print(f"Wydano {ilosc} sztuk produktu {kod_produktu}.")
    else:
        print("Brak wystarczającej ilości w magazynie.")

def menu():
    saldo, stan_magazynu = wczytaj_dane()
    while True:
        print("\n1. Przyjęcie towaru")
        print("2. Wydanie towaru")
        print("3. Stan magazynu")
        print("4. Historia operacji")
        print("5. Zakończ")
        wybor = input("Wybierz opcję: ")
        if wybor == '1':
            kod = input("Kod produktu: ")
            ilosc = int(input("Ilość: "))
            przyjmij_towar(kod, ilosc, saldo, stan_magazynu)
        elif wybor == '2':
            kod = input("Kod produktu: ")
            ilosc = int(input("Ilość: "))
            wydaj_towar(kod, ilosc, saldo, stan_magazynu)
        elif wybor == '3':
            print("Stan magazynu:")
            for kod, ilosc in stan_magazynu.items():
                print(f"{kod}: {ilosc}")
        elif wybor == '4':
            with open('historia.txt', 'r') as f:
                print(f.read())
        elif wybor == '5':
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowy wybór.")
if __name__ == "__main__":
    menu()

