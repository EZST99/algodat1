import csv
import pandas as pd

class HashTable:
    def __init__(self):
        self.MAX = 100 # Maximale Anzahl an Aktien
        self.arr = [[] for i in range(self.MAX)] # Array mit None initialisieren

    def get_hash(self, key): 
        h = 0
        for char in key:
            h += ord(char)
        return h % self.MAX
    
    def __setitem__(self, key, value):
        h = self.get_hash(key)
        found = False
        #self.arr[h] = value
        for idx, element in enumerate(self.arr[h]): # Durchlaufen der Liste am Index h
            if len(element) == 2 and element[0] == key: # Überprüfen, ob der Schlüssel bereits vorhanden ist
                self.arr[h][idx] = (key, value) # Wenn ja, aktualisiere den Wert
                found = True
                break
        if not found:
            self.arr[h].append((key, value))

    def __getitem__(self, key): 
        h = self.get_hash(key)
        for element in self.arr[h]:
            if element[0] == key:
                return element[1]

    def __delitem__(self, key):
        h = self.get_hash(key)
        for index, element in enumerate(self.arr[h]):
            if element[0] == key:
                del self.arr[h][index]
                break

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
    hashtable[symbol] = Stock(name, wkn, symbol)
    print(f"Aktie {name} hinzugefügt.") 

def delete_stock(hashtable):
    symbol = input("Symbol der Aktie zum Löschen: ")
    del hashtable[symbol]
    print(f"Aktie {symbol} gelöscht.")

def search_stock(hashtable):
    symbol = input("Symbol der Aktie zum Suchen: ")
    stock = hashtable[symbol]
    if stock:
        print(f"Aktie gefunden: {stock.name}, {stock.wkn}, {stock.symbol}")
    else:
        print("Aktie nicht gefunden.")

def plot_stock(hashtable):
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
    data = []
    for slot in hashtable.arr:
        for key, value in slot:
            if value:
                data.append({'Name': value.name, 'WKN': value.wkn, 'Symbol': value.symbol, 'StockData': value.course_data})

    df = pd.DataFrame(data)
    df.to_csv('stocks.csv', index=False)

    '''
    filename = input("Dateiname zum Speichern: ")
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        for element in hashtable.arr:
            for item in element:
                if len(item) == 2:
                    stock = item[1]
                    writer.writerow([stock.name, stock.wkn, stock.symbol, f"{stock.symbol}.csv"])
                    with open(f"{stock.symbol}.csv", 'w') as file:
                        writer = csv.writer(file)
                        for data in stock.course_data:
                            writer.writerow(data)
    print("Daten gespeichert.") '''

def load_stock(hashtable):
    filename = input("Dateiname zum Laden: ")
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stock = Stock(row[1], row[2], row[3], import_stock_data(f"{row[3]}.csv"))
            hashtable[row[3]] = stock
    print("Daten geladen.")

def import_stock(hashtable):
    symbol = input("Symbol der Aktie für den Import: ")
    filename = input("CSV-Dateiname: ")
    stock = hashtable[symbol]
    if stock:
        stock.course_data = import_stock_data(filename)
        print(f"Kursdaten für {symbol} importiert.")
    else:
        print("Aktie nicht gefunden.")
    

def main_menu():
    hashtable = HashTable()  # Neue Hash-Tabelle erstellen
    while True:
        print("\n1. ADD-Aktie hinzufügen")
        print("2. DELETE-Aktie löschen")
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
            '3': import_stock,
            '4': search_stock,
            '5': plot_stock,
            '6': save_stock,
            '7': load_stock,
            '8': exit
            }
            func = switcher.get(choice, lambda: print("Ungültige Eingabe."))
            func(hashtable)

        choice = input("Wählen Sie eine Option: ")
        switch_case(choice)            
    
if __name__ == "__main__":
    main_menu()

    