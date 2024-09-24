import os
import shutil


# Funktion zum Durchsuchen des Datensatzes und Kopieren von Captions, die "feminism" enthalten
def copy_files_with_feminism(source_dir, target_dir):
    # Erstellen des Zielordners, falls er noch nicht existiert
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Durchlaufe alle Unterordner und Dateien im Quellverzeichnis
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.txt'):  # Nur .txt-Dateien (Captions) durchsuchen
                file_path = os.path.join(root, file)

                # Datei öffnen und prüfen, ob "feminism" in der Caption vorkommt
                with open(file_path, 'r', encoding='utf-8') as f:
                    caption = f.read()
                    if 'feminism' in caption.lower():  # Suche nach "feminism" (case-insensitive)
                        # Zielpfad für die Datei festlegen
                        target_file_path = os.path.join(target_dir, file)

                        # Datei in den Zielordner kopieren
                        shutil.copyfile(file_path, target_file_path)
                        print(f"Datei '{file}' kopiert.")


source_directory = "E:/Datensätze/accountsinsta" 
target_directory = "E:/Datensätze/feminism_posts"

# Funktion aufrufen, um die relevanten Captions zu kopieren
copy_files_with_feminism(source_directory, target_directory)
