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
    capsules: ['pc-structure', 'pc-sources', 'pc-skills-agents', 'pc-grill-me', 'pc-preplan', 'pc-adversarial', 'pc-synthesis', 'pc-models'],
  },
  {
    id: 'claude-code',
    title: 'Agents CLI',
    description: 'Maîtriser un agent en ligne de commande : Claude Code (idées transposables à Codex et Antigravity)',
    icon: 'Terminal',
    color: 'cosmic',
    capsules: ['cc-install', 'cc-config', 'cc-commands', 'cc-dotclaude', 'cc-bfcours-setup', 'cc-se-former'],
  },
  {
    id: 'avance',
    title: 'Avancé',
    description: 'Architecture agents, skills, hooks et grands chantiers',
    icon: 'Sparkles',
    color: 'nebula',
    capsules: ['av-architecture', 'av-creer-skill', 'av-hooks', 'av-share', 'av-subagents', 'av-chantier'],
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
          Quand vous lancez Claude Code (ou Codex, ou Antigravity), vous parlez à un <strong>agent principal</strong> :
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
          <strong>Codex</strong> (OpenAI), <strong>Antigravity</strong> (Google) ou tout autre agent du même genre.
          Le principe reste le même : un système composé de 5 briques.
        </p>
        <ul>
          <li><strong>Agent principal</strong> : votre interlocuteur, le cerveau qui planifie, orchestre le travail et invoque des sous-agents si nécessaire</li>
          <li><strong>Skills</strong> : des savoir-faire spécialisés (LaTeX, images, présentations...) que l'agent ou ses sous-agents peuvent utiliser</li>
          <li><strong>Instructions</strong> : des fichiers (CLAUDE.md pour Claude Code, AGENTS.md pour Codex) qui définissent le comportement de l'agent</li>
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
        <div style="padding: 0.75rem 1rem; margin-bottom: 1rem; background: rgba(52,211,153,0.08); border-radius: 8px; border-left: 3px solid rgba(52,211,153,0.4);">
          <p style="margin: 0 0 0.4rem 0;"><strong>Le guide officiel</strong></p>
          <ul style="margin: 0;">
            <li><a href="https://support.claude.com/fr/articles/10065433-installer-claude-desktop" target="_blank" rel="noopener noreferrer">Installer Claude Desktop</a> (centre d'aide, en français)</li>
            <li><a href="https://support.claude.com/fr/collections/16163169-bureau-claude" target="_blank" rel="noopener noreferrer">Tous les articles d'aide sur Claude Desktop</a> (en français)</li>
            <li><a href="https://code.claude.com/docs/fr/desktop-quickstart" target="_blank" rel="noopener noreferrer">Démarrer avec l'onglet Code</a> (doc en français)</li>
            <li><a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer">Cours Claude 101</a>, leçon « How you'll work with Claude on your desktop » (gratuit, en anglais)</li>
          </ul>
        </div>
        <h3>Qu'est-ce que Claude Desktop ?</h3>
        <p>
          Claude Desktop est l'application d'Anthropic pour <strong>Windows</strong> (10 ou plus récent),
          <strong>macOS</strong> (13 ou plus récent) et <strong>Linux</strong> (en bêta). Vous dialoguez avec
          Claude depuis votre bureau, sans passer par un navigateur web.
        </p>
        <p>L'application réunit trois façons de travailler :</p>
        <ul>
          <li><strong>Chat</strong> : conversation classique, comme sur <a href="https://claude.ai" target="_blank" rel="noopener noreferrer">claude.ai</a> (offre gratuite comprise)</li>
          <li><strong>Cowork</strong> : Claude mène seul une tâche longue (rapport, tableur, diaporama, rangement de fichiers) dans les dossiers que vous lui ouvrez (offres payantes)</li>
          <li><strong>Code</strong> : Claude Code avec une interface graphique, pour travailler sur vos fichiers sans terminal (offres payantes)</li>
        </ul>
        <p style="font-size: 0.9em; color: #94a3b8;">
          Anthropic est en train de fusionner Chat et Cowork en une seule conversation : selon votre compte,
          vous verrez deux choix « Chat » et « Cowork » près de la zone de saisie, ou une seule zone où Claude
          décide lui-même s'il répond ou s'il mène une tâche
          (<a href="https://support.claude.com/fr/articles/16761823-claude-cowork-et-chat-sont-un-seul-claude" target="_blank" rel="noopener noreferrer">explication officielle</a>).
        </p>
        <p>
          L'onglet Code utilise le <strong>même moteur</strong> que Claude Code en ligne de commande :
          seule l'interface change. Desktop est le point d'entrée idéal si vous débutez avec l'IA.
        </p>
        <h4>Et les autres outils ?</h4>
        <p>
          Deux plateformes permettent aujourd'hui de faire à peu près la même chose :
          <strong>Codex</strong> (OpenAI) et <strong>Antigravity</strong> (Google).
          Le choix dépend surtout de vos goûts et de vos habitudes. Ce site détaille Claude
          parce que c'est l'outil de l'auteur et que le setup partagé est conçu pour lui ;
          les idées (agents, skills, consignes) se transposent d'un outil à l'autre.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Télécharger / Accéder</span>
          <div class="doc-links-buttons">
            <a href="https://claude.com/download" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Télécharger Claude Desktop
            </a>
            <a href="https://support.claude.com/fr/articles/10065433-installer-claude-desktop" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Guide officiel d'installation (en français)
            </a>
            <a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Claude 101 (gratuit, en anglais)
            </a>
            <a href="https://code.claude.com/docs/fr/desktop" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Onglet Code de Desktop (doc en français)
            </a>
            <a href="https://learn.chatgpt.com/docs" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex (OpenAI)
            </a>
            <a href="https://antigravity.google/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Antigravity (Google)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Tutoriel pas-à-pas</h3>
        <ol>
          <li>
            <strong>Téléchargez</strong> l'application depuis
            <a href="https://claude.com/download" target="_blank" rel="noopener noreferrer">claude.com/download</a> :
            cliquez sur « Download » sous <strong>Windows</strong> ou <strong>macOS</strong>
          </li>
          <li>
            <strong>Ouvrez le fichier téléchargé</strong> pour terminer l'installation
            (sur Linux, l'installation passe par <code>apt</code> : suivez le guide officiel)
          </li>
          <li>
            <strong>Lancez</strong> Claude depuis le menu Démarrer (Windows) ou le dossier Applications (macOS),
            puis connectez-vous avec votre compte Claude
          </li>
          <li>
            <strong>Repérez Chat, Cowork et Code</strong> : Chat et Cowork se choisissent près de la zone de saisie,
            Code est un onglet en haut de la fenêtre. Aucun réglage préalable n'est nécessaire.
          </li>
        </ol>
        <p style="font-size: 0.9em; color: #94a3b8;">
          L'application évolue vite : si un menu a changé de nom, l'aide officielle
          (<a href="https://support.claude.com" target="_blank" rel="noopener noreferrer">support.claude.com</a>) donne toujours le chemin à jour.
        </p>
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
              <p>Claude devrait vous proposer l'une de ces voies :</p>
              <ol>
                <li><strong>L'extension Filesystem</strong> dans l'onglet Chat : Paramètres > Extensions > Parcourir les extensions, installer « Filesystem » puis lui indiquer votre dossier de travail</li>
                <li><strong>L'onglet Cowork ou Code</strong>, qui travaillent directement dans un dossier que vous choisissez</li>
              </ol>
              <p>Une fois l'accès donné, Claude peut lire, créer et modifier des fichiers directement sur votre machine. C'est la base pour toute utilisation productive.</p>
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
              <p>Les paramètres s'ouvrent depuis le <strong>menu de votre compte</strong> (vos initiales, en bas à gauche) > <strong>Paramètres</strong>. Vous y trouverez notamment :</p>
              <ul>
                <li><strong>Général</strong> : votre nom, vos instructions pour Claude, vos préférences</li>
                <li><strong>Utilisation</strong> : votre consommation</li>
                <li><strong>Cowork</strong> et <strong>Claude Code</strong> : les réglages propres à ces deux façons de travailler</li>
                <li><strong>Extensions</strong> : installer des outils locaux comme Filesystem (accès à vos fichiers)</li>
                <li><strong>Développeur</strong> : réservé aux réglages techniques (serveurs MCP déclarés à la main)</li>
              </ul>
              <p>Repérez aussi le bouton <strong>Personnaliser</strong> dans la barre latérale gauche : il rassemble <strong>compétences</strong> (skills), <strong>connecteurs</strong> et <strong>plugins</strong> au même endroit. C'est ce dont vous aurez besoin dans la suite du parcours.</p>
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
        <div style="padding: 0.75rem 1rem; margin-bottom: 1rem; background: rgba(52,211,153,0.08); border-radius: 8px; border-left: 3px solid rgba(52,211,153,0.4);">
          <p style="margin: 0 0 0.4rem 0;"><strong>Le guide officiel</strong></p>
          <ul style="margin: 0;">
            <li><a href="https://support.claude.com/fr/articles/10949351-demarrage-avec-les-serveurs-mcp-locaux-sur-claude-desktop" target="_blank" rel="noopener noreferrer">Installer une extension de bureau</a> (centre d'aide, en français)</li>
            <li><a href="https://support.claude.com/fr/articles/13345190-demarrer-avec-claude-cowork" target="_blank" rel="noopener noreferrer">Démarrer avec Claude Cowork</a>, qui travaille directement dans un dossier (en français)</li>
          </ul>
        </div>
        <h3>Configuration via les menus</h3>
        <p>
          La configuration de Claude Desktop se fait entièrement via les menus de l'application.
          Pas besoin de toucher à des fichiers — tout est accessible graphiquement.
        </p>
        <p>Voici les trois étapes principales :</p>
        <ol>
          <li>
            <strong>Ouvrir les Paramètres</strong> (menu de votre compte : vos initiales, en bas à gauche)
          </li>
          <li>
            <strong>Explorer les Extensions</strong> disponibles (Paramètres > Extensions > Parcourir les extensions)
          </li>
          <li>
            <strong>Installer l'extension Filesystem</strong> pour donner à Claude accès à vos fichiers
          </li>
        </ol>
        <p style="font-size: 0.9em; color: #94a3b8;">
          La rubrique <strong>Paramètres > Développeur</strong> (bouton « Edit Config ») n'est utile que pour déclarer
          à la main un serveur MCP dans un fichier de configuration : vous n'en avez pas besoin pour les extensions du catalogue.
          Si vous utilisez Cowork ou l'onglet Code, vous n'avez même pas besoin de Filesystem :
          il suffit de choisir le dossier de travail au lancement de la tâche.
        </p>
        <p>
          Une fois le filesystem activé, Claude peut lire et créer des fichiers directement sur
          votre machine. C'est comme donner une main au programme — il peut enfin toucher vos documents.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://support.claude.com/fr/articles/10949351-demarrage-avec-les-serveurs-mcp-locaux-sur-claude-desktop" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Extensions de bureau (aide en français)
            </a>
            <a href="https://support.claude.com/fr/articles/13345190-demarrer-avec-claude-cowork" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Démarrer avec Cowork (aide en français)
            </a>
            <a href="https://modelcontextprotocol.io/docs/develop/connect-local-servers" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Déclarer un serveur MCP à la main (en anglais)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Parcours dans les menus</h3>
        <p>Voici comment naviguer :</p>
        <ol>
          <li>
            <strong>Ouvrez les Paramètres</strong> : cliquez sur vos initiales en bas à gauche, puis sur « Paramètres »
          </li>
          <li>
            <strong>Cliquez sur « Extensions »</strong> dans le menu de gauche, puis sur « Parcourir les extensions »
          </li>
          <li>
            <strong>Cherchez « Filesystem »</strong> dans le catalogue et installez-la
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
                <li>L'extension Filesystem est installée et activée (Paramètres > Extensions)</li>
                <li>Elle pointe vers le bon dossier</li>
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
        <div style="padding: 0.75rem 1rem; margin-bottom: 1rem; background: rgba(52,211,153,0.08); border-radius: 8px; border-left: 3px solid rgba(52,211,153,0.4);">
          <p style="margin: 0 0 0.4rem 0;"><strong>Le guide officiel</strong></p>
          <ul style="margin: 0;">
            <li><a href="https://support.claude.com/fr/articles/10949351-demarrage-avec-les-serveurs-mcp-locaux-sur-claude-desktop" target="_blank" rel="noopener noreferrer">Extensions de bureau</a> (centre d'aide, en français)</li>
            <li><a href="https://support.claude.com/fr/articles/11176164-utiliser-les-connecteurs-pour-etendre-les-capacites-de-claude" target="_blank" rel="noopener noreferrer">Utiliser les connecteurs</a> (en français)</li>
            <li><a href="https://support.claude.com/fr/articles/14328846-parcourez-les-competences-connecteurs-et-plugins-dans-un-seul-repertoire" target="_blank" rel="noopener noreferrer">Compétences, connecteurs et plugins dans « Personnaliser »</a> (en français)</li>
            <li><a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer">Cours Claude 101</a>, leçons « Working with skills » et « Connecting your tools » (gratuit, en anglais)</li>
          </ul>
        </div>
        <h3>Panorama des possibilités</h3>
        <p>
          Maintenant que le filesystem est activé (capsule précédente), découvrez tout ce qui existe.
          Claude Desktop propose quatre façons d'étendre Claude :
        </p>
        <ol>
          <li>
            <strong>Extensions de bureau</strong> (Paramètres > Extensions) : des outils qui tournent
            sur votre ordinateur, installés en un clic depuis un catalogue (Filesystem, etc.)
          </li>
          <li>
            <strong>Connecteurs</strong> (Personnaliser > Connecteurs, ou bouton <strong>+</strong> près de la zone de saisie) :
            Google Drive, Notion, Slack, etc., avec une simple connexion à votre compte
          </li>
          <li>
            <strong>Compétences (skills) et plugins</strong> (bouton <strong>Personnaliser</strong> dans la barre latérale gauche) :
            des savoir-faire et des paquets d'outils prêts à l'emploi
          </li>
          <li>
            <strong>Serveurs MCP communautaires</strong> : catalogue sur
            <a href="https://github.com/modelcontextprotocol/servers" target="_blank" rel="noopener noreferrer">
            github.com/modelcontextprotocol/servers
            </a>, à déclarer à la main (Paramètres > Développeur)
          </li>
        </ol>
        <p>
          Extensions et connecteurs reposent tous sur le même protocole, <strong>MCP</strong>
          (Model Context Protocol) : une prise standard qui permet à Claude d'utiliser un outil extérieur.
        </p>
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
            <a href="https://code.claude.com/docs/fr/mcp" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              MCP dans Claude Code (doc en français)
            </a>
            <a href="https://anthropic.skilljar.com/introduction-to-model-context-protocol" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Introduction to MCP (développeurs, en anglais)
            </a>
            <a href="https://support.claude.com/fr/articles/10949351-demarrage-avec-les-serveurs-mcp-locaux-sur-claude-desktop" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Extensions de bureau (aide en français)
            </a>
            <a href="https://support.claude.com/fr/articles/11176164-utiliser-les-connecteurs-pour-etendre-les-capacites-de-claude" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Connecteurs (aide en français)
            </a>
            <a href="https://support.claude.com/fr/articles/14328846-parcourez-les-competences-connecteurs-et-plugins-dans-un-seul-repertoire" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Personnaliser : compétences, connecteurs, plugins (aide en français)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Accéder aux extensions depuis Claude Desktop</h3>
        <p>Tout se passe dans les menus de l'application :</p>
        <ol>
          <li>
            Cliquez sur <strong>vos initiales</strong> en bas à gauche de la fenêtre
          </li>
          <li>
            Choisissez <strong>Paramètres</strong>
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
          Notion, Slack...) accessibles via <strong>Personnaliser > Connecteurs</strong> (barre latérale gauche),
          ou via le bouton <strong>+</strong> à côté de la zone de saisie > <strong>Connecteurs</strong> >
          <strong>Gérer les connecteurs</strong>. Ils ne nécessitent pas d'installation : cliquez sur
          « Connecter » puis connectez-vous au service.
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
              <li>Vos initiales (en bas à gauche) → <strong>Paramètres</strong></li>
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
                <li>Une extension qui pilote une application de bureau que vous utilisez déjà (bureautique, calendrier, messagerie…) : Claude agit directement dedans</li>
                <li>Une extension de recherche ou de lecture de pages web : Claude va chercher des informations récentes (programmes officiels mis à jour, ressources en ligne…)</li>
              </ul>
              <p>Google Drive, Notion ou Slack ne sont pas des extensions mais des <strong>connecteurs</strong> (exercice suivant). Le catalogue change souvent : les noms exacts varient, revenez-y de temps en temps.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice bonus</span>
          </div>
          <div class="exercise-body">
            <p>Activez un <strong>Connecteur</strong> : dans une fenêtre de chat, cliquez sur le bouton <strong>+</strong> à côté de la zone de saisie → <strong>Connecteurs</strong> → <strong>Gérer les connecteurs</strong> (ou passez par Personnaliser → Connecteurs). Choisissez un service (Google Drive, Notion, Slack...) et suivez l'authentification.</p>
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
    order: 4,
    sections: {
      info: `
        <div style="padding: 0.75rem 1rem; margin-bottom: 1rem; background: rgba(52,211,153,0.08); border-radius: 8px; border-left: 3px solid rgba(52,211,153,0.4);">
          <p style="margin: 0 0 0.4rem 0;"><strong>Le guide officiel</strong></p>
          <ul style="margin: 0;">
            <li><a href="https://support.claude.com/fr/articles/9517075-qu-est-ce-que-les-projets" target="_blank" rel="noopener noreferrer">Qu'est-ce que les projets ?</a> (centre d'aide, en français)</li>
            <li><a href="https://support.claude.com/fr/articles/9519177-comment-creer-et-gerer-des-projets" target="_blank" rel="noopener noreferrer">Comment créer et gérer des projets</a> (en français)</li>
            <li><a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer">Cours Claude 101</a>, leçon « Introduction to projects » (gratuit, en anglais)</li>
          </ul>
        </div>
        <h3>Qu'est-ce qu'un Projet ?</h3>
        <p>
          Un <strong>Projet</strong> dans Claude Desktop est un espace de travail dédié à un sujet.
          Il regroupe vos conversations, vos fichiers et vos <strong>instructions personnalisées</strong>
          dans un même endroit. Les projets sont ouverts à tous, offre gratuite comprise
          (cinq projets au plus avec un compte gratuit).
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
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://support.claude.com/fr/articles/9519177-comment-creer-et-gerer-des-projets" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Créer et gérer des projets (aide en français)
            </a>
            <a href="https://support.claude.com/fr/articles/9517075-qu-est-ce-que-les-projets" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Qu'est-ce que les projets ? (aide en français)
            </a>
            <a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Claude 101 (gratuit, en anglais)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Créer un Projet pas à pas</h3>
        <ol>
          <li>
            <p>Dans la <strong>sidebar gauche</strong> de Claude Desktop, cliquez sur <strong>Projets</strong> puis sur <strong>+ Nouveau projet</strong> :</p>
            <img src="/images/claude-desktop/projects/overview.png" alt="Vue d'ensemble des projets dans Claude Desktop" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0;" />
          </li>
          <li>
            <p>Remplissez le formulaire : donnez un <strong>nom</strong> à votre projet et décrivez brièvement <strong>ce que vous essayez de faire</strong>. Attention : Claude ne lit ni le nom ni la description, ils servent seulement à vous repérer. Les consignes pour Claude vont dans les <strong>Instructions</strong> (étape suivante).</p>
            <img src="/images/claude-desktop/projects/new.png" alt="Formulaire de création de projet" style="max-width: 400px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 0.75rem 0;" />
          </li>
          <li>
            <p>Une fois créé, vous accédez à l'espace du projet. Sur la droite, vous pouvez :</p>
            <ul>
              <li>Écrire des <strong>Instructions</strong> que Claude relira systématiquement (« Définir les instructions du projet »)</li>
              <li>Ajouter des <strong>Fichiers</strong> de référence (PDF, texte, images...) avec le bouton <strong>+</strong> de la base de connaissances</li>
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
              <li>Dans les <strong>Instructions</strong> (panneau de droite), copiez-collez ce texte :</li>
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
        <div style="padding: 0.75rem 1rem; margin-bottom: 1rem; background: rgba(52,211,153,0.08); border-radius: 8px; border-left: 3px solid rgba(52,211,153,0.4);">
          <p style="margin: 0 0 0.4rem 0;"><strong>Le guide officiel</strong></p>
          <ul style="margin: 0;">
            <li><a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer">Cours Claude 101</a>, leçons « Your first conversation with Claude » et « Getting better results » (gratuit, en anglais)</li>
            <li><a href="https://support.claude.com/fr/articles/13345190-demarrer-avec-claude-cowork" target="_blank" rel="noopener noreferrer">Démarrer avec Claude Cowork</a>, pour confier une tâche entière sur vos fichiers (centre d'aide, en français)</li>
          </ul>
        </div>
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
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Claude 101 (gratuit, en anglais)
            </a>
            <a href="https://support.claude.com/fr/articles/13345190-demarrer-avec-claude-cowork" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Démarrer avec Cowork (aide en français)
            </a>
          </div>
        </div>
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
            <strong>Un compte Claude</strong> avec un abonnement Pro, Max, Team ou Enterprise, ou un compte Console (API).
            L'offre gratuite de claude.ai ne donne pas accès à Claude Code.
          </li>
          <li>
            <strong>Pas besoin de Node.js</strong> : l'installateur natif de Claude Code s'en passe.
            Node.js reste utile plus tard pour certains outils (serveurs MCP, scripts).
          </li>
          <li>
            <strong>Windows</strong> : <a href="https://git-scm.com/downloads/win" target="_blank" rel="noopener noreferrer">Git for Windows</a> est conseillé
            (Claude Code utilise alors Git Bash pour ses commandes). Sans lui, Claude Code passe par PowerShell.
          </li>
        </ul>
        <h4>Et les autres outils ?</h4>
        <p>
          Deux plateformes permettent aujourd'hui de faire à peu près la même chose que Claude Code :
        </p>
        <ul>
          <li>
            <strong>Codex</strong> (OpenAI) : l'agent d'OpenAI, utilisable dans l'application de bureau ChatGPT
            (Windows, macOS, Linux), en ligne de commande, dans un éditeur de code ou en ligne.
            On s'y connecte avec son compte ChatGPT.
            <a href="https://learn.chatgpt.com/docs" target="_blank" rel="noopener noreferrer">Documentation officielle de Codex</a>
          </li>
          <li>
            <strong>Antigravity</strong> (Google) : la plateforme d'agents de Google, sous forme d'application de bureau,
            d'éditeur de code et d'outil en ligne de commande (Windows, macOS, Linux).
            On s'y connecte avec son compte Google.
            <a href="https://antigravity.google/" target="_blank" rel="noopener noreferrer">Site officiel d'Antigravity</a>
          </li>
        </ul>
        <p>
          Le choix dépend avant tout de vos goûts et de vos habitudes. Ce site détaille Claude Code
          parce que c'est l'outil de l'auteur et que le setup partagé est conçu pour lui ;
          les idées (agents, skills, fichier d'instructions) se transposent d'un outil à l'autre.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://academy.claude.com/courses/claude-code-101" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Claude Code 101 (gratuit, en anglais)
            </a>
            <a href="https://code.claude.com/docs/fr/setup" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Installation (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/quickstart" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Démarrage rapide (doc en français)
            </a>
            <a href="https://learn.chatgpt.com/docs" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-openai">
              Codex (OpenAI)
            </a>
            <a href="https://antigravity.google/" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-google">
              Antigravity (Google)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Guide d'installation de Claude Code</h3>

        <div>
          <div>
            <h4>Installation native (recommandée)</h4>
            <p>Claude Code ne nécessite plus Node.js. Utilisez l'installateur natif :</p>
            <p><strong>macOS / Linux / WSL :</strong></p>
            <pre><code>curl -fsSL https://claude.ai/install.sh | bash</code></pre>
            <p><strong>Windows PowerShell :</strong></p>
            <pre><code>irm https://claude.ai/install.ps1 | iex</code></pre>
            <p><strong>Alternatives :</strong> <code>brew install --cask claude-code</code> (Homebrew) ou <code>winget install Anthropic.ClaudeCode</code> (WinGet). L'installateur natif se met à jour tout seul ; avec Homebrew ou WinGet, pensez à faire les mises à jour vous-même.</p>
            <p><strong>Vérifier :</strong> fermez puis rouvrez le terminal et tapez <code>claude --version</code>. Un numéro de version doit s'afficher.</p>
            <h4>Lancer</h4>
            <pre><code>cd votre-dossier-de-travail
claude</code></pre>
            <p>Au premier lancement, suivez les instructions d'authentification à l'écran.</p>
            <p><em>Vérification :</em> <code>claude doctor</code> vérifie que tout est correctement installé.</p>
          </div>
        </div>
        <p style="font-size: 0.9em; color: #94a3b8;">
          Pour Codex ou Antigravity, suivez le guide d'installation de leur site officiel (liens dans la partie précédente).
        </p>
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
                <li>Sous la zone de saisie, une petite ligne rappelle le mode de permission en cours et quelques raccourcis (vous pourrez y ajouter une <strong>statusline</strong> personnalisée, voir la capsule « Commandes essentielles »)</li>
              </ul>
              <p>Pour quitter, tapez <code>/exit</code> ou appuyez deux fois sur <code>Ctrl+C</code>.</p>
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
              <p>Avec ce flag, Claude ne vous demande plus la permission avant de lire/écrire des fichiers ou exécuter des commandes. Il agit en <strong>autonomie complète</strong> (mode <code>bypassPermissions</code>). Seules vos règles d'interdiction (<code>deny</code>, voir capsule suivante) continuent de s'appliquer.</p>
              <p>C'est utile pour des <strong>modifications de routine</strong> où vous faites confiance à l'agent : corrections mineures, mise en forme, tâches prévisibles. À éviter sur des projets sensibles ou quand vous découvrez un nouveau dossier.</p>
              <p><strong>Alternative plus sûre :</strong> le <strong>mode auto</strong>. Un second modèle vérifie chaque action à votre place et bloque celles qui semblent risquées. Dans les versions récentes, c'est le mode de départ par défaut. Appuyez sur <code>Maj+Tab</code> pendant une session pour passer d'un mode à l'autre (manuel, acceptation des modifications, plan, auto) : le mode actif s'affiche sous la zone de saisie.</p>
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
            <a href="https://code.claude.com/docs/fr/settings" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Paramètres (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/memory" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              CLAUDE.md et mémoire (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/permissions" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Permissions (doc en français)
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
    qcm-creator/
      SKILL.md
      references/distracteurs.md
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
              <p>Cela démontre que les <strong>règles d'interdiction (<code>deny</code>) sont plus fortes</strong> que le flag <code>--dangerously-skip-permissions</code> : la documentation officielle précise qu'elles bloquent dans tous les modes.</p>
              <p>C'est un mécanisme essentiel : vous pouvez travailler en mode autonome tout en protégeant certains dossiers sensibles (notes, données personnelles des élèves, etc.).</p>
              <p><strong>Limite à connaître :</strong> ces règles couvrent les outils de Claude (lecture, écriture, commandes comme <code>cat</code>), mais pas un script Python ou Node qui ouvrirait lui-même le fichier. Pour une protection totale, la documentation renvoie au <em>sandbox</em> (bac à sable) du système.</p>
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
          <li><code>/model</code> : change de modèle (Opus, Sonnet, Haiku…) et règle le niveau d'effort</li>
          <li><code>/resume</code> : rouvre une conversation précédente, choisie dans une liste</li>
          <li><code>/usage</code> : affiche votre consommation (session en cours et limites de votre abonnement)</li>
          <li><code>/context</code> : montre ce qui occupe la mémoire de travail de Claude (fichiers, outils, conversation)</li>
          <li><code>/config</code> : ouvre la configuration interactive de Claude Code</li>
          <li><code>/exit</code> : quitte Claude Code</li>
        </ul>
        <h4>Commandes terminal (hors session)</h4>
        <p>Ces commandes se lancent directement dans le terminal, avant ou après une session Claude :</p>
        <ul>
          <li><code>claude</code> : lance une nouvelle session interactive</li>
          <li><code>claude --continue</code> (ou <code>claude -c</code>) : <strong>reprend la dernière conversation</strong> du dossier courant, là où vous l'aviez laissée. Très pratique quand vous avez fermé le terminal par erreur ou quand vous reprenez le travail le lendemain.</li>
          <li><code>claude --resume</code> (ou <code>claude -r</code>) : affiche la liste des conversations passées pour en choisir une</li>
          <li><code>claude doctor</code> : vérifie que tout est correctement installé et configuré</li>
          <li><code>claude update</code> : met à jour Claude Code vers la dernière version (l'installateur natif le fait aussi tout seul)</li>
        </ul>
        <h4>Fonctionnalités avancées intégrées</h4>
        <ul>
          <li>
            <strong>ultrathink</strong> : en ajoutant le mot <code>ultrathink</code> dans votre message, vous demandez à Claude de réfléchir plus longuement <em>pour ce message seulement</em>. Pour régler durablement la profondeur de réflexion, utilisez plutôt <code>/effort</code> (niveaux <code>low</code>, <code>medium</code>, <code>high</code>, <code>xhigh</code>, <code>max</code>).
          </li>
          <li>
            <strong>Statusline</strong> : une barre d'état personnalisable sous la zone de saisie, qui peut afficher le modèle utilisé, le remplissage du contexte, le coût estimé de la session… Elle n'existe pas par défaut : tapez <code>/statusline</code> suivi de ce que vous voulez voir, et Claude écrit le script et le réglage pour vous.
          </li>
          <li>
            <strong>Mode plan</strong> : Claude lit vos fichiers et propose un plan, sans rien modifier tant que vous ne l'avez pas validé. Appuyez sur <code>Maj+Tab</code> jusqu'à voir <code>plan mode on</code> sous la zone de saisie, ou lancez <code>claude --permission-mode plan</code>.
          </li>
        </ul>
        <p>
          L'autocomplétion fonctionne en tapant <code>/</code> puis les premières lettres.
          Les flèches haut/bas naviguent les suggestions, Tab valide.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/fr/cli-reference" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Référence CLI (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/commands" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Commandes slash (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/common-workflows" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Workflows courants (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/statusline" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Statusline (doc en français)
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
/model             → Changer de modèle et d'effort
/resume            → Rouvrir une conversation passée
/usage             → Voir sa consommation
/config            → Configuration interactive</code></pre>
        <h4>Commandes terminal (hors session)</h4>
        <pre><code>claude             → Nouvelle session
claude --continue  → Reprendre la dernière conversation (ou claude -c)
claude --resume    → Choisir une conversation passée (ou claude -r)
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
          Les modèles récents réfléchissent déjà avant de répondre : <code>ultrathink</code> pousse
          simplement cette réflexion plus loin sur un message précis.
        </p>
        <h4>La statusline</h4>
        <p>
          Une fois configurée avec <code>/statusline</code>, vous voyez en permanence sous la zone de saisie une ligne comme :
        </p>
        <pre><code>Opus 5.5  ●  contexte 18 %  ●  0,42 $  ●  session 14 min</code></pre>
        <p>
          Elle vous aide à surveiller votre consommation et à savoir quand utiliser
          <code>/compact</code> pour libérer du contexte. Avec un abonnement (Pro, Max…), le coût
          affiché est une estimation au tarif de l'API : ce n'est pas ce que vous payez.
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
            <p>Faites quelques échanges avec Claude, puis tapez <code>/context</code> pour voir combien de place occupe la conversation. Tapez ensuite <code>/compact</code>, puis de nouveau <code>/context</code>.</p>
            <p>Comment le remplissage change-t-il ?</p>
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
              <p><strong>Règles pratiques :</strong></p>
              <ul>
                <li>Les modèles récents ont une très grande mémoire de travail (un million de tokens) et Claude Code compacte tout seul quand elle est presque pleine. Vous n'avez donc pas à surveiller un seuil précis.</li>
                <li>Utilisez <code>/compact</code> quand vous changez d'étape dans un même travail, ou quand les réponses deviennent moins pertinentes. Vous pouvez préciser quoi garder : <code>/compact garde les décisions sur le barème</code>.</li>
                <li>Utilisez plutôt <code>/clear</code> quand vous passez à un tout autre sujet : c'est gratuit et repartir de zéro coûte moins cher qu'une longue conversation.</li>
              </ul>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 4 : Statusline</span>
          </div>
          <div class="exercise-body">
            <p>Demandez à Claude de configurer votre statusline :</p>
            <pre style="margin: 0.5rem 0; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px; font-size: 0.85em;">/statusline affiche le modèle, le pourcentage de contexte utilisé et le coût de la session</pre>
            <p>Claude écrit un petit script et configure la barre d'état sous la zone de saisie pour vous.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Claude crée un script dans le dossier <code>~/.claude/</code> et ajoute un réglage <code>statusLine</code> dans <code>~/.claude/settings.json</code>. Vous devriez voir apparaître sous la zone de saisie :</p>
              <ul>
                <li>Le <strong>modèle</strong> utilisé (ex : Opus 5.5)</li>
                <li>Le <strong>pourcentage de contexte</strong> déjà rempli</li>
                <li>Le <strong>coût estimé</strong> de la session en cours (indicatif si vous avez un abonnement)</li>
              </ul>
              <p>C'est un bon réflexe de garder un œil sur ces indicateurs, surtout le remplissage du contexte qui vous dit quand un <code>/compact</code> ou un <code>/clear</code> serait utile. Pour la retirer : <code>/statusline supprime-la</code>.</p>
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
          Le dossier <code>.claude/</code> (d'autres outils, comme Codex, ont leur équivalent)
          est le centre névralgique de votre configuration. Il contient tout ce qui permet à l'agent
          de <strong>comprendre votre contexte</strong> et de <strong>savoir quoi faire</strong>.
        </p>
        <h4>Structure type</h4>
        <ul>
          <li>
            <strong>agents/</strong> : sous-processus spécialisés avec leurs propres instructions.
            Chaque agent est un fichier Markdown décrivant une mission précise (créer du LaTeX, déboguer une compilation, préparer un QCM...).
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
        <h4>Et chez les autres ?</h4>
        <ul>
          <li><strong>Claude Code</strong> : <code>.claude/</code> + <code>CLAUDE.md</code></li>
          <li><strong>Codex</strong> (OpenAI) : <code>.codex/</code> + <code>AGENTS.md</code></li>
          <li><strong>Antigravity</strong> (Google) : ses propres fichiers de règles et de skills (voir <a href="https://antigravity.google/docs/getting-started" target="_blank" rel="noopener noreferrer">sa documentation</a>)</li>
        </ul>
        <p>Les concepts sont les mêmes d'un outil à l'autre ; seuls les noms changent.</p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/fr/memory" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              CLAUDE.md et mémoire (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/settings" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Paramètres et permissions (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/sub-agents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Sous-agents (doc en français)
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
    correction-agent.md    → Rédige des corrigés détaillés

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
                <li><strong>Un skill</strong> (ex : <code>bfcours-latex/SKILL.md</code>) : contient un frontmatter YAML (nom, description qui dit quand l'utiliser) puis des instructions détaillées. Vous pouvez l'invoquer <strong>manuellement</strong> via <code>/bfcours-latex</code>, et Claude le charge aussi <strong>tout seul</strong> quand votre demande correspond à sa description.</li>
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
          <li><strong>Agents spécialisés</strong> : création LaTeX, débogage de compilation, présentations...</li>
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
            <p>Identifiez une tâche que vous faites souvent et que le setup ne couvre pas. Installez le <strong>skill-creator officiel d'Anthropic</strong> (une seule fois) puis demandez-lui de créer votre propre skill. Testez-le et affinez-le.</p>
            <pre><code>/plugin install skill-creator@claude-plugins-official</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Exemples de demandes, à taper après l'installation :</p>
              <ul>
                <li><strong>Commentaires de bulletin</strong> : <code>Utilise skill-creator pour créer un skill qui génère des appréciations de bulletin à partir des notes et des remarques que je lui donne</code></li>
                <li><strong>Fiches méthode</strong> : <code>Utilise skill-creator pour créer un skill qui génère des fiches méthode sur une technique de calcul</code></li>
                <li><strong>Activité de groupe</strong> : <code>Utilise skill-creator pour créer un skill qui planifie une activité de groupe avec rôles différenciés</code></li>
              </ul>
              <p>Le skill-creator vous posera des questions pour préciser vos besoins, puis générera un dossier <code>.claude/skills/votre-skill/</code> contenant un <code>SKILL.md</code> (instructions principales) et éventuellement des fichiers de support (références, scripts, exemples). Testez-le immédiatement avec <code>/votre-skill</code> suivi d'une demande concrète. La capsule « Créer un skill » du parcours Avancé détaille la démarche.</p>
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
  'cc-se-former': {
    id: 'cc-se-former',
    title: 'Se former avec Anthropic',
    description: 'Les cours officiels gratuits d\'Anthropic : lesquels suivre, dans quel ordre, et comment les combiner avec ce site',
    parcours: 'claude-code',
    order: 5,
    sections: {
      info: `
        <h3>Les cours officiels sont la référence</h3>
        <p>
          Anthropic publie des <strong>cours gratuits</strong> sur Claude, Claude Code et l'usage de l'IA
          en classe. Ils sont faits par les équipes qui conçoivent les outils, mis à jour à chaque
          nouveauté, et souvent mieux construits que n'importe quel tutoriel maison.
          <strong>Commencez par eux.</strong>
        </p>
        <p>
          Les tutoriels de ce site sont un <strong>complément</strong> : le point de vue d'un enseignant
          de mathématiques français, des exemples tirés de la classe, et le mode d'emploi du setup
          partagé ici (skills LaTeX et Typst, agents, commandes).
        </p>
        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Tous les cours sont en anglais.</strong> Astuce : la traduction intégrée du navigateur
          (clic droit sur la page > « Traduire en français » dans Chrome ou Edge) rend les leçons très
          lisibles. Les vidéos ont en général des sous-titres que l'on peut traduire automatiquement.
        </p>

        <h4>Les cours à connaître</h4>
        <div style="margin: 1rem 0; overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
            <tr style="border-bottom: 2px solid rgba(255,255,255,0.15);">
              <th style="text-align: left; padding: 0.6rem; color: #a78bfa;">Cours</th>
              <th style="text-align: left; padding: 0.6rem; color: #a78bfa;">À qui il sert</th>
              <th style="text-align: left; padding: 0.6rem; color: #a78bfa;">Durée</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://academy.claude.com/courses/claude-code-101" target="_blank" rel="noopener noreferrer"><strong>Claude Code 101</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Le meilleur point d'entrée pour Claude Code : installation, premières sessions, CLAUDE.md, bonnes habitudes. Débutants.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">environ 1 h 30 (12 leçons)</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/claude-101" target="_blank" rel="noopener noreferrer"><strong>Claude 101</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Les usages quotidiens de Claude (application web et Desktop) : projets, fichiers, connecteurs.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/ai-fluency-framework-foundations" target="_blank" rel="noopener noreferrer"><strong>AI Fluency: Framework &amp; Foundations</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Tout le monde. Un cadre en quatre compétences (le « 4D ») pour travailler avec une IA de façon efficace, critique et responsable.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">environ 4 h</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/ai-fluency-for-educators" target="_blank" rel="noopener noreferrer"><strong>AI Fluency for educators</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Enseignants : le même cadre appliqué à la préparation de cours et à l'accompagnement des élèves.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/path/ai-fluency-for-pk-12-educators" target="_blank" rel="noopener noreferrer"><strong>AI Fluency for pK-12 Educators</strong></a> (parcours)</td>
              <td style="padding: 0.6rem; color: #d1d5db;">Enseignants du primaire au lycée, avec un volet pour les formateurs qui animent des ateliers.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">plusieurs cours</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/teaching-ai-fluency" target="_blank" rel="noopener noreferrer"><strong>Teaching AI Fluency</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Formateurs et enseignants qui veulent enseigner ce cadre à d'autres (élèves ou collègues).</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/introduction-to-agent-skills" target="_blank" rel="noopener noreferrer"><strong>Introduction to agent skills</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Utilisateurs de Claude Code qui veulent comprendre et écrire des skills.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/introduction-to-subagents" target="_blank" rel="noopener noreferrer"><strong>Introduction to subagents</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Utilisateurs de Claude Code qui veulent déléguer à des sous-agents.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/claude-code-in-action" target="_blank" rel="noopener noreferrer"><strong>Claude Code in Action</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Niveau intermédiaire, orienté développement logiciel. Utile si vous codez vos propres outils.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
            <tr>
              <td style="padding: 0.6rem;"><a href="https://anthropic.skilljar.com/introduction-to-model-context-protocol" target="_blank" rel="noopener noreferrer"><strong>Introduction to Model Context Protocol</strong></a></td>
              <td style="padding: 0.6rem; color: #d1d5db;">Développeurs (Python) qui veulent créer leurs propres connecteurs MCP.</td>
              <td style="padding: 0.6rem; color: #9ca3af;">—</td>
            </tr>
          </table>
        </div>
        <p style="font-size: 0.9em; color: #94a3b8;">
          « — » : durée non indiquée. Le <a href="https://anthropic.skilljar.com/" target="_blank" rel="noopener noreferrer">catalogue complet</a>
          compte une vingtaine de cours. Tous sont gratuits ; il suffit de créer un compte.
        </p>

        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle en français</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/fr/quickstart" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Démarrage rapide
            </a>
            <a href="https://code.claude.com/docs/fr/best-practices" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Bonnes pratiques
            </a>
            <a href="https://code.claude.com/docs/fr/skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Quel cours pour quel profil ?</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.85rem; background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); border-radius: 8px;">
            <strong style="color: #86efac;">« Je n'ai jamais utilisé d'IA pour préparer mes cours »</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.9em;">
              Claude 101, puis AI Fluency for educators. Ensuite, le parcours Claude Desktop de ce site.
            </p>
          </div>
          <div style="padding: 0.85rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <strong style="color: #93c5fd;">« Je veux passer à Claude Code »</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.9em;">
              Claude Code 101 en entier. Puis le parcours Agents CLI de ce site pour installer le setup partagé.
            </p>
          </div>
          <div style="padding: 0.85rem; background: rgba(168,85,247,0.08); border: 1px solid rgba(168,85,247,0.2); border-radius: 8px;">
            <strong style="color: #d8b4fe;">« Je veux créer mes propres outils »</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.9em;">
              Introduction to agent skills et Introduction to subagents. Puis le parcours Avancé de ce site.
            </p>
          </div>
          <div style="padding: 0.85rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 8px;">
            <strong style="color: #fbbf24;">« J'anime des formations »</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.9em;">
              Le parcours AI Fluency for pK-12 Educators, puis Teaching AI Fluency.
            </p>
          </div>
        </div>
        <p>
          <strong>Ce que ce site ajoute :</strong> les cours officiels expliquent l'outil ;
          ici, vous trouvez des exemples de classe (un cours sur les fractions, une évaluation
          avec barème), la mise en page LaTeX ou Typst des documents élèves, et un dossier
          <code>.claude/</code> prêt à copier.
        </p>
      `,
      pratique: `
        <h3>Votre plan de formation en 3 étapes</h3>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Étape 1 — cette semaine</span>
          </div>
          <div class="exercise-body">
            <p>Suivez <strong>Claude Code 101</strong> (environ 1 h 30). Gardez Claude Code ouvert à côté et refaites chaque manipulation dans un dossier d'essai.</p>
          </div>
          <details class="exercise-solution">
            <summary>À quoi faire attention</summary>
            <div class="solution-content">
              <p>Notez les commandes que vous ne connaissiez pas et comparez avec la capsule « Commandes essentielles » de ce site. Si une manipulation diffère, c'est le cours officiel qui a raison : il est mis à jour plus souvent.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Étape 2 — le mois suivant</span>
          </div>
          <div class="exercise-body">
            <p>Suivez <strong>AI Fluency for educators</strong>, à votre rythme (une leçon par semaine suffit). Pour chaque leçon, essayez l'idée sur un vrai document de votre progression.</p>
          </div>
          <details class="exercise-solution">
            <summary>À quoi faire attention</summary>
            <div class="solution-content">
              <p>Le cadre « 4D » vous aide à décider quoi confier à l'IA, comment le lui demander, et comment vérifier le résultat. C'est le complément idéal du parcours « Communiquer avec un système d'agents IA » de ce site.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Étape 3 — quand vous êtes à l'aise</span>
          </div>
          <div class="exercise-body">
            <p>Suivez <strong>Introduction to agent skills</strong>, puis créez votre premier skill avec la capsule « Créer un skill » du parcours Avancé.</p>
          </div>
          <details class="exercise-solution">
            <summary>À quoi faire attention</summary>
            <div class="solution-content">
              <p>Choisissez une tâche que vous refaites chaque semaine (une fiche d'exercices type, un barème, un compte rendu). C'est le meilleur candidat pour un premier skill.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '10 min',
    tags: ['formation', 'anthropic', 'ressources'],
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
          par exemple <code>PreToolUse</code> (avant une action), <code>PostToolUse</code> (après une action),
          <code>SessionStart</code> (au démarrage) ou <code>Stop</code> (quand Claude a fini de répondre).
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
            <a href="https://code.claude.com/docs/fr/sub-agents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Sous-agents (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/hooks-guide" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Hooks (doc en français)
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
  ├── /qcm-creator → rédiger les questions et des distracteurs
  │                  construits sur les erreurs réelles des élèves
  ├── /html-katex-compiler → créer la page web (formules KaTeX)
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
  'av-creer-skill': {
    id: 'av-creer-skill',
    title: 'Créer un skill',
    description: 'Fabriquer vos propres skills avec le skill-creator officiel d\'Anthropic, ou à partir d\'une ressource avec resource-to-skill',
    parcours: 'avance',
    order: 1,
    sections: {
      info: `
        <h3>Qu'est-ce qu'un skill ?</h3>
        <p>
          Un <strong>skill</strong> est un <strong>dossier</strong> placé dans <code>.claude/skills/</code>
          (pour un projet) ou dans <code>~/.claude/skills/</code> (pour tous vos projets)
          qui enseigne à Claude un savoir-faire spécialisé. Il s'invoque en tapant
          <code>/nom-du-skill</code> suivi de votre demande, et Claude le charge aussi tout seul
          quand votre demande correspond à sa description.
        </p>
        <h4>Structure d'un skill</h4>
        <pre style="margin: 0.75rem 0; padding: 0.75rem; background: rgba(0,0,0,0.2); border-radius: 6px; font-size: 0.85em;"><code>mon-skill/
├── SKILL.md           # Point d'entrée (obligatoire)
├── references/        # Documentation de référence
│   └── programme.md
├── scripts/           # Scripts exécutables par Claude
│   └── compiler.py
├── examples/          # Exemples de sortie attendue
│   └── fiche-type.tex
└── templates/         # Modèles à remplir
    └── modele.tex</code></pre>
        <p>Le fichier <code>SKILL.md</code> est composé de :</p>
        <ul>
          <li>
            <strong>Un en-tête YAML</strong> (entre deux lignes <code>---</code>) : le <code>name</code> du skill
            et surtout sa <code>description</code>, qui dit <em>ce qu'il fait et quand l'utiliser</em>.
            C'est elle que Claude lit pour décider de charger le skill.
          </li>
          <li>
            <strong>Un corps Markdown</strong> : les instructions que Claude suit lorsque le skill est chargé
          </li>
        </ul>
        <p>
          Les fichiers de support permettent de garder le <code>SKILL.md</code> concis (moins de 500 lignes recommandées)
          tout en donnant à Claude accès à de la documentation détaillée, des scripts et des exemples.
          Claude ne les ouvre que quand il en a besoin.
        </p>

        <h4>Deux façons de créer un skill</h4>
        <ul>
          <li>
            <strong>Le skill-creator officiel d'Anthropic</strong> : vous décrivez le savoir-faire,
            il vous pose des questions, écrit le dossier complet, puis peut le tester et l'améliorer.
            Il s'installe en une commande depuis la marketplace officielle :
            <pre><code>/plugin install skill-creator@claude-plugins-official</code></pre>
          </li>
          <li>
            <strong>Le skill <code>resource-to-skill</code></strong> (fourni avec le setup de ce site) :
            vous lui donnez une <em>ressource</em> (un PDF, une vidéo, une page web, un dossier de code)
            et il en tire un skill opérationnel, avec ses références et ses scripts, puis un rapport
            de relecture. Pratique pour « capitaliser » une méthode trouvée en ligne.
          </li>
        </ul>
        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>Pour aller plus loin :</strong> le cours officiel gratuit <em>Introduction to agent skills</em>
          (en anglais) explique en détail comment Claude choisit et charge un skill.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Formation et documentation officielles</span>
          <div class="doc-links-buttons">
            <a href="https://anthropic.skilljar.com/introduction-to-agent-skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Introduction to agent skills (gratuit, en anglais)
            </a>
            <a href="https://code.claude.com/docs/fr/skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills (doc en français)
            </a>
            <a href="https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Le plugin skill-creator
            </a>
            <a href="https://github.com/anthropics/skills" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Skills d'exemple d'Anthropic
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Anatomie d'un SKILL.md</h3>
        <p>Voici un exemple complet de skill pour générer des exercices de mathématiques :</p>
        <pre><code>---
name: exercices-maths
description: Génère une série d'exercices de mathématiques progressifs
  avec corrigés, du collège au lycée. Utiliser dès que l'utilisateur
  demande des exercices, une fiche d'entraînement ou des applications
  directes sur une notion, même sans dire « exercices ».
---

# Skill : exercices-maths

## Rôle
Créer une série d'exercices progressifs sur une notion donnée,
adaptés au niveau précisé, avec corrigés détaillés.

## Prérequis (étape 0)
Avant de générer les exercices, invoquer le skill /programmes-officiels
pour récupérer les attendus officiels du niveau et du thème donnés.

## Structure de sortie
1. Titre et niveau
2. Exercice 1 — facile (avec exemple résolu)
3. Exercice 2 — intermédiaire
4. Exercice 3 — difficile (avec coup de pouce)
5. Corrigés complets

## Règles
- Utiliser le vouvoiement
- Varier les types de questions (calcul, problème, QCM)
- Inclure un encadré « Je retiens » avec la définition clé
- Vérifier chaque résultat numérique avant de l'écrire

## Format de sortie
LaTeX si le niveau est collège ou lycée, Markdown sinon.
Voir examples/fiche-type.tex pour la mise en page attendue.</code></pre>
        <p>
          Ce skill s'invoque avec : <code>/exercices-maths crée des exercices sur Pythagore pour la 4ème</code>.
          Grâce à sa description, Claude le chargera aussi tout seul si vous écrivez simplement
          <em>« il me faut une fiche d'entraînement sur Pythagore »</em>.
        </p>

        <h4>Partir d'une ressource avec resource-to-skill</h4>
        <pre><code>/resource-to-skill voici une vidéo sur la méthode des « problèmes ouverts »
https://www.youtube.com/watch?v=...
Fais-en un skill qui m'aide à préparer une séance de ce type.</code></pre>
        <p>
          Le skill récupère la matière (transcription, texte, captures), en extrait le savoir-faire
          et écrit un skill qui <em>fait faire</em> la méthode, au lieu d'un simple résumé.
          Il termine par une page de relecture : vous vérifiez, vous corrigez, c'est prêt.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1 : créer votre premier skill</span>
          </div>
          <div class="exercise-body">
            <p>Installez le skill-creator (une seule fois), puis décrivez un skill pour votre tâche la plus répétitive (fiches de révision, exercices d'un certain type, bilans de compétences...).</p>
            <pre><code>/plugin install skill-creator@claude-plugins-official</code></pre>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Exemple de demande : <code>/skill-creator:skill-creator crée un skill qui génère des fiches de révision pour le collège avec définitions, propriétés et exercices types</code> (ou simplement : <em>« Utilise skill-creator pour créer un skill qui… »</em>).</p>
              <p>Le skill-creator va :</p>
              <ol>
                <li>Vous poser des questions pour préciser (format, niveau, contenu...)</li>
                <li>Créer un dossier <code>.claude/skills/fiche-revision/</code> avec <code>SKILL.md</code></li>
                <li>Y écrire un en-tête YAML avec une description précise, et des instructions structurées</li>
                <li>Vous proposer de le tester sur quelques demandes et de l'améliorer</li>
              </ol>
              <p>Vérifiez le fichier généré : il doit contenir au minimum une description claire, un rôle, des étapes, des règles et un format de sortie.</p>
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
              <p>Retestez le skill modifié. L'affinage itératif est la clé : un skill s'améliore à chaque utilisation. Vous pouvez aussi demander au skill-creator : <em>« améliore le skill fiche-revision : il oublie souvent les schémas »</em>.</p>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 3 : capitaliser une ressource</span>
          </div>
          <div class="exercise-body">
            <p>Choisissez une ressource dont vous aimeriez que Claude « retienne la méthode » : un PDF de formation, une vidéo, un article de didactique. Donnez-la à <code>/resource-to-skill</code> et relisez le rapport produit.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Dans le rapport de relecture, vérifiez trois points :</p>
              <ul>
                <li><strong>La description</strong> dit-elle clairement quand utiliser le skill ?</li>
                <li><strong>Les instructions</strong> font-elles faire la méthode (étapes, critères), ou se contentent-elles de la résumer ?</li>
                <li><strong>Les références</strong> contiennent-elles ce qui sera utile plus tard (exemples, grilles, citations exactes) ?</li>
              </ul>
              <p>Corrigez ce qui ne va pas directement dans le <code>SKILL.md</code>, puis testez le skill sur une vraie demande.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '20 min',
    tags: ['skills', 'creation', 'skill-creator'],
  },
  'av-hooks': {
    id: 'av-hooks',
    title: 'Hooks et automatisations',
    description: 'Automatiser des tâches avec les hooks Claude',
    parcours: 'avance',
    order: 2,
    sections: {
      info: `
        <h3>Les hooks : des scripts déclenchés automatiquement</h3>
        <p>
          Les <strong>hooks</strong> sont des scripts shell qui s'exécutent automatiquement
          lorsque Claude effectue certaines actions. Ils éliminent les tâches manuelles
          répétitives en les déclenchant sans intervention de votre part.
        </p>
        <p>Chaque hook est rattaché à un <strong>événement</strong>. Il en existe une trentaine ; voici les plus utiles :</p>
        <ul>
          <li>
            <strong>PreToolUse</strong> : s'exécute <em>avant</em> qu'un outil soit utilisé.
            Utile pour valider, préparer ou bloquer une action selon des conditions.
          </li>
          <li>
            <strong>PostToolUse</strong> : s'exécute <em>après</em> qu'un outil a été utilisé.
            Utile pour transformer le résultat, déclencher une compilation, corriger un fichier.
          </li>
          <li>
            <strong>UserPromptSubmit</strong> : s'exécute quand vous envoyez un message, avant que Claude le lise.
            Utile pour ajouter automatiquement un rappel ou un contexte.
          </li>
          <li>
            <strong>SessionStart</strong> / <strong>SessionEnd</strong> : au début et à la fin d'une session.
            Utile pour charger un état, faire un rappel, nettoyer.
          </li>
          <li>
            <strong>Stop</strong> : quand Claude a fini de répondre (et <strong>SubagentStop</strong> pour un sous-agent).
            Utile pour lancer une vérification finale.
          </li>
          <li>
            <strong>Notification</strong> : quand Claude Code veut attirer votre attention (permission à accorder, attente).
          </li>
          <li>
            <strong>PreCompact</strong> : juste avant que la conversation soit compactée.
          </li>
        </ul>
        <p>
          La plupart des hooks lancent une <strong>commande</strong> (type <code>command</code>). Il existe aussi
          des hooks qui interrogent un modèle (<code>prompt</code>), un sous-agent (<code>agent</code>),
          une adresse web (<code>http</code>) ou un outil MCP (<code>mcp_tool</code>).
        </p>
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
            <a href="https://code.claude.com/docs/fr/hooks-guide" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Guide des hooks (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/hooks" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Référence des hooks (doc en français)
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
            "command": "python .claude/scripts/fix-encoding.py"
          }
        ]
      }
    ]
  }
}</code></pre>
        <p>Chaque hook est défini par trois éléments :</p>
        <ul>
          <li><strong>matcher</strong> : l'outil ciblé (ex. <code>Write</code>, <code>Edit</code>, ou une regex comme <code>Write|Edit</code>)</li>
          <li><strong>type</strong> : <code>"command"</code> pour lancer un script (le cas le plus courant)</li>
          <li><strong>command</strong> : la commande à exécuter. Le script reçoit sur son entrée standard un petit texte JSON qui décrit l'action, dont le chemin du fichier modifié (<code>tool_input.file_path</code>).</li>
        </ul>
        <p>Pour vérifier vos hooks, tapez <code>/hooks</code> dans une session : la liste des hooks actifs s'affiche.</p>
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
    "PreToolUse": [
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
                <li><strong>Hooks existants</strong> : si vous avez déjà des hooks dans votre <code>settings.json</code>, ajoutez cette entrée dans le tableau existant <code>PreToolUse</code> plutôt que d'en créer un nouveau.</li>
                <li><strong>Pourquoi PreToolUse ?</strong> Le son doit retentir <em>au moment</em> où Claude pose sa question, donc avant l'outil <code>AskUserQuestion</code>. Pour être aussi prévenu quand Claude attend une permission, ajoutez le même son sur l'événement <code>Notification</code>.</li>
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
    order: 3,
    sections: {
      info: `
        <h3>Les écosystèmes de partage</h3>
        <p>
          Les fournisseurs de CLI proposent désormais des <strong>marketplaces</strong>
          et registres pour partager et découvrir des skills, plugins et extensions.
          Ce n'est plus limité au copier-coller de fichiers.
        </p>
        <h4>Claude Code — plugins et marketplaces</h4>
        <ul>
          <li><strong>Plugin</strong> : un paquet qui regroupe des skills, des agents, des hooks et des serveurs MCP, installable d'une seule commande</li>
          <li><strong>Marketplace officielle</strong> : <code>claude-plugins-official</code>, déjà connue de Claude Code. Tapez <code>/plugin</code> pour ouvrir l'onglet <strong>Découvrir</strong> et chercher en tapant, ou installez directement avec <code>/plugin install nom@claude-plugins-official</code></li>
          <li><strong>Autres marketplaces</strong> : n'importe quel dépôt GitHub peut en être une. On l'ajoute une fois avec <code>/plugin marketplace add propriétaire/dépôt</code> (exemple : <code>anthropics/skills</code>, les skills d'exemple d'Anthropic)</li>
          <li><strong>Catalogue en ligne</strong> : <a href="https://claude.com/marketplace" target="_blank" rel="noopener noreferrer">claude.com/marketplace</a></li>
          <li><strong>Standard ouvert</strong> : format Agent Skills (SKILL.md), lu aussi par d'autres outils comme Codex</li>
          <li><strong>Documentation</strong> : <a href="https://code.claude.com/docs/fr/discover-plugins" target="_blank" rel="noopener noreferrer">installer des plugins (doc en français)</a> · <a href="https://code.claude.com/docs/fr/plugins" target="_blank" rel="noopener noreferrer">créer et publier un plugin</a></li>
        </ul>
        <h4>Et chez les autres ?</h4>
        <p>
          <a href="https://learn.chatgpt.com/docs" target="_blank" rel="noopener noreferrer">Codex</a> (OpenAI) et
          <a href="https://antigravity.google/" target="_blank" rel="noopener noreferrer">Antigravity</a> (Google)
          ont aussi leurs skills, plugins ou extensions. Un skill au format SKILL.md se réutilise
          souvent tel quel ou presque : consultez leur documentation pour savoir où le ranger.
        </p>
        <p style="font-size: 0.9em; color: #94a3b8;">
          Des registres communautaires de skills existent aussi. Leur contenu n'est pas vérifié :
          lisez un skill (et ses scripts) avant de l'installer, comme vous le feriez pour un logiciel.
        </p>
        <h4>Le partage classique reste valide</h4>
        <p>
          Vous pouvez toujours partager via <strong>Git</strong> (committez <code>.claude/</code>),
          <strong>ZIP</strong> (comme sur ce site), ou un <strong>dépôt dédié</strong>.
        </p>
      `,
      exemple: `
        <h3>Installer un plugin depuis une marketplace</h3>
        <p>Exemple avec Claude Code :</p>
        <pre><code># Parcourir les plugins disponibles (onglet Découvrir, recherche en tapant)
/plugin

# Installer le skill-creator officiel d'Anthropic
/plugin install skill-creator@claude-plugins-official

# Ajouter la marketplace des skills d'exemple d'Anthropic, puis installer
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills</code></pre>
        <p>
          Avant d'installer, la fiche du plugin indique ce qu'il ajoute (skills, agents, hooks…)
          et vous demande une <strong>portée</strong> : pour vous dans tous vos projets, pour tout le
          projet, ou pour vous dans ce projet seulement.
        </p>
        <p>
          Le format <strong>SKILL.md</strong> est un standard ouvert : un skill écrit pour
          Claude Code peut être réutilisé avec Codex (et inversement).
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1 : explorer un catalogue</span>
          </div>
          <div class="exercise-body">
            <p>Tapez <code>/plugin</code> dans Claude Code (onglet Découvrir), ou parcourez le <a href="https://claude.com/marketplace" target="_blank" rel="noopener noreferrer">catalogue en ligne</a> ou le dépôt <a href="https://github.com/anthropics/skills" target="_blank" rel="noopener noreferrer">anthropics/skills</a>.</p>
            <p>Identifiez 2 plugins ou skills qui vous seraient utiles. Installez-en un et testez-le.</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir la solution</summary>
            <div class="solution-content">
              <p>Dans l'onglet Découvrir, tapez des mots-clés liés à votre usage. Pour un enseignant de maths, des pistes intéressantes :</p>
              <ul>
                <li><strong>document-skills</strong> (marketplace <code>anthropic-agent-skills</code>) : lire et produire des fichiers Word, Excel, PowerPoint et PDF</li>
                <li><strong>skill-creator</strong> (marketplace officielle) : créer et améliorer vos propres skills</li>
                <li><strong>math-proof</strong> ou <strong>math-olympiad</strong> (marketplace officielle) : à tester pour la rédaction de démonstrations</li>
              </ul>
              <p>Pour installer : <code>/plugin install nom@marketplace</code> puis testez avec une demande concrète. Si le skill ne correspond pas exactement à vos besoins, utilisez-le comme base et créez votre propre version avec le skill-creator (capsule « Créer un skill »).</p>
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
2. /qcm-creator — Rédige des QCM avec des distracteurs tirés des erreurs d'élèves
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
    order: 4,
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
          <strong>Rappel choix de modèle :</strong> l'agent principal est en Opus (aujourd'hui Opus 5.5, planification).
          Les sous-agents de production sont en Sonnet (Sonnet 5.5, rapport qualité/coût optimal).
          Les tâches répétitives simples passent en Haiku (Haiku 5.5) avec des instructions très détaillées.
          Fable 5.1, plus puissant et plus cher, se réserve aux chantiers les plus difficiles.
          Dans la définition d'un agent, il suffit d'écrire <code>model: sonnet</code> ou <code>model: haiku</code> :
          Claude Code choisit la dernière version.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/fr/sub-agents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Sous-agents (doc en français)
            </a>
            <a href="https://anthropic.skilljar.com/introduction-to-subagents" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : Introduction to subagents (en anglais)
            </a>
          </div>
        </div>
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

  'av-chantier': {
    id: 'av-chantier',
    title: 'Mener un grand chantier',
    description: 'Cadrer un projet trop gros pour une seule conversation : cahier des charges avec specs-creator, carte sur plusieurs sessions avec wayfinder, décisions avec grill-me',
    parcours: 'avance',
    order: 5,
    sections: {
      info: `
        <h3>Quand un projet dépasse une conversation</h3>
        <p>
          Une fiche d'exercices tient dans une conversation. Une <strong>application pour vos élèves</strong>,
          une <strong>progression annuelle complète</strong> ou un <strong>paquet de documents pour toute
          une équipe</strong>, non : il faudra plusieurs sessions, et chaque nouvelle session repart
          sans mémoire de la précédente.
        </p>
        <p>
          Le risque : l'IA invente ce que vous n'avez pas précisé, change d'avis d'une session à l'autre,
          et vous découvrez au bout de trois soirées qu'elle a construit autre chose que ce que vous vouliez.
          La parade : <strong>écrire les décisions avant de construire</strong>. Trois skills du setup
          partagé s'en chargent.
        </p>

        <h4>Les trois outils</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.85rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 8px;">
            <strong style="color: #c4b5fd;">specs-creator — le cahier des charges</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.88em;">
              Fabrique en grande partie seul un <strong>dossier de spécifications</strong> : vision, usages,
              fonctionnement, critères de réussite, journal des décisions, plan de construction, et un
              <code>CLAUDE.md</code> qui indexe le tout. Il enquête et décide seul les détails ;
              il ne vous fait trancher que l'essentiel.
            </p>
          </div>
          <div style="padding: 0.85rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <strong style="color: #93c5fd;">wayfinder — la carte sur plusieurs sessions</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.88em;">
              Pour un chantier vraiment gros, il dessine une <strong>carte</strong> : la destination,
              puis une série de <strong>tickets de décision</strong> (une question à trancher par ticket,
              de la taille d'une session). Chaque session lit la carte, règle un ticket, met la carte à jour.
            </p>
          </div>
          <div style="padding: 0.85rem; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 8px;">
            <strong style="color: #fbbf24;">grill-me — trancher</strong>
            <p style="margin: 0.5rem 0 0; color: #d1d5db; font-size: 0.88em;">
              L'interview par manches de questions à choix, avec une recommandation pour chacune
              (voir la capsule « Se faire interviewer avant d'agir »). specs-creator et wayfinder
              l'appellent dès qu'une décision vous revient.
            </p>
          </div>
        </div>
        <p>
          <strong>En bonus : <code>domain-modeling</code>.</strong> Sur un projet qui dure, les mots
          dérivent (« séance », « activité », « chapitre » finissent par désigner la même chose, ou pas).
          Ce skill tient un glossaire (<code>CONTEXT.md</code>) et un registre des décisions importantes,
          pour que chaque session parle la même langue.
        </p>

        <h4>Lequel choisir ?</h4>
        <ul>
          <li><strong>Projet de taille moyenne</strong> (une petite application, un paquet de ressources) : <code>specs-creator</code> seul suffit.</li>
          <li><strong>Projet flou et très gros</strong> (plusieurs semaines, beaucoup d'inconnues) : <code>wayfinder</code> d'abord pour éclaircir la route, puis <code>specs-creator</code> pour le cahier des charges final.</li>
          <li><strong>Une seule décision à prendre</strong> : <code>grill-me</code> directement.</li>
        </ul>
        <p style="padding: 0.75rem 1rem; background: rgba(245,158,11,0.08); border-radius: 8px; border-left: 3px solid rgba(245,158,11,0.4); font-size: 0.95em;">
          <strong>Ce n'est jamais nécessaire</strong> pour les travaux d'enseignement courants : cours,
          fiches, évaluations se font très bien en une conversation, avec un bon pré-plan.
          Ces outils servent quand vous construisez quelque chose qui durera.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://code.claude.com/docs/fr/best-practices" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Bonnes pratiques (doc en français)
            </a>
            <a href="https://code.claude.com/docs/fr/common-workflows" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Reprendre une conversation, mode plan (doc en français)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Exemple : une application de révision pour vos élèves</h3>
        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <pre style="margin: 0; font-size: 0.82em; background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: 6px; color: #d1d5db;"><code>/specs-creator Je voudrais une petite application web
où mes élèves de 2de révisent les automatismes de calcul :
des séries courtes, une correction immédiate, et un bilan
que je peux consulter.</code></pre>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.88em; color: #d1d5db;">
              <p style="margin: 0 0 0.5rem;">J'ai fait le tour des points techniques et choisi seul ce qui est secondaire (thème, format des séries, stockage local). Trois décisions vous reviennent :</p>
              <p style="margin: 0 0 0.25rem;"><strong>Q1 — Comptes élèves :</strong> A) pas de compte, un code de classe (recommandé : aucune donnée personnelle) / B) un compte par élève</p>
              <p style="margin: 0 0 0.25rem;"><strong>Q2 — Hébergement :</strong> A) une page à ouvrir dans le navigateur, sans serveur (recommandé) / B) un site en ligne</p>
              <p style="margin: 0;"><strong>Q3 — Bilan professeur :</strong> A) export d'un fichier à importer (recommandé) / B) tableau de bord en ligne</p>
            </div>
          </div>
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03); border-top: 1px solid rgba(255,255,255,0.05);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.88em; color: #d1d5db;">
              <p style="margin: 0 0 0.5rem;">Dossier écrit :</p>
              <pre style="margin: 0; font-size: 0.85em; background: rgba(0,0,0,0.3); padding: 0.6rem; border-radius: 6px;"><code>specs/
  CLAUDE.md              → index, à lire en premier
  01-vision.md
  02-usages.md           → l'élève, le professeur, un jour type
  03-fonctionnel.md
  04-technique.md
  05-criteres.md         → ce qui prouve que c'est fini
  06-decisions.md        → les 3 décisions et leurs raisons
  07-plan.md             → étapes de construction</code></pre>
            </div>
          </div>
        </div>
        <p>
          Dans une nouvelle session (ou avec un sous-agent), il suffit ensuite de dire :
          <em>« Lis specs/CLAUDE.md et construis l'étape 1 du plan. »</em>
          L'agent repart des décisions écrites, pas de votre mémoire.
        </p>
        <h4>Et avec wayfinder</h4>
        <p>
          Pour un chantier plus flou (par exemple « refondre toute ma progression de 2de avec des
          supports Typst »), <code>/wayfinder</code> écrit d'abord la <strong>destination</strong>,
          puis des tickets comme « Quel découpage en chapitres ? », « Quel format pour les fiches
          d'exercices ? ». Vous en réglez un par session ; la carte garde la liste des décisions prises.
        </p>
      `,
      pratique: `
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 1 : choisir le bon outil</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque projet, indiquez l'outil le plus adapté : une conversation normale, <code>grill-me</code>, <code>specs-creator</code> ou <code>wayfinder</code>.</p>
            <ol>
              <li>Une évaluation de 4e sur les fractions</li>
              <li>Hésiter entre deux formats pour vos fiches de révision</li>
              <li>Une petite application de QCM chronométrés pour la classe</li>
              <li>Construire, sur l'année, une banque de ressources partagée avec votre équipe</li>
            </ol>
          </div>
          <details class="exercise-solution">
            <summary>Voir une proposition</summary>
            <div class="solution-content">
              <ol>
                <li><strong>Conversation normale</strong> : un document, une session, avec un bon pré-plan.</li>
                <li><strong>grill-me</strong> : une seule décision ; les questions à choix vous aident à trancher.</li>
                <li><strong>specs-creator</strong> : projet de taille moyenne, qu'un agent pourra construire ensuite en une ou deux sessions.</li>
                <li><strong>wayfinder</strong> puis <strong>specs-creator</strong> : beaucoup d'inconnues, plusieurs semaines, plusieurs personnes. La carte évite de tout redécider à chaque session. <code>domain-modeling</code> aide à fixer le vocabulaire commun.</li>
              </ol>
            </div>
          </details>
        </div>
        <div class="exercise-card">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice 2 : votre premier dossier de specs</span>
          </div>
          <div class="exercise-body">
            <p>Pensez à un outil que vous aimeriez avoir (une page de révision, un générateur de fiches, un tableau de suivi). Lancez <code>/specs-creator</code> en le décrivant en trois ou quatre phrases. Répondez aux questions, puis lisez le fichier des décisions.</p>
          </div>
          <details class="exercise-solution">
            <summary>Ce que vous devez observer</summary>
            <div class="solution-content">
              <ul>
                <li>L'IA vous pose <strong>peu de questions</strong> : seulement celles qui changent vraiment le résultat.</li>
                <li>Chaque question arrive avec des <strong>options et une recommandation</strong>.</li>
                <li>Le journal des décisions dit <strong>pourquoi</strong> chaque choix a été fait : dans trois mois, vous saurez encore pourquoi.</li>
                <li>Le plan de construction découpe le travail en étapes qu'un agent peut réaliser une par une.</li>
              </ul>
            </div>
          </details>
        </div>
      `,
    },
    duration: '15 min',
    tags: ['specs', 'wayfinder', 'grill-me', 'projet'],
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
        <div class="doc-links">
          <span class="doc-links-label">Formations et guides officiels</span>
          <div class="doc-links-buttons">
            <a href="https://anthropic.skilljar.com/ai-fluency-framework-foundations" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : AI Fluency (gratuit, en anglais)
            </a>
            <a href="https://anthropic.skilljar.com/ai-fluency-for-educators" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              AI Fluency for educators (enseignants)
            </a>
            <a href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Bonnes pratiques de prompt (en anglais)
            </a>
          </div>
        </div>
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
        <h3>À vous de structurer</h3>
        <p>
          Prenez une demande que vous feriez vraiment cette semaine et réécrivez-la avec les
          quatre titres de la capsule : <code># Rôle</code>, <code># Contexte</code>,
          <code># Tâche</code>, <code># Format</code>. Envoyez les deux versions (brute et structurée)
          dans deux conversations séparées et comparez.
        </p>

        <div class="exercise-card" style="margin-top: 1.5rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
            <span style="font-weight: 600; color: white;">Structurer une demande brute</span>
          </div>
          <div class="exercise-body">
            <p>Réécrivez cette demande en Markdown structuré :</p>
            <p><em>« Fais-moi des exercices sur les pourcentages pour ma classe, avec la correction. »</em></p>
          </div>
          <details class="exercise-solution">
            <summary>Voir une proposition</summary>
            <div class="solution-content">
              <pre><code># Rôle
Tu es professeur de mathématiques en collège.

# Contexte
Classe de 4ème, fin du chapitre sur la proportionnalité.
Les élèves savent calculer un pourcentage simple ;
ils confondent encore augmentation et coefficient multiplicateur.

# Tâche
Rédige 5 exercices progressifs sur les pourcentages :
- 2 calculs directs (appliquer un taux)
- 2 situations d'évolution (hausse, baisse)
- 1 problème en contexte (soldes successifs)

# Format
- Fichier LaTeX, énoncés numérotés
- Correction détaillée après chaque exercice
- Une page maximum pour les énoncés</code></pre>
              <p>Le contexte (« ils confondent encore… ») est souvent la ligne qui change le plus le résultat : l'IA construit alors des exercices qui travaillent cette difficulté précise.</p>
            </div>
          </details>
        </div>

        <h4 style="margin-top: 1.5rem;">Auto-vérification</h4>
        <p>Après avoir testé, vérifiez :</p>
        <ul>
          <li>✅ La réponse à la version structurée respecte-t-elle le format demandé (type de fichier, structure) ?</li>
          <li>✅ Le niveau et la difficulté visée sont-ils respectés ?</li>
          <li>✅ Avez-vous eu besoin de moins d'allers-retours qu'avec la version brute ?</li>
          <li>✅ Le contenu mathématique est-il juste ? (à vérifier dans tous les cas)</li>
        </ul>
        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          <strong>Et si vous ne savez pas quoi mettre dans le contexte ?</strong> Laissez l'IA
          vous interviewer : c'est l'objet de la capsule « Se faire interviewer avant d'agir »
          (skill <code>grill-me</code>).
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
    order: 7,
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
          Les noms et versions de modèles changent très fréquemment. Ce qui compte, c'est le <strong>principe des niveaux</strong>.
          Pour repère, en octobre 2026 : <strong>Haiku 5.5</strong>, <strong>Sonnet 5.5</strong>, <strong>Opus 5.5</strong> et <strong>Fable 5.1</strong>.
          La liste à jour est sur la <a href="https://platform.claude.com/docs/en/about-claude/models/overview" target="_blank" rel="noopener noreferrer">page officielle des modèles</a>.
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
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(168,85,247,0.15); color: #d8b4fe; font-size: 0.8em; margin-right: 0.25rem;">Opus</span>
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(236,72,153,0.15); color: #f9a8d4; font-size: 0.8em;">Fable</span>
              </td>
              <td style="padding: 0.75rem; color: #9ca3af;">4 niveaux distincts (Haiku, Sonnet, Opus, Fable) + un réglage d'effort (<code>/effort</code>) et le mot-clé « ultrathink » pour réfléchir plus longtemps</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.75rem; font-weight: 600; color: #d1d5db;">OpenAI (GPT / Codex)</td>
              <td style="padding: 0.75rem; color: #d1d5db;">
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(255,255,255,0.1); color: #d1d5db; font-size: 0.8em;">Modèle principal</span>
              </td>
              <td style="padding: 0.75rem; color: #9ca3af;">Un modèle principal avec différents modes de réflexion (thinking tokens)</td>
            </tr>
            <tr>
              <td style="padding: 0.75rem; font-weight: 600; color: #d1d5db;">Google (Gemini, dans Antigravity)</td>
              <td style="padding: 0.75rem; color: #d1d5db;">
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(255,255,255,0.1); color: #d1d5db; font-size: 0.8em; margin-right: 0.25rem;">Flash / Preview</span>
                <span style="display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; background: rgba(255,255,255,0.1); color: #d1d5db; font-size: 0.8em;">Pro</span>
              </td>
              <td style="padding: 0.75rem; color: #9ca3af;">Versions rapides (Flash/Preview) et version complète (Pro)</td>
            </tr>
          </table>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>L'avantage Claude :</strong> 4 niveaux de modèle = un levier majeur
          d'optimisation. Vous choisissez la puissance en fonction de la tâche, pas l'inverse.
          Dans Claude Code, la commande <code>/model</code> change de modèle en cours de session.
        </p>

        <h4>La règle : adapter la puissance à la tâche</h4>
        <p>Le piège, c'est de toujours utiliser le modèle le plus puissant. Pourquoi ?</p>
        <ul>
          <li><strong>Coût</strong> (tarifs de l'API, octobre 2026) : Opus 5.5 coûte environ 2 fois plus cher que Sonnet 5.5 et une quarantaine de fois plus cher que Haiku 5.5 ; Fable 5.1 coûte 2,5 fois Opus. Avec un abonnement, ce coût se traduit en limites d'usage atteintes plus ou moins vite.</li>
          <li><strong>Sur-interprétation :</strong> un modèle très puissant peut <em>surtraiter</em> une demande simple. Demandez à un philosophe un rapport succinct : il fera 3 pages avec des nuances là où vous vouliez 5 lignes.</li>
          <li><strong>Vitesse :</strong> Haiku répond en quelques secondes. Opus et surtout Fable peuvent réfléchir une à plusieurs minutes sur une tâche complexe.</li>
        </ul>

        <h4>Guide de choix</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 0.75rem; margin: 1rem 0;">
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
              <li>Modèle par défaut de Claude Code, recommandé par Anthropic pour la plupart des usages</li>
            </ul>
          </div>
          <div style="padding: 0.75rem; background: rgba(236,72,153,0.08); border: 1px solid rgba(236,72,153,0.2); border-radius: 8px;">
            <strong style="color: #f9a8d4; font-size: 0.9em;">Fable — le chercheur</strong>
            <ul style="margin: 0.5rem 0 0; padding-left: 1rem; color: #9ca3af; font-size: 0.8em;">
              <li>Problèmes très difficiles</li>
              <li>Longs chantiers autonomes</li>
              <li>Quand Opus, même à effort élevé, ne suffit pas</li>
              <li>Le plus lent et le plus cher : à choisir explicitement</li>
            </ul>
          </div>
        </div>

        <h4>Régler la réflexion : effort et ultrathink</h4>
        <p>
          Les modèles récents réfléchissent toujours un peu avant de répondre. Dans Claude Code, la commande
          <code>/effort</code> règle la profondeur de cette réflexion pour toute la session
          (de <code>low</code> à <code>max</code>). Le mot <strong>ultrathink</strong> glissé dans un message
          la pousse plus loin pour ce message seulement.
          C'est utile pour les tâches qui nécessitent une planification fine ou un raisonnement complexe.
          À éviter pour les demandes simples : c'est comme demander à un architecte de dessiner
          un plan pour accrocher un tableau.
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Documentation officielle</span>
          <div class="doc-links-buttons">
            <a href="https://platform.claude.com/docs/en/about-claude/models/overview" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Les modèles Claude (en anglais)
            </a>
            <a href="https://platform.claude.com/docs/en/about-claude/pricing" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Tarifs de l'API (en anglais)
            </a>
            <a href="https://code.claude.com/docs/fr/model-config" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Choisir le modèle et l'effort dans Claude Code (doc en français)
            </a>
          </div>
        </div>
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
              <p><strong>2. B) Sonnet</strong> — Production standard de contenu pédagogique : Sonnet s'en sort très bien pour deux fois moins cher qu'Opus. Opus, modèle par défaut de Claude Code, fera un peu mieux sur la progression des exercices : c'est un arbitrage coût / finesse.</p>
              <p><strong>3. C) Opus</strong> — Architecture multi-agents = raisonnement complexe et planification. C'est le terrain d'Opus (Fable seulement si Opus échoue).</p>
              <p><strong>4. A) Haiku</strong> — Tâche répétitive et simple. 20 reformulations = beaucoup de tokens. Haiku sera une vingtaine de fois moins cher que Sonnet et suffisamment bon.</p>
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
    order: 2,
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
          à l'aide. L'agent <code>debug-tex-log</code> par exemple est un expert des erreurs de compilation LaTeX :
          il prend le fichier qui plante, cherche la cause et renvoie la correction à faire.
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
              <td style="padding: 0.5rem;"><code>/bfcours-typst</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Cours et fiches en Typst avec la suite farfadet</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/latex-geometry</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Figures de géométrie TikZ</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/qcm-creator</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">QCM avec distracteurs tirés des erreurs d'élèves</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 0.5rem;"><code>/programmes-officiels</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Extraire les compétences du BO</td>
            </tr>
            <tr>
              <td style="padding: 0.5rem;"><code>/grill-me</code></td>
              <td style="padding: 0.5rem; color: #d1d5db;">Se faire interviewer pour préciser une demande</td>
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

  'pc-grill-me': {
    id: 'pc-grill-me',
    title: 'Se faire interviewer avant d\'agir',
    description: 'Quand votre demande est trop vague, laisser l\'IA vous interviewer par questions à choix avant de produire',
    parcours: 'prompt-craft',
    order: 3,
    sections: {
      info: `
        <h3>Le réflexe qui change tout : se faire interviewer</h3>
        <p>
          Vous avez une idée, mais elle est floue. « Fais-moi un truc sur les fractions »,
          « j'aimerais une activité sympa pour les 4ème »... L'IA peut exécuter ça, mais
          le résultat sera <em>aussi flou que votre demande</em> : elle comblera les trous à votre place.
        </p>
        <p>
          La solution : avant de produire quoi que ce soit, demander à l'IA de
          <strong>vous poser des questions</strong> jusqu'à ce que vous soyez d'accord sur tout.
          C'est le rôle du skill <code>grill-me</code>, fourni avec le setup de ce site.
        </p>

        <h4>Comment ça marche</h4>
        <ul>
          <li>
            <strong>Votre demande devient un arbre de décisions.</strong> Certaines se tranchent tout de suite
            (le niveau, le format) ; d'autres dépendent des premières (le nombre d'exercices dépend du format).
          </li>
          <li>
            <strong>L'IA pose les questions par manches.</strong> À chaque manche, toutes les questions
            qu'on peut poser maintenant ; celles qui dépendent d'une réponse attendent la manche suivante.
          </li>
          <li>
            <strong>Chaque question propose des options concrètes et une recommandation argumentée.</strong>
            Vous cliquez, ou vous répondez librement.
          </li>
          <li>
            <strong>Elle cherche elle-même les faits.</strong> Ce qu'elle peut vérifier (vos fichiers, votre
            progression, le programme), elle le vérifie au lieu de vous le demander. Vous ne tranchez que
            les vraies décisions.
          </li>
          <li>
            <strong>À la fin, un récapitulatif</strong> d'une ligne par décision, et elle attend votre
            confirmation avant d'agir.
          </li>
        </ul>

        <h4>Deux façons de répondre</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin: 1rem 0;">
          <div style="padding: 0.75rem; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); border-radius: 8px;">
            <strong style="color: #93c5fd; font-size: 0.9em;">Dans le terminal</strong>
            <p style="margin: 0.5rem 0 0; color: #9ca3af; font-size: 0.85em;">Des questions à choix s'affichent directement dans Claude Code ; on répond avec les flèches.</p>
          </div>
          <div style="padding: 0.75rem; background: rgba(139,92,246,0.08); border: 1px solid rgba(139,92,246,0.2); border-radius: 8px;">
            <strong style="color: #c4b5fd; font-size: 0.9em;">Sur une page web</strong>
            <p style="margin: 0.5rem 0 0; color: #9ca3af; font-size: 0.85em;">Toute la manche s'ouvre dans le navigateur : on clique, on peut <strong>dicter</strong> ses commentaires au micro, puis « Copier les réponses » et coller dans la conversation.</p>
          </div>
        </div>

        <h4>Quand l'utiliser</h4>
        <ul>
          <li>Votre demande est vague : « fais-moi quelque chose sur les équations »</li>
          <li>Vous avez une idée mais pas de plan : « j'aimerais une séquence originale »</li>
          <li>Avant de lancer une tâche complexe impliquant plusieurs skills</li>
          <li>Quand vous voulez <strong>préciser votre propre pensée</strong> : l'IA vous sert de miroir</li>
        </ul>
        <p>
          Il suffit de taper <code>/grill-me</code> suivi de votre idée, ou d'écrire
          <em>« pose-moi des questions avant de te lancer »</em>.
        </p>

        <p style="padding: 0.75rem 1rem; background: rgba(139,92,246,0.08); border-radius: 8px; border-left: 3px solid rgba(139,92,246,0.4); font-size: 0.95em;">
          <strong>Sans le setup ?</strong> Le principe marche avec n'importe quelle IA. Terminez votre demande par :
          <em>« Avant de produire quoi que ce soit, pose-moi tes questions par séries, avec des options
          et ta recommandation pour chacune, jusqu'à ce que tout soit clair. Puis récapitule et attends mon accord. »</em>
        </p>
        <div class="doc-links">
          <span class="doc-links-label">Pour aller plus loin</span>
          <div class="doc-links-buttons">
            <a href="https://anthropic.skilljar.com/ai-fluency-framework-foundations" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Cours officiel : AI Fluency (déléguer et décrire, en anglais)
            </a>
            <a href="https://code.claude.com/docs/fr/best-practices" target="_blank" rel="noopener noreferrer" class="doc-link doc-link-anthropic">
              Bonnes pratiques Claude Code (doc en français)
            </a>
          </div>
        </div>
      `,
      exemple: `
        <h3>Un exemple concret : de « vague » à « précis »</h3>

        <div style="margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; overflow: hidden;">
          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;"><code>/grill-me</code> « J'aimerais un truc bien sur les probabilités pour mes 3ème »</p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.9em;">
              <p style="margin: 0 0 0.75rem; color: #6ee7b7; font-weight: 600;">Manche 1</p>
              <p style="margin: 0 0 0.5rem; color: #d1d5db;"><strong>Q1 — Document :</strong> <span style="color: #9ca3af;">A) Activité de découverte (recommandé si c'est une introduction) / B) Cours / C) Exercices / D) Évaluation</span></p>
              <p style="margin: 0 0 0.5rem; color: #d1d5db;"><strong>Q2 — Support :</strong> <span style="color: #9ca3af;">A) LaTeX imprimable (recommandé : vos autres documents sont en LaTeX) / B) Diaporama / C) Page interactive</span></p>
              <p style="margin: 0; color: #d1d5db;"><strong>Q3 — Moment :</strong> <span style="color: #9ca3af;">A) Introduction / B) Milieu de séquence / C) Révision</span></p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(99,102,241,0.08);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #a5b4fc; flex-shrink: 0;">U</div>
            <div style="flex: 1;">
              <p style="margin: 0; color: #d1d5db;">« A, A, A. Ils n'ont jamais vu les probas. »</p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.9em;">
              <p style="margin: 0 0 0.75rem; color: #6ee7b7; font-weight: 600;">Manche 2 (débloquée par vos réponses)</p>
              <p style="margin: 0 0 0.5rem; color: #d1d5db;"><strong>Q4 — Expérience :</strong> <span style="color: #9ca3af;">A) Lancers de dés réels en binômes (recommandé : manipuler avant de formaliser) / B) Simulation sur tableur</span></p>
              <p style="margin: 0; color: #d1d5db;"><strong>Q5 — Durée :</strong> <span style="color: #9ca3af;">A) Une séance de 55 min (recommandé) / B) Deux séances</span></p>
            </div>
          </div>

          <div style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 1rem; background: rgba(255,255,255,0.03); border-top: 1px solid rgba(255,255,255,0.05);">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(16,185,129,0.3); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; color: #6ee7b7; flex-shrink: 0;">IA</div>
            <div style="flex: 1; font-size: 0.9em;">
              <p style="margin: 0 0 0.5rem; color: #6ee7b7; font-weight: 600;">Récapitulatif — je lance si vous confirmez</p>
              <p style="margin: 0; color: #d1d5db;">Activité de découverte · LaTeX · introduction (aucun prérequis) · lancers de dés en binômes · une séance de 55 min.</p>
            </div>
          </div>
        </div>

        <p style="padding: 0.75rem 1rem; background: rgba(16,185,129,0.08); border-radius: 8px; border-left: 3px solid rgba(16,185,129,0.4); font-size: 0.95em;">
          En deux manches, « un truc bien sur les probas » est devenu
          « activité de découverte en LaTeX pour introduire les probabilités en 3ème, une séance,
          avec une vraie expérience de lancers ». L'IA sait exactement quoi produire, et vous aussi.
        </p>
      `,
      pratique: `
        <h3>Testez par vous-même</h3>
        <p>
          Si vous avez le setup de ce site, tapez <code>/grill-me</code> suivi d'une idée encore floue
          pour votre prochaine séquence. Sinon, utilisez la phrase donnée dans l'onglet « Info »
          avec n'importe quelle IA.
        </p>

        <h4 style="margin-top: 1.5rem;">Ce que vous devez observer</h4>
        <ul>
          <li>✅ L'IA vous pose des questions <strong>avec des choix</strong> et une recommandation, pas des questions ouvertes</li>
          <li>✅ Les questions arrivent <strong>par manches</strong> : la suivante dépend de vos réponses</li>
          <li>✅ Elle ne vous demande pas ce qu'elle peut vérifier elle-même</li>
          <li>✅ Elle termine par un <strong>récapitulatif</strong> et attend votre accord</li>
          <li>✅ Vous découvrez des aspects auxquels vous n'aviez <strong>pas pensé</strong></li>
        </ul>

        <div class="exercise-card" style="margin-top: 1.5rem;">
          <div class="exercise-header">
            <span class="exercise-badge">Exercice</span>
            <span style="font-weight: 600; color: white;">Anticiper les questions</span>
          </div>
          <div class="exercise-body">
            <p>Pour chaque demande, listez les questions qu'une bonne interview vous poserait :</p>
            <p><strong>1.</strong> « Fais-moi un cours sur Thalès »</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Questions attendues : ...</p>
            <p><strong>2.</strong> « Crée un exercice de calcul littéral en LaTeX pour mes 4ème, 6 questions progressives avec correction »</p>
            <p style="color: #9ca3af; font-size: 0.85em;">Questions attendues : ...</p>
          </div>
          <details class="exercise-solution">
            <summary>Voir les réponses</summary>
            <div class="solution-content">
              <p><strong>1.</strong> Presque tout reste à décider : <em>quel niveau</em> (3ème ? 2de ?), <em>quel format</em> (LaTeX, diaporama ?), <em>quelle longueur</em>, <em>quel moment</em> de la séquence (découverte ou institutionnalisation ?), <em>quelles exigences</em> du programme. Seul le thème est fixé.</p>
              <p><strong>2.</strong> Beaucoup mieux ! Il reste surtout le <em>moment</em> (application directe ou révision ?) et le <em>contenu</em> (simple ou double distributivité ? factorisation ?). Une seule manche suffira.</p>
            </div>
          </details>
        </div>
      `,
    },
    duration: '~8 min',
    tags: ['clarification', 'grill-me', 'questions'],
  },

  'pc-preplan': {
    id: 'pc-preplan',
    title: 'Co-construire un pré-plan interactif',
    description: 'Faire produire un plan annotable avant la production finale pour un résultat optimal',
    parcours: 'prompt-craft',
    order: 4,
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
    order: 5,
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
            <div style="font-size: 0.65em; color: #9ca3af;">Grill-me</div>
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
