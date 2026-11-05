import json
class Livre:
   def __init__(self, identifiant, titre, auteur, categorie, exemplaires):
      if not isinstance(identifiant, int):
         raise ValueError("Titre invalide")
      self.identifiant = identifiant
      self.titre = titre
      self.auteur = auteur
      self.categorie = categorie
      self.exemplaires = exemplaires

   @property
   def disponible (self):
       if self.exemplaires>0:
           return True
       return False
   
   
   def emprunter(self):
       if self.exemplaires > 0:
         self.exemplaires -=1
       return False

   def __str__(self):
          return f"{self.identifiant}, {self.titre}, {self.auteur}, {self.categorie}, {self.exemplaires}"
       
   
def charger_livres(chemin: str) -> list[Livre]:
    with open(chemin, "r", encoding="utf-8") as f:
        donnees = json.load(f)
    livres = []
    for d in donnees:
        livres.append(Livre(d["identifiant"], d["titre"], d["auteur"], d["categorie"], d["exemplaires"]))
    return livres

        

def rechercher_titre(livres: list[Livre], texte: str) -> list[Livre]:
    texte = texte.lower()
    resultats = []
    for livre in livres:
        if texte in livre.titre.lower():
            resultats.append(livre)
    return resultats
         
def trouver_par_id(livres: list[Livre], identifiant: int) -> Livre | None:
      for livre in livres:
         if identifiant == livre.identifiant:
            return livre
      return None

def categories(livres: list[Livre]) -> set[str]:
      resultat = set()
      for livre in livres:
          resultat.add(livre.categorie)
      return resultat
      
def bilan(livres: list[Livre]) -> dict[str, int]:
     compteur_diponible = 0
     compteur_exemplaire = 0
     compteur_livre = 0
     for livre in livres:
         compteur_exemplaire += livre.exemplaires
         compteur_livre +=1
         if livre.disponible:
          compteur_diponible += 1
        
     return {"livre": compteur_livre, "exemplaire": compteur_exemplaire, "disponible":compteur_diponible}

def lister_livres(livres: list[Livre]):
   for livre in livres:
    print(livre)
   return livre

def ajouter_livres(livres: list[Livre]) -> None:
    titre = input("Titre : ")
    auteur = input("Auteur : ")
    categorie = input("Catégorie : ")
    try:
     exemplaire = int(input("Nomres d'exmplaires : "))
     if titre.strip() =="":
         print("Titre invalide")
     if not livres:
        identifiant = 1
     else :
        identifiant = max(livre.identifiant for livre in livres) + 1
     monlivre = Livre(identifiant, titre, auteur, categorie, exemplaire)
     livres.append(monlivre)
      
    except ValueError:
        print("Invalide")




def affichage_menu(livres):
  
   while True:
     try:
        print("=====BIBLIOTHEQUE=====")
        print("1.Lister\n2.Rechercher par titre\n3.Ajouter\n4.Emprunter\n5.Enregistrer\n6.Exporter en CSV\n0.Quitter")
  
        choix = int(input("Que voulez faire ? "))
        if choix == 1:
            lister_livres(livres)
        elif choix == 2:
            texte= input("Quelle livre : ")
            resultat = rechercher_titre(livres, texte)
            if resultat:
                print ("Trouvé")
            else :
                print("Pas trouvé")
        elif choix ==3:
            ajouter_livres(livres)
        elif choix == 4:
            identifiant = int(input("Quelle id du livre : "))
            livre = trouver_par_id(livres, identifiant)
            if not livre:
                print("Livre introuvable")
            if livre.emprunter():
                print("Sa a marché")
            else :
                print("Plus d'exmplaires")
         # elif choix == 5:
            
            
            
        else:
           print("Choix valide")
     except ValueError:
       print("Choix invalide")
   
livres = charger_livres("catalogue_initiale.json")     
if __name__ == "__main__":
    affichage_menu(livres)
      