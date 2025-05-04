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
