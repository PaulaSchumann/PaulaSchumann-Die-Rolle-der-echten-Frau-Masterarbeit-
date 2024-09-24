import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from datetime import datetime

# Sicherstellen, dass die NLTK-Daten vorhanden sind
nltk.download('punkt')
nltk.download('stopwords')


# Funktion zum Einlesen von Textdateien und Extrahieren der Zeitstempel aus den Dateinamen
def read_files_with_timestamps(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    # Extrahiere den Zeitstempel aus dem Dateinamen im Format YYYY-MM-DD_HH-MM-SS_UTC.txt
                    timestamp_str = file.split('_UTC')[0]
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                    data.append((timestamp, text))
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei {file_path}: {e}")
    return data


# Vorverarbeitung der Texte: Tokenisierung, Entfernung von Stoppwörtern
def preprocess(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())  # In Kleinbuchstaben umwandeln und tokenisieren
    words = [word for word in words if
             word.isalpha() and word not in stop_words]  # Nur alphabetische Wörter und keine Stoppwörter
    return words


# Funktion zur Analyse der Häufigkeit bestimmter Wörter über die Zeit
def analyze_word_frequency_over_time(data, target_words):
    # Erstelle ein DataFrame mit Zeitstempeln und Texten
    df = pd.DataFrame(data, columns=['Timestamp', 'Text'])

    # Spalte für die Worthäufigkeit hinzufügen
    for word in target_words:
        df[word] = df['Text'].apply(lambda text: preprocess(text).count(word))

    # Resample nach Zeitintervallen
    df.set_index('Timestamp', inplace=True)
    df_resampled = df.resample('M').sum()  # 'M' für monatliche Zusammenfassung

    return df_resampled


# Visualisierung der Häufigkeit der Wörter über die Zeit
def plot_word_trends(df_resampled, target_words):
    plt.figure(figsize=(10, 6))
    for word in target_words:
        plt.plot(df_resampled.index, df_resampled[word], label=word)

    plt.xlabel('Zeit')
    plt.ylabel('Häufigkeit')
    plt.title('Worttrends über die Zeit')
    plt.legend()
    plt.grid(True)
    plt.show()


# Ordner der eingelesen wird
root_directory = "E:/Datensätze/accountsinsta"

# 1. Lesen der Dateien und extrahiere der Zeitstempel
data = read_files_with_timestamps(root_directory)

# 2. Analyse der Wortfrequenz für bestimmte Zielwörter
target_words = ['feminism', 'femininity', 'tradwife' ]
df_resampled = analyze_word_frequency_over_time(data, target_words)

# 3. Visualisierung der Trends
plot_word_trends(df_resampled, target_words)
