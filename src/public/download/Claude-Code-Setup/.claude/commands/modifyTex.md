# /modifyTex - Modifier un document LaTeX existant

## Description

Apporte les modifications demmandées par l'utilisateur dans un fichier existant en respecant les conventions bfcours.

## Cadre d'intervention

Tu dois utiliser ton skill 'bfcours-latex' pour apporter les modifications demandées par l'utilisateur. 

Ensuite tu utilise ton skill 'tex-compiling-skill' pour compiler le document.

Tu demande à l'utilisateur si cela lui convient et s'il souhaite apporter des modifications. 

## Skills

Tu utilisera à fond le skill 'bfcours-latex' pour la création de documents latex.

## Workflow

1. Lire la source que l'utilisateur veut modifier.
2. Utiliser le skill bfcours-latex pour implémenter le code latex du fichier enonce.tex ou un de ses imports avec les demandes utilisateur.
3. Implémenter les éventuels autres documents annexes nécessaires. Gérer les imports éventuels dans le fichier maître.
4. Utiliser ton skill tex-compiling-skill pour compiler le fichier maître du projet créé.
5. Si le document ne compile pas tu réutilise ton skill bfcours-latex en modifiant les erreurs jusqu'à ce que le fichier compile. 
6. Annoncer à l'utilisateur que la tache est terminée et demander s'il y a d'autres modifications à apporter.
