# Masterarbeit 'Die Rolle der "echten Frau" Masterarbeit: Wie rechte Instagrammerinnen eine anti-feministische Identität erzählen'

Repository zur Masterarbeit 'Die Rolle der „echten Frau“: Wie rechte  Instagrammerinnen eine anti-feministische  Identität erzählen'


Drive-Ordner zur Masterarbeit: Die Rolle der „echten Frau“: Wie rechte Instagrammerinnen eine anti-feministische Identität erzählen

Aufbau des Ornders:


/Python_Skripte - die Python-Skripte, mit denen die Analysen durchgeführt wurden

	/Datensätze_teilen_Bilder.py - Kopieren der Bilder in neuen Ordner, wenn gesuchter Begriff in der Cpation ist *1

	/Datensätze_teilen_Captions.py - Kopieren der txt-files in einen neuen Ordner, wenn der gesuchte Begriff in der Caption ist

	/dominante_farben.py - Farbanalyse der Bilder im Datensatz **

	/hashtags.py - Häufigkeit der im Datensatz vorkommenden Hashtags

	/instaloader_accounts - Scrapen der Accounrs für den Datensatz ***

	/Keywords_im_Zeitrend - die Begriffe "tradwife", "femininity", und "feminism" im Verlauf der Zeit in den Instagram Caprions ****

	/Kollokationen.py - Wörter und Phrasen die mit den untersuchten Begriffen oft gemeinsam auftreten

	/objekt_erkennung.py - Code für die Objekterkennung mit Yolov5 *****

	/ocr_wordcloud.py - Wordcloud wird aus den häufigsten Begriffen, die mit texterkennung_easyocr.py an den Posts ausgewähltter Accounts erkannt wurde 

	/sentiment_analyse.py - Sentiment Analyse mit VADER und TextBlob

	/texterkennung_easyocr.py - Texterkennung mit EasyOCR an ausgewählten Accounts

	/topic_modelling - Topic Modelling Verfahren mit LDA ******

	/Worthäufigkeit - Extrahieren und Visualisieren der häufigsten Wörter

	/zeitliche_entwicklung - Anzahl an Posts, die von allen Accounts in den letzten Jahren gepostet wurden


/Ergebnisse - Ergebnisse der Analysen, in Ordnern nochmal nach Themengebieten unterteilt

	/AntConc - die Ergebnisse der KWIC-Analyse verschiedener Begriffe
	
	/Deskriptive Statistik - in dieser Arbeit durchgeführte statistische Untersuchungen

	/Farbanalyse - Dominante Farben des Hauptdatensatzes und der Sub-Datensäte

	/Kollokationen - Kollokationsnetzwerke der Begriffe feminism und femininity

	/ocr - Ergebnisse der Texterkennung mit EasyOCR + WordCloud der Ergbenisse

	/Screenshots - Screenshots von Instagram-Posts

	/Sentiment_Analyse - Ergebnisse der Sentiment Analyse am gesamten Datensatz und an den Teildatensätzen


Die Datensätze konnten leider wegen der großen Datenmenge nicht hochgeladen werden, sie sind allerdings in der ausgedruckten Version der Arbeit auf dem Datenträger vorhanden



---Voraussetzungen für das Durchführen der Skripte---

- Python 3.8 oder höher

- Folgende Bibliotheken 

	pandas
	matplotlib
	nltk
	numpy
	scikit-learn
	textblob
	Pillow
	opencv-python
	tqdm
	torch
	easyocr
	networkx

- Mindestens 8GB RAM für die Verarbeitung größerer Datensätze

- Internetzugang für das Herunterladen von Daten mit Instaloader



Hinweis: Einige Skripte können längere Laufzeiten haben, besonders bei großen Datensätzen


Anmerkung zu den Skripten:

*1 für das Schreiben des Codes, der die Cpations mit den dazugehörigen Bildern anhand des Timecodes im Titel erkennt, wurde ChatGPT genutzt
  
** hier wurde mit ChatGPT Teile des Codes generiert der Farbwerte ausschließt und Ränder erkennt und ausschließt

*** Da der Vorgang mit Instaloader immer wieder wegen der Rate Limits abgebrochen wurde, wurden Teile des Datensatzes auch über das Terminal 
gesprapt. Dafür wurde dieser Code verwendet:  instaloader --no-videos --post-metadata-txt="caption" abiding_home 

**** Der hier verwendete Code basiert auf dieser Seite https://www.nltk.org/book_1ed/ch02.html

***** Für die Objekterkennung wurde Yolov5 verwendet https://github.com/ultralytics/yolov5

****** Das Topic Modelling wurde mit zufälligen Seeds durchgeführt, um variable, leicht unterschiedliche Ergebnisse zu erzielen und so eine bessere Exploration der Ergebnisse zu ermöglichen

