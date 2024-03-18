import csv
import pandas as pd

class HashTable:
    def __init__(self):
        self.MAX = 1301  # Maximale Anzahl an Aktien, Primzahl, damit die Verteilung der Aktien in der Hashtabelle gleichmäßiger ist
        self.arr = [None for i in range(self.MAX)]  # Leere Liste mit 100 Elementen erstellen

    def get_hash(self, key): 
        #print(f"Test get hash")
        h = 0
        for char in key:
            h += ord(char)  # ASCII-Wert jedes Zeichens im Schlüssel addieren
        return h % self.MAX  # Modulo, um den Index im Array zu erhalten

    def __setitem__(self, key, value):
        h = self.get_hash(key)
        if self.arr[h] is None:
            self.arr[h] = [(key, value)]
        else:
            # Starten Sie die quadratische Sondierung
            j = 1
            while True:
                # Berechnen Sie die neue Hash-Position mit quadratischer Sondierung
                new_h = (h + j**2) % self.MAX
                if self.arr[new_h] is None:
                    self.arr[new_h] = [(key, value)]
                    break
                j += 1
                # Abbruchbedingung, um endlose Schleifen zu vermeiden
                if j > self.MAX:
                    print("Hash-Tabelle ist voll, konnte keinen freien Slot finden.")
                    break


                             
        '''found = False
        # Durchlaufen der Liste am Index h, um den Schlüssel zu finden
        for idx, element in enumerate(self.arr[h]): 
            # Überprüfen, ob der Schlüssel bereits vorhanden ist
            if len(element) == 2 and element[0] == key: 
                self.arr[h][idx] = (key, value)  # Wenn ja, aktualisiere den Wert
                found = True 
                break
        if not found:
            self.arr[h].append((key, value))  # Wenn nicht gefunden, hänge das Element an die Liste an
        '''
    def __getitem__(self, key):
        h = self.get_hash(key)
        j = 0  # Beginne bei 0, um den quadratischen Sondierungsprozess einzuleiten

        while j <= self.MAX:  # Fortsetzen, bis self.MAX Versuche erreicht sind
            new_h = (h + j**2) % self.MAX
            slot = self.arr[new_h]
            if slot is not None:
                for k, v in slot:
                    if k == key:
                        return v  # Gefunden
            j += 1

        return None  # Nicht gefunden nach Durchlaufen aller Slots



    def __delitem__(self, key):
        h = self.get_hash(key)
        j = 0  # Beginnen Sie mit 0, um den ursprünglichen Hash-Slot als ersten Schritt einzubeziehen
        while j <= self.MAX:
            new_h = (h + j**2) % self.MAX
            if self.arr[new_h] is not None:
                for i, (k, v) in enumerate(self.arr[new_h]):
                    if k == key:
                        del self.arr[new_h][i]  # Löschen des gefundenen Elements
                        # Prüfen, ob die Liste jetzt leer ist, und wenn ja, setzen Sie sie auf None
                        if not self.arr[new_h]:
                            self.arr[new_h] = None
                        return
            j += 1
        print(f"Element mit dem Schlüssel {key} wurde nicht gefunden.")

                
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
        count = 0  # Zähler für importierte Kurswerte
        for row in reader:
            if count < 30:  # Maximal 30 Kurswerte importieren
                course_data.append((row['Date'], float(row['Open']), float(row['High']), 
                                    float(row['Low']), float(row['Close']), int(row['Volume']), 
                                    float(row['Adj Close'])))
                count += 1
            else:
                break
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
    stock = hashtable[symbol] # Aktie mit dem Symbol als Schlüssel wird aus der Hashtabelle gesucht
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
    doc_name = input("Wählen Sie einen Namen für die Datei: ")
    data = []
    for slot in hashtable.arr:
        if slot is not None:  # Überprüfen, ob der Slot nicht leer ist
            for key, value in slot:  # Durchlaufen aller Schlüssel-Wert-Paare im Slot
                stock_data_formatted = [{'Date': x[0], 'Open': x[1], 'High': x[2], 'Low': x[3], 'Close': x[4], 'Volume': x[5], 'Adj Close': x[6]} for x in value.course_data]
                data.append({'Name': value.name, 'WKN': value.wkn, 'Symbol': value.symbol, 'StockData': stock_data_formatted})
    df = pd.DataFrame(data)
    df.to_csv(f'{doc_name}.csv', index=False)
    print("Daten als {doc_name}.csv gespeichert.")  

def load_stock(hashtable):
    filename = input("Dateiname zum Laden: ")
    df = pd.read_csv(filename)
    for _, row in df.iterrows():
        symbol = row['Symbol']
        # Erstelle ein Stock-Objekt mit den geladenen Daten
        stock = Stock(row['Name'], row['WKN'], row['Symbol'], row.get('StockData', []))
        # Füge das Stock-Objekt in die Hashtabelle ein
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
