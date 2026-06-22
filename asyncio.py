import asyncio
import qrcode
from datetime import datetime
from asyncua import Client

AUTOMATE_URL = "opc.tcp://127.0.0.1:4840" 

async def main():
    print("Connexion à l'automate Festo...")
    async with Client(url=AUTOMATE_URL) as client:
        print("Connecté au serveur OPC UA !")
        
        node_trigger = client.get_node("ns=2;s=Palette_Prete")
        node_c1 = client.get_node("ns=2;s=Compo_Compartiment_1")
        node_c2 = client.get_node("ns=2;s=Compo_Compartiment_2")
        node_c3 = client.get_node("ns=2;s=Compo_Compartiment_3")

        print("En attente d'une palette sur la ligne...")
        
        while True:
            try:
                palette_dispo = await node_trigger.get_value()
                
                if palette_dispo:
                    print("Nouvelle palette détectée ! Récupération des données...")
                    
                    comp_c1 = await node_c1.get_value() 
                    comp_c2 = await node_c2.get_value() 
                    comp_c3 = await node_c3.get_value() 
                    
                    maintenant = datetime.now()
                    date_palette = maintenant.strftime("%d/%m/%Y")
                    heure_actuelle = maintenant.strftime("%H:%M")
                    
                    url_festo = (
                        f"https://TomUIMM.github.io/FESTO/"
                        f"?date={date_palette}"
                        f"&debut={heure_actuelle}"
                        f"&fin={heure_actuelle}"
                        f"&c1={comp_c1}"
                        f"&c2={comp_c2}"
                        f"&c3={comp_c3}"
                    )
                    
                    qr = qrcode.make(url_festo)
                    nom_fichier = f"qr_{maintenant.strftime('%d-%m-%Y_%Hh%M%S')}.png" # Ajout des secondes pour éviter les doublons
                    qr.save(nom_fichier)
                    
                    print(f"QR Code généré avec succès : {nom_fichier}")
                    print(f"Lien : {url_festo}")
                    
                    # IMPORTANT : On remet le trigger à False côté simulateur pour attendre la suivante !
                    await node_trigger.set_value(False)
                    print("Trigger réinitialisé, en attente de la prochaine palette...\n")
                    
            except Exception as e:
                print(f"Erreur durant l'échange de données : {e}")
                
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())