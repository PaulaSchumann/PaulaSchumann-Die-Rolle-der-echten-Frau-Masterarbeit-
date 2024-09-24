import os
from collections import Counter
import matplotlib.pyplot as plt

# Funktion zum Laden der Captions und Hashtags
def load_captions_and_hashtags(folder_path):
    captions = []
    hashtags = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            caption = line.strip()
                            if caption:
                                captions.append(caption)
                                hashtags.extend([tag for tag in caption.split() if tag.startswith('#')])
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
    return captions, hashtags

# Funktion zur Analyse der Hashtags
def analyze_hashtags(hashtags):
    hashtag_counts = Counter(hashtags)
    return hashtag_counts

# Funktion zum Plotten der Top-Hashtags mit Grid
def plot_top_hashtags(hashtag_counts, top_n=20):
    most_common = hashtag_counts.most_common(top_n)
    labels, values = zip(*most_common)

    plt.figure(figsize=(10, 8))
    plt.barh(labels, values, color='skyblue')
    plt.xlabel('Häufigkeit')
    plt.title('Top 20 Hashtags')
    plt.gca().invert_yaxis()
    plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
    plt.subplots_adjust(left=0.3)  # Linken Rand anpassen
    plt.show()


# Pfad zum Hauptordner ersetzen
main_folder = "E:/Datensätze/accountsinsta"
captions, hashtags = load_captions_and_hashtags(main_folder)

if hashtags:
    hashtag_counts = analyze_hashtags(hashtags)

    # Top-Hashtags anzeigen
    print("\nTop Hashtags:")
    for hashtag, count in hashtag_counts.most_common(20):
        print(f"{hashtag}: {count}")

    # Top-Hashtags plotten
    plot_top_hashtags(hashtag_counts)

else:
    print("No hashtags found in the dataset.")
