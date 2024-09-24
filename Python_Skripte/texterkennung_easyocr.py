import easyocr
import os
import json
from pathlib import Path
from tqdm import tqdm
import cv2

# Erstelle einen Reader für Englisch
reader = easyocr.Reader(['en'])

# ordner
folder_path = Path('E:/accountsinsta/artfulhomemaking')

# Pfad zur Checkpoint-Datei
checkpoint_file = Path('checkpoint_easyocr7.json')

# Pfad zur Ausgabedatei
output_file = Path('ocr_results_artfulhomemaking.txt')

# Lade den Fortschritt, wenn vorhanden
if checkpoint_file.exists():
    with open(checkpoint_file, 'r') as f:
        checkpoint = json.load(f)
    last_processed_image = checkpoint.get('last_processed_image', '')
else:
    last_processed_image = ''

# Verarbeite jedes Bild im Ordner
images = sorted(folder_path.glob('*.jpg'))
start_index = images.index(Path(last_processed_image)) + 1 if last_processed_image else 0

for i in tqdm(range(start_index, len(images)), desc="Processing Images"):
    image_path = images[i]

    # Bild mit OpenCV laden
    img = cv2.imread(str(image_path))

    # Texterkennung durchführen
    result = reader.readtext(img)

    # Erkannten Text extrahieren
    extracted_text = "\n".join([text for (_, text, *_) in result])

    # Ergebnisse in Ausgabedatei schreiben
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f'--- Erkannt in {image_path.name} ---\n')
        f.write(extracted_text.strip() + '\n\n')

    # Fortschritt speichern
    checkpoint = {
        'last_processed_image': str(image_path)
    }
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f)

print(f"Die Ergebnisse wurden in der Datei '{output_file}' gespeichert.")