import csv

class Stock:
    

def main_menu():
    choice = input("1: Aktie hinzufügen\n2: Aktie löschen\n3: Aktie suchen\n4: Kursdaten plotten\n5: Daten speichern\n6: Daten laden\n7: Kursdaten importieren\n 8: Beenden\n")
    def scan_input(choice):
        match choice:
            case 1:
                add_stock()
            case 2:
                delete_stock()
            case 3:
                import_stock()
            case 4:
                search_stock()
            case 5:
                plot_stock()
            case 6:
                save_stock()
            case 7:
                load_stock()
            case 8:
                print("Programm beendet")
                exit()

            case _: 
                print("Ungültige Eingabe")
             
    
if __name__ == "__main__":
    main_menu()