import os
import string
import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# NLTK Ressourcen downloaden
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


# Textdateien einlesen
def read_text_files_from_folder(folder_path):
    texts = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    texts.append(text)
    return texts


# Text vorverarbeiten
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and len(word) >= 3]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    text = ' '.join(tokens)
    return text


# Funktion zum Ausführen des LDA-Modells
def run_lda_model(X, feature_names, n_topics=5, random_seed=None):
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=random_seed)
    lda.fit(X)

    print(f"Ergebnisse für Seed: {random_seed}")
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic {topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))
        print()


# Hauptprogramm
folder_path = "E:/Datensätze/accountsinsta"
data = read_text_files_from_folder(folder_path)
preprocessed_data = [preprocess_text(doc) for doc in data]

vectorizer = CountVectorizer(min_df=2, token_pattern=r'\b\w{3,}\b')
X = vectorizer.fit_transform(preprocessed_data)
feature_names = vectorizer.get_feature_names_out()

# Mehrere Durchläufe mit verschiedenen Seeds
num_runs = 3
for i in range(num_runs):
    random_seed = random.randint(1, 1000)
    run_lda_model(X, feature_names, n_topics=5, random_seed=random_seed)
    print("=" * 50)