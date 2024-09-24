import torch
from pathlib import Path
from PIL import Image
from collections import Counter
import json
from tqdm import tqdm

# Lade das Modell
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Pfad zum Bildordner
image_folder = Path("E:/Datensätze/bilder_feminism")

# Pfad zur Checkpoint-Datei
checkpoint_file = Path('checkpoint_yolo3899.json')

# Zähle die Objekte
object_counter = Counter()

# Lade den Fortschritt, wenn vorhanden
if checkpoint_file.exists():
    with open(checkpoint_file, 'r') as f:
        checkpoint = json.load(f)
    last_processed_image = checkpoint.get('last_processed_image', '')
    object_counter.update(checkpoint.get('object_counts', {}))
else:
    last_processed_image = ''

# Die Bilder im Ordner verarbeiten
images = list(image_folder.glob('*.jpg'))
start_index = images.index(Path(last_processed_image)) + 1 if last_processed_image else 0

for i in tqdm(range(start_index, len(images)), desc="Processing Images"):
    image_path = images[i]

    # Bild laden
    img = Image.open(image_path)

    # Objekterkennung durchführen
    results = model(img)

    # Labels extrahieren
    labels = results.names  # Mögliche Labels
    detected_labels = results.xyxy[0][:, -1].tolist()
    detected_labels = [labels[int(label)] for label in detected_labels]

    # Zähler aktualisieren
    object_counter.update(detected_labels)

    # Fortschritt speichern
    checkpoint = {
        'last_processed_image': str(image_path),
        'object_counts': dict(object_counter)
    }
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f)

# häufigste Objekte ausgeben
most_common_objects = object_counter.most_common(10)
for obj, count in most_common_objects:
    print(f"{obj}: {count}")


