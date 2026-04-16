# Zadanie: "Wirtualna Półka"
# Stwórz klasę o nazwie Ksiazka, która pozwoli na przechowywanie informacji o tytule i autorze, a także na sprawdzanie, czy książka jest aktualnie dostępna.

# Wymagania:
# Atrybuty (dane):
# tytul (string)
# autor (string)
# czy_dostepna (boolean – domyślnie ustawiony na True)

# Metody (zachowania):
# wypozycz() – Jeśli książka jest dostępna, zmień jej status na False i wypisz komunikat o sukcesie. Jeśli nie, poinformuj, że jest już zajęta.
# oddaj() – Zmień status książki z powrotem na True.
# informacje() – Wypisz w konsoli tekst w stylu: "Książka 'Wiedźmin' – Andrzej Sapkowski [Dostępna/Wypożyczona]".

class Ksiazka:
    def __init__(self, title:str, author:str):
        self.title = title
        self.author = author
        self.czy_dostepna = True
    def informacje(self):
        if self.czy_dostepna == True:
            print(f"Ksiazka {self.title} - {self.author} jest dostepna")
        else:
            print(f"Ksiazka {self.title} - {self.author} jest niedostepna")
    def oddaj(self):
        self.czy_dostepna = True
    def wypozycz(self):
        if self.czy_dostepna == False:
            print(f"Ksiazka {self.title} - {self.author} jest niedostepna")
        self.czy_dostepna = False

ksiazka1 = Ksiazka("Krew Elfow", "Andrzej Sapkowski")
ksiazka2 = Ksiazka("Czas Pogardy", "Andrzej Sapkowski")
ksiazka3 = Ksiazka("Ostatnie zyczenie", "Andrzej Sapkowski")

ksiazka1.informacje()
ksiazka1.wypozycz()
ksiazka1.wypozycz()
ksiazka1.informacje()
ksiazka1.oddaj()
ksiazka1.informacje()

# Twoje "Następny Poziom" (Level Up)
# Jeśli czujesz się na siłach, spróbuj rozbudować swój system o klasę Biblioteka:

# Stwórz klasę Biblioteka.
# Powinna ona mieć listę ksiazki (jako atrybut).
# Dodaj metodę dodaj_ksiazke(self, nowa_ksiazka), która przyjmuje obiekt klasy Ksiazka i wrzuca go do listy.
# Dodaj metodę pokaz_wszystkie(), która przejdzie pętlą for przez listę i wywoła informacje() dla każdego obiektu.