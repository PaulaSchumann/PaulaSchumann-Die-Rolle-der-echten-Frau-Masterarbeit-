import os
import shutil


# Funktion zum Durchsuchen des Datensatzes und Verschieben von Bildern, deren Captions "feminism" enthalten
def move_images_with_feminism(source_dir, target_dir):
    # Erstellen des Zielordners, falls er noch nicht existiert
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Durchlaufe alle Unterordner und Dateien im Quellverzeichnis
    for root, dirs, files in os.walk(source_dir):
        # Sammle alle Timecodes der .txt-Dateien, die "feminism" enthalten
        for file in files:
            if file.endswith('.txt'):  # Nur .txt-Dateien (Captions) durchsuchen
                file_path = os.path.join(root, file)

                # Extrahiere den Timecode aus dem Dateinamen (ohne Erweiterung)
                timecode = file.replace('.txt', '')

                # Datei öffnen und prüfen, ob "feminism" in der Caption vorkommt
                with open(file_path, 'r', encoding='utf-8') as f:
                    caption = f.read()
                    if 'feminism' in caption.lower():  # Suche nach "feminism" (case-insensitive)
                        # Bilddatei mit gleichem Timecode (jpg) suchen
                        image_file = timecode + '.jpg'
                        image_path = os.path.join(root, image_file)

                        # Wenn das Bild existiert, wird es in den Zielordner verschoben
                        if os.path.exists(image_path):
                            target_image_path = os.path.join(target_dir, image_file)
                            shutil.move(image_path, target_image_path)
                            print(f"Bild '{image_file}' verschoben.")


source_directory = "E:/Datensätze/accountsinsta"
target_directory = "E:/Datensätze/bilder_feminism"

# Funktion aufrufen, um die relevanten Bilder zu verschieben
move_images_with_feminism(source_directory, target_directory)
