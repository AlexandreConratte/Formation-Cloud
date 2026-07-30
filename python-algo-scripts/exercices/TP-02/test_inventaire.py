import json

from inventaire import ecrire_rapport, ping
    
     
def test_ping_localhost_repond():
        assert ping("127.0.0.1") is True
     
    
def test_ping_adresse_documentation_ne_repond_pas():
        assert ping("192.0.2.1") is False
    
    
def test_ecrire_rapport(tmp_path):
        resultats = [
            {
                "nom": "bilibili",
                "adresse": "127.0.0.1",
                "role": "test",
                "joignable": True
            },
           {
                "nom": "bulubulu",
                "adresse": "192.0.2.1",
                "role": "test",
                "joignable": False
            },
            {
                "nom": "bolobolo",
                "adresse": "localhost",
                "role": "test",
                "joignable": True
            }
        ]
    
        chemin_rapport_json = tmp_path / "rapport.json"
    
        ecrire_rapport(resultats, chemin_rapport_json)
    
        with open(chemin_rapport_json, encoding="utf-8") as fichier:
            rapport = json.load(fichier)
    
        assert rapport["total"] == 3
        assert rapport["joignables"] == 2
        assert rapport["injoignables"] == 1


