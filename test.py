import csv

class HashTable:
    def __init__(self, size=1031):  # Eine Primzahl als Tabellengröße
        self.size = size
        self.table = [None for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def add(self, key, value):
        index = self.hash_function(key)
        if not self.table[index]:
            self.table[index] = [(key, value)]
        else:
            # Einfache Kollisionsbehandlung durch Anhängen an die Liste
            self.table[index].append((key, value))

    def delete(self, key):
        index = self.hash_function(key)
        if self.table[index]:
            self.table[index] = [item for item in self.table[index] if item[0] != key]

    def search(self, key):
        index = self.hash_function(key)
        if self.table[index]:
            for item in self.table[index]:
                if item[0] == key:
                    return item[1]
        return None

class Stock:
    def __init__(self, name, wkn, symbol, course_data=[]):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        self.course_data = course_data

    def add_course_data(self, data):
        self.course_data.append(data)

def import_stock_data(filename):
    course_data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            course_data.append((row['Date'], float(row['Open']), float(row['High']), 
                                float(row['Low']), float(row['Close']), int(row['Volume']), 
                                float(row['Adj Close'])))
    return course_data

def add_stock(hashtable):
    name = input("Name der Aktie: ")
    wkn = input("WKN: ")
    symbol = input("Symbol: ")
    hashtable.add(symbol, Stock(name, wkn, symbol))
    print(f"Aktie {name} hinzugefügt.")

def delete_stock(hashtable):
    symbol = input("Symbol der Aktie zum Löschen: ")
    hashtable.delete(symbol)
    print(f"Aktie {symbol} gelöscht.")

def search_stock(hashtable):
    symbol = input("Symbol der Aktie zum Suchen: ")
    stock = hashtable.search(symbol)
    if stock:
        print(f"Aktie gefunden: {stock.name}, {stock.wkn}, {stock.symbol}")
    else:
        print("Aktie nicht gefunden.")

def plot_course_data(hashtable):
    symbol = input("Symbol der Aktie zum Plotten: ")
    stock = hashtable.search(symbol)
    if stock:
        dates = [data[0] for data in stock.course_data]
        closes = [data[4] for data in stock.course_data]
        import matplotlib.pyplot as plt
        plt.plot(dates, closes)
        plt.show()
    else:
        print("Aktie nicht gefunden.")

def save_data(hashtable):
    filename = input("Dateiname zum Speichern: ")
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        for stock in hashtable.table:
            if stock:
                writer.writerow([stock.name, stock.wkn, stock.symbol]) 
    print("Daten gespeichert.")

def load_data(hashtable):
    filename = input("Dateiname zum Laden: ")
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            hashtable.add(row[2], Stock(row[0], row[1], row[2]))    
    print("Daten geladen.")

def import_course_data(hashtable):
    symbol = input("Symbol der Aktie für den Import: ")
    filename = input("CSV-Dateiname: ")
    stock = hashtable.search(symbol)
    if stock:
        stock.course_data = import_stock_data(filename)
        print(f"Kursdaten für {symbol} importiert.")
    else:
        print("Aktie nicht gefunden.")

def main_menu():
    hashtable = HashTable()
    while True:
        print("\n1. ADD-Aktie hinzufügen")
        print("2, DELETE-Aktie löschen")
        print("3. IMPORT-Kursdaten importieren")
        print("4. SEARCH-Aktie suchen")
        print("5. PLOT-Kursdaten plotten")
        print("6. SAVE-Daten speichern")
        print("7. LOAD-Daten laden")
        print("8. QUIT-Programm beenden")
        def switch_case(choice):
            switcher = {
            '1': add_stock,
            '2': delete_stock,
            '3': import_course_data,
            '4': search_stock,
            '5': plot_course_data,
            '6': save_data,
            '7': load_data,
            '8': exit
            }
            func = switcher.get(choice, lambda: print("Ungültige Eingabe."))
            func(hashtable)

        choice = input("Wählen Sie eine Option: ")
        switch_case(choice)

if __name__ == "__main__":
    main_menu()
