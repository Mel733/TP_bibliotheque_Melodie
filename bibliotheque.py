import json     #import le module json
from pathlib import Path      #import la classe Path du module pathlib
import csv     #import le module csv

DOSSIER = Path(__file__).parent    #Définie le chemin de DOSSIER qui est le dossier qui contient le fichier
INITIAL = DOSSIER / "catalogue_initial.json"     #définie le chemin de INITIAL qui est le catalogue.json créer a la main
SAUVEGARDE = DOSSIER / "donnees" / "catalogue.json"     #défini le chemin SAUVEGARDE qui se créera dans le dossier parent sous la forme  d'un dossier donné et dedans un fichier json
EXPORT = DOSSIER / "exports" / "catalogue.csv"     #pareil mais pour export
CHAMPS = ("identifiant", "titre", "auteur", "categorie", "exemplaires")    #CHAMPS est un tuple avec les attributs d'un livres

class Livre:    #créer la classe livre
   def __init__(self, identifiant, titre, auteur, categorie, exemplaires):    #le constructeur d'un livres avec ces attributs
      if not isinstance(identifiant, int): #   si l'identifiant n'est pas un int, alors erreur
         raise ValueError("Identifiant invalide")
      self.identifiant = identifiant     #self est l'objet lui meme
      self.titre = titre
      self.auteur = auteur
      self.categorie = categorie
      self.exemplaires = exemplaires

   @property    #getter pour la propriété disponible qui se fait par rapport au nombre d'exemplaire
   def disponible (self):
       if self.exemplaires>0:    #on return true si y'a au moins 1 exemplaire
           return True
       return False    #sinon false
   
   
   def emprunter(self) -> bool:    #methode pour emprunter qui renvoir un booléen
        if not self.disponible:    #si le livre n'est pas disponible
            return False    #return false
        self.exemplaires -= 1    #sinon -1 au nombre d'exemplaire et return true
        return True


   def vers_dict(self) -> dict:    #methode vers dict qui renvoie un dictionnaire avec les donnée necessaires d'un livres (pour l'écrire dans le json)
        return {"identifiant": self.identifiant, "titre": self.titre,   #on return tout les attributs d'un livres dedans
                "auteur": self.auteur, "categorie": self.categorie,
                "exemplaires": self.exemplaires}
   
   def __str__(self):    #affiche les attributs des livres
          return f"{self.identifiant}, {self.titre}, {self.auteur}, {self.categorie}, {self.exemplaires} exemplaire(s)"
       

        

def rechercher_titre(livres: list[Livre], texte: str) -> list[Livre]:    #fonction pour rechercher (texte en string) un livre dans une liste de livres  et qui renvoie une liste de livres
  recherche = texte.strip().casefold()   #la recherche est le texte taper puis nettoyer des espace inutiles et casefold permet de les mettre en minuscule(cette methode est plus forte que le lower)
  return [livre for livre in livres if recherche in livre.titre.casefold()]   #on return la liste des livres dont le titre contient la recherche

         
def trouver_par_id(livres: list[Livre], identifiant: int) -> Livre | None:   #fonction pour rechercher un livre via son id (int) dans une liste de livres et ça renverra un livre ou None
      for livre in livres:    #boucle de livres dans la liste
         if identifiant == livre.identifiant:    #si l'identifant est identique a un identifiant d'un livre
            return livre    #on return le livre
      return None   #sinon on retourne None

def categories(livres: list[Livre]) -> set[str]:   #fonction pour les catégories qui cherchent les catégorie dans la liste et renvoi un set avec les catégorie en str
      resultat = set()    #la variable resultat est un set vide, un set est un ensemble de collection, il n'y a pas de doublons ni d'ordre
      for livre in livres:    #boucle pour chaque livre dans la liste
          resultat.add(livre.categorie)   #on ajoute dans resultat la catégorie du livre
      return resultat   #et on return resultat donc le set
      
def bilan(livres: list[Livre]) -> dict[str, int]: #fonction pour bilan avec la liste de livres qui renverra un dictionnaire avec des clés str et des valeurs int
    #Cette fonction compte les titres, exemplaires et titres disponibles
    stock = 0    #initialise le stock a 0
    disponibles = 0    #pareil pour le disponibles
    for livre in livres:    #boucle pour chaque livre dans liste
        stock += livre.exemplaires    #on augmente le stok selon le nombre d'exmplaire du livre a chaque tour
        if livre.disponible:    #si le livre est disponible
            disponibles += 1    #on fait une incrémentation de 1
    return {"livres": len(livres), "exemplaires": stock,    #on return le nombre de livres selon la longueur de la liste, avec le nombre d'exemplaire et le nombre de disponible
            "disponibles": disponibles}

def afficher_livres(livres: list[Livre]):    #fonction pour afficher la liste de livres
   for livre in livres:     #pour chaque livre dans la liste
    print(livre)    #on l'affiche

def ajouter_livres(livres: list[Livre]) -> None:    #fonction pour ajouter un livre
    titre = input("Titre : ")    #resnigne le titre
    auteur = input("Auteur : ")    #renseigne l'auteur
    categorie = input("Catégorie : ")    #renseigne la catégorie
    try:      #essaye le bloc et si une ValueError arrive on va dans le except
     exemplaire = int(input("Nombres d'exmplaires : "))    #renseigne le nombre d'exemplaire
     if titre.strip() =="":    #si le titre nettoyé est vide
         raise ValueError("Titre invalide")    #on lève une erreur pour ne pas ajouter le livre
     if not livres:    #si il n'y a pas de livre
        identifiant = 1   #id 1
     else :
        identifiant = max(livre.identifiant for livre in livres) + 1   #sinon on prend le plus grand id de la liste et on fait +1
     monlivre = Livre(identifiant, titre, auteur, categorie, exemplaire)   #creation objet monlivre
     livres.append(monlivre)   #on ajoute le livre créer dans la liste
      
    except ValueError:
        print("Invalide")   #erreur si le nombre exemplaire ou le titre est invalide

def total_exemplaires_recursif(livres: list[Livre]) -> int:  #fonction recursive pour additionner les stock depuis la liste et ça va renvoyer un int
    if not livres:    # Si aucun livre dans la liste
        return 0   #return 0
    # Cas récursif : la liste raccourcit d'un livre à chaque appel.
    return livres[0].exemplaires + total_exemplaires_recursif(livres[1:])   #additionne le total exemplaires en appelant sa propre fonction


def lire_catalogue(chemin: Path) -> list[Livre]:   #fonction pour lire le catalogue json a partir du path et ça va renvoyer une liste de livres
    with chemin.open("r", encoding="utf-8") as fichier:   #on ouvre le fichier et on le lit
        donnees = json.load(fichier)    #on charge les donné du json en objet python
    if not isinstance(donnees, list):    #si les donné ne sont pas sous forme de liste
        raise ValueError("Le catalogue doit être une liste JSON.")    #on lève une ValueError
    livres = []   #liste vide de livres
    identifiants = set()    #set d'identifiant vide (pour repérer les doublons)
    for entree in donnees:   #pour chaque entrer dans les donné(fichier json)
        if not isinstance(entree, dict) or set(entree) != set(CHAMPS):    #si l'entrée n'est pas un dict ou si ses clés ne sont pas exactement les champs attendus
            raise ValueError("Une entrée ne contient pas les cinq champs attendus.")  #erreur
        livre = Livre(entree["identifiant"], entree["titre"], entree["auteur"],
                      entree["categorie"], entree["exemplaires"])   #on crée un objet Livre avec les valeurs de l'entrée
        if livre.identifiant in identifiants:   #si l'id du livre est dans les id
            raise ValueError(f"Identifiant en double : {livre.identifiant}") #livre double
        identifiants.add(livre.identifiant)    #on ajoute l'id du livre dans les identifiant
        livres.append(livre)    #on ajoute a la liste livre
    return livres    #on return la liste


def charger_catalogue(initial: Path, sauvegarde: Path) -> list[Livre]:   #fonction pour charger le catatlogue
    #Utilise la sauvegarde si elle existe, sinon le fichier initial.
    try: 
        return lire_catalogue(sauvegarde)   #on retourne le résultat de lire_catalogue sur la sauvegarde
    except FileNotFoundError:     #erreur si le fichier n'existe pas
        return lire_catalogue(initial)   #sinon on lit le fichier initial


def sauvegarder(livres: list[Livre], chemin: Path) -> None:   #fonction pour sauvegarder la liste dans le Path
    #Crée le dossier et écrit les livres en JSON.
    chemin.parent.mkdir(parents=True, exist_ok=True)   #si le dossier donnees existe pas on le crée (pas le fichier)
    with chemin.open("w", encoding="utf-8") as fichier:   #on l'ouvre en écriture (ça efface l'ancien contenu)
        json.dump([livre.vers_dict() for livre in livres], fichier,
                  ensure_ascii=False, indent=2)   #on écrit chaque livre en dict dans le json (accents gardés, indentation de 2)


def exporter(livres: list[Livre], chemin: Path) -> None:
    #Exporte les livres dans l'ordre d'ajout, au format CSV.
    chemin.parent.mkdir(parents=True, exist_ok=True)   #on crée le dossier exports s'il existe pas
    with chemin.open("w", encoding="utf-8", newline="") as fichier:   #newline="" évite les lignes vides en trop dans le csv
        ecrivain = csv.DictWriter(fichier, fieldnames=CHAMPS, delimiter=";")   #écrivain csv avec les champs comme colonnes, séparées par ;
        ecrivain.writeheader()    #on écrit la ligne des titres de colonnes
        for livre in livres:   #pour chaque livre
            ecrivain.writerow(livre.vers_dict())   #on écrit une ligne avec ses infos



def main() -> None:   #fonction pour programme principale
    #Charge le catalogue, puis exécute le menu sans sauvegarde automatique.
    print("Bienvenue dans la bibliothèque !")
    try:
        livres = charger_catalogue(INITIAL, SAUVEGARDE)    #charge le catalogue selon les chemins définis en haut
    except FileNotFoundError as erreur:    #si aucun des deux fichiers n'existe
        print(f"Fichier initial introuvable : {erreur.filename}")   #on affiche le nom du fichier introuvable
        return    #on quitte main
    except json.JSONDecodeError as erreur:    #si le fichier n'est pas un json valide
        print(f"JSON invalide : {erreur}. Corrigez le fichier avant de relancer.")
        return
    except (ValueError, OSError) as erreur:    #si les données sont fausses (ValueError) ou problème de lecture (OSError)
        print(f"Chargement impossible : {erreur}. Corrigez le fichier avant de relancer.")
        return

    while True:    #boucle du menu, elle tourne jusqu'au break
        print("\n1. Lister \n2. Rechercher \n3. Ajouter \n4. Emprunter")
        print("\n5. Enregistrer \n6. Exporter en CSV \n0. Quitter")
        choix = input("Votre choix : ").strip()   #on récupère le choix sans espaces inutiles
        if choix == "0":
            print("Au revoir (aucune sauvegarde automatique).")
            break    #on sort de la boucle while donc le programme se termine
        if choix == "1":
            afficher_livres(livres)   #on affiche tous les livres
        elif choix == "2":
            texte = input("Titre recherché : ")   #le texte à chercher
            afficher_livres(rechercher_titre(livres, texte))   #rechercher_titre renvoie la liste filtrée, et on l'affiche
        elif choix == "3":
            try:    #essaye ce bout de code
                identifiant = int(input("Identifiant : "))   #id en int (ValueError si ce n'est pas un nombre)
                titre = input("Titre : ") 
                auteur = input("Auteur : ")
                categorie = input("Catégorie : ")
                exemplaires = int(input("Exemplaires : "))   #exemplaire en int
                if trouver_par_id(livres, identifiant) is not None:   #si l'id existe deja
                    raise ValueError("Cet identifiant existe déjà.")   #erreur
                livre = Livre(identifiant, titre, auteur, categorie, exemplaires)   #objet livre
            except ValueError as erreur:    #si une erreur lors des input
                print(f"Ajout refusé : {erreur}")
            else:    #le else se lance seulement s'il n'y a pas eu d'erreur
                livres.append(livre)    #on ajoute le livre dans la liste livres
                print("Livre ajouté.")
        elif choix == "4":
            try:
                identifiant = int(input("Identifiant du livre : "))   #id en int
            except ValueError:
                print("L'identifiant doit être un entier.")   #erreur si ce n'est pas un nombre
                continue   #on retourne au début de la boucle (le menu)
            livre = trouver_par_id(livres, identifiant)   #on appelle la fonction trouver_par_id
            if livre is None:    #si le livre est introuvable
                print("Livre introuvable.")
            elif livre.emprunter():    #sinon on l'emprunte avec la méthode emprunter (True si ça a marché)
                print("Emprunt enregistré.")
            else:
                print("Aucun exemplaire disponible.")   #sinon aucun exemplaire dispo
        elif choix == "5":
            try:
                sauvegarder(livres, SAUVEGARDE)    #on écrit la liste dans le json de sauvegarde
                print("Catalogue enregistré.")
            except OSError as erreur:   #si erreur d'enregistrement
                print(f"Enregistrement impossible : {erreur}")
        elif choix == "6":
            try:
                exporter(livres, EXPORT)   #on écrit la liste dans le csv
                print("Catalogue exporté.") 
            except OSError as erreur:   #si erreur d'export
                print(f"Export impossible : {erreur}")
        else:    #si le choix n'est aucun des cas au-dessus
            print("Choix inconnu.")


if __name__ == "__main__":   #lance main() seulement si on exécute ce fichier directement (pas quand il est importé, par exemple par tests.py)
    main()