# Script — Exercice 5 : tableau croisé d'un énoncé en pourcentages

Un temps fort par section `## id [pause s]`. La pause est le silence placé APRÈS le temps fort.
Texte écrit pour l'oreille : notations dites en toutes lettres (« P de S sachant C »).
Les nombres restent en chiffres ici ; `voix.py` les convertit en mots avant la synthèse.

## b01 [pause 0.6]
Allez, on corrige l'exercice 5 ! Un tableau croisé, construit à partir d'un énoncé en pourcentages.

## b02 [pause 0.4]
Un magasin de sport interroge 600 clients. On a trois informations.

## b03 [pause 0.3]
40 % des clients possèdent la carte de fidélité.

## b04 [pause 0.3]
Chez les porteurs de la carte, 75 % ont fait leurs achats un samedi.

## b05 [pause 0.6]
Et chez les autres clients, cette proportion tombe à 30 %.

## b06 [pause 0.6]
On choisit un client au hasard. C, c'est l'événement : le client possède la carte. Et S : le client a fait ses achats un samedi.

## b07 [pause 1.0]
Quatre questions : construire le tableau croisé, calculer P de C et P de S, puis deux probabilités conditionnelles.

## b08 [pause 0.6]
Question 1 : le tableau croisé. La méthode tient en quatre étapes. Dresser, appliquer au total, appliquer au total de sa ligne, et compléter.

## b09 [pause 0.6]
Étape 1, on dresse le tableau. En lignes : avec carte, sans carte. En colonnes : samedi, et autre jour. Dans le coin, le total : 600 clients.

## b10 [pause 0.6]
Étape 2. Les 40 % portent sur tous les clients. Donc 0,40 fois 600, ça fait 240 clients avec la carte. Il en reste 600 moins 240, soit 360 sans la carte.

## b11 [pause 0.5]
Étape 3, et attention, c'est là le piège ! Les 75 % et les 30 % sont introduits par « chez les ». Ils ne s'appliquent pas à 600, mais au total de leur ligne.

## b12 [pause 0.6]
Avec la carte, le samedi : 0,75 fois 240, ça donne 180. Sans la carte, le samedi : 0,30 fois 360, ça donne 108.

## b13 [pause 0.5]
Étape 4, on complète par différence. Avec carte, autre jour : 240 moins 180, il reste 60. Sans carte, autre jour : 360 moins 108, il reste 252.

## b14 [pause 0.5]
Reste les totaux des colonnes. Le samedi : 180 plus 108, ça fait 288. Un autre jour : 60 plus 252, ça fait 312.

## b15 [pause 1.0]
Petite vérification : 288 plus 312, on retombe bien sur 600. Le tableau est juste !

## b16 [pause 0.5]
Question 2. Une probabilité sans condition se calcule sur l'effectif total : les 600 clients.

## b17 [pause 1.0]
P de C, c'est 240 sur 600, soit 0,4. Et P de S, c'est 288 sur 600, soit 0,48.

## b18 [pause 0.5]
Question 3 : P de S sachant C. Le mot « sachant » nous dit de nous restreindre à la ligne avec carte : 240 clients, dont 180 le samedi.

## b19 [pause 0.5]
P de S sachant C vaut donc 180 sur 240, c'est-à-dire 0,75.

## b20 [pause 1.0]
Et on retrouve les 75 % de l'énoncé ! C'est normal : cette donnée était justement une proportion chez les porteurs de la carte. Ça confirme que notre tableau est correct.

## b21 [pause 0.5]
Question 4 : P de C sachant S. Même méthode, mais cette fois, sachant S, on se restreint à la colonne samedi : 288 clients, dont 180 avec la carte.

## b22 [pause 0.6]
P de C sachant S vaut 180 sur 288, soit 0,625.

## b23 [pause 0.5]
Alors, pourquoi ce n'est pas le même résultat que tout à l'heure ? Regardez : c'est la même case d'intersection, 180. Mais pas le même dénominateur !

## b24 [pause 0.8]
P de S sachant C se calcule sur les 240 porteurs de la carte, et P de C sachant S sur les 288 clients du samedi. Retenez bien : c'est le « sachant » qui donne le dénominateur.
