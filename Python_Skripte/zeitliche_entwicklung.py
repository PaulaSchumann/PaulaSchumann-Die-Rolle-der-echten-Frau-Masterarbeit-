import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Funktion zum Einlesen von Textdateien und Extrahieren der Zeitstempel aus den Dateinamen
def read_files_with_timestamps(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    # Extrahiere den Zeitstempel aus dem Dateinamen im Format YYYY-MM-DD_HH-MM-SS_UTC.txt
                    timestamp_str = file.split('_UTC')[0]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                    data.append(timestamp)
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei {file_path}: {e}")
    return data

# Funktion zur Analyse der Anzahl der Posts über die Zeit
def analyze_posts_over_time(timestamps):
    # Erstelle ein DataFrame mit den Timestamps
    df = pd.DataFrame({'Timestamp': timestamps})

    # Setze den Timestamp als Index
    df.set_index('Timestamp', inplace=True)

    # Zähle die Anzahl der Posts pro Monat
    posts_per_month = df.resample('M').size()

    return posts_per_month

# Visualisierung der Anzahl der Posts über die Zeit
def plot_post_trends(posts_per_month):
    plt.figure(figsize=(12, 8))

    # Plot für die Anzahl der Posts
    posts_per_month.plot(label='Anzahl der Posts', color='blue')

    # Plot-Anpassungen
    plt.title('Anzahl der Posts über die Zeit')
    plt.xlabel('Datum')
    plt.ylabel('Anzahl')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Platziere die Legende außerhalb des Plots
    plt.grid(True)
    plt.xticks(rotation=45)

    # Setze den Bereich der x-Achse auf den ersten und letzten Post
    plt.xlim(posts_per_month.index.min(), posts_per_month.index.max())

    plt.tight_layout()
    plt.show()

# eingelesenr Ordner
root_directory = "E:/Datensätze/accountsinsta"

# 1. Lese die Dateien und extrahiere die Zeitstempel
timestamps = read_files_with_timestamps(root_directory)

# 2. Analyse der Anzahl der Posts über die Zeit
posts_per_month = analyze_posts_over_time(timestamps)

# 3. Visualisiere die Trends
plot_post_trends(posts_per_month)
