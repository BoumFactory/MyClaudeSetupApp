# Grille d'anticipation des usages

Cette grille sert à l'étape 3. Parcours chaque dimension en te demandant : « Concrètement, que se passera-t-il ? » Une dimension sans objet se saute. Le but n'est pas de tout spécifier, mais de repérer les besoins que la demande ne formule pas.

Chaque besoin repéré finit à l'un de ces trois endroits :
- une **décision** (essentielle ou par défaut) dans `05-decisions.md` ;
- une ligne **hors périmètre** ou **évolution** dans `06-perimetre.md` ;
- rien du tout, s'il est trivial ou déjà couvert.

## 1. Le temps

- **Découverte** : comment la personne apprend-elle l'existence de la création, et que voit-elle en premier ?
- **Première fois** : que faut-il installer, comprendre ou régler ? Combien de minutes avant le premier résultat utile ?
- **Usage courant** : la tâche répétée chaque semaine. Combien de clics ou d'étapes ? Qu'est-ce qui deviendra pénible à la dixième fois ?
- **Reprise** : la personne revient après une pause (vacances, année suivante). Retrouve-t-elle son travail ? Les données d'une année se recyclent-elles ?
- **Fin de vie** : comment archiver, exporter, passer à autre chose ?

## 2. Les personnes

- Qui **utilise**, qui **reçoit** le résultat, qui **administre** ou maintient ?
- Le niveau technique de chacun, leur matériel, leur temps disponible.
- **Transmission** : un collègue reprend la création. Que doit-il savoir ? Peut-il la modifier sans l'auteur ?
- **Plusieurs utilisateurs à la fois** : conflits, partage, droits.

## 3. Les situations

- **Lieu et matériel** : salle de classe, vidéoprojecteur, ordinateurs des élèves, téléphone, impression noir et blanc, réseau absent ou filtré.
- **Contraintes de durée** : une séance de 55 minutes, un créneau de 2 heures, cinq minutes en début de cours.
- **Ce qui tourne mal** : fausse manipulation, fichier perdu, panne de réseau, élève absent, mauvaise saisie. Que voit la personne, et comment s'en remet-elle ?
- **Volumes** : de 1 à combien (élèves, classes, fichiers, entrées) ? Que se passe-t-il au maximum ?

## 4. Les sorties

- Qu'est-ce que la personne voudra **emporter** : impression, PDF, export tableur, lien, capture ?
- Dans quel **autre outil** le résultat ira-t-il ensuite : ENT, Pronote, Moodle, un document LaTeX, un mail ?
- Faut-il des **versions** : élève et prof, avec et sans corrigé, projetée et imprimée, différenciées ?

## 5. L'évolution

- Ce que l'utilisateur demandera **juste après** avoir reçu la première version (la question « et maintenant, est-ce qu'on pourrait… ? »).
- Les **variations** prévisibles : autre niveau, autre chapitre, autre classe, autre langue.
- Ce qui doit rester **paramétrable** plutôt que figé dans le code ou le texte.
- Ce que l'architecture doit préserver pour ne pas fermer ces portes, sans les construire maintenant.

## 6. Le cadre

- **Données personnelles** : noms d'élèves, notes, photos. Ce qui est stocké, où, et ce qui ne doit jamais quitter le poste.
- **Cadre institutionnel** : programme officiel, règles de l'établissement, accessibilité (DYS, malvoyance).
- **Droits** : sources réutilisées, licences, publication.
- **Coût** : gratuit exigé ? Clés d'API, abonnements ?

## 7. Spécifique aux ressources pédagogiques

- **Place dans la séquence** : ce qui précède et ce qui suit, les prérequis réels des élèves.
- **Hétérogénéité** : l'élève qui finit en dix minutes, celui qui bloque à la première question.
- **Rôle du professeur** pendant l'usage : il circule, il projette, il corrige au tableau.
- **Trace écrite** : ce que l'élève garde dans son cahier.
- **Évaluation** : comment savoir que l'objectif est atteint.

## 8. Spécifique aux applications

- **Installation** : exécutable, page web, double clic, aucun droit administrateur sur les postes cibles ?
- **Persistance** : où vivent les données, et que deviennent-elles quand on vide le navigateur ou change de poste ?
- **Mises à jour** : comment une nouvelle version arrive sans perdre les données.
- **Diagnostic** : quand ça casse chez l'utilisateur, comment le développeur l'apprend et reproduit le problème.
- **Tests** : ce qui doit être testé automatiquement, ce qui se vérifie à la main.
