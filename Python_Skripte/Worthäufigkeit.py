import os
import collections
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Sicherstellen, dass die NLTK-Daten vorhanden sind
nltk.download('punkt')
nltk.download('stopwords')

# Funktion zum Einlesen der Textdateien aus einem Verzeichnis
def read_files(root_dir):
    text_data = ""
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_data += f.read() + " "  # Texte zusammenführen
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei {file_path}: {e}")
    return text_data

# Vorverarbeitung der Texte: Tokenisierung und Entfernung von Stoppwörtern
def preprocess(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())  # In Kleinbuchstaben umwandeln und tokenisieren
    words = [word for word in words if word.isalpha() and word not in stop_words]  # Nur alphabetische Wörter und keine Stoppwörter
    return words

# Funktion zur Häufigkeitszählung der Wörter
def get_word_frequencies(words):
    word_counter = collections.Counter(words)
    return word_counter.most_common(30)  # Top 30 Wörter zurückgeben

# Funktion zum Erstellen eines Diagramms
def plot_top_words(word_frequencies):
    words, frequencies = zip(*word_frequencies)
    plt.figure(figsize=(10, 6))
    plt.plot(words, frequencies, 'bo-', linewidth=2, markersize=5)
    plt.xlabel('Wörter')
    plt.ylabel('Häufigkeit')
    plt.title('Häufigkeit der Top 30 Wörter')
    plt.grid(True)
    plt.xticks(rotation=45)  # Wörter neigen, damit sie lesbar sind
    plt.show()

# Hauptprogramm
root_directory = "E:/Datensätze/accountsinsta"

# 1. Lese die Textdaten aus den Dateien
text_data = read_files(root_directory)

# 2. Vorverarbeitung der Texte
words = preprocess(text_data)

# 3. Häufigkeitszählung der Wörter
word_frequencies = get_word_frequencies(words)

# 4. Visualisiere die Top 30 Wörter
plot_top_words(word_frequencies)
