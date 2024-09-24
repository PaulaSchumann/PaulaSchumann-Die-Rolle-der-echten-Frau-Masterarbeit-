import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Herunterladen der benötigten NLTK-Daten
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def combine_text_files(directory):
    combined_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Filtere OCR-spezifische Zeilen heraus
                    if not line.strip().startswith("--- Erkannt in"):
                        combined_text += line
    return combined_text


def preprocess_text(text):
    # Laden der englischen Stoppwörter
    stop_words = set(stopwords.words('english'))

    # Tokenisierung
    tokens = word_tokenize(text.lower())

    # Lemmatisierung
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]

    # Entfernen von Stoppwörtern und nicht-alphabetischen Tokens
    cleaned_words = [word for word in lemmatized if word.isalpha() and word not in stop_words]

    return cleaned_words


def create_word_cloud(text, max_words=100):
    # Vorverarbeitung des Textes
    words = preprocess_text(text)

    # Zählen der Wörter
    word_counts = Counter(words)

    # Auswählen der häufigsten Wörter
    top_words = dict(word_counts.most_common(max_words))

    # Erstellen der Wortwolke
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          max_words=max_words).generate_from_frequencies(top_words)

    # Anzeigen der Wortwolke
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

    # Speichern der Wortwolke als Bild
    wordcloud.to_file("wordcloud.png")


# Hauptprogramm
if __name__ == "__main__":
    directory = "E:/Datensätze/ergebnisse/ocr"
    combined_text = combine_text_files(directory)
    create_word_cloud(combined_text, max_words=50)