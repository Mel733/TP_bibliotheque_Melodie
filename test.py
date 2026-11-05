from bibliotheque import charger_livres, Livre, categories, bilan, lister_livres

livres = charger_livres("catalogue_initiale.json")
print(len(livres))
for livre in livres:
    print(livre)

#--------------------------------------------------
try:
    Livre(1, "", "Auteur", "Cat", -1)
except ValueError as e:
    print("OK :", e)

#--------------------------
print(categories(livres))

print(bilan(livres))

lister_livres(livres)