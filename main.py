import csv
import pandas as pd

class HashTable:
    def __init__(self):
        self.MAX = 100  # Maximale Anzahl an Aktien
        self.arr = [[] for i in range(self.MAX)]  # Leere Liste mit 100 Elementen erstellen

    def get_hash(self, key): 
        h = 0
        for char in key:
            h += ord(char)  # ASCII-Wert jedes Zeichens im Schlüssel addieren
        return h % self.MAX  # Modulo, um den Index im Array zu erhalten

    def __setitem__(self, key, value):
        h = self.get_hash(key)
        found = False
        # Durchlaufen der Liste am Index h, um den Schlüssel zu finden
        for idx, element in enumerate(self.arr[h]): 
            # Überprüfen, ob der Schlüssel bereits vorhanden ist
            if len(element) == 2 and element[0] == key: 
                self.arr[h][idx] = (key, value)  # Wenn ja, aktualisiere den Wert
                found = True 
                break
        if not found:
            self.arr[h].append((key, value))  # Wenn nicht gefunden, hänge das Element an die Liste an

    def __getitem__(self, key): 
        h = self.get_hash(key)
        for element in self.arr[h]:
            if element[0] == key:  # Durchlaufen der Liste am Index h, um den Schlüssel zu finden
                return element[1]

    def __delitem__(self, key):
        h = self.get_hash(key)
        for index, element in enumerate(self.arr[h]): 
            if element[0] == key:  # Durchlaufen der Liste am Index h, um den Schlüssel zu finden, wobei [0] den Schlüssel im Tupel darstellt
                del self.arr[h][index]  # Wenn gefunden, lösche das Element
                break

class Stock:
    def __init__(self, name, wkn, symbol, course_data=[]):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        self.course_data = course_data  # Kursdaten für die Aktie

    def add_course_data(self, data):
        self.course_data.append(data)  # Kursdaten hinzufügen

def import_stock_data(filename):
    # Kursdaten aus einer CSV-Datei importieren und als Liste von Tupeln zurückgeben
    course_data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course_data.append((row['Date'], float(row['Open']), float(row['High']), 
                                float(row['Low']), float(row['Close']), int(row['Volume']), 
                                float(row['Adj Close'])))
    return course_data

def add_stock(hashtable):
    # Neue Aktie hinzufügen
    name = input("Name der Aktie: ")
    wkn = input("WKN: ")
    symbol = input("Symbol: ")
    hashtable[symbol] = Stock(name, wkn, symbol) # Aktie wird mit dem Symbol als Schlüssel zur Hashtabelle hinzugefügt
    print(f"Aktie {name} hinzugefügt.") 

def delete_stock(hashtable):
    # Aktie aus der Hashtabelle löschen
    symbol = input("Symbol der Aktie zum Löschen: ")
    del hashtable[symbol] # Aktie mit dem Symbol als Schlüssel wird aus der Hashtabelle gelöscht
    print(f"Aktie {symbol} gelöscht.")

def search_stock(hashtable):
    # Nach einer Aktie in der Hashtabelle suchen
    symbol = input("Symbol der Aktie zum Suchen: ")
    stock = hashtable[symbol]
    if stock:
        print(f"Aktie gefunden: {stock.name}, {stock.wkn}, {stock.symbol}")
    else:
        print("Aktie nicht gefunden.")

def plot_stock(hashtable):
    # Kursdaten einer Aktie plotten
    import matplotlib.pyplot as plt
    symbol = input("Symbol der Aktie zum Plotten: ")
    stock = hashtable[symbol]
    if stock:
        course_data = stock.course_data
        dates = [data[0] for data in course_data]
        close_values = [data[4] for data in course_data]
        plt.plot(dates, close_values)
        plt.xticks(rotation=45, ha='right')  # X-Achsenbeschriftung anpassen
        plt.xlabel('Datum')
        plt.ylabel('Schlusskurs')
        plt.title(f'Schlusskursverlauf von {stock.name}')
        plt.show()
    else:
        print("Aktie nicht gefunden.")

def save_stock(hashtable):
    # Aktien-Daten speichern und plotten
    data = []
    for slot in hashtable.arr:
        for key, value in slot:
            if value:
                data.append({'Name': value.name, 'WKN': value.wkn, 'Symbol': value.symbol, 'StockData': value.course_data})

    df = pd.DataFrame(data)
    df.to_csv('stocks.csv', index=False)
    print(f"Daten als stocks.csv gespeichert.")

def load_stock(hashtable):
    filename = input("Dateiname zum Laden: ")
    df = pd.read_csv(filename)  # CSV-Datei als DataFrame laden
    for _, row in df.iterrows():  # Durchlaufe jede Zeile des DataFrames
        symbol = row['Symbol']
        stock = Stock(row['Name'], row['WKN'], row['Symbol'], import_stock_data(f"{row['Symbol']}.csv"))
        hashtable[symbol] = stock
    print("Daten geladen.")


def import_stock(hashtable):
    # Kursdaten für eine Aktie importieren
    symbol = input("Symbol der Aktie für den Import: ") 
    filename = input("CSV-Dateiname: ")
    stock = hashtable[symbol] # stock speichert die Aktie mit dem Symbol als Schlüssel
    if stock: # Wenn die Aktie gefunden wurde
        stock.course_data = import_stock_data(filename) # Kursdaten importieren und in stock.course_data speichern
        print(f"Kursdaten für {symbol} importiert.")
    else:
        print("Aktie nicht gefunden.")

def main_menu():
    hashtable = HashTable()  # Neue Hash-Tabelle erstellen
    while True:
        # Hauptmenü anzeigen
        print("\n1. ADD-Aktie hinzufügen")
        print("2. DELETE-Aktie löschen")
        print("3. IMPORT-Kursdaten importieren")
        print("4. SEARCH-Aktie suchen")
        print("5. PLOT-Kursdaten plotten")
        print("6. SAVE-Daten speichern und plotten")
        print("7. LOAD-Daten laden")
        print("8. QUIT-Programm beenden")
        # Funktionen je nach Benutzereingabe aufrufen
        choice = input("Wählen Sie eine Option: ")

        match choice:
            case '1':
                add_stock(hashtable)
            case '2':
                delete_stock(hashtable)
            case '3':
                import_stock(hashtable)
            case '4':
                search_stock(hashtable)
            case '5':
                plot_stock(hashtable)
            case '6':
                save_stock(hashtable)
            case '7':
                load_stock(hashtable)
            case '8':
                exit()
            case _:
                print("Ungültige Eingabe.")

if __name__ == "__main__":
    main_menu()
