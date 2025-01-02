import os

# Den aktuellen Ordner ermitteln, in dem das Skript ausgeführt wird
current_directory = os.getcwd()

# Alle Dateien im aktuellen Verzeichnis auflisten
for filename in os.listdir(current_directory):
    file_path = os.path.join(current_directory, filename)

    # Prüfen, ob es sich um eine Datei handelt (keine Unterordner)
    if os.path.isfile(file_path) and filename.endswith(('.txt', '.csv')):
        print(f"--- Inhalt der Datei: {filename} ---")

        # Dateiinhalt lesen und in der Konsole ausgeben
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                print(file.read())
        except Exception as e:
            print(f"Fehler beim Lesen der Datei {filename}: {e}")
        print("\n")
