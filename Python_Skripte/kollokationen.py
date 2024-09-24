import os
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt

# Funktion zum Laden der vorverarbeiteten Captions und Entfernen von '#'
def load_captions_from_folder(folder_path):
    captions = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    caption = f.read().lower().replace('#', '')  # Entfernt das '#' Zeichen
                    captions.append(caption)
    return captions

# Funktion zum Finden von Kollokationen (Wörter, die in einem Text zusammen vorkommen)
def find_collocations(captions, target_words, window_size=5):
    collocations = {word: Counter() for word in target_words}
    for caption in captions:
        tokens = caption.split()  # Angenommen, der Text ist bereits tokenisiert
        for i, token in enumerate(tokens):
            if token in target_words:
                # Umgebende Wörter im definierten Fenster
                window = tokens[max(0, i - window_size): i + window_size + 1]
                collocations[token].update(w for w in window if w != token)
    return collocations

# Funktion zum Erstellen eines Netzwerkdiagramms mit verbesserten visuellen Features
def plot_word_network(collocations, target_word, top_n=30):
    G = nx.Graph()

    # Füge Knoten für das Zielwort und die Top-N Kollokationen hinzu
    G.add_node(target_word, color='red', size=1500)  # Zielwort in Rot, größere Größe
    top_collocations = collocations[target_word].most_common(top_n)
    max_freq = top_collocations[0][1] if top_collocations else 1  # Maximale Häufigkeit

    for word, freq in top_collocations:
        G.add_node(word, color='lightblue', size=1000)  # Kollokationen in Blau, größere Größe
        normalized_weight = freq / max_freq * 5  # Kantenbreite proportional zur Häufigkeit, normalisiert
        G.add_edge(target_word, word, weight=normalized_weight)  # Kante mit normalisierter Breite

    # Zeichne das Netzwerkdiagramm mit verbesserten visuellen Anpassungen
    pos = nx.spring_layout(G, k=0.5)  # Positionierung des Netzwerks
    node_colors = [G.nodes[n]['color'] for n in G.nodes]
    node_sizes = [G.nodes[n]['size'] for n in G.nodes]
    edge_weights = [G.edges[e]['weight'] for e in G.edges]

    plt.figure(figsize=(14, 14))

    # Kantenstärken an die normalisierte Häufigkeit der Kollokationen anpassen
    nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color='gray', alpha=0.7)

    # Knoten und Labels zeichnen
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, edgecolors=None)  # Keine Randfarben
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', font_weight='bold')

    plt.title(f'Wortnetzwerk für "{target_word}" (Top {top_n} Kollokationen)', fontsize=16)
    plt.axis('off')  # Achsen ausblenden
    plt.show()

# Hauptprogramm

# 1. Verzeichnis mit den vorverarbeiteten Instagram-Captions
folder_path = "E:/Datensatz_vorverarbeitet/text_vorverarbeitet"  # Hier den Pfad zum Ordner anpassen

# 2. Captions laden (Hashtags werden entfernt)
captions = load_captions_from_folder(folder_path)

# 3. Zielwörter festlegen
target_words = ['feminism']

# 4. Kollokationen finden
collocations = find_collocations(captions, target_words)

# 5. Netzwerkdiagramme für jedes Zielwort erstellen (mit Begrenzung auf die Top 30 Kollokationen)
for word in target_words:
    plot_word_network(collocations, word, top_n=30)  # Hier die Anzahl der anzuzeigenden Kollokationen auf 30 erhöhen
