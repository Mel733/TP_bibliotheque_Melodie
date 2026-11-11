"""Tests autonomes ; les fichiers sont écrits dans un dossier temporaire."""
import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from bibliotheque import (Livre, bilan, categories, charger_catalogue, exporter,
                         lire_catalogue, rechercher_titre, sauvegarder,
                         total_exemplaires_recursif, trouver_par_id)


def doit_echouer(fonction, exception): #on vérifie qu'une fonction lève bien l'erreur attendue
    try:
        fonction() #on lance la fonction
    except exception: #si l'erreur attendue arrive, c'est bon
        return
    raise AssertionError(f"{exception.__name__} attendue") #sinon le test échoue


def tests():
    livres = [Livre(1, "Le petit robot", "Alice Martin", "Science-fiction", 2),
              Livre(2, "Jardin secret", "Bilal Haddad", "Nature", 1),
              Livre(3, "Python pas à pas", "Chloé Bernard", "Informatique", 0)]
    
    assert bilan(livres) == {"livres": 3, "exemplaires": 3, "disponibles": 2} #3 livres, 2+1+0 exemplaires, le livre 3 n'est pas dispo

    assert categories(livres) == {"Science-fiction", "Nature", "Informatique"} #les 3 catégories (set, donc sans doublon)

    assert rechercher_titre(livres, "  PYTHON ") == [livres[2]] #espaces et majuscules ignorés, on trouve que le livre 3

    assert rechercher_titre(livres, "inconnu") == [] #aucun titre ne correspond, liste vide

    assert rechercher_titre(livres, "  ") == livres #recherche vide après strip, donc tous les livres

    assert trouver_par_id(livres, 99) is None #id qui n'existe pas, on renvoie None

    assert trouver_par_id(livres, 1) is livres[0] #on retrouve le bon livre (le même objet)

    assert (total_exemplaires_recursif([]), total_exemplaires_recursif(livres[:1]),
            total_exemplaires_recursif(livres)) == (0, 2, 3)  # tuple : liste vide, 1 livre, 3 livres  
    assert not livres[2].disponible and not livres[2].emprunter() #livre à 0 exemplaire : pas dispo et emprunt impossible

    assert livres[0].emprunter() and livres[0].emprunter() #le livre 1 a 2 exemplaires, donc 2 emprunts réussis

    assert not livres[0].emprunter() and livres[0].exemplaires == 0 #3e emprunt refusé, il reste 0 exemplaire

    assert livres[1].exemplaires == 1  # Une autre instance est inchangée. #emprunter le livre 1 ne touche pas le livre 2

    assert bilan(livres) == {"livres": 3, "exemplaires": 1, "disponibles": 1} #il reste 1 seul exemplaire (livre 2)
    for arguments in [(0, "T", "A", "C", 1), (1, " ", "A", "C", 1),
                      (1, "T", "A", "C", -1), (1, "T", "A", "C", 1.5)]: #4 livres invalides : id 0, titre vide, exemplaires négatif, exemplaires pas un int
        doit_echouer(lambda: Livre(*arguments), ValueError) #chacun doit lever une ValueError

    assert Livre(9, " T ", " A ", " C ", 1).titre == "T" #les espaces autour sont enlevés


    with TemporaryDirectory() as dossier: #dossier temporaire supprimé à la fin du with
        racine = Path(dossier)
        initial = racine / "initial.json"
        sauvegarde = racine / "donnees" / "catalogue.json"
        export = racine / "exports" / "catalogue.csv"
        sauvegarder(livres, initial) #on écrit le fichier initial

        assert bilan(charger_catalogue(initial, sauvegarde)) == bilan(livres) #pas de sauvegarde, donc on lit l'initial et on retrouve les mêmes données
        sauvegarder(livres, sauvegarde) #on crée la sauvegarde
        livres[1].emprunter()  # Non sauvegardé : le disque reste inchangé. #on modifie en mémoire seulement
        charges = charger_catalogue(initial, sauvegarde) #cette fois on lit la sauvegarde

        assert bilan(charges) == {"livres": 3, "exemplaires": 1, "disponibles": 1} #on a bien les données du disque, sans le dernier emprunt
        exporter(charges, export) #on exporte en csv
        with export.open(encoding="utf-8", newline="") as fichier:
            lignes = list(csv.reader(fichier, delimiter=";")) #on relit le csv ligne par ligne (liste de listes)

        assert lignes[0] == ["identifiant", "titre", "auteur", "categorie", "exemplaires"] #1re ligne : les titres de colonnes

        assert lignes[1] == ["1", "Le petit robot", "Alice Martin", "Science-fiction", "0"] #2e ligne : le livre 1 (tout est en str dans un csv)
        sauvegarde.write_text("[]", encoding="utf-8") #on met une liste vide dans la sauvegarde

        assert charger_catalogue(initial, sauvegarde) == [] #la sauvegarde existe, donc on la prend, même vide
        invalide = "{ JSON incorrect"
        sauvegarde.write_text(invalide, encoding="utf-8") #on met un json cassé
        doit_echouer(lambda: charger_catalogue(initial, sauvegarde), json.JSONDecodeError) #on doit avoir une JSONDecodeError
        
        assert sauvegarde.read_text(encoding="utf-8") == invalide #le fichier cassé n'a pas été modifié ni écrasé
        doublon = [charges[0].vers_dict(), charges[0].vers_dict()] #2 fois le même livre (même id)
        sauvegarde.write_text(json.dumps(doublon), encoding="utf-8")
        doit_echouer(lambda: lire_catalogue(sauvegarde), ValueError) #id en double, donc ValueError
        initial.unlink() #on supprime les 2 fichiers
        sauvegarde.unlink()
        doit_echouer(lambda: charger_catalogue(initial, sauvegarde), FileNotFoundError) #plus aucun fichier, donc FileNotFoundError
    print("Tous les tests sont passés.")


if __name__ == "__main__": #lance tests() seulement si on exécute ce fichier directement
    tests()