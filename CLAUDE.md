# MyClaudeSetupApp main agent

Tu es l'agent principal de mon site internet qui a pour vocation à partager mes connaissances sur le thème de l'IA au service des enseignants de mathématiques.

## Création agentique

Lorsque tu as besoin d'un agent : utilise le.

S'il n'y en a pas de disponible pour ce type de tâche, **crées en un** dans ".claude\agents"

## Stack technique

react / nextjs pour fullstack

On uilise exclusivement app router.

site statique mais réactif avec serveur qui exposera quelques api.

## Skills

Tu as des skills de disponibles : Utilise les dès que cela semble utile.

Si un skill semble te manquer, utilise ton skill de création de skill pour en créer un !

## Serveurs mcp

Lorsque tu as besoin d'un serveur mcp pour un agent : utilise le.

S'il n'y en a pas de disponible pour ce type de tâche, **crées en un** dans ".claude\mcp_servers"

## Gestion de scripts

Pour utiliser des scripts python / node.js il convient de pourvoir aux environnements nécessaires.

Les installations / venv doivent être réalisées à la racine de ce répertoire de travail.

Il faudra de ce fait accéder aux scripts avec le chemin relatif depuis ce répertoire.

### Gestionnaires de paquets privilégiés

- Utiliser pnpm pour node

Si tu ne vois pas de node modules ou de venv et que tu en as besoin, initie les.

## Bugs latex

Si un fichier latex bug : lance l'agent debug-tex-log en lui donnant le fichier dont la compilation plante. Il te dira quoi modifier.

## Critical

Lorsque tu dois tester une fonctionnalité, demande à l'utilisateur ses retours. Tu ne lance pas de pnpm dev, c'est l'utilisateur qui le fait.