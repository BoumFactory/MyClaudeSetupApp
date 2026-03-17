export interface VocabTerm {
  term: string
  aliases?: string[]
  definition: string
  docUrl?: string
}

export const VOCABULARY: VocabTerm[] = [
  {
    term: 'Agent',
    aliases: ['Agents', 'agent', 'agents'],
    definition: '<b>Sous-processus IA autonome</b> spécialisé pour une tâche. Utilise des outils et <b>décide seul</b> des actions.',
    docUrl: 'https://code.claude.com/docs/fr/sub-agents',
  },
  {
    term: 'Skill',
    aliases: ['Skills', 'skill', 'skills'],
    definition: '<b>Savoir-faire invocable</b> via <b>/commande</b>. Fichier Markdown avec des instructions réutilisables.',
    docUrl: 'https://code.claude.com/docs/fr/skills',
  },
  {
    term: 'Hook',
    aliases: ['Hooks', 'hook', 'hooks'],
    definition: '<b>Script automatique</b> déclenché avant ou après une action. Élimine les <b>tâches répétitives</b>.',
    docUrl: 'https://code.claude.com/docs/fr/hooks',
  },
  {
    term: 'MCP',
    aliases: ['Model Context Protocol'],
    definition: '<b>Protocole standard</b> pour connecter des <b>outils externes</b> à l\'IA (données, services, APIs).',
    docUrl: 'https://modelcontextprotocol.io',
  },
  {
    term: 'CLAUDE.md',
    definition: '<b>Méta-prompt permanent</b> : instructions lues automatiquement à chaque conversation. Le <b>cerveau</b> de votre config.',
    docUrl: 'https://code.claude.com/docs/fr/memory',
  },
  {
    term: 'Prompt',
    aliases: ['Prompts', 'prompt', 'prompts'],
    definition: '<b>Instruction envoyée</b> à l\'IA. Plus il est <b>précis</b>, meilleure est la réponse.',
  },
  {
    term: 'CLI',
    definition: '<b>Interface en ligne de commande</b>. On tape du texte dans un terminal au lieu de cliquer.',
    docUrl: 'https://code.claude.com/docs/fr/overview',
  },
  {
    term: 'Terminal',
    aliases: ['terminal'],
    definition: 'Application pour <b>exécuter des commandes</b> textuelles. PowerShell (Windows) ou Terminal (Mac).',
  },
  {
    term: 'LaTeX',
    aliases: ['latex'],
    definition: 'Système de <b>composition de documents</b>. Référence en maths pour des <b>formules impeccables</b>.',
    docUrl: 'https://www.latex-project.org',
  },
  {
    term: 'Node.js',
    aliases: ['Node', 'nodejs'],
    definition: '<b>Environnement JavaScript</b> côté serveur. <b>Prérequis</b> pour Claude Code.',
    docUrl: 'https://nodejs.org',
  },
  {
    term: 'API',
    aliases: ['APIs'],
    definition: '<b>Interface de programmation</b> : permet à des logiciels de <b>communiquer entre eux</b>.',
  },
  {
    term: 'Token',
    aliases: ['Tokens', 'token', 'tokens'],
    definition: '<b>Unité de texte</b> traitée par l\'IA (~¾ d\'un mot). Les modèles ont une <b>limite par conversation</b>.',
  },
  {
    term: 'Context window',
    aliases: ['context window', 'fenêtre de contexte'],
    definition: '<b>Mémoire de travail</b> du modèle. Au-delà de la limite, les infos anciennes sont <b>oubliées</b>.',
  },
  {
    term: 'Slash command',
    aliases: ['Slash commands', 'slash command', 'slash commands', 'commande slash', 'commandes slash'],
    definition: 'Commande tapée avec <b>/nom</b> (ex : /help). Accès rapide aux <b>skills et fonctions</b>.',
    docUrl: 'https://code.claude.com/docs/fr/skills',
  },
  {
    term: 'ZIP',
    aliases: ['zip', 'fichier ZIP', 'fichier zip'],
    definition: '<b>Archive compressée</b> regroupant plusieurs fichiers en un seul <b>téléchargement</b>.',
  },
  {
    term: 'Markdown',
    aliases: ['markdown'],
    definition: '<b>Langage de balisage</b> léger : titres (#), listes (-), gras (**). Utilisé pour <b>structurer</b> les prompts.',
    docUrl: 'https://www.markdownguide.org',
  },
  {
    term: 'Pré-plan',
    aliases: ['pré-plan', 'pre-plan', 'Pre-plan'],
    definition: '<b>Document intermédiaire</b> produit par l\'IA pour <b>valider vos choix</b> avant la production finale.',
  },
  {
    term: 'Meta-prompt',
    aliases: ['meta-prompt', 'Meta-Prompt', 'méta-prompt'],
    definition: '<b>Prompt qui génère des prompts</b>. Technique avancée pour produire des instructions optimisées.',
  },
  {
    term: 'Adversarial review',
    aliases: ['adversarial review', 'revue adversariale', 'review adversariale'],
    definition: '<b>Relecture critique</b> par plusieurs agents aux points de vue différents pour <b>améliorer un plan</b>.',
  },
  {
    term: 'Vibe coding',
    aliases: ['vibe coding', 'Vibe Coding', 'vibe coder', 'vibe prompting', 'Vibe prompting'],
    definition: 'Approche <b>essai-erreur</b> : on envoie un prompt, on regarde le résultat, on corrige. <b>Coûteux</b> en tokens et en temps.',
  },
  {
    term: 'Prompt engineering',
    aliases: ['prompt engineering', 'Prompt Engineering', 'ingénierie de prompt', 'architecture du prompt', 'ingénierie du prompt'],
    definition: '<b>Ingénierie / architecture du prompt</b> : approche méthodique pour structurer, planifier et valider avant de produire. Moins d\'allers-retours, <b>meilleur résultat</b>.',
  },
]
