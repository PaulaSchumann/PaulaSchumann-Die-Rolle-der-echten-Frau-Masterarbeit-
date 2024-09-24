import instaloader

# Instaloader Objekt erstellen
L = instaloader.Instaloader()

# Profil laden
profile_name = "abiding_home" #Accountname der heruntergeladen werden soll
profile = instaloader.Profile.from_username(L.context, profile_name)

# Posts durchlaufen und nur Bilder und Captions herunterladen
for post in profile.get_posts():
    if not post.is_video:  
        L.download_post(post, target=profile.username)
