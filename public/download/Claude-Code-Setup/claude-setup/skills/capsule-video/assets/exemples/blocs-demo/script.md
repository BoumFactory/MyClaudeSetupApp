# Script — démonstration des blocs « code », « terminal », « compile » et des voix mixtes

## Choix didactiques

- Mini-capsule de 25 à 30 s : le professeur (voix enregistrée, ici simulée par la voix Piper siwis) et Claude (Piper tom) écrivent à tour de rôle un petit cours Typst.
- Le « professeur » est un faux enregistrement avec défauts (« euh », phrase recommencée, longs blancs) nettoyé par `nettoyer_audio.py` ; Claude est synthétisé par `assembler_voix.py`.
- Blocs `[prof]` : texte réellement dit à l'enregistrement. Blocs `[tom]` : texte synthétisé. Les lignes `> visuel` ne sont jamais dites.

## b01 [prof] [pause 0.4]
Aujourd'hui, on écrit un cours de maths en Typst.
> visuel : titre de la capsule, éditeur vide

## b02 [tom] [pause 0.4]
Je suis Claude. Je règle d'abord la langue, puis je pose un titre.
> visuel : frappe des lignes 1 à 3, surlignage de la langue

## b03 [prof] [pause 0.4]
Un signe égal, puis le titre de la leçon.
> visuel : surlignage du signe égal

## b04 [tom] [pause 0.5]
Une formule s'écrit entre dollars : f de x égale deux x plus un.
> visuel : frappe de la formule, surlignage

## b05 [prof] [pause 0.3]
Voilà, je compile.
> visuel : le terminal tape la commande

## b06 [tom] [pause 0.8]
Le terminal confirme : le fichier est compilé, et voici le rendu.
> visuel : coche verte, le rendu apparaît à droite, zoom sur la formule
