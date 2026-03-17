import { Parcours, Capsule } from '@/types/tutorial'

/**
 * Définition des parcours de formation
 */
export const PARCOURS: Parcours[] = [
  {
    id: 'quick-view',
    title: 'Quick View',
    description: 'Comprendre le système en 5 minutes',
    icon: 'Zap',
    color: 'amber',
    capsules: ['qv-overview'],
  },
  {
    id: 'claude-desktop',
    title: 'Claude Desktop',
    description: 'Installer et configurer Claude Desktop',
    icon: 'Monitor',
    color: 'emerald',
    capsules: ['cd-install', 'cd-config', 'cd-extensions', 'cd-first-prompt', 'cd-projects'],
  },
  {
    id: 'prompt-craft',
    title: 'Communiquer avec un système d\'agents IA',
    description: 'Structurer ses prompts, invoquer les bons outils, co-construire avec l\'IA',
    icon: 'MessageSquareText',
    color: 'violet',
    capsules: ['pc-structure', 'pc-sources', 'pc-skills-agents', 'pc-idea-challenger', 'pc-preplan', 'pc-adversarial', 'pc-synthesis', 'pc-models'],
  },
  {
    id: 'claude-code',
    title: 'Agents CLI',
    description: 'Maîtriser les agents CLI : Claude Code, Codex et Gemini CLI',
    icon: 'Terminal',
    color: 'cosmic',
    capsules: ['cc-install', 'cc-config', 'cc-commands', 'cc-dotclaude', 'cc-bfcours-setup'],
  },
  {
    id: 'avance',
    title: 'Avancé',
    description: 'Architecture agents, skills et hooks',
    icon: 'Sparkles',
    color: 'nebula',
    capsules: ['av-architecture', 'av-meta-prompt', 'av-skill-creator', 'av-hooks', 'av-share', 'av-subagents', 'av-teamplay'],
  },
]

/**
 * Définition de toutes les capsules
 */
export const CAPSULES: Record<string, Capsule> = {
  // --- Quick View ---
  'qv-overview': {
    id: 'qv-overview',
    title: 'Vue d\'ensemble',
    description: 'Découvrir le système d\'agents IA et ses possibilités pour l\'enseignement',
    parcours: 'quick-view',
    order: 0,
    sections: {
      info: `
        <h3>Qu'est-ce qu'un système d'agents IA ?</h3>
        <p>
          Un <strong>agent IA</strong> est un programme qui utilise un modèle de langage
          (comme Claude, Gemini, GPT...) pour <em>planifier</em> et <em>exécuter</em>
          des tâches complexes de manière autonome. Contrairement à un simple chatbot,
          un agent peut lire et écrire des fichiers, exécuter des scripts, et enchaîner
          plusieurs étapes sans intervention humaine.
        </p>

        <h4>Agent principal vs sous-agents</h4>
        <p>
          Quand vous lancez Claude Code ou Gemini CLI, vous parlez à un <strong>agent principal</strong> :
          c'est votre interlocuteur direct, celui qui comprend votre demande et décide comment y répondre.
        </p>
        <p>
          Pour les tâches complexes, cet agent principal peut invoquer des <strong>sous-agents</strong>
          (ou <em>sub-agents</em>) — des agents spécialisés qui travaillent en parallèle sur des
          sous-tâches précises, puis renvoient leurs résultats à l'agent principal.
        </p>
        <p style="padding: 0.75rem 1rem; background: rgba(129,140,248,0.08); border-radius: 8px; border-left: 3px solid rgba(129,140,248,0.4); font-size: 0.95em;">
          <strong>En pratique</strong>, le terme « agent » est souvent utilisé pour désigner les deux.
          C'est normal : un sous-agent <em>est</em> un agent à part entière, simplement il a été
          lancé par un autre agent plutôt que par vous. Dans la suite, quand la distinction compte,
          nous préciserons « agent principal » ou « sous-agent ».
        </p>

        <h4>Les 5 briques d'un système agentique</h4>
        <p>
          Ce que nous présentons ici fonctionne avec <strong>Claude Code</strong>,
          <strong>Gemini CLI</strong>, ou tout autre agent en ligne de commande.
          Le principe reste le même : un système composé de 5 briques.
        </p>
        <ul>
          <li><strong>Agent principal</strong> : votre interlocuteur, le cerveau qui planifie, orchestre le travail et invoque des sous-agents si nécessaire</li>
          <li><strong>Skills</strong> : des savoir-faire spécialisés (LaTeX, images, présentations...) que l'agent ou ses sous-agents peuvent utiliser</li>
          <li><strong>Instructions</strong> : des fichiers (CLAUDE.md, GEMINI.md) qui définissent le comportement de l'agent</li>
          <li><strong>Références</strong> : de la documentation et des exemples que l'agent peut consulter</li>
          <li><strong>Scripts</strong> : des programmes déterministes qui éliminent l'aléatoire (compilation, conversion...)</li>
        </ul>
        <p>
          L'intérêt pour un enseignant ? Vous décrivez ce que vous voulez en langage naturel,
          et le système produit des documents professionnels (cours, exercices, évaluations)
          directement sur votre machine.
        </p>
      `,
      exemple: `
        <p>
          Le graphe interactif ci-dessous illustre l'architecture d'un système agentique.
          <strong>Cliquez sur chaque nœud</strong> pour découvrir son rôle,
          puis explorez l'exemple concret du workflow <code>/latex</code> pour voir
          comment les skills s'enchaînent pour produire un PDF.
        </p>
        <div id="quickview-graph-mount"></div>
      `,
      pratique: `
        <h3>Explorer</h3>
        <p>Testez votre compréhension du schéma en répondant à ces questions :</p>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Question 1</span>
          </div>
          <div class="exercise-body">
            <p style="font-weight: 600;">Que semble être le rôle du composant Scripts dans le schéma ?</p>
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q1" disabled /> A) Planifier les tâches de l'agent</label>
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q1" disabled /> B) Garantir la reproductibilité du résultat</label>
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q1" disabled /> C) Stocker les instructions de l'utilisateur</label>
            </div>
          </div>
          <details class="exercise-solution">
            <summary>Voir la réponse</summary>
            <div class="solution-content">
              <p><strong>Réponse : B)</strong> Les scripts sont des programmes déterministes qui éliminent l'aléatoire — même source, même résultat.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Question 2</span>
          </div>
          <div class="exercise-body">
            <p style="font-weight: 600;">Pourquoi l'Agent est-il connecté aux Skills plutôt qu'aux Scripts directement ?</p>
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q2" disabled /> A) Les Scripts sont trop lents</label>
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q2" disabled /> B) L'Agent décide quoi faire, les Skills savent comment, les Scripts exécutent</label>
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q2" disabled /> C) Les Scripts ne fonctionnent que sur Windows</label>
            </div>
          </div>
          <details class="exercise-solution">
            <summary>Voir la réponse</summary>
            <div class="solution-content">
              <p><strong>Réponse : B)</strong> C'est une architecture en couches : décision → expertise → exécution déterministe.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Question 3</span>
          </div>
          <div class="exercise-body">
            <p style="font-weight: 600;">À quoi servent les Instructions (CLAUDE.md) ?</p>
            <div style="display: flex; flex-direction: column; gap: 0.4rem;">
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q3" disabled /> A) À installer Claude sur sa machine</label>
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q3" disabled /> B) À définir les règles permanentes que l'agent suit sans avoir à les répéter</label>
              <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.4rem 0.6rem; border-radius: 6px; cursor: pointer; background: rgba(255,255,255,0.03);"><input type="radio" name="q3" disabled /> C) À stocker les résultats des conversations précédentes</label>
            </div>
          </div>
          <details class="exercise-solution">
            <summary>Voir la réponse</summary>
            <div class="solution-content">
              <p><strong>Réponse : B)</strong> Le CLAUDE.md est un méta-prompt permanent lu automatiquement à chaque conversation.</p>
            </div>
          </details>
        </div>
        <p>
          Prêt à passer à la pratique ? Choisissez votre parcours :
        </p>
        <ul>
          <li>
            <a href="/claude-code/tutorials/parcours/claude-desktop" style="color: #34d399; text-decoration: underline;">
              Parcours Claude Desktop
            </a> : pour une utilisation graphique, sans ligne de commande
          </li>
          <li>
            <a href="/claude-code/tutorials/parcours/claude-code" style="color: #818cf8; text-decoration: underline;">
              Parcours Claude Code CLI
            </a> : pour la puissance maximale en ligne de commande
          </li>
        </ul>
      `,
    },
    duration: '5 min',
    tags: ['introduction', 'découverte'],
  },

  // --- Claude Desktop ---
  'cd-install': {
    id: 'cd-install',
    title: 'Installation',
    description: 'Télécharger et installer Claude Desktop sur votre machine',
    parcours: 'claude-desktop',
    order: 0,
    sections: {
      info: `
        <h3>Qu'est-ce que Claude Desktop ?</h3>
        <p>
          Claude Desktop est l'application native d'Anthropic, disponible sur <strong>Windows</strong>
          et <strong>macOS</strong>. C'est une interface graphique qui vous permet de dialoguer avec
          Claude directement depuis votre bureau, sans passer par un navigateur web.
        </p>
        <p>L'application propose trois modes de travail :</p>
        <ul>
          <li><strong>Chat</strong> : conversation classique, comme sur <a href="https://claude.ai" target="_blank" rel="noopener noreferrer">claude.ai</a></li>
          <li><strong>Cowork</strong> : un agent autonome qui travaille en arrière-plan sur vos tâches (macOS uniquement)</li>
          <li><strong>Code</strong> : Claude Code avec interface graphique, pour coder sans terminal (nécessite le mode développeur)</li>
        </ul>
        <p>
          Claude Desktop utilise le <strong>même moteur</strong> que Claude Code CLI. Les deux outils
          partagent la même intelligence, seule l'interface change. C'est le point d'entrée idéal
          si vous débutez avec l'IA.
        </p>
        <h4>Un écosystème ouvert</h4>
        <p>
          Claude Desktop n'est qu'une option parmi d'autres. D'autres plateformes proposent des
          expériences similaires : <strong>Gemini</strong> (Google), <strong>ChatGPT</strong> (OpenAI),
          <strong>Codex</strong>, <strong>Antigravity</strong>, etc. Les concepts que vous apprenez ici
          — agents, skills, prompts — sont <strong>transférables</strong> d'un outil à l'autre.
          Tout ce que nous présentons sur ce site est <strong>adaptable</strong> à la plateforme de votre choix.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Telecharger / Acceder</span>
          <div class="doc-links-buttons">
            <a href="https://claude.ai/download" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Claude Desktop
            </a>
            <a href="https://antigravity.google/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Antigravity (Google)
            </a>
            <a href="https://developers.openai.com/codex/cli" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex CLI (OpenAI)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Tutoriel pas-à-pas</h3>
        <ol>
          <li>
            <strong>Téléchargez</strong> l'application depuis
            <a href="https://claude.ai/download" target="_blank" rel="noopener noreferrer">claude.ai/download</a>
          </li>
          <li>
            <strong>Installez</strong> l'application :
            <ul style="margin-top: 0.5rem;">
              <li><strong>Windows</strong> : double-cliquez le fichier .exe et suivez l'assistant d'installation</li>
              <li><strong>macOS</strong> : ouvrez le .dmg et glissez l'icône Claude dans le dossier Applications</li>
            </ul>
          </li>
          <li>
            <strong>Lancez</strong> l'application et connectez-vous avec votre compte Claude
          </li>
          <li>
            <strong>Activez le mode développeur</strong> pour accéder à l'onglet Code :
            Paramètres > Développeur > Activer
          </li>
          <li>
            <strong>Découvrez les 3 onglets</strong> : Chat (conversation simple), Cowork (agent autonome sur macOS),
            Code (Claude Code avec interface)
          </li>
        </ol>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Ouvrez l'application Claude Desktop (onglet <strong>Chat</strong>) et envoyez ce prompt :</p>
            <p><em>"Je suis sur l'application Claude Desktop. Comment faire pour que tu puisses lire et modifier mes fichiers Excel directement sur mon ordinateur ?"</em></p>
            <p>Suivez les instructions qu'il vous donne.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude devrait vous expliquer qu'il a besoin de l'<strong>extension filesystem</strong> pour accéder à vos fichiers. Il vous guidera vers :</p>
              <ol>
                <li>Paramètres > Développeur > Activer le mode développeur</li>
                <li>Menu Extensions > Activer "filesystem"</li>
                <li>Pointer le filesystem vers votre dossier de travail</li>
              </ol>
              <p>Une fois activé, Claude peut lire, créer et modifier des fichiers directement sur votre machine. C'est la base pour toute utilisation productive.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Comparez les onglets <strong>Chat</strong> et <strong>Code</strong>.</p>
            <p>Envoyez le même message dans les deux. Quelle différence observez-vous ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Les différences principales :</p>
              <ul>
                <li><strong>Chat</strong> : réponse conversationnelle classique, centrée sur le texte. Claude répond dans la fenêtre de conversation.</li>
                <li><strong>Code</strong> : Claude a accès aux outils système (lecture/écriture de fichiers, exécution de commandes). Il peut créer des fichiers, naviguer dans votre arborescence, et exécuter des scripts.</li>
              </ul>
              <p>En résumé : Chat = conversation, Code = action sur votre machine. L'onglet Code est un véritable Claude Code intégré dans l'interface graphique.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Défi rapide</span>
          </div>
          <div class="exercise-body">
            <p>Trouvez où se cache le menu des paramètres. Que pouvez-vous y configurer ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Le menu des paramètres est accessible via l'<strong>icône engrenage</strong> en haut à droite de la fenêtre. Vous y trouverez :</p>
              <ul>
                <li><strong>Général</strong> : langue, thème, raccourcis clavier</li>
                <li><strong>Développeur</strong> : activer/désactiver le mode développeur (nécessaire pour l'onglet Code et les Extensions)</li>
                <li><strong>Extensions</strong> : gérer les serveurs MCP (filesystem, etc.)</li>
                <li><strong>Abonnement</strong> : détails de votre plan et consommation</li>
              </ul>
              <p>Le paramètre le plus important pour la suite du parcours est le <strong>mode développeur</strong> — activez-le si ce n'est pas déjà fait.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '5 min',
    tags: ['installation', 'setup'],
  },
  'cd-config': {
    id: 'cd-config',
    title: 'Configuration',
    description: 'Configurer Claude Desktop pour un usage optimal',
    parcours: 'claude-desktop',
    order: 1,
    sections: {
      info: `
        <h3>Configuration via les menus</h3>
        <p>
          La configuration de Claude Desktop se fait entièrement via les menus de l'application.
          Pas besoin de toucher à des fichiers — tout est accessible graphiquement.
        </p>
        <p>Voici les trois étapes principales :</p>
        <ol>
          <li>
            <strong>Activer le mode développeur</strong> (Paramètres > Développeur) pour accéder
            aux extensions avancées
          </li>
          <li>
            <strong>Explorer les Extensions</strong> disponibles dans le menu (suites Office,
            filesystem, etc.)
          </li>
          <li>
            <strong>Activer le serveur filesystem</strong> pour donner à Claude accès à vos fichiers
          </li>
        </ol>
        <p>
          Une fois le filesystem activé, Claude peut lire et créer des fichiers directement sur
          votre machine. C'est comme donner une main au programme — il peut enfin toucher vos documents.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/settings" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Claude Settings
            </a>
            <a href="https://antigravity.google/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Antigravity (Google)
            </a>
            <a href="https://developers.openai.com/codex/config-basic/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex Config (OpenAI)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Parcours dans les menus</h3>
        <p>Voici comment naviguer :</p>
        <ol>
          <li>
            <strong>Ouvrez les Paramètres</strong> : cliquez sur l'icône engrenage en haut à droite
          </li>
          <li>
            <strong>Rendez-vous à "Développeur"</strong> et activez le mode développeur
          </li>
          <li>
            <strong>Retournez au menu principal</strong> et cliquez sur "Extensions"
          </li>
          <li>
            <strong>Cherchez "filesystem"</strong> dans la liste des extensions disponibles
          </li>
          <li>
            <strong>Activez-le</strong> et pointez vers votre dossier de travail (par exemple,
            votre dossier Documents ou un dossier spécifique pour vos cours)
          </li>
        </ol>
        <p>
          <strong>Test</strong> : Une fois activé, ouvrez une conversation et demandez à Claude :
          <em>"Liste les fichiers dans mon dossier"</em>. Il devrait vous afficher le contenu de votre dossier.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
          </div>
          <div class="exercise-body">
            <p>Activez l'extension filesystem en pointant vers votre dossier de cours. Puis demandez à Claude :</p>
            <p><em>"Liste les fichiers dans mon dossier."</em></p>
            <p>Que voyez-vous ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude devrait afficher la <strong>liste complète des fichiers et dossiers</strong> présents dans le répertoire que vous avez configuré. Vous verrez quelque chose comme :</p>
              <pre><code>Voici les fichiers dans votre dossier :
- Cours/
- Exercices/
- Évaluations/
- notes.xlsx
- planning.docx</code></pre>
              <p>Si Claude répond qu'il n'a pas accès aux fichiers, vérifiez que :</p>
              <ul>
                <li>Le mode développeur est bien activé</li>
                <li>L'extension filesystem est activée et pointe vers le bon dossier</li>
                <li>Vous avez redémarré la conversation après l'activation</li>
              </ul>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Défi bonus</span>
          </div>
          <div class="exercise-body">
            <p>Demandez à Claude de <strong>créer un fichier texte</strong> dans votre dossier. Vérifiez qu'il apparaît vraiment sur votre machine.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Essayez par exemple : <em>"Crée un fichier test-claude.txt dans mon dossier avec le texte 'Bonjour depuis Claude Desktop !'"</em></p>
              <p>Claude devrait confirmer la création du fichier. Ouvrez votre explorateur de fichiers et naviguez vers le dossier configuré : le fichier <code>test-claude.txt</code> doit s'y trouver avec le contenu demandé.</p>
              <p>C'est la preuve que Claude peut <strong>agir sur votre système de fichiers</strong>. Cette capacité est la base de tout ce qui suit dans les parcours : création de cours, d'exercices, de présentations...</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['configuration'],
  },
  'cd-extensions': {
    id: 'cd-extensions',
    title: 'Extensions MCP',
    description: 'Ajouter des extensions pour étendre les capacités de Claude',
    parcours: 'claude-desktop',
    order: 2,
    sections: {
      info: `
        <h3>Panorama des possibilités</h3>
        <p>
          Maintenant que le filesystem est activé (capsule précédente), découvrez tout ce qui existe.
          Claude Desktop propose trois catégories de extensibilité :
        </p>
        <ol>
          <li>
            <strong>Extensions intégrées</strong> (un clic dans le menu) : filesystem, suites Office,
            et autres outils de base
          </li>
          <li>
            <strong>Connecteurs intégrés</strong> (menu ... > Connectors) : Google Drive, Notion,
            Slack, etc. sans configuration manuelle
          </li>
          <li>
            <strong>Serveurs MCP communautaires</strong> : catalogue sur
            <a href="https://github.com/modelcontextprotocol/servers" target="_blank" rel="noopener noreferrer">
            github.com/modelcontextprotocol/servers
            </a>
          </li>
        </ol>
        <p>
          Ces extensions ouvrent des possibilités infinies : lire vos fichiers, chercher sur internet,
          vous connecter à Google Drive, Notion, Slack, etc.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://modelcontextprotocol.io/introduction" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Protocole MCP
            </a>
            <a href="https://code.claude.com/docs/en/mcp" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              MCP dans Claude Code
            </a>
            <a href="https://geminicli.com/docs/extensions/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Extensions Gemini CLI
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Accéder aux extensions depuis Claude Desktop</h3>
        <p>Tout se passe dans les menus de l'application :</p>
        <ol>
          <li>
            Cliquez sur les <strong>trois barres</strong> (☰) en haut à gauche de la fenêtre
          </li>
          <li>
            Allez dans <strong>Fichier → Paramètres</strong>
          </li>
          <li>
            Dans la fenêtre qui s'affiche, cliquez sur <strong>Extensions</strong> dans le menu de gauche
          </li>
          <li>
            Cliquez sur <strong>Parcourir les extensions</strong> pour voir le catalogue complet
          </li>
        </ol>
        <p>
          Vous y trouverez des extensions classées par catégorie : <strong>productivité</strong>,
          <strong>développement</strong>, <strong>recherche</strong>, etc.
          Il suffit de cliquer sur une extension puis sur <strong>Installer</strong> pour l'activer.
        </p>
        <h4>Connecteurs intégrés</h4>
        <p>
          En plus des extensions, Claude Desktop propose des <strong>Connecteurs</strong> (Google Drive,
          Notion, Slack...) accessibles via le menu <strong>... > Connectors</strong> en haut à droite
          de la fenêtre de chat. Ces connecteurs s'activent en un clic et ne nécessitent pas d'installation.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
          </div>
          <div class="exercise-body">
            <p>Ouvrez Claude Desktop et accédez au catalogue d'extensions :</p>
            <ol>
              <li>☰ (trois barres en haut à gauche) → <strong>Fichier</strong> → <strong>Paramètres</strong></li>
              <li><strong>Extensions</strong> → <strong>Parcourir les extensions</strong></li>
            </ol>
            <p>Parcourez le catalogue et identifiez <strong>2 extensions</strong> qui seraient utiles dans votre discipline. Pour chacune, notez : son nom, ce qu'elle fait, et en quoi elle vous serait utile.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici quelques extensions pertinentes pour un enseignant :</p>
              <ul>
                <li><strong>Filesystem</strong> : accès en lecture/écriture aux fichiers locaux — indispensable pour créer et modifier des documents directement sur votre machine</li>
                <li><strong>Brave Search</strong> : recherche web — permet à Claude de chercher des informations récentes (programmes officiels mis à jour, exercices en ligne...)</li>
                <li><strong>Google Drive</strong> : accès à votre Drive — Claude peut lire et organiser vos documents partagés</li>
                <li><strong>Puppeteer</strong> : navigation web automatisée — Claude peut visiter des pages et en extraire du contenu pédagogique</li>
              </ul>
              <p>Le catalogue est régulièrement enrichi. N'hésitez pas à y revenir de temps en temps pour découvrir de nouvelles extensions.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice bonus</span>
          </div>
          <div class="exercise-body">
            <p>Activez un <strong>Connecteur intégré</strong> : dans une fenêtre de chat, cliquez sur <strong>...</strong> (trois points en haut à droite) → <strong>Connectors</strong>. Choisissez un service (Google Drive, Notion, Slack...) et suivez l'authentification.</p>
            <p>Testez-le ensuite en demandant à Claude : <em>"Quels outils as-tu à disposition ?"</em></p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Après activation d'un connecteur (par exemple Google Drive) :</p>
              <ol>
                <li>Claude vous demande de vous authentifier via OAuth (une fenêtre de navigateur s'ouvre)</li>
                <li>Une fois connecté, demandez : <em>"Quels outils as-tu à disposition ?"</em></li>
                <li>Claude devrait lister les capacités du connecteur (lire des fichiers Drive, chercher des documents, etc.)</li>
              </ol>
              <p>Testez ensuite avec une demande concrète comme : <em>"Liste mes 5 derniers documents Google Docs"</em>. Si cela fonctionne, le connecteur est correctement configuré.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['extensions', 'mcp'],
  },
  'cd-projects': {
    id: 'cd-projects',
    title: 'Projets',
    description: 'Organiser votre travail avec les Projets Claude Desktop',
    parcours: 'claude-desktop',
    order: 3,
    sections: {
      info: `
        <h3>Qu'est-ce qu'un Projet ?</h3>
        <p>
          Un <strong>Projet</strong> dans Claude Desktop est un espace de travail dédié à un sujet.
          Il regroupe vos conversations, vos fichiers et vos <strong>instructions personnalisées</strong>
          dans un même endroit.
        </p>
        <p>Concrètement, un Projet vous permet de :</p>
        <ul>
          <li><strong>Donner des instructions permanentes</strong> à Claude : par exemple <em>"Tu es un assistant pour un cours de maths en 3ème"</em>. Claude les relira à chaque nouvelle conversation dans ce projet.</li>
          <li><strong>Joindre des fichiers de référence</strong> : programme officiel, cours existant, barème... Claude les consultera pour produire des réponses adaptées.</li>
          <li><strong>Retrouver vos conversations</strong> : toutes les discussions liées à ce projet sont regroupées au même endroit.</li>
        </ul>
        <p style="padding: 0.75rem 1rem; background: rgba(52,211,153,0.08); border-radius: 8px; border-left: 3px solid rgba(52,211,153,0.4); font-size: 0.95em;">
          <strong>Analogie</strong> : un Projet, c'est comme donner un dossier de travail complet
          à un assistant avant de lui confier une mission. Plus le dossier est précis,
          plus le travail rendu sera pertinent.
        </p>
      `,
      exemple: `
        <h3>Créer un Projet pas à pas</h3>
        <ol>
          <li>
            <p>Dans la <strong>sidebar gauche</strong> de Claude Desktop, cliquez sur <strong>Projets</strong> puis sur <strong>+ Nouveau projet</strong> :</p>
            <img src="/images/claude-desktop/projects/overview.png" alt="Vue d'ensemble des projets dans Claude Desktop" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0;" />
          </li>
          <li>
            <p>Remplissez le formulaire : donnez un <strong>nom</strong> à votre projet et décrivez brièvement <strong>ce que vous essayez de faire</strong> :</p>
            <img src="/images/claude-desktop/projects/new.png" alt="Formulaire de création de projet" style="max-width: 400px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0;" />
          </li>
          <li>
            <p>Une fois créé, vous accédez à l'espace du projet. Sur la droite, vous pouvez :</p>
            <ul>
              <li>Écrire des <strong>Instructions</strong> que Claude relira systématiquement</li>
              <li>Ajouter des <strong>Fichiers</strong> de référence (PDF, texte, images...)</li>
            </ul>
            <img src="/images/claude-desktop/projects/setup.png" alt="Configuration du projet avec instructions et fichiers" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0;" />
          </li>
        </ol>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice : Analyse didactique</span>
          </div>
          <div class="exercise-body">
            <p>Créez un projet <strong>"Analyse didactique"</strong> qui transforme n'importe quel document pédagogique en plan de séance(s) structuré :</p>
            <ol>
              <li>Sidebar gauche → <strong>Projets</strong> → <strong>+ Nouveau projet</strong></li>
              <li>Nom : <em>"Analyse didactique"</em></li>
              <li>Dans les <strong>Instructions</strong> (panneau droit, icône crayon), copiez-collez ce texte :</li>
            </ol>
            <pre style="margin: 0.75rem 0; padding: 1rem; background: rgba(0,0,0,0.25); border-radius: 8px; font-size: 0.82em; white-space: pre-wrap; border-left: 3px solid rgba(129,140,248,0.4); line-height: 1.5;">Tu es un conseiller pédagogique expérimenté. Quand je dépose un document (cours, exercices, chapitre de manuel...), produis une analyse didactique complète sous forme de plan de séance(s).

Si je n'ai pas précisé le niveau et la discipline, demande-les avant de commencer.

Pour chaque document, produis un fichier HTML autonome contenant :

1. PLAN DE SÉANCE(S)
- Découper en plusieurs séances si le document est trop long pour une seule (45-55 min par séance)
- Pour chaque séance : objectifs visés, déroulement minuté (durée approximative par activité), modalités (individuel/groupe/classe entière)
- Inclure des moments d'évaluation formative

2. ANALYSE DIDACTIQUE (pour chaque exercice ou notion)
- Problèmes anticipés : erreurs fréquentes, obstacles cognitifs, prérequis fragiles
- Aides élèves : pour chaque problème relevé, proposer une remédiation concrète (question intermédiaire, rappel, manipulation, schéma...)
- Reformulations : proposer une version alternative de chaque énoncé, plus accessible sans perdre l'exigence

FORMAT HTML : document autonome avec styles inline, sobre, imprimable, bien structuré avec des tableaux pour le minutage et des encadrés colorés pour les alertes didactiques (orange) et les aides (vert).</pre>
            <ol start="4">
              <li>Ajoutez un <strong>fichier</strong> : un cours, une fiche d'exercices ou un chapitre de manuel (PDF, image, texte...)</li>
              <li>Lancez une conversation et demandez simplement : <em>"Analyse ce document. Niveau 3ème, mathématiques."</em></li>
              <li>Claude produira un fichier HTML complet. Copiez le code HTML et ouvrez-le dans votre navigateur pour voir le résultat.</li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude devrait produire un document HTML contenant :</p>
              <ul>
                <li><strong>Un plan de séance(s) minuté</strong> avec un tableau indiquant chaque activité, sa durée (ex: "Activité 1 — 10 min — Rappel des prérequis"), et les modalités de travail</li>
                <li><strong>Des encadrés orange "Alerte didactique"</strong> signalant les erreurs fréquentes (ex: pour Thalès, confusion entre le théorème direct et sa réciproque, erreurs dans l'identification des triangles emboîtés)</li>
                <li><strong>Des encadrés verts "Aide élève"</strong> proposant des remédiations (ex: "Si l'élève ne voit pas les triangles, lui proposer de colorier les côtés parallèles")</li>
                <li><strong>Des reformulations</strong> pour chaque énoncé d'exercice (ex: l'original "Calculer AB" reformulé en "On cherche la longueur du segment [AB]. Pour cela, identifie d'abord quels triangles sont en configuration de Thalès.")</li>
              </ul>
              <p>Si le document est long (plus d'une séance), Claude le découpera automatiquement en plusieurs séances avec des transitions logiques.</p>
              <p style="margin-top: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(129,140,248,0.08); border-radius: 6px; font-size: 0.9em;">
                <strong>Astuce</strong> : ce projet est réutilisable ! Pour chaque nouveau document, ouvrez simplement une nouvelle conversation dans le même projet. Les instructions restent actives.
              </p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Pour aller plus loin</span>
          </div>
          <div class="exercise-body">
            <p>Enrichissez votre projet en ajoutant des fichiers de référence supplémentaires :</p>
            <ul>
              <li>Un extrait du <strong>programme officiel</strong> de votre discipline (PDF du BO)</li>
              <li>Un <strong>exemple de plan de séance</strong> que vous avez déjà rédigé (pour que Claude s'en inspire)</li>
            </ul>
            <p>Plus le projet contient de contexte, plus les analyses seront pertinentes et adaptées à votre pratique.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>En ajoutant le programme officiel, Claude pourra :</p>
              <ul>
                <li>Citer les <strong>compétences du programme</strong> visées par chaque séance</li>
                <li>Vérifier que les prérequis mentionnés sont <strong>cohérents avec la progression officielle</strong></li>
                <li>Proposer des <strong>liens avec d'autres chapitres</strong> du programme</li>
              </ul>
              <p>En ajoutant un exemple de plan de séance existant, Claude reproduira votre <strong>style de rédaction</strong> et votre <strong>format préféré</strong>. C'est la puissance des Projets : Claude s'adapte à vous, pas l'inverse.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['projets', 'organisation'],
  },
  'cd-first-prompt': {
    id: 'cd-first-prompt',
    title: 'Premier prompt',
    description: 'Rédiger votre premier prompt efficace avec Claude Desktop',
    parcours: 'claude-desktop',
    order: 3,
    sections: {
      info: `
        <h3>Comment bien formuler une demande</h3>
        <p>
          La qualité de la réponse de Claude dépend directement de la qualité de votre demande
          (le "prompt"). Voici les principes clés pour obtenir des résultats pertinents :
        </p>
        <ul>
          <li>
            <strong>Soyez précis</strong> : au lieu de "fais-moi un exercice", dites
            "fais-moi un exercice de mathématiques"
          </li>
          <li>
            <strong>Donnez du contexte</strong> : préciser le niveau (6ème, 3ème, seconde...),
            la notion (fractions, Pythagore...), le type de document (cours, exercice, évaluation...)
          </li>
          <li>
            <strong>Spécifiez le format</strong> : indiquez si vous voulez un document LaTeX,
            un texte simple, un tableau, une liste à puces, etc.
          </li>
          <li><strong>Indiquez le public</strong> : pour des élèves, pour vous, pour les parents...</li>
        </ul>
        <p>
          Un bon prompt est comme une consigne d'exercice : plus elle est claire, meilleure sera
          la réponse. N'hésitez pas à donner des exemples de ce que vous attendez, ou à préciser
          ce que vous ne voulez pas.
        </p>
        <p>
          <strong>Nouveauté :</strong> Maintenant que l'extension filesystem est installée (capsule
          précédente), Claude peut directement créer et modifier des fichiers sur votre machine.
          Vous pouvez lui demander de créer un exercice, il va l'écrire dans un vrai fichier.
        </p>
      `,
      exemple: `
        <h3>Exemple de workflow complet avec fichiers</h3>
        <p>Voici un exemple concret d'échange itératif avec Claude Desktop :</p>
        <h4>Étape 1 : créer un exercice</h4>
        <pre><code>Crée un exercice de mathématiques sur les fractions
pour une classe de 6ème dans le fichier exercice.txt

Contexte :
- Les élèves ont déjà vu l'écriture fractionnaire
- Ils découvrent les fractions égales
- Niveau hétérogène (certains en difficulté)

Format :
- 3 exercices progressifs (facile, moyen, difficile)
- Chaque exercice avec un exemple résolu
- Une partie "coup de pouce" pour les élèves en difficulté</code></pre>
        <h4>Étape 2 : modifier le fichier</h4>
        <p>Claude crée le fichier. Vous observez. Puis vous demandez :</p>
        <pre><code>Ajoute un corrigé détaillé en bas du fichier.</code></pre>
        <h4>Étape 3 : créer une version différenciée</h4>
        <pre><code>Crée une version simplifiée du même exercice pour les élèves
en difficulté. Sauvegarde-la dans exercice_differentie.txt</code></pre>
        <p>
          À chaque étape, Claude <strong>modifie directement vos fichiers</strong> grâce à
          l'extension filesystem. C'est un vrai workflow de collaboration.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice comparatif</span>
          </div>
          <div class="exercise-body">
            <p>Envoyez ce prompt vague à Claude :</p>
            <p><em>"Fais-moi un exercice de maths."</em></p>
            <p>Observez la réponse. Puis envoyez le même prompt, mais enrichi avec contexte/niveau/format (inspirez-vous de l'exemple). Comparez les deux réponses.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Vous devriez observer des différences nettes :</p>
              <ul>
                <li><strong>Prompt vague</strong> : Claude produit un exercice générique, souvent trop simple ou mal ciblé. Il choisit un sujet au hasard, sans savoir le niveau ni le contexte pédagogique.</li>
                <li><strong>Prompt enrichi</strong> : l'exercice est adapté au niveau demandé, progressif, avec un format structuré. Claude peut même intégrer des encadrés "coup de pouce" ou des exemples résolus.</li>
              </ul>
              <p><strong>Leçon clé :</strong> un prompt précis produit un résultat 10x meilleur. Les 30 secondes investies à formuler votre demande vous font gagner plusieurs minutes de retouches.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Défi fichier</span>
          </div>
          <div class="exercise-body">
            <p>Demandez à Claude de :</p>
            <ol>
              <li>Créer un fichier avec un exercice</li>
              <li>Le modifier pour ajouter un corrigé</li>
              <li>En faire une version différenciée dans un second fichier</li>
            </ol>
            <p>Observez comment il modifie directement les fichiers sur votre machine.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici ce que vous devriez observer à chaque étape :</p>
              <ol>
                <li><strong>Création</strong> : Claude crée le fichier (ex : <code>exercice.txt</code>) et confirme son emplacement. Vérifiez dans votre explorateur de fichiers qu'il existe.</li>
                <li><strong>Modification</strong> : Claude lit le fichier existant, puis y ajoute le corrigé en bas. Le fichier est modifié en place.</li>
                <li><strong>Version différenciée</strong> : Claude crée un nouveau fichier (ex : <code>exercice_differentie.txt</code>) avec une version adaptée.</li>
              </ol>
              <p>Ce workflow montre la puissance de l'extension filesystem : Claude ne se contente pas de répondre dans le chat, il <strong>agit sur vos fichiers</strong> comme le ferait un assistant humain.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['prompt', 'découverte'],
  },

  // --- Claude Code CLI ---
  'cc-install': {
    id: 'cc-install',
    title: 'Installation',
    description: 'Installer Claude Code en ligne de commande',
    parcours: 'claude-code',
    order: 0,
    sections: {
      info: `
        <h3>Qu'est-ce que Claude Code ?</h3>
        <p>
          Claude Code est un outil en <strong>ligne de commande</strong> (CLI) qui permet
          d'interagir avec Claude directement depuis un terminal. Contrairement à Claude Desktop
          qui offre une interface graphique, Claude Code s'utilise en tapant des commandes textuelles.
        </p>
        <p>
          Pourquoi utiliser le CLI plutôt que Desktop ? Parce qu'il est plus puissant pour les
          tâches automatisées : création de fichiers, exécution de scripts, gestion de projets
          complexes. C'est l'outil privilégié pour utiliser les <strong>agents</strong>,
          <strong>skills</strong> et <strong>commandes personnalisées</strong>.
        </p>
        <h4>Prérequis</h4>
        <ul>
          <li>
            <strong>Un terminal</strong> : Git Bash ou PowerShell sur Windows ; Terminal sur macOS/Linux
          </li>
          <li>
            <strong>Un compte</strong> sur la plateforme de votre choix (Claude, Gemini, Codex)
          </li>
          <li>
            <strong>Node.js 18+</strong> : nécessaire uniquement pour Gemini CLI et Codex.
            Claude Code dispose désormais d'un installateur natif qui ne requiert pas Node.js.
            Téléchargez Node.js si besoin sur <a href="https://nodejs.org" target="_blank" rel="noopener noreferrer">nodejs.org</a>
          </li>
          <li>
            <strong>Windows</strong> : <a href="https://git-scm.com/downloads/win" target="_blank" rel="noopener noreferrer">Git for Windows</a> est requis pour Claude Code natif
          </li>
        </ul>
        <p>
          Claude Code est l'outil présenté ici, mais les concepts sont <strong>identiques</strong>
          sur d'autres CLI comme <strong>Gemini CLI</strong> ou <strong>Codex</strong>.
          Les agents, skills et CLAUDE.md s'adaptent facilement à n'importe quelle plateforme.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/setup" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Installation Claude Code
            </a>
            <a href="https://code.claude.com/docs/en/quickstart" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Quickstart
            </a>
            <a href="https://geminicli.com/docs/get-started/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Gemini CLI Get Started
            </a>
            <a href="https://developers.openai.com/codex/cli" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex CLI Docs
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Guide d'installation</h3>
        <p>Choisissez votre CLI et suivez les étapes :</p>

        <div class="cli-tabs" data-cli-tabs>
          <div class="cli-tabs-nav">
            <button class="cli-tab-btn active" data-tab-brand="anthropic" data-tab-target="tab-claude">Claude Code</button>
            <button class="cli-tab-btn" data-tab-brand="google" data-tab-target="tab-gemini">Gemini CLI</button>
            <button class="cli-tab-btn" data-tab-brand="openai" data-tab-target="tab-codex">Codex CLI</button>
          </div>

          <div class="cli-tab-panel active" id="tab-claude">
            <h4>Installation native (recommandée)</h4>
            <p>Claude Code ne nécessite plus Node.js. Utilisez l'installateur natif :</p>
            <p><strong>macOS / Linux / WSL :</strong></p>
            <pre><code>curl -fsSL https://claude.ai/install.sh | bash</code></pre>
            <p><strong>Windows PowerShell :</strong></p>
            <pre><code>irm https://claude.ai/install.ps1 | iex</code></pre>
            <p><strong>Alternatives :</strong> <code>brew install --cask claude-code</code> (Homebrew) ou <code>winget install Anthropic.ClaudeCode</code> (WinGet)</p>
            <h4>Lancer</h4>
            <pre><code>cd votre-dossier-de-travail
claude</code></pre>
            <p>Au premier lancement, suivez les instructions d'authentification à l'écran.</p>
            <p><em>Vérification :</em> <code>claude doctor</code> vérifie que tout est correctement installé.</p>
          </div>

          <div class="cli-tab-panel" id="tab-gemini">
            <h4>Prérequis</h4>
            <p><a href="https://nodejs.org" target="_blank" rel="noopener noreferrer">Node.js</a> et npm doivent être installés (<code>node --version</code> pour vérifier).</p>
            <h4>Installation</h4>
            <pre><code>npm install -g @google/gemini-cli</code></pre>
            <h4>Lancer</h4>
            <pre><code>gemini</code></pre>
            <p>Au premier lancement, suivez les instructions pour connecter votre compte Google.</p>
          </div>

          <div class="cli-tab-panel" id="tab-codex">
            <h4>Prérequis</h4>
            <p><a href="https://nodejs.org" target="_blank" rel="noopener noreferrer">Node.js</a> et npm. Compte ChatGPT Plus/Pro/Business ou clé API OpenAI. macOS ou Linux (Windows via WSL).</p>
            <h4>Installation</h4>
            <pre><code>npm i -g @openai/codex</code></pre>
            <h4>Lancer</h4>
            <pre><code>codex</code></pre>
            <p>Authentification avec votre compte ChatGPT ou clé API au premier lancement.</p>
            <p><em>Mise à jour :</em> <code>npm i -g @openai/codex@latest</code></p>
          </div>
        </div>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Lancez <code>claude</code> dans votre terminal. Envoyez <code>/help</code> et identifiez 3 commandes qui vous semblent utiles.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici les commandes les plus utiles pour débuter :</p>
              <ul>
                <li><code>/help</code> : affiche toutes les commandes disponibles — c'est votre point de repère</li>
                <li><code>/compact</code> : compacte la conversation pour économiser les tokens — indispensable lors de sessions longues</li>
                <li><code>/init</code> : analyse votre projet et génère un CLAUDE.md — le point de départ pour configurer votre environnement</li>
                <li><code>/clear</code> : remet la conversation à zéro — utile quand Claude se perd dans un contexte trop long</li>
                <li><code>/exit</code> : quitte proprement Claude Code</li>
              </ul>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
          </div>
          <div class="exercise-body">
            <p>Envoyez un message simple et observez comment Claude répond dans le terminal. Puis quittez avec <code>/exit</code>.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude répond directement dans le terminal, en texte formaté (Markdown rendu). Vous remarquerez :</p>
              <ul>
                <li>Les blocs de code sont colorés syntaxiquement</li>
                <li>Les listes sont indentées proprement</li>
                <li>La <strong>statusline</strong> en bas affiche le modèle, les tokens consommés et le coût</li>
              </ul>
              <p>Pour quitter, tapez <code>/exit</code> ou utilisez le raccourci <code>Ctrl+C</code> puis confirmez.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Découverte</span>
          </div>
          <div class="exercise-body">
            <p>Relancez Claude avec cette commande :</p>
            <pre><code>claude --dangerously-skip-permissions</code></pre>
            <p>Que remarquez-vous de différent par rapport au lancement classique ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Avec ce flag, Claude ne vous demande plus la permission avant de lire/écrire des fichiers ou exécuter des commandes. Il agit en <strong>autonomie complète</strong>.</p>
              <p>C'est utile pour des <strong>modifications de routine</strong> où vous faites confiance à l'agent : corrections mineures, mise en forme, tâches prévisibles. À éviter sur des projets sensibles ou quand vous découvrez un nouveau codebase.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '5 min',
    tags: ['installation', 'cli'],
  },
  'cc-config': {
    id: 'cc-config',
    title: 'Configuration',
    description: 'Configurer Claude Code pour votre environnement',
    parcours: 'claude-code',
    order: 1,
    sections: {
      info: `
        <h3>Les fichiers de configuration</h3>
        <p>
          Claude Code utilise plusieurs fichiers pour personnaliser son comportement.
          Comprendre cette hiérarchie est essentiel pour tirer le meilleur parti de l'outil.
        </p>
        <h4>CLAUDE.md : le fichier d'instructions</h4>
        <p>
          Le fichier <code>CLAUDE.md</code> placé à la racine de votre projet contient des
          <strong>instructions persistantes</strong> que Claude lit automatiquement à chaque
          lancement. C'est comme un briefing permanent : vous y décrivez votre contexte,
          vos préférences, vos règles.
        </p>
        <h4>Le dossier .claude/</h4>
        <p>Le dossier <code>.claude/</code> à la racine de votre projet contient les outils avancés :</p>
        <ul>
          <li><strong>agents/</strong> : des agents spécialisés pour des tâches précises (création LaTeX, présentations, etc.)</li>
          <li><strong>skills/</strong> : des compétences invocables via <code>/nom-du-skill</code> — chaque skill est un <strong>dossier</strong> avec <code>SKILL.md</code> + fichiers de support (references, scripts, examples...)</li>
          <li><strong>commands/</strong> : des commandes personnalisées organisées par catégories</li>
          <li><strong>settings.json</strong> : paramètres globaux (hooks, permissions, etc.)</li>
        </ul>
        <h4>Hiérarchie de configuration</h4>
        <p>
          Claude Code lit la configuration à trois niveaux : le <strong>settings.json global</strong>
          (préférences système), le <strong>CLAUDE.md du projet</strong> (instructions spécifiques)
          et le <strong>dossier .claude/</strong> (agents et skills). Les trois se combinent pour
          définir le comportement de Claude dans votre projet.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/settings" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Claude Code Settings
            </a>
            <a href="https://code.claude.com/docs/en/memory" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              CLAUDE.md & Memory
            </a>
            <a href="https://geminicli.com/docs/reference/configuration/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Gemini CLI Config
            </a>
            <a href="https://developers.openai.com/codex/config-basic/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex Config
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Exemple de configuration</h3>
        <h4>Un CLAUDE.md simple pour un enseignant</h4>
        <pre><code># Mon projet d'enseignement

## Contexte
Je suis enseignant de mathématiques au collège.
Je travaille avec des classes de 6ème à 3ème.

## Règles
- Utilise le vouvoiement dans les documents élèves
- Respecte les programmes officiels de l'Éducation nationale
- Les exercices doivent être progressifs (facile à difficile)
- Génère les documents en LaTeX quand c'est possible

## Structure de mes fichiers
- Cours/ : les cours par niveau
- Exercices/ : les exercices par notion
- Évaluations/ : les contrôles et devoirs</code></pre>
        <h4>Structure du dossier .claude/</h4>
        <pre><code>.claude/
  agents/                -> Agents spécialisés (fichiers .md)
    tex-agent.md
    debug-agent.md
  skills/                -> Skills (chaque skill = un dossier)
    bfcours-latex/
      SKILL.md           -> Instructions principales
      references/        -> Docs de référence
      scripts/           -> Scripts exécutables
    image-generator/
      SKILL.md
      scripts/generate.py
  commands/              -> Commandes slash rapides
    createTex.md
    adaptTex.md
  settings.json          -> Hooks et permissions</code></pre>
        <p>
          Vous pouvez télécharger une configuration complète et prête à l'emploi depuis la
          page Téléchargements de ce site.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice : tester le système de permissions</span>
          </div>
          <div class="exercise-body">
            <p>Cet exercice vous fait découvrir la configuration de sécurité de Claude Code en situation réelle.</p>
            <ol>
              <li>
                <strong>Préparez le terrain</strong> : créez un dossier <code>secret/</code> à la racine de votre répertoire de travail, puis placez-y un fichier <code>mot-de-passe.txt</code> contenant un mot de votre choix.
                <pre><code>mkdir secret
echo "papillon" > secret/mot-de-passe.txt</code></pre>
              </li>
              <li>
                <strong>Configurez l'interdiction</strong> : lancez <code>claude</code> et demandez-lui de configurer les settings pour <strong>interdire tout accès au dossier <code>secret/</code></strong>. Il modifiera <code>.claude/settings.json</code> pour vous.
              </li>
              <li>
                <strong>Testez</strong> : relancez une nouvelle conversation (même en mode <code>--dangerously-skip-permissions</code> si vous voulez pousser le test). Demandez à Claude : <em>"Lis le contenu du fichier mot-de-passe.txt dans le dossier secret/"</em>.
              </li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude tente de lire le fichier, reçoit une erreur de permission de son propre système de sécurité, et vous répond qu'il <strong>n'a pas le droit</strong> d'accéder aux fichiers du dossier <code>secret/</code>.</p>
              <p>Cela démontre que les <strong>settings de permission sont plus forts</strong> que le flag <code>--dangerously-skip-permissions</code>. La sécurité configurée dans <code>settings.json</code> prime toujours.</p>
              <p>C'est un mécanisme essentiel : vous pouvez travailler en mode autonome tout en protégeant certains dossiers sensibles (notes, données personnelles des élèves, etc.).</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['configuration', 'cli'],
  },
  'cc-commands': {
    id: 'cc-commands',
    title: 'Commandes essentielles',
    description: 'Les commandes Claude Code à connaître',
    parcours: 'claude-code',
    order: 2,
    sections: {
      info: `
        <h3>Les commandes et fonctionnalités natives</h3>
        <p>
          Claude Code intègre des commandes et fonctionnalités puissantes directement accessibles,
          sans configuration supplémentaire.
        </p>
        <h4>Commandes slash essentielles</h4>
        <ul>
          <li><code>/help</code> : affiche l'aide et les commandes disponibles</li>
          <li><code>/init</code> : <strong>à lancer en premier dans tout nouveau projet</strong>. Claude analyse votre dossier (fichiers, dépendances, structure) et génère un fichier <code>CLAUDE.md</code> qui le guidera dans toutes les conversations futures. C'est le point de départ pour que Claude comprenne votre projet sans que vous ayez à tout lui expliquer à chaque fois.</li>
          <li><code>/compact</code> : compacte la conversation pour économiser la mémoire (indispensable en sessions longues)</li>
          <li><code>/clear</code> : efface la conversation et repart à zéro</li>
          <li><code>/config</code> : ouvre la configuration interactive de Claude Code</li>
          <li><code>/status</code> : affiche l'état de la session (modèle, tokens consommés...)</li>
          <li><code>/exit</code> : quitte Claude Code</li>
        </ul>
        <h4>Commandes terminal (hors session)</h4>
        <p>Ces commandes se lancent directement dans le terminal, avant ou après une session Claude :</p>
        <ul>
          <li><code>claude</code> : lance une nouvelle session interactive</li>
          <li><code>claude resume</code> : <strong>reprend la dernière conversation</strong> là où vous l'aviez laissée. Très pratique quand vous avez fermé le terminal par erreur ou quand vous reprenez le travail le lendemain.</li>
          <li><code>claude continue</code> : similaire à resume, reprend la conversation la plus récente</li>
          <li><code>claude doctor</code> : vérifie que tout est correctement installé et configuré</li>
          <li><code>claude update</code> : met à jour Claude Code vers la dernière version</li>
        </ul>
        <h4>Fonctionnalités avancées intégrées</h4>
        <ul>
          <li>
            <strong>ultrathink</strong> : en ajoutant le mot <code>ultrathink</code> dans votre message, vous activez la réflexion approfondie. Le modèle prend plus de temps pour réfléchir avant de répondre, produisant des résultats plus précis et structurés sur les tâches complexes.
          </li>
          <li>
            <strong>Statusline</strong> : la barre d'état en bas du terminal affiche en temps réel le modèle utilisé, les tokens consommés, le coût de la session et l'état de la connexion. Pour l'activer ou la personnaliser, demandez simplement à Claude : <em>"Configure ma statusline"</em> — il s'en occupera pour vous.
          </li>
          <li>
            <strong>Mode plan</strong> : Claude peut planifier les étapes d'une tâche complexe avant de l'exécuter. Demandez-lui de "planifier" ou "faire un plan" et il décomposera le travail en étapes.
          </li>
        </ul>
        <p>
          L'autocomplétion fonctionne en tapant <code>/</code> puis les premières lettres.
          Les flèches haut/bas naviguent les suggestions, Tab valide.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/cli-reference" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              CLI Reference
            </a>
            <a href="https://code.claude.com/docs/en/slash-commands" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Slash Commands
            </a>
            <a href="https://code.claude.com/docs/en/common-workflows" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Common Workflows
            </a>
            <a href="https://developers.openai.com/codex/cli/slash-commands/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex Commands
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Exemples de commandes en action</h3>
        <h4>Commandes slash (dans une session)</h4>
        <pre><code>/init              → À faire EN PREMIER : génère votre CLAUDE.md
/help              → Affiche l'aide complète
/compact           → Compacte la conversation (libère du contexte)
/config            → Configuration interactive
/status            → Voir le modèle, les tokens, le coût</code></pre>
        <h4>Commandes terminal (hors session)</h4>
        <pre><code>claude             → Nouvelle session
claude resume      → Reprendre la dernière conversation
claude continue    → Idem, reprend la conversation récente
claude doctor      → Vérifier l'installation
claude update      → Mettre à jour</code></pre>
        <h4>ultrathink en action</h4>
        <p>Comparez ces deux prompts :</p>
        <pre><code># Sans ultrathink :
Crée un exercice sur Pythagore pour les 4ème

# Avec ultrathink :
ultrathink Crée un exercice sur Pythagore pour les 4ème</code></pre>
        <p>
          Avec <code>ultrathink</code>, Claude réfléchit plus longuement et produit un exercice
          mieux structuré, avec une progression plus soignée et des cas de figure variés.
          C'est particulièrement utile pour les tâches créatives ou les problèmes complexes.
        </p>
        <h4>La statusline</h4>
        <p>
          En bas du terminal, vous voyez en permanence une ligne comme :
        </p>
        <pre><code>claude-sonnet-4  ●  12.4k tokens  ●  $0.08  ●  session 14min</code></pre>
        <p>
          Elle vous aide à surveiller votre consommation et à savoir quand utiliser
          <code>/compact</code> pour libérer du contexte.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Ouvrez un terminal dans un dossier vide (ou un projet existant). Lancez <code>claude</code> puis tapez <code>/init</code>.</p>
            <p>Lisez le CLAUDE.md généré : est-il pertinent ? Que décrit-il ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>La commande <code>/init</code> analyse automatiquement votre projet et génère un fichier <code>CLAUDE.md</code> contenant :</p>
              <ul>
                <li>Le <strong>type de projet</strong> détecté (Node.js, Python, LaTeX...)</li>
                <li>La <strong>structure des dossiers</strong> et fichiers principaux</li>
                <li>Les <strong>technologies</strong> utilisées (frameworks, langages...)</li>
                <li>Des <strong>conventions</strong> suggérées (style de code, nommage...)</li>
              </ul>
              <p>Sur un dossier vide, le CLAUDE.md sera minimal. Sur un projet existant, il sera plus riche. Dans tous les cas, c'est un point de départ que vous pouvez personnaliser en ajoutant vos propres règles et préférences.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2 : défi ultrathink</span>
          </div>
          <div class="exercise-body">
            <p>Envoyez la même demande deux fois :</p>
            <ol>
              <li>Une fois normalement : <code>Crée un exercice sur Pythagore pour les 4ème</code></li>
              <li>Une fois avec ultrathink : <code>ultrathink Crée un exercice sur Pythagore pour les 4ème</code></li>
            </ol>
            <p>Comparez la profondeur et la qualité des deux réponses.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Avec <code>ultrathink</code>, vous devriez observer :</p>
              <ul>
                <li><strong>Plus de variété</strong> : des cas de figure différents (triangle rectangle classique, applications concrètes, problèmes inverses...)</li>
                <li><strong>Meilleure progression</strong> : exercices ordonnés du plus simple au plus complexe</li>
                <li><strong>Plus de rigueur</strong> : vérification des valeurs numériques, justifications pédagogiques</li>
                <li><strong>Temps de réponse plus long</strong> : normal, Claude "réfléchit" plus longtemps avant de répondre</li>
              </ul>
              <p><strong>Quand utiliser ultrathink ?</strong> Pour les tâches complexes (création de contenu, résolution de problèmes, planification). Pour les tâches simples (lister des fichiers, reformater du texte), le mode normal suffit.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3</span>
          </div>
          <div class="exercise-body">
            <p>Faites quelques échanges avec Claude et surveillez la <strong>statusline</strong> en bas du terminal. Observez les tokens consommés. Puis tapez <code>/compact</code>.</p>
            <p>Comment le compteur change-t-il ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Après <code>/compact</code>, vous devriez observer :</p>
              <ul>
                <li>Le <strong>compteur de tokens diminue fortement</strong> (souvent de 50 à 80%)</li>
                <li>Claude <strong>résume la conversation</strong> en conservant les points essentiels et en supprimant les détails verbeux</li>
                <li>La conversation <strong>continue normalement</strong> — Claude se souvient du contexte important</li>
              </ul>
              <p><strong>Règle pratique :</strong> utilisez <code>/compact</code> quand vous approchez des 50-60k tokens, ou quand vous sentez que les réponses deviennent moins pertinentes (signe que le contexte est trop chargé).</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 4 : Statusline</span>
          </div>
          <div class="exercise-body">
            <p>Demandez à Claude de configurer votre statusline :</p>
            <pre style="margin: 0.5rem 0; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px; font-size: 0.85em;">Configure ma statusline</pre>
            <p>Claude va vous proposer différentes options d'affichage et configurer la barre d'état en bas du terminal pour vous.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude configure le fichier <code>~/.claude/settings.json</code> pour activer et personnaliser la statusline. Vous devriez voir apparaître en bas du terminal :</p>
              <ul>
                <li>Le <strong>modèle</strong> utilisé (ex: claude-sonnet-4)</li>
                <li>Le <strong>nombre de tokens</strong> consommés dans la session</li>
                <li>Le <strong>coût estimé</strong> de la session en cours</li>
                <li>La <strong>durée</strong> de la session</li>
              </ul>
              <p>C'est un bon réflexe de garder un œil sur ces indicateurs, surtout le compteur de tokens qui vous dit quand il est temps de faire un <code>/compact</code>.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['commandes', 'cli'],
  },
  'cc-dotclaude': {
    id: 'cc-dotclaude',
    title: 'Le dossier .claude',
    description: 'Comprendre la structure du dossier .claude et la gestion du contexte',
    parcours: 'claude-code',
    order: 3,
    sections: {
      info: `
        <h3>Le dossier .claude : manager du contexte</h3>
        <p>
          Le dossier <code>.claude/</code> (ou <code>.gemini/</code>, <code>.codex/</code> chez les concurrents)
          est le centre névralgique de votre configuration. Il contient tout ce qui permet à l'agent
          de <strong>comprendre votre contexte</strong> et de <strong>savoir quoi faire</strong>.
        </p>
        <h4>Structure type</h4>
        <ul>
          <li>
            <strong>agents/</strong> : sous-processus spécialisés avec leurs propres instructions.
            Chaque agent est un fichier Markdown décrivant une mission précise (créer du LaTeX, déboguer, générer des images...).
          </li>
          <li>
            <strong>skills/</strong> : savoir-faire invocables via <code>/nom-du-skill</code>.
            Chaque skill est un <strong>dossier</strong> contenant un fichier <code>SKILL.md</code> (point d'entrée obligatoire) et éventuellement des fichiers de support : <code>references/</code> (documentation), <code>scripts/</code> (programmes exécutables), <code>examples/</code> (exemples de sortie), templates, etc.
          </li>
          <li>
            <strong>commands/</strong> : commandes organisées par catégories et sous-dossiers.
            L'arborescence définit la syntaxe : <code>/categorie:sous-cat:commande</code>.
          </li>
          <li>
            <strong>settings.json</strong> : hooks (scripts automatiques), permissions, et configuration globale du projet.
          </li>
        </ul>
        <p>
          Le fichier <code>CLAUDE.md</code> à la racine orchestre l'ensemble : il définit le contexte,
          les règles, la stack technique, et indique à l'agent quels outils sont à sa disposition.
        </p>
        <h4>Équivalences multi-fournisseur</h4>
        <ul>
          <li><strong>Claude Code</strong> : <code>.claude/</code> + <code>CLAUDE.md</code></li>
          <li><strong>Gemini CLI</strong> : <code>.gemini/</code> + <code>GEMINI.md</code></li>
          <li><strong>OpenAI Codex</strong> : <code>.codex/</code> + <code>AGENTS.md</code></li>
        </ul>
        <p>Les concepts sont identiques d'un outil à l'autre — seuls les noms changent.</p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/memory" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Memory & CLAUDE.md
            </a>
            <a href="https://code.claude.com/docs/en/settings" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Settings & Permissions
            </a>
            <a href="https://code.claude.com/docs/en/sub-agents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Sub-agents & Skills
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Arborescence commentée</h3>
        <pre><code>.claude/
  agents/
    latex-main-worker.md   → Orchestre la création de documents LaTeX
    debug-tex-log.md       → Analyse les erreurs de compilation
    image-gen-agent.md     → Génère des illustrations

  skills/
    bfcours-latex/             → Un skill = un DOSSIER
      SKILL.md                 → Point d'entrée (instructions principales)
      references/              → Documentation de référence
        techniques-catalogue.md
      scripts/                 → Scripts exécutables par Claude
        compile.sh
      examples/                → Exemples de sortie attendue
        sample-output.tex
    tex-compiling-skill/
      SKILL.md
      scripts/
        compile.sh
    reveals-presentation/
      SKILL.md
      references/
        reveal-api.md

  commands/                    → Commandes slash (fusionnées avec les skills)
    createTex.md               → /createTex (raccourci rapide)
    createReveals.md           → /createReveals

  settings.json                → Hooks et permissions globales

CLAUDE.md                      → Instructions permanentes du projet</code></pre>
        <p>Voici la différence entre ces composants :</p>
        <ul>
          <li><strong>Agent</strong> : fichier .md dans <code>agents/</code>. Lancé automatiquement par l'agent principal quand il en a besoin. L'utilisateur ne l'invoque pas directement.</li>
          <li><strong>Skill</strong> : <strong>dossier</strong> dans <code>skills/</code> avec un <code>SKILL.md</code> comme point d'entrée + fichiers de support (references, scripts, examples...). Invoqué via <code>/nom-du-skill</code>. Claude peut aussi le charger automatiquement quand c'est pertinent.</li>
          <li><strong>Commande</strong> : fichier .md dans <code>commands/</code>. Fonctionnement identique à un skill simple, mais sans les fichiers de support. Les skills sont recommandés pour les nouveaux projets.</li>
        </ul>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1 : exploration</span>
          </div>
          <div class="exercise-body">
            <p>Ouvrez le dossier <code>.claude/</code> (si vous l'avez téléchargé depuis ce site). Ouvrez un fichier agent et un fichier skill dans un éditeur de texte.</p>
            <p>Pour chacun, identifiez : quel est son rôle ? quels outils utilise-t-il ? comment est-il invoqué (automatiquement ou via commande) ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici ce que vous devriez observer :</p>
              <ul>
                <li><strong>Un agent</strong> (ex : <code>latex-main-worker.md</code>) : contient un rôle ("orchestre la création LaTeX"), des étapes de workflow, et des références à d'autres skills. Il est invoqué <strong>automatiquement</strong> par l'agent principal quand la demande concerne du LaTeX.</li>
                <li><strong>Un skill</strong> (ex : <code>bfcours-latex.md</code>) : contient un frontmatter YAML (nom, description, triggers) puis des instructions détaillées. Il est invoqué <strong>manuellement</strong> via <code>/bfcours-latex</code>.</li>
              </ul>
              <p>La distinction clé : un agent est un <strong>sous-processus autonome</strong> (il a sa propre conversation), tandis qu'un skill est un <strong>ensemble d'instructions</strong> chargé dans la conversation en cours.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2 : conception</span>
          </div>
          <div class="exercise-body">
            <p>Dessinez l'arborescence de votre <code>.claude/</code> idéal. Quels agents vous manquent ? Quels skills aimeriez-vous avoir ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici un exemple d'arborescence pour un enseignant de mathématiques :</p>
              <pre><code>.claude/
  agents/
    exercice-builder.md        → Agent : crée des séries d'exercices
    evaluation-builder.md      → Agent : génère des contrôles avec barème
    correction-helper.md       → Agent : rédige des corrections détaillées
  skills/
    programmes-officiels/      → Skill (dossier)
      SKILL.md                 →   Instructions principales
      references/              →   Extraits du B.O.
    exercices-maths/
      SKILL.md
      references/
      scripts/
    fiche-revision/
      SKILL.md
      examples/sample.md
    bulletin-comments/
      SKILL.md
  commands/
    createExo.md               → /createExo (commande rapide)</code></pre>
              <p>L'idée est de penser à vos <strong>tâches répétitives</strong> : chaque tâche que vous faites souvent mérite potentiellement un skill dédié.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['configuration', 'structure'],
  },
  'cc-bfcours-setup': {
    id: 'cc-bfcours-setup',
    title: 'Exploiter le setup bfcours',
    description: 'Utiliser la configuration bfcours et créer ses propres skills',
    parcours: 'claude-code',
    order: 4,
    sections: {
      info: `
        <h3>Le setup bfcours : une configuration prête à l'emploi</h3>
        <p>
          Le setup <strong>bfcours</strong> est une configuration complète et documentée, conçue
          pour l'enseignement des mathématiques. Téléchargeable depuis ce site, il contient :
        </p>
        <ul>
          <li><strong>Agents spécialisés</strong> : création LaTeX, débogage de compilation, génération d'images, présentations...</li>
          <li><strong>Skills thématiques</strong> : <code>/bfcours-latex</code> (contenu pédagogique), <code>/reveals-presentation</code> (présentations web), <code>/programmes-officiels</code> (programmes du B.O.), etc.</li>
          <li><strong>Commandes organisées</strong> : <code>/creer:latex:createTex</code>, <code>/modifier:latex:adaptTex</code>, <code>/creer:html:createReveals</code>...</li>
          <li><strong>Hooks automatiques</strong> : correction d'encodage UTF-8 après chaque modification de fichier</li>
        </ul>
        <p>
          Ce setup est un <strong>point de départ</strong>, pas une fin en soi. Vous pouvez l'utiliser
          tel quel ou le personnaliser. Vous pouvez aussi <strong>créer vos propres skills</strong>
          au fur et à mesure de vos besoins, en vous inspirant des skills existants.
        </p>
      `,
      exemple: `
        <h3>Workflow concret avec le setup bfcours</h3>
        <h4>Créer un cours complet</h4>
        <pre><code>/createTex dans ./Cours/6eme/ fais un cours sur les fractions</code></pre>
        <p>
          Claude invoque les skills <code>tex-document-creator</code> (choix du template)
          puis <code>bfcours-latex</code> (rédaction du contenu) et enfin
          <code>tex-compiling-skill</code> (compilation en PDF). Le résultat : un fichier
          LaTeX complet avec mise en page professionnelle, directement compilé en PDF.
        </p>
        <h4>Créer une présentation</h4>
        <pre><code>/createReveals fais une présentation sur les équations pour les 4ème</code></pre>
        <h4>Adapter un document existant</h4>
        <pre><code>/modifier:latex:adaptTex adapte ce cours pour les 5ème</code></pre>
        <p>
          Chaque commande déclenche un workflow complet avec les bons skills.
          Vous n'avez pas à connaître les détails internes — décrivez ce que vous voulez,
          le système s'occupe du reste.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
          </div>
          <div class="exercise-body">
            <p>Choisissez un skill du setup bfcours et testez-le avec une demande concrète liée à votre programme actuel.</p>
            <p>Notez ce qui vous convient et ce que vous aimeriez modifier.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici comment tester un skill :</p>
              <ol>
                <li>Lancez <code>claude</code> dans le dossier où se trouve votre <code>.claude/</code></li>
                <li>Tapez <code>/</code> pour voir la liste des skills disponibles</li>
                <li>Choisissez-en un, par exemple : <code>/bfcours-latex crée un cours sur les fractions pour les 6ème</code></li>
              </ol>
              <p>Points à évaluer :</p>
              <ul>
                <li><strong>Structure</strong> : le document est-il bien organisé (titre, sections, exercices) ?</li>
                <li><strong>Contenu</strong> : est-il conforme au programme officiel du niveau demandé ?</li>
                <li><strong>Format</strong> : le LaTeX compile-t-il correctement ?</li>
                <li><strong>Adaptations souhaitées</strong> : notez ce que vous changeriez (plus d'exemples, autre progression, format différent...)</li>
              </ul>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2 : créer votre propre skill</span>
          </div>
          <div class="exercise-body">
            <p>Identifiez une tâche que vous faites souvent et que le setup ne couvre pas. Utilisez <code>/skill-creator</code> pour créer votre propre skill. Testez-le et affinez-le.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Exemples de skills utiles à créer :</p>
              <ul>
                <li><strong>Commentaires de bulletin</strong> : <code>/skill-creator crée un skill qui génère des appréciations de bulletin à partir du niveau et du comportement de l'élève</code></li>
                <li><strong>Fiches méthode</strong> : <code>/skill-creator crée un skill qui génère des fiches méthode sur une technique de calcul</code></li>
                <li><strong>Activité de groupe</strong> : <code>/skill-creator crée un skill qui planifie une activité de groupe avec rôles différenciés</code></li>
              </ul>
              <p>Le skill-creator vous posera des questions pour préciser vos besoins, puis générera un dossier <code>.claude/skills/votre-skill/</code> contenant un <code>SKILL.md</code> (instructions principales) et éventuellement des fichiers de support (références, scripts, exemples). Testez-le immédiatement avec <code>/votre-skill</code> suivi d'une demande concrète.</p>
            </div>
          </details>
        </div>
        <p>
          Le setup bfcours est fait pour évoluer avec votre pratique. Chaque skill que vous
          créez s'ajoute à votre boîte à outils et rend vos sessions plus efficaces.
        </p>
      `,
    },
    duration: '15 min',
    tags: ['bfcours', 'skills', 'workflow'],
  },

  // --- Avance ---
  'av-architecture': {
    id: 'av-architecture',
    title: 'Architecture agentique',
    description: 'Comprendre l\'architecture agents et skills de Claude',
    parcours: 'avance',
    order: 0,
    sections: {
      info: `
        <h3>Les trois piliers de l'architecture agentique</h3>
        <p>
          Claude Code repose sur une architecture en trois couches qui se combinent pour créer
          un système puissant et extensible.
        </p>
        <h4>Les agents</h4>
        <p>
          Un <strong>agent</strong> est un sous-processus spécialisé avec ses propres instructions
          et outils. Il est décrit dans un fichier Markdown placé dans <code>.claude/agents/</code>.
          Chaque agent a une mission précise : compiler du LaTeX, déboguer un fichier, générer des
          images, etc. L'agent principal orchestre les agents spécialisés selon les besoins.
        </p>
        <h4>Les skills</h4>
        <p>
          Un <strong>skill</strong> est un savoir-faire invocable via une commande slash
          (<code>/nom-du-skill</code>). Chaque skill est un <strong>dossier</strong> dans
          <code>.claude/skills/</code> contenant un <code>SKILL.md</code> (instructions principales)
          et des fichiers de support (références, scripts, exemples). Claude ne charge
          le contenu complet que quand le skill est invoqué.
        </p>
        <h4>Les hooks</h4>
        <p>
          Les <strong>hooks</strong> sont des scripts automatiques déclenchés par des événements :
          <code>PreToolUse</code> (avant une action) et <code>PostToolUse</code> (après une action).
          Configurés dans <code>settings.json</code>, ils permettent d'automatiser des tâches
          récurrentes sans intervention manuelle.
        </p>
        <p>
          Le fichier <code>CLAUDE.md</code> à la racine du projet orchestre l'ensemble :
          il définit le contexte, les règles, la stack technique, et indique quels agents
          et skills sont disponibles.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/sub-agents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Sub-agents Claude
            </a>
            <a href="https://code.claude.com/docs/en/slash-commands" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills & Commands
            </a>
            <a href="https://ai.google.dev/gemini-api/docs/function-calling" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Gemini Function Calling
            </a>
            <a href="https://geminicli.com/docs/extensions/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Gemini CLI Extensions
            </a>
            <a href="https://developers.openai.com/codex/cli/features/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex CLI Features
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Exemple concret : l'agent latex-main-worker</h3>
        <p>
          Voici comment fonctionne un workflow réel de création de document LaTeX.
          L'agent <code>latex-main-worker</code> orchestre deux skills successifs :
        </p>
        <pre><code># Agent : latex-main-worker
# Rôle : coordonner la création d'un document LaTeX complet

## Workflow
1. Invoque le skill /bfcours-latex pour générer le contenu LaTeX
2. Invoque le skill /tex-compiling-skill pour compiler en PDF
3. Signale le PDF final à l'utilisateur</code></pre>
        <h4>Structure du dossier .claude/</h4>
        <pre><code>.claude/
  agents/
    latex-main-worker.md       -> Agent : orchestre la création LaTeX
    debug-tex-log.md           -> Agent : analyse les erreurs de compilation
  skills/
    bfcours-latex/             -> Skill = un DOSSIER
      SKILL.md                 -> Instructions principales
      references/              -> Docs de référence
      scripts/                 -> Scripts exécutables
    tex-compiling-skill/
      SKILL.md
      scripts/compile.sh
    reveals-presentation/
      SKILL.md
      references/reveal-api.md
  commands/
    createTex.md               -> Commande slash rapide
  settings.json                -> Hooks et permissions</code></pre>
        <p>
          Les <strong>agents</strong> sont des fichiers .md simples. Les <strong>skills</strong> sont
          des dossiers complets avec fichiers de support. L'orchestration est pilotée par Claude,
          qui choisit les bons outils en fonction de la demande.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Investigation</span>
          </div>
          <div class="exercise-body">
            <ol>
              <li><strong>Ouvrez</strong> un fichier agent au hasard dans <code>.claude/agents/</code>. Lisez-le attentivement.</li>
              <li><strong>Devinez</strong> ce qu'il fait avant de le tester. Notez votre prédiction.</li>
              <li><strong>Testez-le</strong> en lançant Claude Code et en déclenchant une demande qui devrait activer cet agent. Votre prédiction était-elle correcte ?</li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Prenons l'exemple de <code>latex-main-worker.md</code> :</p>
              <ul>
                <li><strong>Prédiction attendue</strong> : cet agent coordonne la création de documents LaTeX en appelant des skills spécialisés</li>
                <li><strong>Test</strong> : demandez <code>/createTex crée un exercice sur les fractions</code></li>
                <li><strong>Observation</strong> : Claude lance un sous-agent qui invoque successivement les skills de rédaction LaTeX puis de compilation</li>
              </ul>
              <p>La lecture d'un fichier agent vous apprend à comprendre le <strong>workflow orchestré</strong> : quels skills sont appelés, dans quel ordre, et avec quelles conditions.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Défi : décomposer une tâche complexe</span>
          </div>
          <div class="exercise-body">
            <p>
              Imaginez que vous devez créer une <strong>petite interface web de QCM</strong> sur un thème
              donné (par exemple : QCM interactif sur les fractions pour les 6ème).
            </p>
            <ol>
              <li><strong>Identifiez les briques nécessaires</strong> : quelles étapes dans le workflow ? Quels skills intermédiaires faudrait-il ?</li>
              <li><strong>Dessinez le schéma</strong> : agent principal → skills intermédiaires → scripts d'exécution → résultat final</li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <pre><code>Agent principal
  ├── /programmes-officiels → récupérer les attendus du B.O.
  ├── /meta-prompt → générer un prompt de qualité pour les questions
  ├── /educational-app-builder → créer l'interface web
  │     ├── Générer le HTML/CSS/JS
  │     ├── Intégrer les questions
  │     └── Ajouter la correction interactive
  └── Résultat : application QCM prête à l'emploi</code></pre>
              <p>L'objectif est de penser en <strong>briques réutilisables</strong> : chaque skill peut servir dans d'autres workflows. Par exemple, <code>/programmes-officiels</code> sert aussi bien pour un QCM que pour un cours ou une évaluation.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['architecture', 'agents'],
  },
  'av-meta-prompt': {
    id: 'av-meta-prompt',
    title: 'Meta-prompt',
    description: 'Créer des prompts optimisés avec le meta-prompt',
    parcours: 'avance',
    order: 1,
    sections: {
      info: `
        <h3>Le meta-prompt : un prompt qui génère des prompts</h3>
        <p>
          Un <strong>meta-prompt</strong> est un prompt spécialisé qui permet à Claude de
          <strong>produire lui-même des prompts de qualité</strong> à partir d'une simple demande.
          Au lieu d'écrire vos prompts à la main, vous décrivez ce que vous voulez et le
          meta-prompt génère un prompt optimisé, structuré et testé.
        </p>
        <p>
          Le skill <code>/meta-prompt</code> embarque <strong>23 techniques de prompt engineering</strong>
          issues des meilleures pratiques 2025-2026 (Anthropic, OpenAI, Google, Meta). Il propose
          trois workflows :
        </p>
        <ul>
          <li>
            <strong>Création</strong> (<code>/meta-prompt create</code>) : pipeline complet en 6 phases —
            clarification de la demande → sélection des techniques adaptées → spécification →
            génération du prompt → diagnostic qualité → transformation en skill réutilisable
          </li>
          <li>
            <strong>Refactoring</strong> (<code>/meta-prompt refactor</code>) : amélioration d'un
            prompt existant en 4 phases — analyse → diagnostic → application de techniques → diff
          </li>
          <li>
            <strong>Diagnostic</strong> (<code>/meta-prompt diagnose</code>) : évaluation et scoring
            d'un prompt sur 8 axes de qualité (clarté, spécificité, structure, etc.)
          </li>
        </ul>
        <h4>Lien avec le skill-creator</h4>
        <p>
          Le skill <code>/skill-creator</code> (fourni par Anthropic) est également une forme de
          meta-prompt : il transforme une description en skill structuré. Le pipeline typique est :
        </p>
        <ol>
          <li>Idée vague → <code>/meta-prompt create</code> → prompt optimisé</li>
          <li>Prompt optimisé → <code>/skill-creator</code> → skill réutilisable dans <code>.claude/skills/</code></li>
        </ol>
      `,
      exemple: `
        <h3>Pipeline complet : de l'idée au skill</h3>
        <h4>Étape 1 : l'idée de départ</h4>
        <pre><code>/meta-prompt create
Je veux un truc qui génère des QCM</code></pre>
        <h4>Étape 2 : le meta-prompt pose des questions</h4>
        <p>Claude vous interroge pour préciser la demande :</p>
        <ul>
          <li>Pour quel niveau ? (6ème, 3ème, seconde...)</li>
          <li>Combien de questions par QCM ?</li>
          <li>Quel type de distracteurs ? (erreurs courantes, pièges calculatoires...)</li>
          <li>Format de sortie ? (LaTeX, HTML, texte brut)</li>
        </ul>
        <h4>Étape 3 : sélection automatique des techniques</h4>
        <p>Le meta-prompt choisit les techniques adaptées au contexte :</p>
        <pre><code>Contexte "Éducation/Exercices" →
  ✓ Rôle expert (professeur de mathématiques)
  ✓ Few-shot (exemples de QCM bien construits)
  ✓ Structured Output (format JSON/LaTeX structuré)
  ✓ Constitutional (vérification pédagogique)</code></pre>
        <h4>Étape 4 : prompt généré et testé</h4>
        <p>Le meta-prompt produit un prompt structuré avec rôle, contexte, instructions, contraintes et format de sortie.</p>
        <h4>Étape 5 : transformation en skill</h4>
        <pre><code>/skill-creator
Transforme ce prompt en skill réutilisable</code></pre>
        <p>
          Résultat : un dossier <code>.claude/skills/qcm-generator/SKILL.md</code> que vous pouvez
          invoquer avec <code>/qcm-generator</code> à chaque fois que vous avez besoin d'un QCM.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice : le pipeline complet</span>
          </div>
          <div class="exercise-body">
            <ol>
              <li><strong>Choisissez</strong> une tâche répétitive de votre quotidien : générer des exercices, créer des fiches de révision, rédiger des commentaires de bulletin, préparer des activités de groupe...</li>
              <li><strong>Lancez</strong> <code>/meta-prompt create</code> et décrivez cette tâche en une phrase. Observez les questions que Claude pose pour préciser votre besoin.</li>
              <li><strong>Examinez</strong> le prompt généré : est-il plus précis que ce que vous auriez écrit à la main ? Quelles techniques a-t-il choisies ?</li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Voici un exemple avec la tâche "générer des fiches de révision" :</p>
              <ol>
                <li><strong>Commande</strong> : <code>/meta-prompt create je veux générer des fiches de révision pour mes élèves</code></li>
                <li><strong>Questions posées par Claude</strong> : niveau, matière, format (A4, A5, recto-verso ?), contenu souhaité (définitions, exemples, exercices types ?), style visuel</li>
                <li><strong>Techniques sélectionnées</strong> : Rôle expert + Few-shot (exemple de fiche modèle) + Structured Output (format LaTeX) + Chain-of-Thought (progression logique du contenu)</li>
              </ol>
              <p>Le prompt généré est généralement <strong>3 à 5 fois plus détaillé</strong> que ce qu'on écrirait spontanément. Il inclut des contraintes auxquelles on ne pense pas (vérification des prérequis, variété des exercices, cohérence avec le programme...).</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Défi enchaînement</span>
          </div>
          <div class="exercise-body">
            <p>Prenez le prompt généré par l'exercice précédent et transformez-le en skill avec <code>/skill-creator</code>.</p>
            <p>Testez le skill obtenu sur une demande réelle. Est-il meilleur qu'un prompt écrit à la main ?</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>La commande : <code>/skill-creator transforme ce prompt en skill réutilisable</code></p>
              <p>Le skill-creator va :</p>
              <ol>
                <li>Extraire les instructions du prompt généré</li>
                <li>Structurer le fichier avec un frontmatter YAML (nom, description, triggers)</li>
                <li>Organiser les instructions en sections claires (Rôle, Étapes, Règles, Format)</li>
                <li>Créer le dossier <code>.claude/skills/votre-skill/</code> avec <code>SKILL.md</code> + fichiers de support</li>
              </ol>
              <p>Testez avec : <code>/votre-skill crée une fiche de révision sur les équations pour les 4ème</code>. Le résultat devrait être nettement plus structuré et complet qu'avec un prompt improvisé, car le skill intègre toutes les techniques de prompt engineering sélectionnées.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['meta-prompt', 'prompt-engineering'],
  },
  'av-skill-creator': {
    id: 'av-skill-creator',
    title: 'Créateur de skills',
    description: 'Créer vos propres skills pour Claude',
    parcours: 'avance',
    order: 2,
    sections: {
      info: `
        <h3>Qu'est-ce qu'un skill ?</h3>
        <p>
          Un <strong>skill</strong> est un <strong>dossier</strong> placé dans <code>.claude/skills/</code>
          qui enseigne à Claude un savoir-faire spécialisé. Il s'invoque en tapant
          <code>/nom-du-skill</code> suivi de votre demande, ou Claude peut le charger automatiquement
          quand c'est pertinent.
        </p>
        <h4>Structure d'un skill</h4>
        <pre style="margin: 0.75rem 0; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px; font-size: 0.85em;"><code>mon-skill/
├── SKILL.md           # Point d'entrée (obligatoire)
├── references/        # Documentation de référence
│   └── api-docs.md
├── scripts/           # Scripts exécutables par Claude
│   └── validate.sh
├── examples/          # Exemples de sortie attendue
│   └── sample.md
└── templates/         # Templates à remplir
    └── template.md</code></pre>
        <p>Le fichier <code>SKILL.md</code> est composé de :</p>
        <ul>
          <li>
            <strong>Un frontmatter YAML</strong> (entre <code>---</code>) : métadonnées du skill
            (nom, description, outils autorisés, mode d'invocation)
          </li>
          <li>
            <strong>Un corps Markdown</strong> : les instructions spécialisées que Claude
            suit lorsque le skill est invoqué
          </li>
        </ul>
        <p>
          Les fichiers de support permettent de garder le <code>SKILL.md</code> concis (moins de 500 lignes recommandées)
          tout en donnant accès à Claude à de la documentation détaillée, des scripts, et des exemples.
          Claude ne les charge que quand il en a besoin.
        </p>
        <h4>Le skill-creator</h4>
        <p>
          La commande <code>/skill-creator</code> est un skill qui aide à en créer d'autres.
          Décrivez le savoir-faire que vous souhaitez encapsuler, et il génère un dossier
          skill complet dans <code>.claude/skills/</code>.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/slash-commands" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills & Slash Commands
            </a>
            <a href="https://code.claude.com/docs/en/sub-agents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Custom Agents
            </a>
            <a href="https://developers.openai.com/codex/cli/features/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex CLI Features
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Anatomie d'un skill</h3>
        <p>Voici un exemple complet de skill pour générer des exercices de mathématiques :</p>
        <pre><code>---
name: exercices-maths
description: Génère des exercices de mathématiques progressifs
triggers:
  - exercices-maths
  - ex-maths
---

# Skill : exercices-maths

## Rôle
Créer une série d'exercices progressifs sur une notion donnée,
adaptés au niveau précisé, avec corrigés détaillés.

## Structure de sortie
1. Titre et niveau
2. Exercice 1 — facile (avec exemple résolu)
3. Exercice 2 — intermédiaire
4. Exercice 3 — difficile (avec coup de pouce)
5. Corrigés complets

## Prérequis (étape 0)
Avant de générer les exercices, invoquer le skill /programmes-officiels
pour récupérer les attendus officiels du niveau et du thème donnés.
Les exercices doivent impérativement porter sur les compétences
et capacités du programme en vigueur.

## Règles
- Utiliser le vouvoiement
- Varier les types de questions (calcul, problème, QCM)
- Inclure un encadré "Je retiens" avec la définition clé
- Pour la création du contenu de chaque exercice, utiliser ultrathink
  pour une réflexion approfondie sur la pertinence pédagogique,
  la progressivité et la variété des questions

## Format de sortie
LaTeX si le niveau est collège ou lycée, Markdown sinon.</code></pre>
        <p>
          Ce skill s'invoque avec : <code>/exercices-maths crée des exercices sur Pythagore pour la 4ème</code>.
          Claude suit alors exactement les instructions du fichier.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1 : créer votre premier skill</span>
          </div>
          <div class="exercise-body">
            <p>Lancez <code>/skill-creator</code> et décrivez un skill pour votre tâche la plus répétitive (fiches de révision, exercices d'un certain type, bilans de compétences...).</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Exemple de commande : <code>/skill-creator crée un skill qui génère des fiches de révision pour le collège avec définitions, propriétés et exercices types</code></p>
              <p>Le skill-creator va :</p>
              <ol>
                <li>Vous poser des questions pour préciser (format, niveau, contenu...)</li>
                <li>Créer un dossier <code>.claude/skills/fiche-revision/</code> avec <code>SKILL.md</code></li>
                <li>Y inclure un frontmatter YAML et des instructions structurées</li>
              </ol>
              <p>Vérifiez le fichier généré : il doit contenir au minimum un rôle, des étapes, des règles et un format de sortie.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2 : tester et affiner</span>
          </div>
          <div class="exercise-body">
            <p>Testez le skill généré avec une demande concrète liée à votre programme actuel. Puis ouvrez le fichier du skill dans <code>.claude/skills/</code> et ajoutez une règle qui manquait.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Exemple de test : <code>/fiche-revision crée une fiche sur le théorème de Pythagore pour les 4ème</code></p>
              <p>Après le test, ouvrez le fichier <code>.claude/skills/fiche-revision/SKILL.md</code> et ajoutez par exemple :</p>
              <pre><code>## Règles supplémentaires
- Inclure un schéma descriptif pour chaque propriété géométrique
- Limiter à une page recto-verso maximum
- Utiliser des couleurs pour distinguer définitions (bleu) et propriétés (rouge)</code></pre>
              <p>Retestez le skill modifié. L'affinage itératif est la clé : un skill s'améliore à chaque utilisation.</p>
            </div>
          </details>
        </div>
        <p>
          L'objectif est de pratiquer <code>/skill-creator</code>, pas de créer un fichier
          Markdown à la main. Le skill-creator fait le gros du travail pour vous.
        </p>
      `,
    },
    duration: '20 min',
    tags: ['skills', 'creation'],
  },
  'av-hooks': {
    id: 'av-hooks',
    title: 'Hooks et automatisations',
    description: 'Automatiser des tâches avec les hooks Claude',
    parcours: 'avance',
    order: 3,
    sections: {
      info: `
        <h3>Les hooks : des scripts déclenchés automatiquement</h3>
        <p>
          Les <strong>hooks</strong> sont des scripts shell qui s'exécutent automatiquement
          lorsque Claude effectue certaines actions. Ils éliminent les tâches manuelles
          répétitives en les déclenchant sans intervention de votre part.
        </p>
        <p>Il existe deux types de hooks :</p>
        <ul>
          <li>
            <strong>PreToolUse</strong> : s'exécute <em>avant</em> qu'un outil soit utilisé.
            Utile pour valider, préparer ou bloquer une action selon des conditions.
          </li>
          <li>
            <strong>PostToolUse</strong> : s'exécute <em>après</em> qu'un outil a été utilisé.
            Utile pour transformer le résultat, déclencher une compilation, corriger un fichier.
          </li>
        </ul>
        <p>Les hooks se configurent dans le fichier <code>settings.json</code> de votre dossier <code>.claude/</code>.</p>
        <h4>Exemple concret</h4>
        <p>
          Sur ce site même, un hook <strong>PostToolUse</strong> est configuré sur tous les outils
          d'écriture (<code>Write</code>, <code>Edit</code>, <code>MultiEdit</code>). Il lance
          automatiquement un script de correction d'encodage UTF-8 après chaque modification de
          fichier. Résultat : les accents sont toujours corrects sans aucune intervention manuelle.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/en/hooks" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Hooks Reference
            </a>
            <a href="https://code.claude.com/docs/en/settings" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Settings (hooks config)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Exemple de configuration de hooks</h3>
        <p>Voici un <code>settings.json</code> avec un hook configuré :</p>
        <pre><code>{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/fix-encoding.py $CLAUDE_FILE_PATHS"
          }
        ]
      }
    ]
  }
}</code></pre>
        <p>Chaque hook est défini par trois éléments :</p>
        <ul>
          <li><strong>matcher</strong> : l'outil ciblé (ex. <code>Write</code>, <code>Edit</code>, ou une regex comme <code>Write|Edit</code>)</li>
          <li><strong>type</strong> : toujours <code>"command"</code> pour un script shell</li>
          <li><strong>command</strong> : la commande à exécuter. <code>$CLAUDE_FILE_PATHS</code> contient le chemin du fichier modifié.</li>
        </ul>
        <p>
          Dans cet exemple, chaque fois que Claude écrit ou modifie un fichier, le script
          <code>fix-encoding.py</code> corrige automatiquement l'encodage UTF-8. Les accents
          sont toujours corrects sans aucune intervention manuelle.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice : ajouter un hook sonore</span>
          </div>
          <div class="exercise-body">
            <p>Configurez un hook qui <strong>joue un son</strong> lorsque Claude a une question pour vous. Pratique quand vous faites autre chose en attendant !</p>
            <ol>
              <li>
                <strong>Ajoutez</strong> ce hook dans votre <code>.claude/settings.json</code> :
              </li>
            </ol>
            <pre><code>{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -c [System.Media.SystemSounds]::Exclamation.Play()"
          }
        ]
      }
    ]
  }
}</code></pre>
            <p style="font-size: 0.85rem; color: #94a3b8;">
              Sur macOS, remplacez la commande par : <code>afplay /System/Library/Sounds/Glass.aiff</code>
              <br/>Vous pouvez aussi utiliser le chemin d'un sample son de votre choix.
            </p>
            <ol start="2">
              <li>
                <strong>Testez</strong> : lancez Claude Code et posez-lui une question ambiguë qui nécessite une clarification (ex: "Modifie le fichier" sans préciser lequel). Le son se joue-t-il quand Claude vous pose une question ?
              </li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Si le son se joue quand Claude vous pose une question, le hook fonctionne correctement.</p>
              <p>Si cela ne fonctionne pas, vérifiez :</p>
              <ul>
                <li><strong>JSON valide</strong> : pas de virgule en trop, accolades bien fermées. Utilisez un validateur JSON en ligne en cas de doute.</li>
                <li><strong>Hooks existants</strong> : si vous avez déjà des hooks dans votre <code>settings.json</code>, ajoutez cette entrée dans le tableau existant <code>PostToolUse</code> plutôt que d'en créer un nouveau.</li>
                <li><strong>Commande correcte</strong> : testez la commande PowerShell seule dans un terminal pour vérifier qu'elle joue bien un son.</li>
              </ul>
              <p>Ce hook est un bon point de départ pour comprendre le mécanisme. Vous pouvez ensuite créer des hooks plus utiles : compiler automatiquement un fichier LaTeX après modification, lancer des tests, etc.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['hooks', 'automatisation'],
  },
  'av-share': {
    id: 'av-share',
    title: 'Partager sa configuration',
    description: 'Publier et découvrir des skills via les marketplaces',
    parcours: 'avance',
    order: 4,
    sections: {
      info: `
        <h3>Les écosystèmes de partage</h3>
        <p>
          Les fournisseurs de CLI proposent désormais des <strong>marketplaces</strong>
          et registres pour partager et découvrir des skills, plugins et extensions.
          Ce n'est plus limité au copier-coller de fichiers.
        </p>
        <h4>Claude Code — Skill Hub</h4>
        <ul>
          <li><strong>Marketplace officielle</strong> : <code>claude-plugins-official</code>, accessible via <code>/plugin install nom</code></li>
          <li><strong>Standard ouvert</strong> : format Agent Skills (SKILL.md), adopté aussi par OpenAI</li>
          <li><strong>Publication</strong> : soumettez vos skills via <a href="https://docs.anthropic.com/en/docs/claude-code/overview" target="_blank" rel="noopener noreferrer">la documentation officielle</a></li>
          <li><strong>Documentation</strong> : <a href="https://docs.anthropic.com/en/docs/claude-code/overview" target="_blank" rel="noopener noreferrer">docs.anthropic.com/en/docs/claude-code/overview</a></li>
        </ul>
        <h4>Gemini CLI — Extensions Gallery</h4>
        <ul>
          <li><strong>Galerie officielle</strong> : <a href="https://github.com/google-gemini/gemini-cli" target="_blank" rel="noopener noreferrer">github.com/google-gemini/gemini-cli</a>, classée par popularité</li>
          <li><strong>Installation</strong> : <code>gemini extensions install &lt;URL GitHub&gt;</code></li>
          <li><strong>Partenaires</strong> : Figma, Postman, Shopify, Stripe, et plus</li>
          <li><strong>Documentation</strong> : <a href="https://github.com/google-gemini/gemini-cli" target="_blank" rel="noopener noreferrer">github.com/google-gemini/gemini-cli</a></li>
        </ul>
        <h4>OpenAI Codex CLI — SkillsMP</h4>
        <ul>
          <li><strong>Registre communautaire</strong> : SkillsMP (71 000+ skills compatibles)</li>
          <li><strong>Installation</strong> : <code>npx skills add</code></li>
          <li><strong>Configuration</strong> : fichiers TOML (<code>~/.codex/config.toml</code>)</li>
          <li><strong>Documentation</strong> : <a href="https://github.com/openai/codex" target="_blank" rel="noopener noreferrer">github.com/openai/codex</a></li>
        </ul>
        <h4>Le partage classique reste valide</h4>
        <p>
          Vous pouvez toujours partager via <strong>Git</strong> (committez <code>.claude/</code>),
          <strong>ZIP</strong> (comme sur ce site), ou un <strong>dépôt dédié</strong>.
        </p>
      `,
      exemple: `
        <h3>Comparaison des écosystèmes</h3>
        <pre><code>Plateforme     | Marketplace          | Installation CLI                  | Standard
---------------+----------------------+-----------------------------------+-----------
Claude Code    | Skill Hub            | /plugin install nom               | SKILL.md
Gemini CLI     | Extensions Gallery   | gemini extensions install URL     | Propriétaire
Codex CLI      | SkillsMP             | npx skills add                    | SKILL.md</code></pre>
        <h4>Installer un skill depuis un marketplace</h4>
        <p>Exemple avec Claude Code :</p>
        <pre><code># Découvrir les plugins disponibles
/plugin search latex

# Installer un plugin
/plugin install latex-helper</code></pre>
        <p>Exemple avec Gemini CLI :</p>
        <pre><code># Parcourir la galerie
# → geminicli.com/extensions/browse/

# Installer une extension
gemini extensions install https://github.com/exemple/extension</code></pre>
        <p>
          Le format <strong>SKILL.md</strong> est un standard ouvert : un skill écrit pour
          Claude Code peut être réutilisé avec Codex CLI (et inversement).
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1 : explorer un catalogue</span>
          </div>
          <div class="exercise-body">
            <p>Rendez-vous sur le <a href="https://github.com/anthropics/skills" target="_blank" rel="noopener noreferrer">Skill Hub Claude Code</a> ou la <a href="https://geminicli.com/extensions/" target="_blank" rel="noopener noreferrer">galerie Gemini CLI</a>.</p>
            <p>Identifiez 2 skills/extensions qui vous seraient utiles. Installez-en un et testez-le.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Sur le Skill Hub, cherchez par mots-clés liés à votre discipline. Pour un enseignant de maths, des skills intéressants pourraient être :</p>
              <ul>
                <li><strong>latex-helper</strong> : assistance à la rédaction LaTeX avec templates éducatifs</li>
                <li><strong>diagram-generator</strong> : génération de diagrammes et schémas</li>
                <li><strong>pdf-reader</strong> : lecture et analyse de documents PDF</li>
              </ul>
              <p>Pour installer : <code>/plugin install nom-du-skill</code> puis testez avec une demande concrète. Si le skill ne correspond pas exactement à vos besoins, utilisez-le comme base et créez votre propre version avec <code>/skill-creator</code>.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2 : recommandations collègues</span>
          </div>
          <div class="exercise-body">
            <p>Listez les 3 skills que vous recommanderiez à un collègue de votre discipline. Rédigez un mini-README de 5 lignes pour les accompagner.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Exemple de recommandation pour un collègue de maths :</p>
              <pre><code># Mes 3 skills indispensables

1. /bfcours-latex — Génère des cours LaTeX complets avec mise en page pro
2. /exercices-maths — Crée des séries d'exercices progressifs avec corrigés
3. /programmes-officiels — Vérifie la conformité avec le B.O. en vigueur

## Pour démarrer
Copiez le dossier .claude/ dans votre projet et lancez claude.
Tapez / pour voir les skills disponibles.</code></pre>
              <p>L'idée est de partager non seulement les skills mais aussi le <strong>contexte d'utilisation</strong> : dans quelle situation les utiliser, avec quels paramètres, et ce qu'on peut en attendre.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['partage', 'marketplace', 'ecosysteme'],
  },

  'av-subagents': {
    id: 'av-subagents',
    title: 'Orchestrer des sous-agents spécialisés',
    description: 'Répartir une tâche complexe entre plusieurs agents dédiés pilotés par un agent principal',
    parcours: 'avance',
    order: 5,
    sections: {
      info: `
        <h3>Diviser pour mieux produire</h3>
        <p>
          Quand une tâche est trop complexe pour un seul agent, la solution est de la
          <strong>découper en sous-tâches</strong> confiées à des agents spécialisés.
          Un agent principal (Opus) orchestre, planifie et contrôle la qualité.
          Des sous-agents (Sonnet ou Haiku) exécutent chacun leur partie.
        </p>

        <h4>Le principe</h4>
        <ol>
          <li><strong>Pré-plan</strong> — L'agent principal établit un plan avec répartition des tâches</li>
          <li><strong>Dispatch</strong> — Chaque sous-tâche est confiée à un agent spécialisé avec un prompt ciblé</li>
          <li><strong>Exécution parallèle</strong> — Les agents indépendants travaillent en même temps</li>
          <li><strong>Collecte</strong> — L'agent principal récupère les résultats</li>
          <li><strong>Assemblage</strong> — Vérification de cohérence et livraison finale</li>
        </ol>

        <h4>Architecture type</h4>
        <div style="padding: 1rem; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; margin: 1rem 0; font-size: 0.85em; font-family: monospace; color: #d1d5db;">
          <div style="text-align: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.3rem 0.75rem; background: rgba(168,85,247,0.2); border: 1px solid rgba(168,85,247,0.3); border-radius: 6px; color: #d8b4fe;">Agent Principal (Opus)</span>
          </div>
          <div style="text-align: center; color: #6b7280; margin: 0.25rem 0;">├── planifie ── dispatche ── assemble</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-top: 0.75rem;">
            <div style="padding: 0.4rem; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); border-radius: 6px; text-align: center;">
              <div style="color: #93c5fd; font-size: 0.8em;">Sonnet</div>
              <div style="color: #9ca3af; font-size: 0.7em;">Cours LaTeX</div>
            </div>
            <div style="padding: 0.4rem; background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3); border-radius: 6px; text-align: center;">
              <div style="color: #93c5fd; font-size: 0.8em;">Sonnet</div>
              <div style="color: #9ca3af; font-size: 0.7em;">Exercices</div>
            </div>
            <div style="padding: 0.4rem; background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); border-radius: 6px; text-align: center;">
              <div style="color: #86efac; font-size: 0.8em;">Haiku</div>
              <div style="color: #9ca3af; font-size: 0.7em;">Reformulations</div>
            </div>
          </div>
        </div>

        <h4>Pourquoi c'est puissant</h4>
        <p>Au-delà de la vitesse (parallélisme), les sous-agents apportent un avantage stratégique :</p>
        <ul>
          <li><strong>Économie de contexte pour l'agent principal</strong> — chaque sous-agent travaille dans sa propre fenêtre de contexte. L'agent principal ne voit que le résultat, pas les centaines de lignes de code ou de LaTeX générées. Son contexte reste propre et disponible pour la suite.</li>
          <li><strong>Conversations plus longues</strong> — puisque le contexte principal n'est pas pollué par l'implémentation, vous pouvez aller beaucoup plus loin dans une même conversation : enchaîner production, corrections, ajouts, sans que l'agent "oublie" le début.</li>
          <li><strong>Modifications ciblées</strong> — l'agent principal connaît l'existence et la structure de chaque document produit, sans en avoir lu chaque ligne. Il peut donc demander une modification ciblée à un sous-agent ("dans le fichier exercices, remplace l'exercice 3") sans recharger tout le contexte.</li>
          <li><strong>Vitesse</strong> — les agents indépendants travaillent en même temps, divisant le temps total par le nombre d'agents parallèles.</li>
        </ul>

        <h4>Quand utiliser cette approche</h4>
        <ul>
          <li>Production d'une <strong>séquence complète</strong> (cours + exercices + évaluation + diaporama)</li>
          <li>Tâche nécessitant <strong>plusieurs formats</strong> en parallèle</li>
          <li>Projet impliquant <strong>recherche + production + vérification</strong></li>
          <li>Tout cas où le pré-plan comporte <strong>3+ étapes indépendantes</strong></li>
          <li>Quand vous prévoyez une <strong>conversation longue</strong> avec des itérations multiples</li>
        </ul>

        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Rappel choix de modèle :</strong> l'agent principal est en Opus (planification).
          Les sous-agents de production sont en Sonnet (rapport qualité/coût optimal).
          Les tâches répétitives simples passent en Haiku avec des instructions très détaillées.
        </p>
      `,
      exemple: `
        <h3>Exemple : produire une séquence complète</h3>

        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Tâche
Produis une séquence complète sur les fonctions
affines en 3ème (5 séances).

# Méthode
Utilise des sous-agents spécialisés :
- Un agent pour le cours (LaTeX)
- Un agent pour les exercices (LaTeX)
- Un agent pour le diaporama (Reveals)
- Un agent pour l'évaluation finale (LaTeX)

Lance les agents indépendants en parallèle.
Vérifie la cohérence entre tous les documents.</code></pre>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db; font-size: 0.85em;">
                <span style="color: #d8b4fe;">Opus</span> — Plan établi, 4 agents lancés en parallèle<br>
                <span style="color: #93c5fd;">Sonnet #1</span> — Cours 5 séances → <code>cours-fonctions-affines.tex</code> ✅<br>
                <span style="color: #93c5fd;">Sonnet #2</span> — 18 exercices progressifs → <code>exercices-fonctions.tex</code> ✅<br>
                <span style="color: #93c5fd;">Sonnet #3</span> — Diaporama 22 slides → <code>diaporama-fonctions.html</code> ✅<br>
                <span style="color: #93c5fd;">Sonnet #4</span> — Évaluation par compétences → <code>eval-fonctions.tex</code> ✅<br>
                <span style="color: #d8b4fe;">Opus</span> — Cohérence vérifiée, 2 ajustements appliqués. Séquence livrée.
              </p>
            </div>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(129,140,248,0.08); border-radius: 8px; border-left: 3px solid rgba(129,140,248,0.4); font-size: 0.95em;">
          <strong>Temps total :</strong> ~3 minutes au lieu de ~15 minutes en séquentiel.
          Les 4 agents travaillent en même temps, l'agent principal ne fait que coordonner.
        </p>
      `,
      pratique: `
        <h3>Concevoir votre propre dispatch</h3>

        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
            <span style="font-weight: 600; color: white;">Découper une tâche en sous-agents</span>
          </div>
          <div class="exercise-body">
            <p>Vous devez produire un <strong>dossier complet pour une sortie scolaire au musée des mathématiques</strong> : fiche de préparation, questionnaire élèves, fiche de synthèse post-visite, et courrier aux parents.</p>
            <p>Découpez cette tâche :</p>
            <ul>
              <li>Combien de sous-agents lanceriez-vous ?</li>
              <li>Quel modèle pour chacun (Haiku, Sonnet, Opus) ?</li>
              <li>Lesquels peuvent tourner en parallèle ?</li>
              <li>Lesquels dépendent d'un autre ?</li>
            </ul>
          </div>
          <details class="exercise-solution">
            <summary>Voir une proposition</summary>
            <div class="solution-content">
              <p><strong>4 sous-agents :</strong></p>
              <ul>
                <li><strong>Sonnet #1</strong> — Fiche de préparation (contenu pédagogique)</li>
                <li><strong>Sonnet #2</strong> — Questionnaire élèves (dépend de #1 pour les objectifs → séquentiel)</li>
                <li><strong>Haiku #3</strong> — Courrier aux parents (tâche simple, template classique → Haiku suffit)</li>
                <li><strong>Sonnet #4</strong> — Fiche de synthèse (dépend de #1 et #2 → séquentiel)</li>
              </ul>
              <p><strong>Parallélisables :</strong> #1 et #3 (indépendants). Puis #2 après #1. Puis #4 après #1 et #2.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '~10 min',
    tags: ['sous-agents', 'orchestration', 'parallèle'],
  },

  'av-teamplay': {
    id: 'av-teamplay',
    title: 'TeamPlay : équipes d\'agents (expérimental)',
    description: 'Organiser une équipe complète d\'agents spécialisés avec mémoire partagée — avancé et expérimental',
    parcours: 'avance',
    order: 6,
    sections: {
      info: `
        <h3>Au-delà des sous-agents : les équipes persistantes</h3>
        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Capsule expérimentale.</strong> Le concept de TeamPlay est fonctionnel mais
          avancé. Il n'est <strong>jamais nécessaire</strong> pour les travaux d'enseignement courants.
          Les sous-agents classiques (capsule précédente) couvrent 99% des besoins.
          Cette capsule est là pour les curieux et les power users.
        </p>

        <p>
          La différence entre des sous-agents et une <strong>équipe TeamPlay</strong>, c'est
          la <em>persistance</em> et la <em>spécialisation profonde</em>. Dans un TeamPlay :
        </p>
        <ul>
          <li>Chaque agent a son <strong>propre skill</strong> avec des connaissances métier</li>
          <li>Chaque agent a une <strong>mémoire persistante</strong> (fichier STATUS.md) qui survit entre les sessions</li>
          <li>Les agents ont des <strong>périmètres stricts</strong> : chacun ne touche qu'à ses fichiers</li>
          <li>Un <strong>coordinateur Opus</strong> dispatche les tâches au bon agent</li>
        </ul>

        <h4>Comment ça marche</h4>
        <div style="padding: 1rem; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; margin: 1rem 0;">
          <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 1rem; font-size: 0.85em;">
            <div>
              <strong style="color: #d8b4fe;">Coordinateur (Opus)</strong>
              <ul style="color: #9ca3af; font-size: 0.9em; padding-left: 1rem; margin-top: 0.5rem;">
                <li>Lit l'état global</li>
                <li>Identifie les tâches</li>
                <li>Dispatche aux agents</li>
                <li>Valide les résultats</li>
              </ul>
            </div>
            <div>
              <strong style="color: #93c5fd;">Agents spécialisés (Sonnet)</strong>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;">
                <div style="padding: 0.4rem; background: rgba(59,130,246,0.1); border-radius: 4px; font-size: 0.8em; color: #93c5fd;">Agent Cours</div>
                <div style="padding: 0.4rem; background: rgba(59,130,246,0.1); border-radius: 4px; font-size: 0.8em; color: #93c5fd;">Agent Exercices</div>
                <div style="padding: 0.4rem; background: rgba(59,130,246,0.1); border-radius: 4px; font-size: 0.8em; color: #93c5fd;">Agent Évaluation</div>
                <div style="padding: 0.4rem; background: rgba(59,130,246,0.1); border-radius: 4px; font-size: 0.8em; color: #93c5fd;">Agent Diaporama</div>
              </div>
              <p style="color: #6b7280; font-size: 0.8em; margin-top: 0.5rem;">Chacun avec son skill, sa mémoire, son périmètre</p>
            </div>
          </div>
        </div>

        <h4>Disponibilité</h4>
        <p>
          Le skill <code>teamPlay</code> est disponible uniquement dans le
          <strong>bundle Power User</strong>. Il nécessite une configuration spécifique
          avec des skills par module et une structure de mémoire dédiée.
        </p>
      `,
      exemple: `
        <h3>Cas d'usage : projet logiciel avec équipe</h3>
        <p>
          L'exemple type de TeamPlay est un projet logiciel avec plusieurs modules.
          Le coordinateur Opus reçoit une demande, identifie les modules concernés,
          et dispatche à chaque agent spécialisé.
        </p>

        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;"><code>/teamPlay audit+fix</code></p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.85em; color: #d1d5db;">
              <p style="margin: 0 0 0.5rem;"><span style="color: #d8b4fe;">Coordinateur</span> — Lecture des STATUS.md de 9 modules</p>
              <p style="margin: 0 0 0.5rem;">9 agents lancés en parallèle (audit)...</p>
              <p style="margin: 0 0 0.5rem;"><span style="color: #93c5fd;">Agent Dashboard</span> — 11/11 features OK<br>
              <span style="color: #93c5fd;">Agent Generator</span> — 18/20 features, 2 manquantes → fix lancé<br>
              <span style="color: #93c5fd;">Agent Evaluation</span> — 22/24 features, 2 bugs → fix lancé<br>
              <em style="color: #6b7280;">... (6 autres agents)</em></p>
              <p style="margin: 0.5rem 0 0; color: #4ade80;">Rapport : 95% de parité, 3 fixes appliqués, build validé ✅</p>
            </div>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Pour l'enseignement :</strong> ce niveau d'organisation n'est pas nécessaire
          pour créer des cours ou des exercices. Les sous-agents simples (capsule précédente)
          suffisent largement. TeamPlay est conçu pour des projets logiciels ou des productions
          à très grande échelle.
        </p>
      `,
      pratique: `
        <h3>Réflexion : quand passer au TeamPlay ?</h3>

        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
            <span style="font-weight: 600; color: white;">Sous-agents classiques ou TeamPlay ?</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque situation, indiquez si des sous-agents classiques suffisent ou si TeamPlay serait pertinent :</p>
            <p><strong>1.</strong> Produire un cours + exercices + évaluation sur un chapitre</p>
            <p><strong>2.</strong> Gérer un site web avec 9 modules, chacun avec son propre code source</p>
            <p><strong>3.</strong> Créer une banque de 50 exercices classés par compétence</p>
            <p><strong>4.</strong> Maintenir une application avec mémoire des décisions passées entre sessions</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir les réponses</summary>
            <div class="solution-content">
              <p><strong>1. Sous-agents classiques</strong> — 3-4 agents ponctuels, pas besoin de mémoire persistante.</p>
              <p><strong>2. TeamPlay</strong> — 9 modules = 9 agents avec périmètres stricts et mémoire. C'est le cas d'usage type.</p>
              <p><strong>3. Sous-agents classiques</strong> — Des agents Haiku en parallèle avec instructions détaillées suffisent.</p>
              <p><strong>4. TeamPlay</strong> — La mémoire persistante (STATUS.md) entre sessions est la valeur ajoutée clé.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '~8 min',
    tags: ['teamplay', 'équipe', 'expérimental'],
  },

  // --- Prompt Craft : Parler à une IA ---
  'pc-structure': {
    id: 'pc-structure',
    title: 'Organiser ses demandes clairement',
    description: 'Structurer un prompt avec titres, listes et blocs pour obtenir de meilleures réponses',
    parcours: 'prompt-craft',
    order: 0,
    sections: {
      info: `
        <h3>Voyez la différence par vous-même</h3>
        <p>
          Avant d'expliquer quoi que ce soit, regardez ces deux messages envoyés à la même IA,
          pour la même demande :
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
          <div style="padding: 1rem; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px;">
            <strong style="color: #f87171;">❌ Message brut</strong>
            <p style="font-size: 0.9em; margin-top: 0.5rem; color: #d1d5db;">
              "Fais-moi un exercice de maths sur les fractions pour des 5ème avec 3 questions progressives et la correction"
            </p>
          </div>
          <div style="padding: 1rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px;">
            <strong style="color: #4ade80;">✅ Message structuré</strong>
            <pre style="font-size: 0.8em; margin-top: 0.5rem; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; overflow-x: auto; color: #d1d5db;"><code># Rôle
Enseignant de maths expérimenté

# Contexte
- Classe de 5ème, niveau hétérogène
- Thème : fractions (addition)

# Tâche
3 questions progressives

# Format
- Fichier : exercice.tex (LaTeX)
- Énoncé numéroté + correction détaillée</code></pre>
          </div>
        </div>
        <p>
          Le message de gauche produit une réponse <em>acceptable</em>. Celui de droite produit
          une réponse <strong>exactement comme vous la vouliez</strong>. La différence ?
          Quelques titres et listes. C'est tout.
        </p>

        <h4>Les niveaux de titres : la hiérarchie</h4>
        <p>
          En Markdown, les <code>#</code> créent des titres avec une <strong>hiérarchie</strong> :
        </p>
        <ul>
          <li><code>#</code> = Titre principal — <strong>un seul</strong> par prompt, c'est le sujet global</li>
          <li><code>##</code> = Sous-titres — autant que nécessaire pour structurer les sections</li>
          <li><code>###</code> = Sous-sous-titres — pour détailler à l'intérieur d'une section</li>
        </ul>
        <p>
          C'est comme un plan de cours : un titre de chapitre, puis des parties, puis des sous-parties.
          Ce sont les conventions standard du Markdown, utilisées partout (GitHub, documentation, IA).
        </p>

        <h4>Les autres briques utiles</h4>
        <ul>
          <li><code>**Gras**</code> et <code>*italique*</code> — pour l'emphase sur les points importants</li>
          <li><code>- Listes</code> à puces ou numérotées — pour les étapes, critères, contraintes</li>
          <li><code>\`code inline\`</code> et blocs <code>\`\`\`</code> — pour les termes techniques, noms de fichiers, exemples de code (surtout utile pour les agents, mais bon à connaître)</li>
          <li><code>> Citations</code> — pour encadrer du contexte, des consignes spéciales ou des extraits</li>
        </ul>
        <p>
          Ces éléments forment le Markdown : un langage de mise en forme que toutes les IA
          lisent nativement. Les <code>#</code> sont réellement interprétés comme des séparateurs
          de sections par le modèle.
        </p>

        <h4>Le patron universel : Rôle — Contexte — Tâche — Format</h4>
        <p>
          Tout bon prompt suit cette structure en 4 blocs. Chaque bloc est un titre <code>##</code>.
        </p>

        <p><strong>## Rôle</strong> — Le prisme de lecture du modèle</p>
        <p>
          Le rôle définit la <em>perspective</em> avec laquelle l'IA va traiter votre demande.
          Ce n'est pas toujours "enseignant de maths" ! Exemples :
        </p>
        <ul>
          <li><em>"Tu es un enseignant de mathématiques expérimenté en collège"</em> → production pédagogique classique</li>
          <li><em>"Tu es un développeur, tu reçois les demandes de l'enseignant et tu codes les ressources"</em> → production technique, code, scripts</li>
          <li><em>"Tu es un élève de 3ème. Tu analyses cette ressource et tu donnes un rapport simple : ce que tu comprends, ce qui te bloque, ce qui est trop long"</em> → relecture critique côté apprenant</li>
          <li><em>"Tu es un inspecteur pédagogique. Tu vérifies la conformité avec le programme officiel"</em> → audit de conformité</li>
        </ul>
        <p style="padding: 0.75rem 1rem; background: rgba(129,140,148,0.08); border-radius: 8px; border-left: 3px solid rgba(129,140,148,0.4); font-size: 0.95em;">
          Changer le rôle, c'est changer le <strong>point de vue</strong> du modèle sur votre demande.
          La même ressource analysée par un "élève", un "enseignant" et un "inspecteur" donnera
          trois retours complètement différents.
        </p>

        <p><strong>## Contexte</strong> — Le cadre de travail</p>
        <p>Niveau, thème, effectif, durée, contraintes particulières. Plus c'est précis, moins l'IA invente.</p>

        <p><strong>## Tâche</strong> — Ce que l'IA doit faire</p>
        <p>L'action concrète, découpée en étapes si nécessaire.</p>

        <p><strong>## Format</strong> — Comment vous voulez le résultat</p>
        <p>
          Le format, c'est <strong>d'abord le type de fichier</strong> : LaTeX (<code>.tex</code>),
          HTML (<code>.html</code>), JSON (<code>.json</code>), Python (<code>.py</code>),
          Markdown (<code>.md</code>)... Puis ensuite les détails de présentation :
          combien de colonnes, correction séparée ou non, style des en-têtes, etc.
        </p>
        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Le format change radicalement le résultat.</strong> Un même QCM demandé en
          <code>.tex</code> donnera un PDF imprimable, en <code>.json</code> des données
          exploitables par une app, en <code>.html</code> un quiz interactif.
        </p>

        <h4>L'approche par ajustements successifs</h4>
        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>3 choses à retenir :</strong><br>
          1. Les allers-retours avec l'IA sont <strong>coûteux en tokens</strong> (= en temps et en argent).<br>
          2. Il y aura <strong>toujours</strong> des ajustements — c'est normal.<br>
          3. L'objectif est d'en avoir <strong>le moins possible</strong>. Un prompt bien structuré dès le départ, c'est moins de corrections après.
        </p>

        <p style="padding: 0.75rem 1rem; background: rgba(239,68,68,0.08); border-radius: 8px; border-left: 3px solid rgba(239,68,68,0.4); font-size: 0.95em;">
          <strong>Attention :</strong> Un prompt bien structuré améliore la réponse, mais
          <strong>ne garantit pas qu'elle soit correcte</strong>. Vérifiez toujours le contenu
          mathématique produit par l'IA. Les modèles peuvent halluciner des théorèmes ou
          faire des erreurs de calcul.
        </p>
      `,
      exemple: `
        <h3>Deux scénarios pour voir l'impact</h3>
        <p>Voici deux conversations fictives montrant la différence concrète entre un prompt brut et un prompt structuré.</p>

        <h4>Scénario A : demande plate</h4>
        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;">"Fais-moi un QCM sur les fractions pour des 5ème"</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1;">
              <p style="margin: 0 0 0.5rem; color: #d1d5db;">Voici un QCM sur les fractions :</p>
              <p style="margin: 0; color: #9ca3af; font-size: 0.9em;">
                1. 1/2 + 1/3 = ? &nbsp; A) 2/5 &nbsp; B) 5/6 &nbsp; C) 1/6<br>
                2. Simplifier 4/8 &nbsp; A) 1/2 &nbsp; B) 2/4 &nbsp; C) 1/4<br>
                <em>(Texte brut, pas de mise en page, pas de contexte pédagogique, mélange les notions...)</em>
              </p>
            </div>
          </div>
        </div>

        <h4>Scénario B : demande structurée → format JSON</h4>
        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.85em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Rôle
Enseignant de maths en collège

# Contexte
- 5ème, thème : addition de fractions
- QCM de 5 questions

# Tâche
Créer un QCM progressif (facile → difficile)

# Format
- Fichier : qcm-fractions.json
- Structure : question, options[], answer, explanation
- 4 choix par question</code></pre>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.8em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code>[
  {
    "question": "Calculer 1/4 + 1/4",
    "options": ["1/2", "2/8", "1/8", "2/4"],
    "answer": "1/2",
    "explanation": "1/4 + 1/4 = 2/4 = 1/2"
  },
  ...
]</code></pre>
            </div>
          </div>
        </div>

        <h4>Le même JSON, rendu visuellement</h4>
        <p style="color: #9ca3af; font-size: 0.9em; margin-bottom: 0.75rem;">
          Ce JSON peut être directement injecté dans une application web. Voici ce que l'utilisateur final verrait :
        </p>
        <div style="margin: 1rem 0; padding: 1.25rem; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;">
          <div style="font-size: 0.85em; color: #e0e0f0;">
            <div style="margin-bottom: 1.25rem;">
              <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="background: rgba(139,92,246,0.2); color: #c4b5fd; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">Question 1</span>
              </div>
              <p style="margin: 0 0 0.75rem; font-weight: 500;">Calculer &nbsp;<span style="font-family: serif; font-size: 1.1em;">1/4 + 1/4</span></p>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.3); border-radius: 6px; cursor: pointer;">
                  <span style="width: 16px; height: 16px; border-radius: 50%; border: 2px solid #4ade80; display: inline-flex; align-items: center; justify-content: center;"><span style="width: 8px; height: 8px; border-radius: 50%; background: #4ade80;"></span></span>
                  <span>A) 1/2</span>
                  <span style="margin-left: auto; font-size: 0.75rem; color: #4ade80;">✓</span>
                </label>
                <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;">
                  <span style="width: 16px; height: 16px; border-radius: 50%; border: 2px solid #6b7280; display: inline-block;"></span>
                  <span>B) 2/8</span>
                </label>
                <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;">
                  <span style="width: 16px; height: 16px; border-radius: 50%; border: 2px solid #6b7280; display: inline-block;"></span>
                  <span>C) 1/8</span>
                </label>
                <label style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;">
                  <span style="width: 16px; height: 16px; border-radius: 50%; border: 2px solid #6b7280; display: inline-block;"></span>
                  <span>D) 2/4</span>
                </label>
              </div>
              <div style="margin-top: 0.5rem; padding: 0.5rem 0.75rem; background: rgba(34,197,94,0.08); border-radius: 6px; font-size: 0.85em; color: #86efac;">
                <strong>Explication :</strong> 1/4 + 1/4 = 2/4 = 1/2
              </div>
            </div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
          <div style="padding: 0.75rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; color: #a78bfa; font-weight: 600; text-transform: uppercase; margin-bottom: 0.25rem;">Vue développeur</div>
            <div style="font-size: 0.85rem; color: #d1d5db;">Données JSON brutes</div>
          </div>
          <div style="padding: 0.75rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px; text-align: center;">
            <div style="font-size: 0.75rem; color: #4ade80; font-weight: 600; text-transform: uppercase; margin-bottom: 0.25rem;">Vue utilisateur</div>
            <div style="font-size: 0.85rem; color: #d1d5db;">Quiz interactif rendu</div>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(129,140,148,0.08); border-radius: 8px; border-left: 3px solid rgba(129,140,148,0.4); font-size: 0.95em;">
          <strong>C'est le même contenu.</strong> Le format que vous demandez détermine ce que l'IA produit :
          du JSON exploitable par une app, du LaTeX compilable en PDF, ou du HTML directement affichable.
          Le <code>## Format</code> est la section qui change le plus radicalement le résultat.
        </p>
      `,
      pratique: `
        <h3>Testez avec le vrai skill Meta-Prompt</h3>
        <p>
          Ce que vous allez copier ci-dessous n'est pas un simple exemple — c'est le
          <strong>vrai skill professionnel</strong> utilisé par les agents IA pour optimiser
          des prompts. Vous copiez les mêmes instructions qu'un agent Claude Code recevrait.
        </p>

        <div style="margin: 1.5rem 0;">
          <h4>Mode d'emploi</h4>
          <ol>
            <li>Écrivez votre demande dans la zone de texte ci-dessous</li>
            <li>Cliquez sur "Copier le tout" — votre demande sera ajoutée au skill complet</li>
            <li>Collez dans Claude Desktop, Claude Code, ou toute autre IA</li>
            <li>Observez : l'IA applique les 23 techniques de prompt engineering pour restructurer votre demande</li>
          </ol>
        </div>

        <div style="position: relative; margin: 1.5rem 0;">
          <div style="font-size: 0.8rem; color: #a78bfa; font-weight: 600; margin-bottom: 0.5rem;">SKILL META-PROMPT (142 lignes — aperçu)</div>
          <pre id="meta-prompt-preview" style="background: rgba(0,0,0,0.4); border: 1px solid rgba(139,92,246,0.3); border-radius: 8px 8px 0 0; padding: 1rem; font-size: 0.78em; line-height: 1.5; overflow: hidden; max-height: 12rem; color: #d1d5db;"><code># Meta-Prompt - Fabrique de Prompts Optimises

Skill central pour creer, refactorer et optimiser des prompts
selon les techniques de pointe 2025-2026.

## Declenchement
- Creer un nouveau prompt pour une tache specifique
- Ameliorer/refactorer un prompt existant
- Diagnostiquer la qualite d'un prompt

## Trois workflows
### Workflow 1 : Creation
Pipeline complet en 6 phases obligatoires :
clarification → techniques → specification → generation
→ diagnostic → livrable
...</code></pre>
          <div style="background: linear-gradient(transparent, rgba(0,0,0,0.6)); height: 3rem; margin-top: -3rem; position: relative; border-radius: 0; pointer-events: none;"></div>
          <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(139,92,246,0.3); border-top: none; border-radius: 0 0 8px 8px; padding: 0.75rem 1rem;">
            <div style="font-size: 0.8rem; color: #9ca3af; margin-bottom: 0.5rem;">Votre demande (sera ajoutée à la fin du skill) :</div>
            <textarea id="user-request-input" placeholder="Ex : Crée-moi un exercice sur les équations en 4ème avec correction détaillée..." style="width: 100%; min-height: 60px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 0.75rem; color: #e0e0f0; font-family: inherit; font-size: 0.85rem; resize: vertical;"></textarea>
          </div>
        </div>

        <button onclick="
          var skillContent = '# Meta-Prompt - Fabrique de Prompts Optimises\\n\\nSkill central pour creer, refactorer et optimiser des prompts selon les techniques de pointe 2025-2026. Chaque prompt produit est transforme en livrable reutilisable (skill, agent ou commande).\\n\\n## Declenchement\\n\\n- Creer un nouveau prompt pour une tache specifique\\n- Ameliorer/refactorer un prompt existant\\n- Diagnostiquer la qualite d\\'un prompt\\n- Comprendre quelle technique appliquer selon un contexte\\n- Preparer un prompt avant de creer un skill ou un agent\\n\\n## Trois workflows\\n\\n### Workflow 1 : Creation\\n\\nPipeline complet en 6 phases obligatoires : clarification → techniques → specification → generation → diagnostic → livrable.\\n\\nPhases :\\n1. Challenger la demande — Clarifier sur 7 dimensions\\n2. Selectionner les techniques — Choisir dans le catalogue selon la matrice de decision\\n3. Specifier — Formulaire HTML interactif ou questions structurees\\n4. Generer — Appliquer les techniques, produire le prompt structure\\n5. Diagnostiquer — Scoring automatique 8 axes, corriger les faiblesses\\n6. Rendre utile — Transformer en livrable\\n\\n### Workflow 2 : Refactoring\\n\\nAmelioration d\\'un prompt existant en 4 phases : charger → diagnostiquer → appliquer techniques → presenter diff.\\n\\n### Workflow 3 : Diagnostic\\n\\nEvaluation et scoring d\\'un prompt sur 8 axes de qualite (1-5 par axe).\\n\\n## Matrice de decision rapide\\n\\n| Contexte | Techniques prioritaires |\\n|----------|------------------------|\\n| Logiciel/Code | Role expert + XML tags + CoT structure + Structured Output + ReAct |\\n| Education/Cours | Role pedagogique + Few-shot + CoT + Constitutional (verification) |\\n| Analyse de donnees | RAG + Structured Output + Self-Consistency + CoT |\\n| Generation creative | Role + Temperature guidance + Few-shot style + Constitutional |\\n| Agent autonome | System prompt architecture + ReAct + State management + Agentic 3-reminders |\\n| Classification/Tri | Structured Output + Few-shot + Zero-shot CoT |\\n\\n## Structure obligatoire d\\'un prompt genere\\n\\nTout prompt produit respecte cette structure :\\n\\n# [Titre descriptif]\\n## Role\\n## Contexte\\n## Instructions\\n## Contraintes\\n## Format de sortie\\n## Exemples\\n## Variables\\n## Criteres de qualite (auto-verification)\\n\\n## Regles de generation\\n\\n1. XML tags pour toute donnee variable\\n2. Forme imperative\\n3. Variables en SCREAMING_SNAKE_CASE\\n4. Minimum 2 exemples si format de sortie precis\\n5. Integrer raisonnement etape par etape pour taches complexes\\n6. Toujours specifier le format exact de sortie\\n7. Criteres d\\'auto-verification en fin de prompt\\n8. Instructions critiques en debut ET en fin de prompt';
          var userReq = document.getElementById('user-request-input').value;
          var full = skillContent + (userReq ? '\\n\\n---\\n\\n# Ma demande\\n\\n' + userReq : '');
          navigator.clipboard.writeText(full).then(function(){
            var b = event.target;
            b.textContent = '✅ Copié ! (' + full.length + ' caractères)';
            b.style.background = 'linear-gradient(135deg, rgba(34,197,94,0.4), rgba(16,185,129,0.4))';
            setTimeout(function(){ b.textContent = '📋 Copier le tout (skill + votre demande)'; b.style.background = 'linear-gradient(135deg, rgba(139,92,246,0.4), rgba(99,102,241,0.4))'; }, 2500);
          });
        " style="width: 100%; padding: 0.75rem; background: linear-gradient(135deg, rgba(139,92,246,0.4), rgba(99,102,241,0.4)); border: 1px solid rgba(139,92,246,0.5); color: #e0e0f0; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: all 0.2s; margin-top: 0.5rem;">📋 Copier le tout (skill + votre demande)</button>

        <h4 style="margin-top: 1.5rem;">Auto-vérification</h4>
        <p>Après avoir testé, vérifiez :</p>
        <ul>
          <li>✅ L'IA a-t-elle appliqué la structure Rôle/Contexte/Tâche/Format ?</li>
          <li>✅ A-t-elle ajouté des détails que vous aviez oubliés ?</li>
          <li>✅ Le format de sortie est-il explicitement spécifié (type de fichier + structure) ?</li>
          <li>✅ Des critères d'auto-vérification sont-ils présents ?</li>
        </ul>
        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          <strong>Ce que vous venez de faire :</strong> vous avez utilisé un skill professionnel
          de 142 lignes pour optimiser votre prompt. C'est exactement ce que fait un agent IA
          quand vous tapez <code>/meta-prompt</code> dans Claude Code.
        </p>
      `,
    },
    duration: '~10 min',
    tags: ['markdown', 'prompt', 'structure'],
  },

  'pc-sources': {
    id: 'pc-sources',
    title: 'S\'appuyer sur ses propres ressources',
    description: 'Fournir des fichiers sources à l\'IA pour limiter les hallucinations et garantir la qualité du contenu',
    parcours: 'prompt-craft',
    order: 1,
    sections: {
      info: `
        <h3>La règle d'or : moins l'IA invente, mieux c'est</h3>
        <p>
          Une IA qui travaille <em>à partir de rien</em> va inventer du contenu. Et quand elle
          invente, elle peut <strong>halluciner</strong> : théorèmes faux, formules incorrectes,
          exercices incohérents. C'est le risque principal.
        </p>
        <p>
          La parade est simple : <strong>donnez-lui vos fichiers</strong>. Un ancien cours,
          des notes manuscrites scannées, un extrait du programme officiel, une fiche d'exercices
          existante... Plus l'IA s'appuie sur du contenu <em>que vous avez validé</em>,
          moins elle a besoin d'inventer, et moins elle hallucine.
        </p>

        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          <strong>C'est ici que votre expertise fait la différence.</strong>
          L'IA excelle pour le formatage, la personnalisation et la production de dérivés.
          Mais la qualité du contenu mathématique, c'est <em>vous</em> qui la garantissez —
          en fournissant les bonnes sources.
        </p>

        <h4>Quels fichiers fournir ?</h4>
        <ul>
          <li><strong>Vos documents de cours</strong> — fichiers .tex, .docx, .pdf, même des scans de notes manuscrites</li>
          <li><strong>Vos anciens exercices</strong> — l'IA peut en générer des variantes sans inventer de contenu</li>
          <li><strong>Le programme officiel</strong> — via le skill <code>/programmes-officiels</code> ou un extrait du BO</li>
          <li><strong>Des manuels ou extraits</strong> — pour cadrer le vocabulaire et le niveau de formalisme</li>
          <li><strong>Des corrections existantes</strong> — pour que l'IA reproduise votre style de correction</li>
        </ul>

        <h4>Comment fournir un fichier</h4>
        <p>Deux méthodes selon votre outil :</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.75rem; background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); border-radius: 8px;">
            <strong style="color: #86efac; font-size: 0.9em;">Claude Code / CLI</strong>
            <p style="font-size: 0.85em; color: #9ca3af; margin: 0.5rem 0 0;">
              Utilisez <code>@nom-du-fichier</code> dans votre message.
              L'agent lira le fichier automatiquement.<br>
              <code style="font-size: 0.85em;">@mon-cours-thales.tex</code>
            </p>
          </div>
          <div style="padding: 0.75rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <strong style="color: #93c5fd; font-size: 0.9em;">Claude Desktop</strong>
            <p style="font-size: 0.85em; color: #9ca3af; margin: 0.5rem 0 0;">
              Glissez le fichier dans la zone de chat, ou utilisez
              le bouton d'attachement (trombone).<br>
              Formats : PDF, images, texte, code...
            </p>
          </div>
        </div>

        <h4>Ce que l'IA fait bien avec vos sources</h4>
        <div style="margin: 1rem 0;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.85em;">
            <tr style="border-bottom: 2px solid rgba(255,255,255,0.15);">
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Tâche</th>
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Source nécessaire</th>
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Risque sans source</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem; color: #d1d5db;">Reformater un cours en LaTeX</td>
              <td style="padding: 0.5rem; color: #86efac;">Votre cours (.docx, .pdf, scan)</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Quasi nul — elle reformate, n'invente pas</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem; color: #d1d5db;">Créer des exercices variantes</td>
              <td style="padding: 0.5rem; color: #86efac;">Vos exercices existants</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Faible — elle varie la forme, garde la logique</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem; color: #d1d5db;">Créer un blueprint / fiche de révision</td>
              <td style="padding: 0.5rem; color: #86efac;">Votre cours complet</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Faible — elle extrait et synthétise</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem; color: #d1d5db;">Créer un diaporama depuis un cours</td>
              <td style="padding: 0.5rem; color: #86efac;">Votre cours comme base</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Faible — elle reformate en slides</td>
            </tr>
            <tr>
              <td style="padding: 0.5rem; color: #d1d5db;">Créer un cours de zéro</td>
              <td style="padding: 0.5rem; color: #f87171;">Programme officiel + notes</td>
              <td style="padding: 0.5rem; color: #f87171;">Élevé — contenu inventé, à vérifier</td>
            </tr>
          </table>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Retenez :</strong> plus vous fournissez de sources, plus l'IA se comporte
          comme un <em>assistant de mise en forme</em> et moins comme un <em>auteur</em>.
          C'est quand elle est auteur qu'elle hallucine.
        </p>
      `,
      exemple: `
        <h3>Le même besoin, avec et sans source</h3>

        <h4>Sans source — l'IA invente</h4>
        <div style="margin: 0.75rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db; font-size: 0.9em;">Crée-moi un cours sur le théorème de Thalès pour des 3ème</p>
            </div>
          </div>
          <div style="padding: 0.5rem 1rem; background: rgba(239,68,68,0.05); font-size: 0.8em; color: #f87171;">
            ⚠️ L'IA va inventer le contenu, choisir ses propres exemples, sa progression, ses formulations.
            Résultat potentiellement correct mais à vérifier intégralement — autant l'écrire soi-même.
          </div>
        </div>

        <h4>Avec source — l'IA transforme</h4>
        <div style="margin: 0.75rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Contexte
Cours de 3ème sur Thalès
@mon-cours-thales-brouillon.docx

# Tâche
/createTex
Mets en forme ce cours en LaTeX avec le package bfcours.
Garde exactement mon contenu, mes exemples et ma progression.
Ajoute les figures TikZ correspondant à mes descriptions.</code></pre>
            </div>
          </div>
          <div style="padding: 0.5rem 1rem; background: rgba(16,185,129,0.05); font-size: 0.8em; color: #86efac;">
            ✅ L'IA reformate votre contenu validé. Elle n'invente rien.
            Les figures sont générées à partir de vos descriptions. Vérification rapide.
          </div>
        </div>

        <h4>Encore mieux : produire des dérivés</h4>
        <p>Une fois que vous avez un cours source validé, l'IA peut en produire des dérivés sans inventer :</p>
        <div style="display: grid; grid-template-columns: 1fr; gap: 0.5rem; margin: 1rem 0;">
          <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;">
            <span style="font-size: 0.9em;">📄</span>
            <span style="color: #d1d5db; font-size: 0.85em;"><strong>Cours source</strong> → <em>Fiche de révision</em> (blueprint) : synthèse des points clés</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;">
            <span style="font-size: 0.9em;">📄</span>
            <span style="color: #d1d5db; font-size: 0.85em;"><strong>Cours source</strong> → <em>Diaporama</em> : mêmes contenus, format slides</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;">
            <span style="font-size: 0.9em;">📄</span>
            <span style="color: #d1d5db; font-size: 0.85em;"><strong>Cours source</strong> → <em>QCM d'auto-évaluation</em> : questions tirées du cours</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;">
            <span style="font-size: 0.9em;">📄</span>
            <span style="color: #d1d5db; font-size: 0.85em;"><strong>Exercices source</strong> → <em>Variantes</em> : mêmes types, valeurs différentes</span>
          </div>
          <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.75rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;">
            <span style="font-size: 0.9em;">📄</span>
            <span style="color: #d1d5db; font-size: 0.85em;"><strong>Exercices source</strong> → <em>Correction détaillée</em> : pas besoin de la rédiger vous-même</span>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(129,140,248,0.08); border-radius: 8px; border-left: 3px solid rgba(129,140,248,0.4); font-size: 0.95em;">
          <strong>L'IA comme multiplicateur :</strong> un seul document source bien fait
          peut donner 5 dérivés de qualité — sans invention, sans hallucination, et en quelques minutes.
        </p>
      `,
      pratique: `
        <h3>Prenez le réflexe "source d'abord"</h3>

        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
            <span style="font-weight: 600; color: white;">Identifier la bonne source</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque tâche, quelle source fourniriez-vous à l'IA ?</p>

            <p><strong>A)</strong> Créer une fiche de révision sur les identités remarquables</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Source : ...</p>

            <p><strong>B)</strong> Mettre en forme vos notes manuscrites sur les vecteurs en LaTeX</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Source : ...</p>

            <p><strong>C)</strong> Créer 10 exercices supplémentaires sur les équations</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Source : ...</p>

            <p><strong>D)</strong> Produire un diaporama pour une séance sur les probabilités</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Source : ...</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir les réponses</summary>
            <div class="solution-content">
              <p><strong>A)</strong> Votre cours sur les identités remarquables (le fichier .tex ou .docx). La fiche de révision en est un <em>dérivé</em> — l'IA extrait et synthétise, elle n'invente pas.</p>
              <p><strong>B)</strong> Le scan ou la photo de vos notes manuscrites. L'IA fait de la reconnaissance + mise en forme. Risque d'hallucination quasi nul.</p>
              <p><strong>C)</strong> Vos exercices existants sur les équations (même 3-4 suffisent). L'IA en génère des variantes en changeant les valeurs et les contextes, pas la structure mathématique.</p>
              <p><strong>D)</strong> Votre cours écrit sur les probabilités. Le diaporama est un reformatage en slides — mêmes contenus, présentation différente.</p>
            </div>
          </details>
        </div>

        <div class="exercise-card" style="margin-top: 1rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
            <span style="font-weight: 600; color: white;">Évaluer le risque d'hallucination</span>
          </div>
          <div class="exercise-body">
            <p>Classez ces demandes du <strong>moins risqué</strong> au <strong>plus risqué</strong> en termes d'hallucination :</p>
            <ol type="a">
              <li>"Reformate mon cours Word en LaTeX" (avec le fichier fourni)</li>
              <li>"Crée un cours complet sur les statistiques pour des 2nde"</li>
              <li>"Génère 5 variantes de cet exercice" (avec l'exercice fourni)</li>
              <li>"Crée une évaluation sur les fonctions affines"</li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir la réponse</summary>
            <div class="solution-content">
              <p>Du moins risqué au plus risqué :</p>
              <p><strong>1. (a)</strong> Reformatage — risque quasi nul, l'IA ne fait que changer le format</p>
              <p><strong>2. (c)</strong> Variantes — risque faible, l'IA modifie des valeurs dans une structure existante</p>
              <p><strong>3. (d)</strong> Évaluation sans source — risque moyen, l'IA invente les exercices mais le thème est ciblé</p>
              <p><strong>4. (b)</strong> Cours complet sans source — risque élevé, l'IA invente tout le contenu, la progression, les exemples</p>
              <p style="margin-top: 0.5rem;"><strong>Règle :</strong> plus la tâche demande de la <em>création de contenu</em>, plus le risque augmente. Plus elle se limite à de la <em>transformation</em>, plus le risque diminue.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '~8 min',
    tags: ['sources', 'fichiers', 'hallucinations'],
  },

  'pc-models': {
    id: 'pc-models',
    title: 'Choisir le bon modèle',
    description: 'Adapter la puissance du modèle à la complexité de la tâche pour optimiser coût et qualité',
    parcours: 'prompt-craft',
    order: 1,
    sections: {
      info: `
        <h3>Tous les modèles ne se valent pas — et c'est une force</h3>
        <p>
          Quand vous parlez à une IA, vous ne parlez pas toujours au même "cerveau".
          Selon le fournisseur, vous avez accès à <strong>un ou plusieurs modèles</strong>
          de puissances différentes. Choisir le bon modèle pour la bonne tâche, c'est
          comme choisir entre un stylo, un crayon et un feutre : tous écrivent,
          mais pas avec la même précision ni le même coût.
        </p>

        <h4>Ce que proposent les fournisseurs</h4>
        <p style="padding: 0.5rem 0.75rem; background: rgba(245,158,11,0.08); border-radius: 6px; border-left: 3px solid rgba(245,158,11,0.3); font-size: 0.85em; color: #fbbf24; margin-bottom: 0.75rem;">
          Les noms et versions de modèles changent très fréquemment. On ne les affiche pas ici pour éviter les mises à jour perpétuelles. Ce qui compte, c'est le <strong>principe des niveaux</strong>.
        </p>
        <div style="margin: 1rem 0; overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
            <tr style="border-bottom: 2px solid rgba(255,255,255,0.15);">
              <th style="text-align: left; padding: 0.75rem; color: #a78bfa;">Fournisseur</th>
              <th style="text-align: left; padding: 0.75rem; color: #a78bfa;">Niveaux de modèle</th>
              <th style="text-align: left; padding: 0.75rem; color: #a78bfa;">Particularité</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.75rem; font-weight: 600; color: #c4b5fd;">Anthropic (Claude)</td>
              <td style="padding: 0.75rem; color: #d1d5db;">
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(34,197,94,0.15); color: #86efac; font-size: 0.8em; margin-right: 0.25rem;">Haiku</span>
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(59,130,246,0.15); color: #93c5fd; font-size: 0.8em; margin-right: 0.25rem;">Sonnet</span>
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(168,85,247,0.15); color: #d8b4fe; font-size: 0.8em;">Opus</span>
              </td>
              <td style="padding: 0.75rem; color: #9ca3af;">3 niveaux distincts (Haiku, Sonnet, Opus) + mode "ultrathink" pour la réflexion étendue</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.75rem; font-weight: 600; color: #d1d5db;">OpenAI (GPT / Codex)</td>
              <td style="padding: 0.75rem; color: #d1d5db;">
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(255,255,255,0.1); color: #d1d5db; font-size: 0.8em;">Modèle principal</span>
              </td>
              <td style="padding: 0.75rem; color: #9ca3af;">Un modèle principal avec différents modes de réflexion (thinking tokens)</td>
            </tr>
            <tr>
              <td style="padding: 0.75rem; font-weight: 600; color: #d1d5db;">Google (Gemini CLI)</td>
              <td style="padding: 0.75rem; color: #d1d5db;">
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(255,255,255,0.1); color: #d1d5db; font-size: 0.8em; margin-right: 0.25rem;">Flash / Preview</span>
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(255,255,255,0.1); color: #d1d5db; font-size: 0.8em;">Pro</span>
              </td>
              <td style="padding: 0.75rem; color: #9ca3af;">Versions rapides (Flash/Preview) et version complète (Pro)</td>
            </tr>
          </table>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>L'avantage Claude :</strong> 3 niveaux de modèle = un levier majeur
          d'optimisation. Vous choisissez la puissance en fonction de la tâche, pas l'inverse.
        </p>

        <h4>La règle : adapter la puissance à la tâche</h4>
        <p>Le piège, c'est de toujours utiliser le modèle le plus puissant. Pourquoi ?</p>
        <ul>
          <li><strong>Coût :</strong> Opus coûte ~15x plus cher que Haiku en tokens. Pour 100 demandes simples, la différence est énorme.</li>
          <li><strong>Sur-interprétation :</strong> un modèle très puissant peut <em>surtraiter</em> une demande simple. Demandez à un philosophe un rapport succinct : il fera 3 pages avec des nuances là où vous vouliez 5 lignes.</li>
          <li><strong>Vitesse :</strong> Haiku répond en 2-3 secondes, Opus peut prendre 30 secondes à 2 minutes.</li>
        </ul>

        <h4>Guide de choix</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.75rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px;">
            <strong style="color: #86efac; font-size: 0.9em;">Haiku — le rapide</strong>
            <ul style="margin: 0.5rem 0 0; padding-left: 1rem; color: #9ca3af; font-size: 0.8em;">
              <li>Reformulations simples</li>
              <li>Corrections orthographiques</li>
              <li>Tâches répétitives</li>
              <li>Tri / classification</li>
              <li>Résumés courts</li>
            </ul>
          </div>
          <div style="padding: 0.75rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <strong style="color: #93c5fd; font-size: 0.9em;">Sonnet — le polyvalent</strong>
            <ul style="margin: 0.5rem 0 0; padding-left: 1rem; color: #9ca3af; font-size: 0.8em;">
              <li>Création de cours / exercices</li>
              <li>Production de documents</li>
              <li>Analyse de fichiers</li>
              <li>Coding standard</li>
              <li>La plupart des tâches</li>
            </ul>
          </div>
          <div style="padding: 0.75rem; background: rgba(168,85,247,0.08); border: 1px solid rgba(168,85,247,0.2); border-radius: 8px;">
            <strong style="color: #d8b4fe; font-size: 0.9em;">Opus — le stratège</strong>
            <ul style="margin: 0.5rem 0 0; padding-left: 1rem; color: #9ca3af; font-size: 0.8em;">
              <li>Architecture complexe</li>
              <li>Raisonnement multi-étapes</li>
              <li>Adversarial review</li>
              <li>Création de skills</li>
              <li>Pré-plans ambitieux</li>
            </ul>
          </div>
        </div>

        <h4>Le mode ultrathink (Opus)</h4>
        <p>
          Avec Claude Code, vous pouvez activer le mode <strong>ultrathink</strong> sur Opus.
          L'agent prend alors un temps de réflexion étendu avant de répondre — il "pense plus longtemps".
          C'est utile pour les tâches qui nécessitent une planification fine ou un raisonnement complexe.
          À éviter pour les demandes simples : c'est comme demander à un architecte de dessiner
          un plan pour accrocher un tableau.
        </p>
      `,
      exemple: `
        <h3>La même demande, 3 modèles, 3 résultats</h3>
        <p>Observez comment la même demande produit des résultats très différents selon le modèle choisi.</p>

        <div style="padding: 0.75rem 1rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; margin-bottom: 1rem;">
          <strong style="color: #d1d5db;">Demande :</strong>
          <span style="color: #9ca3af;"> "Résume le théorème de Pythagore en 2 phrases pour un élève de 4ème."</span>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.75rem; background: rgba(34,197,94,0.06); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
              <span style="padding: 0.1rem 0.4rem; border-radius: 4px; background: rgba(34,197,94,0.2); color: #86efac; font-size: 0.75em; font-weight: 600;">Haiku</span>
              <span style="font-size: 0.7em; color: #6b7280;">~2 sec</span>
            </div>
            <p style="font-size: 0.85em; color: #d1d5db; margin: 0;">
              "Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés. Si on connaît deux côtés, on peut calculer le troisième."
            </p>
            <p style="font-size: 0.75em; color: #4ade80; margin: 0.5rem 0 0;">✅ Concis, correct, adapté.</p>
          </div>
          <div style="padding: 0.75rem; background: rgba(59,130,246,0.06); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
              <span style="padding: 0.1rem 0.4rem; border-radius: 4px; background: rgba(59,130,246,0.2); color: #93c5fd; font-size: 0.75em; font-weight: 600;">Sonnet</span>
              <span style="font-size: 0.7em; color: #6b7280;">~5 sec</span>
            </div>
            <p style="font-size: 0.85em; color: #d1d5db; margin: 0;">
              "Dans un triangle rectangle, le carré de l'hypoténuse (le plus grand côté, face à l'angle droit) est égal à la somme des carrés des deux autres côtés : a² + b² = c². Ce théorème permet de calculer une longueur manquante quand on connaît les deux autres."
            </p>
            <p style="font-size: 0.75em; color: #60a5fa; margin: 0.5rem 0 0;">✅ Plus détaillé, avec la formule.</p>
          </div>
          <div style="padding: 0.75rem; background: rgba(168,85,247,0.06); border: 1px solid rgba(168,85,247,0.2); border-radius: 8px;">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
              <span style="padding: 0.1rem 0.4rem; border-radius: 4px; background: rgba(168,85,247,0.2); color: #d8b4fe; font-size: 0.75em; font-weight: 600;">Opus</span>
              <span style="font-size: 0.7em; color: #6b7280;">~15 sec</span>
            </div>
            <p style="font-size: 0.85em; color: #d1d5db; margin: 0;">
              "Le théorème de Pythagore établit que dans tout triangle rectangle — et uniquement dans un triangle rectangle — la somme des aires des carrés construits sur les côtés de l'angle droit égale l'aire du carré construit sur l'hypoténuse. Noté a² + b² = c², il constitue un outil fondamental pour calculer des distances, et sa réciproque permet de prouver qu'un triangle est rectangle."
            </p>
            <p style="font-size: 0.75em; color: #c084fc; margin: 0.5rem 0 0;">⚠️ Correct mais trop dense pour un 4ème. Sur-traitement.</p>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Ici, Haiku gagne.</strong> Pour une demande simple et courte,
          le modèle le moins cher produit le meilleur résultat. Opus a sur-interprété
          la demande en ajoutant la réciproque et les aires — hors sujet pour un résumé de 2 phrases.
        </p>

        <h4>Quand Opus devient indispensable</h4>
        <p>
          En revanche, pour une tâche comme <em>"Conçois une séquence complète de 5 séances sur
          les fonctions affines en 3ème, avec progression spiralaire, exercices différenciés,
          évaluation par compétences et intégration du numérique"</em>, Haiku et Sonnet produiront
          quelque chose de superficiel. Opus planifiera, structurera et articulera chaque séance
          avec cohérence.
        </p>
      `,
      pratique: `
        <h3>Testez par vous-même</h3>
        <p>
          Voici un prompt simple à tester avec différents modèles. Si vous avez accès
          à Claude Code, changez le modèle avec <code>/model</code>. Sur Claude Desktop,
          le modèle est sélectionnable dans l'interface.
        </p>

        <div style="position: relative; margin: 1.5rem 0;">
          <pre id="model-test-prompt" style="background: rgba(0,0,0,0.4); border: 1px solid rgba(139,92,246,0.3); border-radius: 8px; padding: 1rem; font-size: 0.85em; line-height: 1.5; color: #d1d5db;"><code>Rédige une définition du PGCD pour un élève de 3ème.
Maximum 3 phrases.
Inclus un exemple numérique.</code></pre>
          <button onclick="navigator.clipboard.writeText(document.getElementById('model-test-prompt').innerText).then(()=>{const b=this;b.textContent='✅ Copié !';b.style.background='rgba(34,197,94,0.3)';setTimeout(()=>{b.textContent='📋 Copier';b.style.background='rgba(139,92,246,0.3)'},2000)})" style="position: absolute; top: 0.5rem; right: 0.5rem; background: rgba(139,92,246,0.3); border: 1px solid rgba(139,92,246,0.4); color: #c4b5fd; padding: 0.4rem 0.75rem; border-radius: 6px; font-size: 0.8rem; cursor: pointer;">📋 Copier</button>
        </div>

        <h4>Expérience guidée</h4>
        <ol>
          <li>Envoyez ce prompt avec <strong>Haiku</strong> — notez le résultat, le temps, la longueur</li>
          <li>Renvoyez exactement le même prompt avec <strong>Sonnet</strong></li>
          <li>Si vous avez accès à Opus, testez aussi — observez la différence de profondeur</li>
        </ol>

        <div class="exercise-card" style="margin-top: 1.5rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
            <span style="font-weight: 600; color: white;">Quel modèle pour quelle tâche ?</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque situation, choisissez le modèle le plus adapté :</p>
            <p><strong>1.</strong> Corriger 3 fautes d'orthographe dans un énoncé</p>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q1" disabled /> A) Haiku</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q1" disabled /> B) Sonnet</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q1" disabled /> C) Opus</label>

            <p style="margin-top: 1rem;"><strong>2.</strong> Créer un cours complet sur les probabilités avec 8 exercices progressifs</p>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q2" disabled /> A) Haiku</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q2" disabled /> B) Sonnet</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q2" disabled /> C) Opus</label>

            <p style="margin-top: 1rem;"><strong>3.</strong> Architecturer un système de 4 agents qui collaborent pour produire une séquence complète</p>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q3" disabled /> A) Haiku</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q3" disabled /> B) Sonnet</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q3" disabled /> C) Opus</label>

            <p style="margin-top: 1rem;"><strong>4.</strong> Reformuler 20 consignes d'exercices pour les rendre plus claires</p>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q4" disabled /> A) Haiku</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q4" disabled /> B) Sonnet</label>
            <label style="display: block; margin: 0.25rem 0;"><input type="radio" name="q4" disabled /> C) Opus</label>
          </div>
          <details class="exercise-solution">
            <summary>Voir les réponses</summary>
            <div class="solution-content">
              <p><strong>1. A) Haiku</strong> — Correction simple, pas besoin de réflexion profonde. Rapide et pas cher.</p>
              <p><strong>2. B) Sonnet</strong> — Production standard de contenu pédagogique. Sonnet est le modèle par défaut pour la majorité des tâches.</p>
              <p><strong>3. C) Opus</strong> — Architecture multi-agents = raisonnement complexe et planification. C'est le terrain d'Opus.</p>
              <p><strong>4. A) Haiku</strong> — Tâche répétitive et simple. 20 reformulations = beaucoup de tokens. Haiku sera 15x moins cher et suffisamment bon.</p>
              <hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;" />
              <p><strong>En pratique, la meilleure architecture combine les trois :</strong></p>
              <ul>
                <li>Un <strong>agent principal Opus</strong> qui planifie, orchestre et contrôle la qualité</li>
                <li>Des <strong>sous-agents Sonnet</strong> dédiés à chaque tâche de production (un pour le cours, un pour les exercices, un pour l'évaluation...)</li>
                <li>Pour les tâches répétitives peu complexes, l'agent principal prompte des <strong>agents Haiku</strong> avec des instructions extrêmement détaillées, ce qui permet un contrôle fin des résultats à moindre coût</li>
              </ul>
              <p>Cette architecture avancée (agent principal + sous-agents de différents niveaux) peut être mise en place de plusieurs manières, explorées dans les capsules du <strong>parcours Avancé</strong>.</p>
            </div>
          </details>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em; margin-top: 1.5rem;">
          <strong>La règle d'or :</strong> commencez toujours par vous demander
          <em>"est-ce que cette tâche a vraiment besoin d'un modèle puissant ?"</em>
          Si la réponse est non, utilisez le modèle le plus léger. Vous économiserez du temps,
          de l'argent, et le résultat sera souvent meilleur car moins sur-interprété.
        </p>
      `,
    },
    duration: '~8 min',
    tags: ['modèle', 'coût', 'optimisation'],
  },

  'pc-skills-agents': {
    id: 'pc-skills-agents',
    title: 'Invoquer les bons outils au bon moment',
    description: 'Déclencher skills et agents par leur nom, cibler des fichiers, contrôler le workflow',
    parcours: 'prompt-craft',
    order: 1,
    sections: {
      info: `
        <h3>Skills et agents : vos raccourcis vers l'expertise</h3>
        <p>
          Un <strong>skill</strong>, c'est une <em>recette toute faite</em> que l'IA connaît par cœur :
          elle sait exactement quoi faire, dans quel ordre, avec quels outils. Par exemple, le skill
          <code>bfcours-latex</code> sait créer un document LaTeX pédagogique complet sans que vous
          ayez à tout expliquer.
        </p>
        <p>
          Un <strong>agent</strong>, c'est un <em>collègue spécialiste</em> que l'IA peut appeler
          à l'aide. L'agent <code>beamer-worker</code> par exemple est un expert en diaporamas Beamer :
          il prend la tâche, la traite de A à Z, et renvoie le résultat.
        </p>

        <h4>Les 3 façons d'invoquer un skill</h4>
        <ol>
          <li>
            <strong>Commande slash</strong> (la plus fiable) : <code>/createTex</code>, <code>/createReveals</code><br>
            <span style="color: #9ca3af;">→ Déclenchement garanti, pas d'ambiguïté.</span>
          </li>
          <li>
            <strong>Mention naturelle</strong> : "utilise le skill bfcours-latex pour..."<br>
            <span style="color: #9ca3af;">→ Fonctionne bien si vous nommez exactement le skill.</span>
          </li>
          <li>
            <strong>Déclenchement implicite</strong> : "crée-moi un cours LaTeX sur..."<br>
            <span style="color: #f87171;">⚠️ Risqué : l'IA peut ne pas reconnaître quel skill utiliser.
            Ça fonctionne mieux si le skill a déjà été invoqué dans la conversation — le modèle
            retient la méthode.</span>
          </li>
        </ol>

        <h4>Cibler des fichiers avec @</h4>
        <p>
          Comme vous diriez "regarde <em>ce</em> document", vous pouvez pointer l'IA vers un fichier
          précis avec <code>@nom-du-fichier</code>. C'est crucial pour <strong>éviter que l'agent
          perde du temps</strong> à explorer tout votre projet.
        </p>
        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Règle d'or : dirigez vos agents.</strong> Sans direction claire, un agent va
          explorer, lire des dizaines de fichiers, hésiter. Avec un ciblage précis, il va droit
          au but.<br><br>
          <strong>Critère de réussite :</strong> vos agents lisent <em>seulement</em> les fichiers
          dont ils ont la responsabilité ET les fichiers de connaissances nécessaires à leur réussite.
        </p>

        <h4>Tableau des skills les plus utiles</h4>
        <details>
          <summary style="cursor: pointer; color: #a78bfa; font-weight: 600;">Voir le tableau</summary>
          <table style="width: 100%; margin-top: 0.75rem; border-collapse: collapse; font-size: 0.9em;">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Commande</th>
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Ce qu'il fait</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/createTex</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Cours, exercices, évaluations en LaTeX</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/createReveals</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Diaporama interactif HTML</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/createBeamer</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Diaporama Beamer (PDF)</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/create-app</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Application éducative Flask</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/image-generator</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Images pédagogiques (Imagen)</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/programmes-officiels</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Extraire les compétences du BO</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/meta-prompt</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Optimiser un prompt</td>
            </tr>
            <tr>
              <td style="padding: 0.5rem;"><code>/ficheTexnique</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Fiche technique d'une ressource</td>
            </tr>
          </table>
        </details>
      `,
      exemple: `
        <h3>La puissance du workflow structuré</h3>
        <p>
          Le vrai pouvoir n'est pas d'invoquer un skill isolé — c'est de <strong>contrôler
          le processus et la temporalité</strong> de l'agent en structurant votre demande
          comme un workflow avec des étapes.
        </p>

        <h4>Scénario simple : une commande slash suffit</h4>
        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;"><code>/createReveals</code> Un diaporama sur le théorème de Pythagore, niveau 4ème, style collège</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #6ee7b7;">✅ Skill <code>reveals-presentation</code> chargé → Agent <code>reveals-creator</code> lancé → fichier .html produit</p>
              <p style="margin: 0.5rem 0 0; color: #9ca3af; font-size: 0.85em;">Une seule ligne suffit parce que le skill connaît déjà le contexte de production.</p>
            </div>
          </div>
        </div>

        <h4>Scénario avancé : workflow multi-étapes</h4>
        <p>
          Ici, on utilise les titres <code>##</code> pour découper le travail en <strong>étapes
          séquentielles</strong>. L'agent les exécute dans l'ordre — vous contrôlez
          <strong>quoi</strong>, <strong>quand</strong> et <strong>avec quel outil</strong>.
        </p>
        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Contexte
Classe de 6ème, 25 élèves, séance de 55 min
Thème : les angles — @mon-cours-angles.tex

## Étape 1 : Vérifier le programme
/programmes-officiels 6ème Géométrie
Identifier les compétences sur les angles

## Étape 2 : Créer le diaporama de cours
/createReveals
- Style collège, 15 slides max
- Inclure 2 exercices interactifs
- Se baser sur @mon-cours-angles.tex

## Étape 3 : Créer la fiche d'exercices
/createTex
- 6 exercices progressifs
- Alignés sur les compétences de l'étape 1
- Correction détaillée en annexe

## Étape 4 : Vérification finale
Vérifie la cohérence entre le diaporama et les exercices</code></pre>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;">
                <span style="color: #a78bfa;">📋 Étape 1</span> — Compétences identifiées : mesurer, nommer, estimer un angle<br>
                <span style="color: #a78bfa;">📋 Étape 2</span> — Agent <code>reveals-creator</code> lancé → 14 slides + 2 exercices<br>
                <span style="color: #a78bfa;">📋 Étape 3</span> — Agent <code>latex-main-worker</code> lancé → fiche 6 exercices<br>
                <span style="color: #a78bfa;">📋 Étape 4</span> — Cohérence vérifiée ✅
              </p>
            </div>
          </div>
        </div>
        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>Ce qui est puissant ici :</strong> vous contrôlez non seulement le <em>processus</em>
          d'action de l'agent, mais aussi sa <em>temporalité</em>. L'étape 3 utilise les résultats
          de l'étape 1. Chaque <code>##</code> est une porte que l'agent franchit dans l'ordre.
        </p>
      `,
      pratique: `
        <h3>Construisez votre propre prompt avec l'arbre de décision</h3>
        <p>
          L'outil ci-dessous vous guide pas à pas : à chaque choix que vous faites, il détermine
          quels skills sont nécessaires et génère le prompt structuré correspondant.
        </p>
        <p style="color: #a78bfa; font-size: 0.9em;">
          Faites vos choix dans chaque étape, puis observez le prompt généré en bas.
          Vous pouvez aussi écrire vos propres valeurs dans les champs libres.
        </p>
      `,
    },
    duration: '~12 min',
    tags: ['skills', 'agents', 'workflow'],
  },

  'pc-idea-challenger': {
    id: 'pc-idea-challenger',
    title: 'Clarifier avant d\'agir',
    description: 'Quand votre demande est trop vague, faire préciser par l\'IA avant de produire',
    parcours: 'prompt-craft',
    order: 3,
    sections: {
      info: `
        <h3>Le réflexe qui change tout : se faire challenger</h3>
        <p>
          Vous avez une idée, mais elle est floue. "Fais-moi un truc sur les fractions",
          "j'aimerais une activité sympa pour les 4ème"... L'IA peut exécuter ça, mais
          le résultat sera <em>aussi flou que votre demande</em>.
        </p>
        <p>
          La solution : avant de produire quoi que ce soit, demander à l'IA de
          <strong>vous poser des questions</strong> pour préciser votre pensée.
          C'est le rôle du skill <code>idea-challenger</code>.
        </p>

        <h4>Comment ça marche</h4>
        <p>Le skill analyse votre demande sur <strong>7 dimensions</strong> :</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.5rem; margin: 1rem 0;">
          <div style="padding: 0.5rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #c4b5fd;">Objectif</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Quel résultat final ?</div>
          </div>
          <div style="padding: 0.5rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #93c5fd;">Public</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Pour qui exactement ?</div>
          </div>
          <div style="padding: 0.5rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #86efac;">Périmètre</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Quelles limites ?</div>
          </div>
          <div style="padding: 0.5rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #fbbf24;">Format</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Quel livrable ?</div>
          </div>
          <div style="padding: 0.5rem; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #f87171;">Contraintes</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Quelles obligations ?</div>
          </div>
          <div style="padding: 0.5rem; background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #22d3ee;">Contexte</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Dans quel cadre ?</div>
          </div>
          <div style="padding: 0.5rem; background: rgba(168,85,247,0.08); border: 1px solid rgba(168,85,247,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 0.8em; font-weight: 600; color: #d8b4fe;">Qualité</div>
            <div style="font-size: 0.7em; color: #9ca3af;">Critères de réussite ?</div>
          </div>
        </div>

        <p>
          Pour chaque dimension floue, il vous pose <strong>maximum 4 questions par round</strong>,
          avec des choix suggérés. Il itère jusqu'à ce que votre demande soit à 4/5 de clarté
          sur chaque axe.
        </p>

        <h4>Quand l'utiliser</h4>
        <ul>
          <li>Votre demande est vague : "fais-moi quelque chose sur les équations"</li>
          <li>Vous avez une idée mais pas de plan : "j'aimerais une séquence originale"</li>
          <li>Avant de lancer une tâche complexe impliquant plusieurs skills</li>
          <li>Quand vous voulez <strong>préciser votre propre pensée</strong> — l'IA vous sert de miroir</li>
        </ul>

        <h4>Le résultat</h4>
        <p>
          À la fin du processus, le skill génère un <strong>fichier .md structuré</strong>
          contenant un prompt optimisé prêt à l'emploi — avec rôle, contexte, instructions,
          contraintes et format de sortie. Vous pouvez l'utiliser directement ou le passer
          à un autre skill.
        </p>

        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>Intégration avec meta-prompt :</strong> le skill <code>meta-prompt</code>
          invoque automatiquement <code>idea-challenger</code> en Phase 1 quand votre demande
          est trop vague. Vous n'avez même pas besoin de l'appeler manuellement si vous utilisez
          déjà <code>/meta-prompt</code>.
        </p>
      `,
      exemple: `
        <h3>Un exemple concret : de "vague" à "précis"</h3>

        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;">"J'aimerais un truc bien sur les probabilités pour mes 3ème"</p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.9em;">
              <p style="margin: 0 0 0.75rem; color: #6ee7b7; font-weight: 600;">Idea Challenger — Round 1</p>
              <p style="margin: 0 0 0.5rem; color: #d1d5db;"><strong>Q1 — Objectif :</strong> Quel type de document ? <span style="color: #9ca3af;">A) Cours complet / B) Activité découverte / C) Exercices / D) Évaluation</span></p>
              <p style="margin: 0 0 0.5rem; color: #d1d5db;"><strong>Q2 — Format :</strong> Quel support ? <span style="color: #9ca3af;">A) LaTeX imprimable / B) Diaporama / C) App interactive / D) Autre</span></p>
              <p style="margin: 0; color: #d1d5db;"><strong>Q3 — Contexte :</strong> C'est pour quand dans votre séquence ? <span style="color: #9ca3af;">A) Introduction / B) Milieu / C) Fin / D) Révision</span></p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;">"B, A, et c'est pour l'intro. Ils n'ont jamais vu les probas."</p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.9em;">
              <p style="margin: 0 0 0.5rem; color: #6ee7b7; font-weight: 600;">Clarté : 4/5 — prêt pour la génération</p>
              <p style="margin: 0; color: #d1d5db;">Prompt structuré généré → <code>prompt-activite-probas-3eme.md</code></p>
            </div>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          En 2 échanges, la demande "un truc bien sur les probas" est devenue
          "activité de découverte en LaTeX pour introduction aux probabilités en 3ème,
          première fois que les élèves abordent la notion". L'IA sait exactement quoi produire.
        </p>
      `,
      pratique: `
        <h3>Testez avec le vrai skill Idea Challenger</h3>
        <p>
          Comme pour le meta-prompt de la capsule 1, vous copiez ici le <strong>vrai skill professionnel</strong>
          utilisé par les agents IA. Il contient le workflow complet de clarification (225 lignes)
          + les conventions Anthropic de prompt engineering (190 lignes).
          Écrivez votre demande, puis copiez le tout.
        </p>

        <h4 style="margin-top: 1.5rem;">Ce que vous devez observer</h4>
        <ul>
          <li>✅ L'IA vous pose des questions <strong>avec des choix</strong>, pas des questions ouvertes</li>
          <li>✅ Chaque round affine la compréhension (la demande se précise à chaque échange)</li>
          <li>✅ Au bout de 2-3 rounds, l'IA vous propose un prompt structuré</li>
          <li>✅ Vous découvrez des aspects auxquels vous n'aviez <strong>pas pensé</strong></li>
        </ul>

        <div class="exercise-card" style="margin-top: 1.5rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
            <span style="font-weight: 600; color: white;">Identifier les dimensions manquantes</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque demande, identifiez les dimensions qui manquent :</p>
            <p><strong>1.</strong> "Fais-moi un cours sur Thalès"</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Dimensions manquantes : ...</p>
            <p><strong>2.</strong> "Crée un exercice de calcul littéral en LaTeX pour mes 4ème, 6 questions progressives avec correction"</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Dimensions manquantes : ...</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir les réponses</summary>
            <div class="solution-content">
              <p><strong>1.</strong> Il manque presque tout : <em>Public</em> (quel niveau ?), <em>Format</em> (LaTeX, diaporama ?), <em>Périmètre</em> (combien de pages ?), <em>Contexte</em> (introduction ou révision ?), <em>Contraintes</em> (programme officiel ?). Seul l'objectif est vaguement défini.</p>
              <p><strong>2.</strong> Beaucoup mieux ! Il manque surtout le <em>Contexte</em> (où dans la séquence ?) et éventuellement les <em>Contraintes</em> (notion de simple ou double distributivité ?). Mais c'est suffisamment clair pour produire quelque chose de correct.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '~8 min',
    tags: ['clarification', 'idea-challenger', 'questions'],
  },

  'pc-preplan': {
    id: 'pc-preplan',
    title: 'Co-construire un pré-plan interactif',
    description: 'Faire produire un plan annotable avant la production finale pour un résultat optimal',
    parcours: 'prompt-craft',
    order: 2,
    sections: {
      info: `
        <h3>Spoiler : vous lisez un pré-plan depuis le début</h3>
        <p>
          Ce parcours que vous suivez en ce moment ? Il a été conçu exactement avec la technique
          que cette capsule enseigne. L'auteur a d'abord demandé à l'IA un <strong>pré-plan
          interactif</strong> avec des cases cochables et des zones de remarques, l'a annoté,
          puis a lancé la production finale. Résultat : ce que vous lisez maintenant.
        </p>

        <h4>Le problème du one-shot</h4>
        <p>
          Quand on envoie un prompt directement, on ne sait pas ce qu'on a oublié. L'IA produit
          quelque chose, mais c'est souvent <em>à côté</em> de ce qu'on voulait vraiment.
          On corrige, on relance, on re-corrige... C'est l'approche "vibe coding" : on tâtonne
          en espérant que ça converge.
        </p>
        <p>
          L'alternative, c'est le <strong>"prompt engineering"</strong> : on établi un plan avec une architecture élaborée avant toute génération afin de s'assurer que le produit correspond à notre attente.
        </p>

        <h4>Le pré-plan : votre brouillon avant le propre</h4>
        <p>Un pré-plan, c'est un document intermédiaire que l'IA produit pour :</p>
        <ul>
          <li>Vous montrer <strong>ce qu'elle a compris</strong> de votre demande</li>
          <li>Proposer des <strong>options</strong> (cases à cocher, choix multiples)</li>
          <li>Laisser des <strong>espaces pour vos remarques</strong></li>
          <li>Vous permettre de <strong>valider avant la production</strong></li>
        </ul>
        <p>C'est à cette étape qu'on se pose les vraies questions d'architecture de la ressource
          à produire. C'est aussi là que <strong>vous précisez votre pensée</strong> — souvent,
          on ne sait pas exactement ce qu'on veut tant qu'on n'a pas vu les options.</p>

        <h4>La boucle Plan → Review → Exécute</h4>
        <div style="display: flex; gap: 0.5rem; align-items: center; justify-content: center; margin: 1.5rem 0; flex-wrap: wrap;">
          <div style="padding: 0.75rem 1.25rem; background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.3); border-radius: 8px; text-align: center;">
            <div style="font-size: 1.5rem;">📝</div>
            <div style="font-size: 0.85rem; color: #c4b5fd; font-weight: 600;">1. Demander</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">"Fais-moi un pré-plan"</div>
          </div>
          <div style="color: #6b7280; font-size: 1.2rem;">→</div>
          <div style="padding: 0.75rem 1.25rem; background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); border-radius: 8px; text-align: center;">
            <div style="font-size: 1.5rem;">✏️</div>
            <div style="font-size: 0.85rem; color: #fbbf24; font-weight: 600;">2. Annoter</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">Cocher, décocher, commenter</div>
          </div>
          <div style="color: #6b7280; font-size: 1.2rem;">→</div>
          <div style="padding: 0.75rem 1.25rem; background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); border-radius: 8px; text-align: center;">
            <div style="font-size: 1.5rem;">🚀</div>
            <div style="font-size: 0.85rem; color: #4ade80; font-weight: 600;">3. Exécuter</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">"Exécute selon ce plan"</div>
          </div>
        </div>
        <p>
          Cette boucle est <strong>itérable</strong> : si le pré-plan ne vous convient pas encore,
          renvoyez vos annotations et demandez une version améliorée. Répétez jusqu'à satisfaction.
        </p>

        <h4>Les 3 formats de pré-plan</h4>
        <ol>
          <li><strong>HTML interactif</strong> — cases cochables, zones de texte, téléchargeable (le plus visuel)</li>
          <li><strong>Markdown structuré</strong> — directement dans le chat, plus rapide</li>
          <li><strong>Plan mode</strong> — mode natif de Claude Code, intégré au terminal</li>
        </ol>

        <h4>Pourquoi c'est rentable</h4>
        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          <strong>Économie de tokens :</strong> un pré-plan consomme ~500 tokens. Une production
          ratée puis corrigée en consomme ~5000. Investir dans un plan, c'est diviser par 10
          le coût des ajustements. Et le résultat est meilleur.
        </p>

        <h4>Quand utiliser un pré-plan ?</h4>
        <p>
          <strong>Oui</strong> : documents longs, séquences, évaluations, présentations, code, tout ce qui est difficile à corriger après coup.<br>
          <strong>Non</strong> : questions courtes, corrections mineures, reformulations simples.
        </p>
      `,
      exemple: `
        <h3>Anatomie d'un pré-plan</h3>
        <p>Voici le schéma de ce qui se passe quand vous demandez un pré-plan :</p>

        <div style="margin: 1.5rem 0; padding: 1.25rem; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;">
          <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
              <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(139,92,246,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #c4b5fd; flex-shrink: 0;">1</div>
              <div>
                <strong style="color: #c4b5fd;">Votre demande</strong>
                <p style="color: #9ca3af; font-size: 0.9em; margin: 0.25rem 0 0;">"Prépare un pré-plan pour une séquence sur les probabilités en 3ème"</p>
              </div>
            </div>
            <div style="border-left: 2px dashed rgba(255,255,255,0.1); margin-left: 14px; padding-left: 1.5rem;">
              <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(245,158,11,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #fbbf24; flex-shrink: 0;">2</div>
                <div>
                  <strong style="color: #fbbf24;">L'IA analyse et propose</strong>
                  <div style="color: #d1d5db; font-size: 0.85em; margin-top: 0.5rem; padding: 0.75rem; background: rgba(255,255,255,0.03); border-radius: 6px;">
                    ☐ Objectifs : vocabulaire des probabilités<br>
                    ☑ Objectifs : calcul de probabilités simples<br>
                    ☑ Objectifs : expériences aléatoires<br>
                    ☐ Activité d'introduction : lancer de dés<br>
                    ☑ Activité d'introduction : jeu de cartes<br>
                    <em style="color: #9ca3af;">Remarques : _______________</em>
                  </div>
                </div>
              </div>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
              <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(34,197,94,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #4ade80; flex-shrink: 0;">3</div>
              <div>
                <strong style="color: #4ade80;">Vous annotez et renvoyez</strong>
                <p style="color: #9ca3af; font-size: 0.9em; margin: 0.25rem 0 0;">"OK pour les probas simples mais ajoute les arbres de probabilité. L'intro avec le jeu de cartes c'est bien."</p>
              </div>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
              <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(59,130,246,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #60a5fa; flex-shrink: 0;">4</div>
              <div>
                <strong style="color: #60a5fa;">Production ciblée</strong>
                <p style="color: #9ca3af; font-size: 0.9em; margin: 0.25rem 0 0;">L'IA produit exactement ce que vous avez validé. Pas de surprise.</p>
              </div>
            </div>
          </div>
        </div>

        <h4>Vibe coder vs Prompt engineer</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
          <div style="padding: 1rem; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 8px;">
            <strong style="color: #f87171;">Vibe prompting</strong>
            <ul style="margin: 0.5rem 0 0; padding-left: 1.25rem; color: #d1d5db; font-size: 0.85em;">
              <li>Envoie, regarde, corrige</li>
              <li>5-10 allers-retours</li>
              <li>~8000 tokens consommés</li>
              <li>Résultat "acceptable"</li>
            </ul>
          </div>
          <div style="padding: 1rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px;">
            <strong style="color: #4ade80;">Prompt engineering</strong>
            <ul style="margin: 0.5rem 0 0; padding-left: 1.25rem; color: #d1d5db; font-size: 0.85em;">
              <li>Planifie, valide, exécute</li>
              <li>1-2 allers-retours</li>
              <li>~2000 tokens consommés</li>
              <li>Résultat "exactement ça"</li>
            </ul>
          </div>
        </div>
      `,
      pratique: `
        <h3>Manipulez un mini pré-plan interactif</h3>
        <p>
          L'outil ci-dessous simule un vrai pré-plan : cochez vos choix, ajoutez vos remarques,
          puis générez le prompt optimisé. C'est exactement ce que fait l'IA quand vous lui
          demandez un pré-plan — sauf qu'ici, c'est vous qui expérimentez.
        </p>

        <div style="position: relative; margin: 1.5rem 0;">
          <div style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.9em; margin-bottom: 1rem;">
            <strong>La phrase qui change tout :</strong><br>
            <em>"Avant de produire quoi que ce soit, propose-moi un pré-plan détaillé avec des options que je puisse valider."</em>
          </div>
          <button onclick="navigator.clipboard.writeText('Avant de produire quoi que ce soit, propose-moi un pré-plan détaillé avec des options que je puisse valider.').then(()=>{const b=this;b.textContent='✅ Copié !';b.style.background='rgba(34,197,94,0.3)';setTimeout(()=>{b.textContent='📋 Copier cette phrase';b.style.background='rgba(139,92,246,0.3)'},2000)})" style="background: rgba(139,92,246,0.3); border: 1px solid rgba(139,92,246,0.4); color: #c4b5fd; padding: 0.4rem 0.75rem; border-radius: 6px; font-size: 0.8rem; cursor: pointer; margin-bottom: 1rem;">📋 Copier cette phrase</button>
        </div>
      `,
    },
    duration: '~10 min',
    tags: ['pré-plan', 'interactif', 'workflow'],
  },

  'pc-adversarial': {
    id: 'pc-adversarial',
    title: 'La revue par les pairs : adversarial review',
    description: 'Faire critiquer un plan par plusieurs agents aux points de vue différents',
    parcours: 'prompt-craft',
    order: 3,
    sections: {
      info: `
        <h3>Pourquoi un seul point de vue ne suffit pas</h3>
        <p>
          Quand vous demandez un pré-plan à l'IA, elle produit <em>sa</em> version.
          C'est déjà mieux qu'un one-shot, mais cette version a un biais : elle reflète
          un seul angle d'analyse. Pour obtenir un plan vraiment solide, il faut le faire
          <strong>critiquer par plusieurs "pairs"</strong> aux perspectives différentes.
        </p>

        <h4>Le principe de l'adversarial review</h4>
        <p>L'agent principal :</p>
        <ol>
          <li>Produit un <strong>pré-plan v1</strong></li>
          <li>Lance <strong>plusieurs sous-agents</strong>, chacun avec un rôle de critique différent</li>
          <li>Chaque critique produit un <strong>rapport</strong> pointant les faiblesses</li>
          <li>L'agent principal <strong>arbitre</strong> et produit un <strong>pré-plan v2 amélioré</strong></li>
          <li>Vous ne lisez que la version finale — la meilleure</li>
        </ol>

        <h4>Les rôles de critiques</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.75rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <strong style="color: #60a5fa;">🎓 L'enseignant</strong>
            <p style="font-size: 0.85em; color: #9ca3af; margin: 0.25rem 0 0;">Vérifie en premier lieu que le <strong>contenu mathématique est correct</strong>. Puis la <strong>conformité avec ses habitudes</strong> : la progression est-elle logique ? La présentation respecte-t-elle le style de ses documents habituels ? Les exercices sont-ils au bon niveau ? Il cherche de la <em>cohérence</em> avec ce qu'il fait déjà.</p>
          </div>
          <div style="padding: 0.75rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px;">
            <strong style="color: #4ade80;">📚 L'élève</strong>
            <p style="font-size: 0.85em; color: #9ca3af; margin: 0.25rem 0 0;">Signale ce qu'il <strong>ne comprend pas</strong>, demande des reformulations, identifie ce qui est trop long ou trop rapide. Peut aussi exprimer <em>ce dont il aurait besoin pour mieux réussir</em> — ce qui peut donner lieu à la création automatique d'annexes ou de supports supplémentaires dans le pré-plan.</p>
          </div>
          <div style="padding: 0.75rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 8px;">
            <strong style="color: #a78bfa;">💻 Le développeur</strong>
            <p style="font-size: 0.85em; color: #9ca3af; margin: 0.25rem 0 0;">Pousse au <strong>réalisme technique</strong> et à l'ambition. Vérifie que les skills demandés existent, mais aussi propose des améliorations : "pourquoi se contenter de ça alors qu'on pourrait faire mieux à moindre coût ?" C'est un <em>amplificateur de possibilités</em> — ce qui est faisable techniquement, personnalisation, interactivité...</p>
          </div>
          <div style="padding: 0.75rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 8px;">
            <strong style="color: #fbbf24;">🔍 L'inspecteur</strong>
            <p style="font-size: 0.85em; color: #9ca3af; margin: 0.25rem 0 0;">Se concentre sur <strong>ce que font les élèves mathématiquement</strong> : quelle activité mathématique est réellement engagée ? Les compétences du programme sont-elles mobilisées ? Vérifie aussi les <strong>changements de registre</strong> (passer du tableau au graphique, de l'algébrique au géométrique...), la présence d'<strong>illustrations</strong>, et la <em>dimension didactique</em> de la production. À terme, un agent inspecteur dédié sera co-construit avec de vrais inspecteurs pour affiner ces critères.</p>
          </div>
        </div>

        <h4>Le résultat</h4>
        <p>
          Chaque critique identifie des angles morts que les autres ne voient pas. L'agent
          principal synthétise tout et produit un plan <strong>plus robuste, plus complet,
          mieux calibré</strong>. Vous économisez du temps car vous ne découvrez pas les
          problèmes après production.
        </p>
        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          <strong>Coût :</strong> ~1500 tokens de plus qu'un pré-plan simple. Mais la qualité
          du résultat final est incomparablement meilleure, et les corrections post-production
          sont quasi nulles.
        </p>

        <h4>Quand utiliser l'adversarial review ?</h4>
        <p>Ce n'est pas réservé aux cas "classiques". Voici des situations concrètes :</p>
        <ul>
          <li><strong>La tâche est techniquement difficile</strong> — vous savez que le résultat sera complexe à produire (séquence multi-séances, évaluation avec barème, application interactive...)</li>
          <li><strong>Vous n'avez pas envie de passer du temps en allers-retours</strong> — la review fait le travail de correction en amont, en une seule passe, plutôt que 5 échanges de corrections après coup</li>
          <li><strong>Vous n'avez pas encore une idée précise</strong> — le pré-plan avec adversarial review vous <em>donne des idées</em>. Chaque critique apporte un angle auquel vous n'aviez pas pensé. C'est un outil d'exploration autant que de production</li>
          <li><strong>Vous voulez du "clé en main"</strong> — un seul message, un seul résultat final déjà optimisé. Vous lisez, vous validez, c'est fait</li>
        </ul>
      `,
      exemple: `
        <h3>Workflow concret : adversarial review en action</h3>

        <div style="margin: 1.5rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Tâche
Crée un pré-plan pour une évaluation sur
les fonctions affines en 3ème

# Méthode
Fais une adversarial review avec 4 points de vue :
- enseignant de maths
- élève de 3ème
- développeur (faisabilité technique)
- inspecteur (conformité programme)

Présente-moi uniquement la version finale
améliorée après arbitrage.</code></pre>
            </div>
          </div>

          <div style="padding: 0.75rem 1rem; background: rgba(255,255,255,0.02); border-top: 1px solid rgba(255,255,255,0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-style: italic;">🤖 L'agent principal lance 4 sous-agents en parallèle...</div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0; border-top: 1px solid rgba(255,255,255,0.05);">
            <div style="padding: 0.75rem; border-right: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05);">
              <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="width: 24px; height: 24px; border-radius: 50%; background: rgba(59,130,246,0.3); display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">🎓</span>
                <strong style="color: #60a5fa; font-size: 0.85em;">Enseignant</strong>
              </div>
              <p style="font-size: 0.8em; color: #9ca3af; margin: 0;">"Il manque un exercice d'application directe avant le problème ouvert. La progression est trop rapide."</p>
            </div>
            <div style="padding: 0.75rem; border-bottom: 1px solid rgba(255,255,255,0.05);">
              <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="width: 24px; height: 24px; border-radius: 50%; background: rgba(34,197,94,0.3); display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">📚</span>
                <strong style="color: #4ade80; font-size: 0.85em;">Élève</strong>
              </div>
              <p style="font-size: 0.8em; color: #9ca3af; margin: 0;">"L'exercice 3 utilise du vocabulaire que je n'ai pas vu. C'est quoi un 'coefficient directeur' ?"</p>
            </div>
            <div style="padding: 0.75rem; border-right: 1px solid rgba(255,255,255,0.05);">
              <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="width: 24px; height: 24px; border-radius: 50%; background: rgba(139,92,246,0.3); display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">💻</span>
                <strong style="color: #a78bfa; font-size: 0.85em;">Développeur</strong>
              </div>
              <p style="font-size: 0.8em; color: #9ca3af; margin: 0;">"Le skill bfcours-latex peut gérer ce format. Ajouter un graphique TikZ pour la question 4."</p>
            </div>
            <div style="padding: 0.75rem;">
              <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <span style="width: 24px; height: 24px; border-radius: 50%; background: rgba(245,158,11,0.3); display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">🔍</span>
                <strong style="color: #fbbf24; font-size: 0.85em;">Inspecteur</strong>
              </div>
              <p style="font-size: 0.8em; color: #9ca3af; margin: 0;">"La compétence 'modéliser par une fonction affine' du BO n'est pas évaluée. Ajouter un exercice de modélisation."</p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03); border-top: 1px solid rgba(255,255,255,0.05);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1;">
              <p style="margin: 0 0 0.5rem; color: #4ade80; font-weight: 600;">Pré-plan v2 (après arbitrage) :</p>
              <p style="margin: 0; color: #d1d5db; font-size: 0.85em;">
                ✅ Exercice d'application directe ajouté (critique enseignant)<br>
                ✅ Vocabulaire simplifié, "coefficient directeur" remplacé par "nombre devant x" (critique élève)<br>
                ✅ Graphique TikZ prévu pour l'exercice 4 (critique développeur)<br>
                ✅ Exercice de modélisation ajouté en fin d'évaluation (critique inspecteur)
              </p>
            </div>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>4 critiques, 4 améliorations concrètes.</strong> Sans cette revue, vous auriez
          découvert ces problèmes <em>après</em> avoir produit l'évaluation complète —
          et il aurait fallu tout recommencer.
        </p>
      `,
      pratique: `
        <h3>À vous de jouer</h3>

        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
            <span style="font-weight: 600; color: white;">Choisir les bons reviewers</span>
          </div>
          <div class="exercise-body">
            <p>Vous voulez créer une <strong>séquence de 4 séances sur les probabilités en 3ème</strong>,
            avec cours, exercices et évaluation finale.</p>
            <p>Parmi ces rôles de reviewers, lesquels sont les plus pertinents pour cette tâche ?</p>
            <label style="display: block; margin: 0.5rem 0;"><input type="checkbox" disabled /> A) Un parent d'élève</label>
            <label style="display: block; margin: 0.5rem 0;"><input type="checkbox" disabled /> B) Un enseignant de mathématiques</label>
            <label style="display: block; margin: 0.5rem 0;"><input type="checkbox" disabled /> C) Un graphiste</label>
            <label style="display: block; margin: 0.5rem 0;"><input type="checkbox" disabled /> D) Un élève de 3ème</label>
            <label style="display: block; margin: 0.5rem 0;"><input type="checkbox" disabled /> E) Un inspecteur pédagogique</label>
            <label style="display: block; margin: 0.5rem 0;"><input type="checkbox" disabled /> F) Un historien des sciences</label>
          </div>
          <details class="exercise-solution">
            <summary>Voir la réponse</summary>
            <div class="solution-content">
              <p><strong>B, D et E</strong> sont les plus pertinents. <strong>F</strong> est aussi pertinent, mais plus secondaire.</p>
              <p><strong>B (enseignant)</strong> : progression pédagogique, niveau de difficulté, pertinence des exercices.</p>
              <p><strong>D (élève)</strong> : compréhension, vocabulaire accessible, durée réaliste.</p>
              <p><strong>E (inspecteur)</strong> : conformité avec le programme officiel, compétences du socle, changements de registre.</p>
              <p><strong>F (historien des sciences)</strong> : pertinent car l'histoire des mathématiques fait partie du programme officiel. Il pourrait enrichir la séquence avec un éclairage historique sur les probabilités (Pascal, Fermat...). C'est secondaire mais pas à écarter.</p>
              <p>A est trop éloigné du contexte. C pourrait être utile si le format visuel compte (diaporama), mais pas en priorité.</p>
            </div>
          </details>
        </div>

        <div class="exercise-card" style="margin-top: 1rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
            <span style="font-weight: 600; color: white;">Rédiger une demande d'adversarial review</span>
          </div>
          <div class="exercise-body">
            <p>Vous avez un projet : créer une <strong>activité d'introduction aux équations en 4ème</strong>
            avec manipulation de balances.</p>
            <p>Rédigez le message que vous enverriez à l'IA pour obtenir un pré-plan avec adversarial review.
            Pensez à :</p>
            <ul>
              <li>Décrire la tâche</li>
              <li>Choisir les rôles de reviewers pertinents</li>
              <li>Préciser ce que vous voulez recevoir (version finale uniquement ? tous les rapports ?)</li>
            </ul>
          </div>
          <details class="exercise-solution">
            <summary>Voir un exemple de réponse</summary>
            <div class="solution-content">
              <pre style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; font-size: 0.85em; color: #d1d5db;"><code># Tâche
Crée un pré-plan pour une activité d'introduction
aux équations en 4ème, basée sur la métaphore
de la balance.

# Adversarial review
Fais critiquer le plan par :
- un enseignant de maths (progression, clarté)
- un élève de 4ème (compréhension, engagement)
- un didacticien (pertinence de la métaphore)

# Livrable
Montre-moi le pré-plan final après arbitrage,
avec un résumé des modifications apportées
suite aux critiques.</code></pre>
            </div>
          </details>
        </div>

        <div style="margin-top: 1.5rem; padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.9em;">
          <strong>Les 3 réflexes du bon prompt :</strong>
          <ol style="margin: 0.5rem 0 0; padding-left: 1.25rem;">
            <li><strong>Structurer</strong> avec des titres # et des listes</li>
            <li><strong>Nommer</strong> les skills et cibler les fichiers avec @</li>
            <li><strong>Planifier</strong> avec un pré-plan avant de produire</li>
          </ol>
        </div>
      `,
    },
    duration: '~8 min',
    tags: ['adversarial', 'agents', 'review'],
  },

  'pc-synthesis': {
    id: 'pc-synthesis',
    title: 'Tout combiner : le prompt complet',
    description: 'Mobiliser conjointement toutes les briques pour des demandes de plus en plus ambitieuses',
    parcours: 'prompt-craft',
    order: 6,
    sections: {
      info: `
        <h3>Chaque brique seule est utile — ensemble, elles sont puissantes</h3>
        <p>
          Au fil de ce parcours, vous avez acquis <strong>6 briques</strong> :
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.5rem; margin: 1rem 0;">
          <div style="padding: 0.6rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 1.1rem;">🧱</div>
            <div style="font-size: 0.75em; font-weight: 600; color: #fbbf24;">Structurer</div>
            <div style="font-size: 0.65em; color: #9ca3af;">Markdown, titres, format</div>
          </div>
          <div style="padding: 0.6rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 1.1rem;">⚡</div>
            <div style="font-size: 0.75em; font-weight: 600; color: #86efac;">Modèle</div>
            <div style="font-size: 0.65em; color: #9ca3af;">Haiku, Sonnet, Opus</div>
          </div>
          <div style="padding: 0.6rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 1.1rem;">🎯</div>
            <div style="font-size: 0.75em; font-weight: 600; color: #c4b5fd;">Skills</div>
            <div style="font-size: 0.65em; color: #9ca3af;">Commandes, agents, @</div>
          </div>
          <div style="padding: 0.6rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 1.1rem;">💡</div>
            <div style="font-size: 0.75em; font-weight: 600; color: #fbbf24;">Clarifier</div>
            <div style="font-size: 0.65em; color: #9ca3af;">Idea-challenger</div>
          </div>
          <div style="padding: 0.6rem; background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 1.1rem;">🤝</div>
            <div style="font-size: 0.75em; font-weight: 600; color: #22d3ee;">Pré-plan</div>
            <div style="font-size: 0.65em; color: #9ca3af;">Plan → Review → Exécute</div>
          </div>
          <div style="padding: 0.6rem; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 6px; text-align: center;">
            <div style="font-size: 1.1rem;">🔍</div>
            <div style="font-size: 0.75em; font-weight: 600; color: #f87171;">Review</div>
            <div style="font-size: 0.65em; color: #9ca3af;">Adversarial multi-agents</div>
          </div>
        </div>

        <p>
          Chaque brique peut être utilisée <strong>indépendamment</strong>. Elles peuvent aussi
          se combiner — conjointement ou successivement. La question n'est pas "comment
          tout utiliser en même temps", mais <strong>quand mobiliser quelle brique</strong>
          pour trouver le bon compromis entre complexité d'exécution et qualité de production.
        </p>

        <h4>Le raisonnement coût / bénéfice</h4>
        <p>
          Chaque brique consomme des <strong>tokens</strong> (= du temps et de l'argent).
          L'enjeu est d'investir les tokens là où ils font une vraie différence :
        </p>
        <div style="margin: 1rem 0; overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.85em;">
            <tr style="border-bottom: 2px solid rgba(255,255,255,0.15);">
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Brique</th>
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Coût</th>
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Utile quand...</th>
              <th style="text-align: left; padding: 0.5rem; color: #a78bfa;">Inutile quand...</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;">🧱 Structure</td>
              <td style="padding: 0.5rem; color: #86efac;">Gratuit</td>
              <td style="padding: 0.5rem; color: #d1d5db;">Toujours</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Jamais inutile</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;">⚡ Choix modèle</td>
              <td style="padding: 0.5rem; color: #86efac;">Gratuit</td>
              <td style="padding: 0.5rem; color: #d1d5db;">Toujours</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Jamais inutile</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;">🎯 Skills</td>
              <td style="padding: 0.5rem; color: #fbbf24;">Faible</td>
              <td style="padding: 0.5rem; color: #d1d5db;">Tâche spécialisée (LaTeX, slides...)</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Question simple, reformulation</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;">💡 Clarifier</td>
              <td style="padding: 0.5rem; color: #fbbf24;">~500 tokens</td>
              <td style="padding: 0.5rem; color: #d1d5db;">Idée vague, projet mal défini</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Demande déjà précise</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;">🤝 Pré-plan</td>
              <td style="padding: 0.5rem; color: #f59e0b;">~500-1000 tokens</td>
              <td style="padding: 0.5rem; color: #d1d5db;">Production longue ou difficile à corriger</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Tâche courte ou facilement retouchable</td>
            </tr>
            <tr>
              <td style="padding: 0.5rem;">🔍 Review</td>
              <td style="padding: 0.5rem; color: #f87171;">~1500 tokens</td>
              <td style="padding: 0.5rem; color: #d1d5db;">Document critique (évaluation, séquence officielle)</td>
              <td style="padding: 0.5rem; color: #9ca3af;">Brouillon, exercice rapide, usage personnel</td>
            </tr>
          </table>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Chaque token compte.</strong> Un adversarial review sur une correction de 3 fautes d'orthographe,
          c'est du gaspillage. Un prompt structuré sans pré-plan pour une séquence de 5 séances,
          c'est un pari risqué. Le bon réflexe : <strong>évaluer la complexité de la tâche d'abord</strong>,
          puis mobiliser les briques qui valent le coup.
        </p>
      `,
      exemple: `
        <h3>3 demandes, 3 niveaux d'investissement</h3>
        <p>Le même enseignant, 3 tâches différentes. Observez comment il dose les briques en fonction du rapport coût/bénéfice.</p>

        <h4>Demande 1 — Investissement minimal</h4>
        <div style="margin: 0.75rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db; font-size: 0.9em;">Corrige les fautes dans @exercice-fractions.tex</p>
            </div>
          </div>
          <div style="padding: 0.5rem 1rem; background: rgba(255,255,255,0.02); font-size: 0.8em;">
            <span style="color: #86efac;">Briques :</span> <span style="color: #9ca3af;">🧱 Structure (implicite) · ⚡ Haiku</span><br>
            <span style="color: #86efac;">Coût :</span> <span style="color: #9ca3af;">~100 tokens · Pas de pré-plan, pas de review, pas de skill</span><br>
            <span style="color: #86efac;">Pourquoi :</span> <span style="color: #9ca3af;">Tâche simple, facilement vérifiable, correction rapide</span>
          </div>
        </div>

        <h4>Demande 2 — Investissement ciblé</h4>
        <div style="margin: 0.75rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Contexte
Classe de 4ème, chapitre Thalès, fin de séquence

# Tâche
/createTex
- Fiche d'exercices, 8 exercices progressifs
- Correction en annexe
- @mon-cours-thales.tex comme référence</code></pre>
            </div>
          </div>
          <div style="padding: 0.5rem 1rem; background: rgba(255,255,255,0.02); font-size: 0.8em;">
            <span style="color: #fbbf24;">Briques :</span> <span style="color: #9ca3af;">🧱 Structure · 🎯 Skill (createTex) · ⚡ Sonnet</span><br>
            <span style="color: #fbbf24;">Coût :</span> <span style="color: #9ca3af;">~2000 tokens · Pas de pré-plan (le cadre est clair), pas de review (exercices classiques)</span><br>
            <span style="color: #fbbf24;">Pourquoi :</span> <span style="color: #9ca3af;">Production standard, contexte précis, skill dédié → pas besoin de plus</span>
          </div>
        </div>

        <h4>Demande 3 — Investissement complet</h4>
        <div style="margin: 0.75rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.75rem 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code># Contexte
Classe de 3ème, 28 élèves
Séquence fonctions affines — @mon-cours-fonctions.tex

## Étape 1 : Programme
/programmes-officiels 3ème Fonctions

## Étape 2 : Pré-plan
Propose un pré-plan pour 5 séances avec
options cochables. Je valide avant production.

## Étape 3 : Production (après validation)
- /createTex cours (agent Sonnet)
- /createTex exercices (agent Sonnet)
- /createReveals diaporama (agent Sonnet)
- /createTex évaluation (agent Sonnet)

## Étape 4 : Review
Adversarial review : enseignant + élève + inspecteur
Appliquer les corrections.</code></pre>
            </div>
          </div>
          <div style="padding: 0.5rem 1rem; background: rgba(255,255,255,0.02); font-size: 0.8em;">
            <span style="color: #f87171;">Briques :</span> <span style="color: #9ca3af;">🧱 Structure · ⚡ Opus + Sonnet · 🎯 Multi-skills · 🤝 Pré-plan · 🔍 Review</span><br>
            <span style="color: #f87171;">Coût :</span> <span style="color: #9ca3af;">~8000 tokens · Pré-plan + review justifiés par la complexité</span><br>
            <span style="color: #f87171;">Pourquoi :</span> <span style="color: #9ca3af;">Séquence entière, 4 documents liés, inspection possible → chaque brique se justifie</span>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>La demande 2 n'a pas besoin de review</strong> — les exercices sur Thalès sont vérifiables rapidement à l'œil.
          <strong>La demande 3 en a besoin</strong> — une séquence de 5 séances avec 4 documents, c'est difficile à vérifier manuellement
          et coûteux à refaire. L'investissement en tokens de la review est rentabilisé.
        </p>
      `,
      pratique: `
        <h3>Évaluez le bon investissement</h3>

        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1</span>
            <span style="font-weight: 600; color: white;">Quelles briques pour quelles tâches ?</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque tâche, choisissez les briques à mobiliser <strong>et justifiez ce que vous n'utilisez PAS</strong> :</p>

            <p><strong>A)</strong> Reformuler 15 consignes d'exercices pour les rendre plus claires</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Briques : ... · Pourquoi pas de review : ...</p>

            <p><strong>B)</strong> Créer un DM noté sur les probabilités en 3ème, avec barème par compétences</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Briques : ... · Justification : ...</p>

            <p><strong>C)</strong> Préparer l'intégralité de la semaine des maths (5 activités ludiques + affichage)</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Briques : ... · Justification : ...</p>

            <p><strong>D)</strong> Créer un QCM de 5 questions sur les identités remarquables</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Briques : ... · Justification : ...</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir les réponses</summary>
            <div class="solution-content">
              <p><strong>A)</strong> 🧱 Structure + ⚡ <strong>Haiku</strong> (tâche répétitive simple). Pas de skill, pas de pré-plan, pas de review : chaque reformulation est vérifiable en 5 secondes. Économie : ~15x moins cher qu'avec Opus.</p>
              <p><strong>B)</strong> 🧱 Structure + 🎯 Skill (/createTex) + ⚡ Sonnet + 🤝 <strong>Pré-plan</strong> (barème = choix complexes à valider) + 🔍 <strong>Review inspecteur</strong> (document officiel noté, conformité programme critique). Pas de clarification : la demande est précise.</p>
              <p><strong>C)</strong> 💡 <strong>Clarifier d'abord</strong> (qu'est-ce qu'on entend par "ludique" ? quel budget temps ?) → 🤝 Pré-plan → 🧱 Structure + 🎯 Multi-skills + ⚡ Opus orchestre. <strong>Pas forcément de review</strong> : ce sont des activités ludiques, pas un document officiel — la vérification manuelle rapide suffit.</p>
              <p><strong>D)</strong> 🧱 Structure + ⚡ <strong>Sonnet</strong> (ou Haiku). Pas de pré-plan (5 questions = rapide à refaire si ça ne convient pas), pas de review (vérifiable en 30 secondes). C'est la demande la plus simple du lot.</p>
            </div>
          </details>
        </div>

        <div class="exercise-card" style="margin-top: 1rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2</span>
            <span style="font-weight: 600; color: white;">Votre prochain projet — dosez les briques</span>
          </div>
          <div class="exercise-body">
            <p>
              Pensez à un projet pédagogique réel que vous aimeriez réaliser.
              Avant de rédiger le prompt, posez-vous ces 3 questions :
            </p>
            <ol>
              <li><strong>Complexité :</strong> combien de documents / formats différents ?</li>
              <li><strong>Enjeu :</strong> est-ce un brouillon ou un document officiel ?</li>
              <li><strong>Vérifiabilité :</strong> puis-je vérifier le résultat en 1 minute ou faut-il 20 minutes ?</li>
            </ol>
            <p style="color: #9ca3af; font-size: 0.85em;">
              Si c'est simple + brouillon + vérifiable rapidement → message direct, Haiku.<br>
              Si c'est complexe + officiel + long à vérifier → toutes les briques se justifient.
            </p>
          </div>
        </div>

        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 8px;">
          <h4 style="color: #c4b5fd; margin-bottom: 0.75rem;">Récapitulatif du parcours</h4>
          <p style="font-size: 0.9em; color: #d1d5db; margin-bottom: 0.75rem;">
            6 briques à votre disposition. Le réflexe à retenir :
          </p>
          <ol style="font-size: 0.85em; color: #9ca3af; padding-left: 1.25rem;">
            <li><strong style="color: #fbbf24;">Structurer</strong> — toujours (gratuit, jamais inutile)</li>
            <li><strong style="color: #86efac;">Choisir le modèle</strong> — toujours (adapter la puissance au besoin)</li>
            <li><strong style="color: #c4b5fd;">Invoquer les skills</strong> — quand la tâche est spécialisée</li>
            <li><strong style="color: #fbbf24;">Clarifier</strong> — quand l'idée est floue (économise des corrections)</li>
            <li><strong style="color: #22d3ee;">Pré-planifier</strong> — quand le résultat est difficile à corriger après coup</li>
            <li><strong style="color: #f87171;">Faire critiquer</strong> — quand le document est critique et long à vérifier</li>
          </ol>
          <p style="font-size: 0.85em; color: #9ca3af; margin-top: 0.75rem;">
            La suite ? Le <strong>parcours Avancé</strong> vous apprendra à créer vos propres
            skills, orchestrer des sous-agents en parallèle, et mettre en place des équipes
            d'agents persistantes.
          </p>
        </div>
      `,
    },
    duration: '~8 min',
    tags: ['synthèse', 'combinaison', 'récapitulatif'],
  },
}

/**
 * Retrouver un parcours par son ID
 */
export function getParcoursById(id: string): Parcours | undefined {
  return PARCOURS.find((p) => p.id === id)
}

/**
 * Retrouver une capsule par son ID
 */
export function getCapsuleById(id: string): Capsule | undefined {
  return CAPSULES[id]
}
