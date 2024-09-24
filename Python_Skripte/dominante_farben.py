import os
import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
import pickle
import time
import cv2

def get_dominant_colors(image_path, num_colors=5):
    img = Image.open(image_path)
    img_array = np.array(img)

    # Schwarze und weiße Ränder entfernen
    non_border = np.where((img_array != 0) & (img_array != 255))
    if len(non_border[0]) > 0 and len(non_border[1]) > 0:
        img_array = img_array[non_border[0].min():non_border[0].max(),
                    non_border[1].min():non_border[1].max()]

    img = Image.fromarray(img_array)
    img = img.resize((100, 100))
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # ZU OpenCV konvertieren
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Gaußschen Weichzeichner anwenden um Rauschen zu verringern
    img_cv = cv2.GaussianBlur(img_cv, (5, 5), 0)

    # Zu Lab color space konvertieren
    lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2Lab)

    # Salienzkarte berechnen
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (success, saliencyMap) = saliency.computeSaliency(lab)
    saliencyMap = (saliencyMap * 255).astype("uint8")

    # Threshold Salienzkarte
    thresh = cv2.threshold(saliencyMap, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Salienzkarte als Maske anwenden
    img_masked = cv2.bitwise_and(img_cv, img_cv, mask=thresh)

    # Zu PIL
    img = Image.fromarray(cv2.cvtColor(img_masked, cv2.COLOR_BGR2RGB))

    # Farben reduzieren
    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    img = img.convert('RGB')

    pixels = list(img.getdata())
    # Ganz helle und ganz dinkle Farben ignorieren
    pixels = [p for p in pixels if 50 < sum(p) < 700]  # Schwellenwert
    color_counts = Counter(pixels)
    return color_counts.most_common(num_colors)

def analyze_jpgs_in_folder(root_folder_path, checkpoint_file, batch_size=500):
    all_colors = Counter()
    file_count = 0
    processed_files = set()
    total_files = 0

    # Checkpoint laden, falls vorhanden
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'rb') as f:
            checkpoint = pickle.load(f)
            processed_files = checkpoint['processed_files']
            all_colors = Counter(checkpoint['color_counts'])
            file_count = checkpoint['file_count']
            total_files = checkpoint['total_files']
    else:
        # Erster Durchlauf zur Zählung der Gesamtdateien
        for subdir, _, files in os.walk(root_folder_path):
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    total_files += 1

        checkpoint = {'processed_files': processed_files, 'color_counts': all_colors, 'file_count': file_count,
                      'total_files': total_files}

    start_time = time.time()
    last_time = start_time

    for subdir, _, files in os.walk(root_folder_path):
        batch = []
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg')):
                file_path = os.path.join(subdir, filename)
                if file_path not in processed_files:
                    batch.append(file_path)
                    if len(batch) >= batch_size:
                        # Batch verarbeiten
                        for file_path in batch:
                            try:
                                dominant_colors = get_dominant_colors(file_path)
                                all_colors.update(dict(dominant_colors))
                                file_count += 1
                                processed_files.add(file_path)
                            except Exception as e:
                                print(f"Fehler bei der Verarbeitung von {filename} in {subdir}: {str(e)}")

                        # Checkpoint speichern
                        checkpoint = {
                            'processed_files': processed_files,
                            'color_counts': all_colors,
                            'file_count': file_count,
                            'total_files': total_files
                        }
                        with open(checkpoint_file, 'wb') as f:
                            pickle.dump(checkpoint, f)

                        # Verbleibende Zeit schätzen
                        elapsed_time = time.time() - start_time
                        time_since_last_update = time.time() - last_time
                        estimated_total_time = (elapsed_time / file_count) * total_files
                        estimated_time_left = estimated_total_time - elapsed_time
                        print(
                            f"Verarbeitet {file_count}/{total_files} Dateien. Geschätzte verbleibende Zeit: {estimated_time_left / 60:.2f} Minuten")

                        last_time = time.time()
                        batch = []  # Batch leeren

        # Alle verbleibenden Dateien im letzten Batch verarbeiten
        if batch:
            for file_path in batch:
                try:
                    dominant_colors = get_dominant_colors(file_path)
                    all_colors.update(dict(dominant_colors))
                    file_count += 1
                    processed_files.add(file_path)
                except Exception as e:
                    print(f"Fehler bei der Verarbeitung von {filename} in {subdir}: {str(e)}")
            # Checkpoint speichern
            checkpoint = {
                'processed_files': processed_files,
                'color_counts': all_colors,
                'file_count': file_count,
                'total_files': total_files
            }
            with open(checkpoint_file, 'wb') as f:
                pickle.dump(checkpoint, f)

            # Verbleibende Zeit schätzen
            elapsed_time = time.time() - start_time
            time_since_last_update = time.time() - last_time
            estimated_total_time = (elapsed_time / file_count) * total_files
            estimated_time_left = estimated_total_time - elapsed_time
            print(
                f"Verarbeitet {file_count}/{total_files} Dateien. Geschätzte verbleibende Zeit: {estimated_time_left / 60:.2f} Minuten")

    # Abschlussnachricht
    print(f"Verarbeitung abgeschlossen. Gesamt verarbeitete Dateien: {file_count}/{total_files}")

    return all_colors, file_count

def print_color_statistics(all_colors, file_count):
    total_pixels = sum(all_colors.values())
    print(f"Analysierte {file_count} JPG-Dateien")
    print(f"Gesamtanzahl der verarbeiteten Pixel: {total_pixels}")
    print("\nTop 20 dominante Farben in allen Bildern:")
    for color, count in all_colors.most_common(20):
        percentage = (count / total_pixels) * 100
        print(f"  RGB: {color}, Anzahl: {count}, Prozentsatz: {percentage:.2f}%")

def plot_color_distribution(all_colors, save_path='Farbverteilung.png'):
    colors, counts = zip(*all_colors.most_common(20))

    # RGB-Werte auf Bereich 0-1 normalisieren
    normalized_colors = [(r / 255, g / 255, b / 255) for r, g, b in colors]

    plt.figure(figsize=(15, 8))
    bars = plt.bar(range(len(colors)), counts, color=normalized_colors)
    plt.xlabel('Farben (RGB)')
    plt.ylabel('Pixelanzahl')
    plt.title('Top 20 dominante Farben in allen Bildern')
    plt.xticks(range(len(colors)), [str(c) for c in colors], rotation=90)

    # Farbkennzeichnungen oben auf jede Leiste setzen
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height}',
                 ha='center', va='bottom', rotation=90)

    plt.tight_layout()

    # Grafik speichern
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Grafik anzeigen
    plt.show()

# Ordner
root_folder_path = "E:/Datensätze/accountsinsta"
checkpoint_file = "checkpoint.pkl"
all_colors, file_count = analyze_jpgs_in_folder(root_folder_path, checkpoint_file)
print_color_statistics(all_colors, file_count)
plot_color_distribution(all_colors)
