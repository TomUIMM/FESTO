pip install qrcode pillow
import qrcode

# L'URL exacte pointant vers ton GitHub avec des données de test
url_festo = (
    "https://lohouevan-alt.github.io/Festo-tracking/"
    "?date=22/06/2026"
    "&debut=09:15"
    "&fin=09:17"
    "&c1=2R1V2B"
    "&c2=3R3V1B"
    "&c3=1R1V1B"
)

# Configuration du QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Ajout du lien
qr.add_data(url_festo)
qr.make(fit=True)

# Création et sauvegarde de l'image
img = qr.make_image(fill_color="black", back_color="white")
img.save("vrai_qr_test.png")

print("Génération réussie ! Ouvre le fichier 'vrai_qr_test.png' pour le scanner.")