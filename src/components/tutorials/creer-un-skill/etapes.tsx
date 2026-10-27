'use client'

import type { ReactNode } from 'react'
import Link from 'next/link'
import { AlertTriangle, Info, Lightbulb } from 'lucide-react'
import { SkillPackCard, SkillPackInstall } from '@/components/skills/SkillPackPanel'
import { CodeBlock } from '@/components/ui/code-block'
import { SKILL_PACKS } from '@/data/ai-packages'
import { cn } from '@/lib/utils'
import { PromptACopier } from './PromptACopier'

/**
 * Contenu du tutoriel « Créer son propre skill avec skill-creator ».
 * Fil conducteur : faire écrire à l'agent un skill qui rédige des cours « comme le prof »,
 * à partir d'un cours déjà fait dont il extrait les principes.
 *
 * Sources vérifiées (octobre 2026) :
 * - skill-creator : plugin du catalogue officiel d'Anthropic (anthropics/claude-plugins-official,
 *   plugins/skill-creator) ; installation et vérification d'après
 *   https://code.claude.com/docs/en/discover-plugins ;
 * - Codex : skill système $skill-creator, d'après https://learn.chatgpt.com/docs/build-skills ;
 * - grill-me : SKILL.md publié dans public/download/Claude-Code-Setup/claude-setup/skills/grill-me/.
 */

export type CouleurEtape = 'emerald' | 'sky' | 'amber' | 'violet' | 'teal' | 'slate'

export interface EtapeTuto {
  id: string
  titre: string
  /** Une phrase : ce que l'on fait à cette étape */
  resume: string
  /** Durée indicative */
  duree: string
  couleur: CouleurEtape
  contenu: ReactNode
}

/* ---------- Petits blocs de mise en page ---------- */

function Sous({ children }: { children: ReactNode }) {
  return <h3 className="text-lg font-semibold text-white mt-8 mb-3 first:mt-0">{children}</h3>
}

function P({ children }: { children: ReactNode }) {
  return <p className="text-sm text-white/70 leading-relaxed my-2">{children}</p>
}

function Liste({ items, ordonnee = false }: { items: ReactNode[]; ordonnee?: boolean }) {
  const Tag = ordonnee ? 'ol' : 'ul'
  return (
    <Tag className={cn('text-sm text-white/70 space-y-1.5 my-2 ml-5', ordonnee ? 'list-decimal' : 'list-disc')}>
      {items.map((it, i) => <li key={i} className="pl-1">{it}</li>)}
    </Tag>
  )
}

function Encadre({ type, titre, children }: { type: 'info' | 'attention' | 'astuce'; titre: string; children: ReactNode }) {
  const styles = {
    info: { cls: 'border-sky-500/30 bg-sky-950/20', icone: Info, couleur: 'text-sky-300' },
    attention: { cls: 'border-amber-500/30 bg-amber-950/20', icone: AlertTriangle, couleur: 'text-amber-300' },
    astuce: { cls: 'border-emerald-500/30 bg-emerald-950/20', icone: Lightbulb, couleur: 'text-emerald-300' },
  }[type]
  const Icone = styles.icone
  return (
    <div className={cn('rounded-lg border p-4 my-4', styles.cls)}>
      <div className={cn('flex items-center gap-2 font-semibold text-sm mb-1', styles.couleur)}>
        <Icone className="w-4 h-4" /> {titre}
      </div>
      <div className="text-sm text-white/70 leading-relaxed space-y-2">{children}</div>
    </div>
  )
}

function C({ children }: { children: ReactNode }) {
  return <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-[0.85em]">{children}</code>
}

function Lien({ href, children }: { href: string; children: ReactNode }) {
  const externe = href.startsWith('http')
  return externe ? (
    <a href={href} target="_blank" rel="noopener noreferrer" className="underline text-cosmic-300 hover:text-cosmic-200">{children}</a>
  ) : (
    <Link href={href} className="underline text-cosmic-300 hover:text-cosmic-200">{children}</Link>
  )
}

/* ---------- Les prompts ---------- */

const PROMPT_DEMANDE = `Je veux créer un skill avec skill-creator, mais pas tout de suite : commence par une séance grill-me pour préciser l'idée avec moi.

L'idée
Un skill qui rédige mes cours de [matière] en [niveaux] comme je les rédige moi-même : je lui dis « le cours sur [une notion] » et il produit un document prêt à relire, dans mon format habituel ([LaTeX / Word / Typst / Markdown]).

Ma façon de faire habituelle
- [Comment j'ouvre un chapitre : activité, problème, rappel…]
- [L'ordre des blocs : définitions, propriétés, exemples, méthodes, exercices…]
- [Le niveau de détail, le ton, ce que j'écris toujours ou jamais]
- [Ma mise en forme : encadrés, couleurs, longueur]

Mon cours modèle
[modeles/mon-cours-modele.tex] : lis-le en entier. C'est la référence dont le skill doit tirer ses principes (structure, ton, mise en forme, niveau d'exigence). Il ne doit pas le recopier : il doit savoir en écrire d'autres du même genre.

La séance grill-me
- Interroge-moi sur ce que le skill doit faire et ne pas faire, ce qu'il reçoit (ma demande, des documents), ce qu'il produit (format, fichiers, emplacement) et les principes à retenir de mon cours.
- Ce que tu peux lire dans mon cours, cherche-le toi-même au lieu de me le demander.
- Termine par un récapitulatif, une ligne par décision, et attends ma validation.

Ensuite seulement
Utilise skill-creator pour écrire le skill dans .claude/skills/[nom-du-skill]/ de ce projet, à partir des décisions validées. Range les principes détaillés dans references/ pour garder le SKILL.md court.`

const PROMPT_PRESENTER = `Présente-moi le skill [nom-du-skill] en moins de 15 lignes :
- sa description (quand il se déclenche) ;
- ce qu'il fait, étape par étape ;
- les principes qu'il a retenus de mon cours modèle ;
- ce qu'il me demandera avant d'agir ;
- la liste de ses fichiers.
Signale tout ce que tu as dû deviner faute d'information.`

const PROMPT_TEST = `/[nom-du-skill] Rédige le cours sur [la notion de mon cours modèle] pour [niveau].
Pour ce test, n'ouvre ni mon cours modèle ni sa copie éventuelle dans le dossier du skill : appuie-toi seulement sur les consignes du skill.
Enregistre le résultat dans essais/[notion]-essai-1.[extension].`

const PROMPT_COMPARER = `Compare essais/[notion]-essai-1.[extension] à mon vrai cours [modeles/mon-cours-modele.tex].
Fais un tableau : structure, ordre des notions, ton et vocabulaire, mise en forme, exemples, exercices, exactitude, niveau d'exigence.
Pour chaque écart, dis s'il vient d'une consigne absente, floue ou mal suivie dans le skill, et propose la correction du skill (avant / après).
N'applique rien avant mon accord.`

const PROMPT_CORRIGER = `Applique au skill [nom-du-skill] les corrections [1, 3 et 4]. Pour la [2] : [ma précision].
Puis refais le même test dans essais/[notion]-essai-2.[extension] et dis-moi ce qui a changé.`

const PROMPT_TEST_2 = `/[nom-du-skill] Rédige le cours sur [une autre notion que je connais bien] pour [niveau].
Ensuite, dis-moi ce qui t'a manqué dans le skill pour la traiter : consignes trop liées à mon cours modèle, cas non prévus, choix que tu as dû faire seul.`

const PROMPT_AUTO = `Ajoute au skill [nom-du-skill] un mécanisme d'amélioration continue :

1. Crée dans son dossier un fichier retours.md : un journal daté de mes remarques et préférences, une ligne par remarque, avec un statut (à traiter, intégré, écarté).
2. Dans SKILL.md, ajoute la consigne de lire retours.md au début de chaque usage et d'appliquer les préférences qui y figurent.
3. À la fin de chaque usage, me demander en une seule question si quelque chose est à corriger, puis noter ma réponse dans retours.md.
4. Quand une remarque revient, ou quand je dis « intègre-la », me proposer la modification précise du SKILL.md (avant / après). Ne l'appliquer qu'après mon accord, puis passer la ligne en « intégré ».
5. Avant toute modification du SKILL.md, en garder une copie datée dans le dossier sauvegardes/ du skill, sous le nom SKILL-AAAA-MM-JJ.md.

Garde le SKILL.md court : les préférences de détail restent dans retours.md. Montre-moi le résultat avant de l'enregistrer.`

const PROMPT_USAGE = `/[nom-du-skill] Le cours sur [notion] pour [niveau], [contrainte éventuelle : deux pages, avec activité d'introduction…].`

const PROMPT_REMARQUE = `Remarque pour le skill [nom-du-skill] : [ce qui ne va pas, et ce que j'aurais voulu]. Note-la dans retours.md.`

const PROMPT_BILAN = `Relis retours.md du skill [nom-du-skill] : quelles remarques reviennent ? Propose les modifications du SKILL.md correspondantes (avant / après), sans rien appliquer avant mon accord.`

const PROMPT_SAUVEGARDE = `Fais une copie de secours du dossier .claude/skills/[nom-du-skill]/ dans sauvegardes-skills/[nom-du-skill]-[AAAA-MM-JJ]/, à la racine du projet (hors de .claude/skills/).`

const PROMPT_RESTAURER = `Le skill [nom-du-skill] marchait mieux avant. Montre-moi ce qui diffère entre la version actuelle et sauvegardes-skills/[nom-du-skill]-[AAAA-MM-JJ]/, puis remets l'ancienne version si je confirme.`

/* ---------- Les six étapes ---------- */

const PACK_GRILL_ME = SKILL_PACKS.find(p => p.id === 'skill-grill-me')

const PREREQUIS_GRILL_ME = [
  {
    texte: 'Claude Code (ou Codex). Le mode terminal de grill-me utilise les questions à choix de Claude Code ; avec Codex, choisissez la page web.',
    lien: { href: '/claude-code/tutorials/claude-code-install', label: 'Installer Claude Code' },
  },
  {
    texte: 'Python 3, seulement pour le mode page web (aucun module à installer).',
    lien: { href: '/claude-code/tutorials/python-install', label: 'Installer Python' },
  },
  { texte: 'Chrome ou Edge pour la dictée vocale de la page web (facultatif ; sinon Win + H sous Windows).' },
  {
    texte: 'Vous avez déjà le bundle Généraliste, LaTeX Enseignant ou Power User ? grill-me y est : rien à installer.',
    lien: { href: '/claude-code/download-ai-packages', label: 'Les bundles' },
  },
]

export const ETAPES: EtapeTuto[] = [
  {
    id: 'preparer',
    titre: 'Préparer',
    resume: 'Réunir les trois ingrédients : skill-creator, grill-me et un cours modèle.',
    duree: '10 min',
    couleur: 'emerald',
    contenu: (
      <>
        <P>
          Avant de commencer, il vous faut trois choses : <strong className="text-white">skill-creator</strong>, qui écrit
          le skill ; <strong className="text-white">grill-me</strong>, qui vous interviewe d&apos;abord ; et{' '}
          <strong className="text-white">un de vos cours</strong>, qui servira de modèle.
        </P>

        <Sous>1. skill-creator, fourni par Anthropic</Sous>
        <Encadre type="info" titre="Il n'est pas dans le pack de ce site">
          <p>
            skill-creator est fourni et maintenu par Anthropic, l&apos;éditeur de Claude. Il s&apos;installe depuis le
            catalogue officiel de Claude Code et se met à jour tout seul.
          </p>
        </Encadre>
        <P>
          <strong className="text-white">Vérifier s&apos;il est déjà là.</strong> Dans Claude Code, tapez <C>/</C> puis{' '}
          <C>skill-creator</C> : si <C>/skill-creator:skill-creator</C> apparaît dans la liste, passez à la suite.
        </P>
        <P><strong className="text-white">Sinon, l&apos;installer</strong>, dans une session Claude Code :</P>
        <CodeBlock code="/plugin install skill-creator@claude-plugins-official" language="text" filename="Dans Claude Code" />
        <Liste
          ordonnee
          items={[
            'Claude Code ouvre la fiche du plugin : lisez ce qu\'il ajoute.',
            'Choisissez la portée : pour vous, dans tous vos projets (« Install for you »), ou seulement dans ce projet (« Install for you, in this repo only »).',
            <>Si le message final demande <C>/reload-plugins</C>, tapez-le (ou relancez Claude Code).</>,
          ]}
        />
        <Encadre type="astuce" titre="Si l'installation ne trouve pas le catalogue">
          <p>
            Claude Code ajoute le catalogue officiel d&apos;Anthropic au premier lancement dans un terminal. S&apos;il
            manque (première installation par script, extension VS Code), ajoutez-le puis relancez l&apos;installation :
          </p>
          <CodeBlock code="/plugin marketplace add anthropics/claude-plugins-official" language="text" filename="Dans Claude Code" />
          <p>
            Avec <strong className="text-white">Codex</strong>, rien à installer : <C>$skill-creator</C> fait partie des
            skills intégrés. Sources :{' '}
            <Lien href="https://code.claude.com/docs/en/discover-plugins">documentation Claude Code</Lien>,{' '}
            <Lien href="https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator">le plugin skill-creator</Lien>,{' '}
            <Lien href="https://learn.chatgpt.com/docs/build-skills">documentation Codex</Lien>.
          </p>
        </Encadre>

        <Sous>2. grill-me, depuis ce site</Sous>
        <P>
          grill-me est le seul skill à télécharger ici. Ajoutez son pack au panier, téléchargez l&apos;archive, puis
          décompressez-la dans le dossier de votre projet.
        </P>
        {PACK_GRILL_ME && (
          <div className="space-y-4 my-4">
            <SkillPackCard pack={PACK_GRILL_ME} />
            <SkillPackInstall pack={PACK_GRILL_ME} prerequis={PREREQUIS_GRILL_ME} />
          </div>
        )}
        <P>
          Pour vérifier : relancez <C>claude</C> dans le projet et tapez <C>/grill-me</C>. Pour découvrir le skill seul,
          voyez la capsule <Lien href="/claude-code/tutorials/parcours/prompt-craft/pc-grill-me">Se faire interroger par l&apos;IA</Lien>.
        </P>

        <Sous>3. Un cours modèle</Sous>
        <Liste
          items={[
            'Un cours dont vous êtes content et qui ressemble à ce que vous faites d\'habitude.',
            'Le fichier source (.tex, .docx, .typ, .md) plutôt que le PDF : l\'agent y lit aussi votre mise en forme.',
            'Sans nom d\'élève ni information personnelle.',
            <>Copiez-le dans le projet, par exemple <C>modeles/mon-cours-modele.tex</C>.</>,
          ]}
        />
        <P>
          Notez aussi, en quatre ou cinq lignes, votre façon habituelle de procéder : comment vous ouvrez un chapitre,
          l&apos;ordre des blocs, ce que vous écrivez toujours ou jamais. Vous les collerez dans la demande de l&apos;étape 2.
        </P>
      </>
    ),
  },
  {
    id: 'interview',
    titre: 'Se faire interviewer',
    resume: 'Demander le skill, en exigeant d\'abord une séance grill-me pour préciser l\'idée.',
    duree: '15 à 30 min',
    couleur: 'sky',
    contenu: (
      <>
        <P>
          Ouvrez Claude Code dans le dossier du projet, puis collez cette demande après avoir remplacé les passages{' '}
          <mark className="bg-amber-400/20 text-amber-200 rounded px-0.5">[entre crochets]</mark>.
        </P>
        <PromptACopier titre="Demander le skill, interview d'abord" texte={PROMPT_DEMANDE} />

        <Sous>Ce qui va se passer</Sous>
        <Liste
          ordonnee
          items={[
            'L\'agent vous demande où poser les questions : dans le terminal, ou sur une page web cliquable avec dictée vocale.',
            'Il lit votre cours modèle et y relève lui-même ce qu\'il peut y voir.',
            'Il pose une première manche : toutes les questions qu\'il peut poser maintenant, chacune avec deux à quatre options et sa recommandation.',
            'Vous répondez en cliquant, ou librement. Vos réponses débloquent la manche suivante.',
            'Quand plus rien n\'est implicite, il affiche un récapitulatif, une ligne par décision. Vous corrigez, puis vous validez.',
            'Alors seulement, skill-creator écrit le skill (étape 3).',
          ]}
        />

        <Sous>Exemples de questions</Sous>
        <div className="grid gap-3 md:grid-cols-3 my-3">
          {[
            { q: 'Que reçoit le skill ?', o: ['Le titre de la notion seulement (recommandé)', 'Une fiche du programme', 'Un ancien cours à reprendre'] },
            { q: 'Que doit-il produire ?', o: ['Le cours seul (recommandé)', 'Cours + fiche d\'exercices', 'Cours + version élève à trous'] },
            { q: 'Votre cours ouvre sur une activité : à garder ?', o: ['Toujours (recommandé)', 'Seulement en début de chapitre', 'Jamais'] },
          ].map(({ q, o }) => (
            <div key={q} className="rounded-lg border border-sky-500/30 bg-sky-950/20 p-3 text-sm">
              <div className="font-semibold text-sky-200 mb-2">{q}</div>
              <ul className="space-y-1 text-white/70">
                {o.map((x, i) => (
                  <li key={x} className={cn('rounded px-2 py-1', i === 0 ? 'bg-sky-500/20 text-white' : 'bg-white/5')}>{x}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <Sous>Pourquoi ça change la qualité</Sous>
        <Liste
          items={[
            'Un skill vaut ce que valent ses consignes. Sans interview, l\'agent comble vos choix implicites par des choix moyens.',
            'L\'interview transforme vos habitudes en règles écrites : l\'ordre des blocs, le niveau de détail, ce que vous ne faites jamais.',
            'Chaque question arrive avec une recommandation : vous validez plus que vous ne rédigez.',
            'Le récapitulatif final est le cahier des charges du skill. Vous le relisez avant qu\'une ligne soit écrite.',
          ]}
        />
        <Encadre type="astuce" titre="Pour bien répondre">
          <p>Répondez court. « Comme dans mon cours » est une bonne réponse. Dites aussi ce que vous refusez.</p>
          <p>Vous hésitez ? « Je ne sais pas, propose » : l&apos;agent tranchera et le notera dans le récapitulatif.</p>
        </Encadre>
      </>
    ),
  },
  {
    id: 'ecrire',
    titre: 'Laisser écrire le skill',
    resume: 'skill-creator écrit le dossier du skill ; vous le relisez en cinq minutes.',
    duree: '10 min',
    couleur: 'amber',
    contenu: (
      <>
        <P>
          Après votre validation, skill-creator écrit le skill dans le dossier indiqué. Un skill est un simple dossier :
        </P>
        <pre className="rounded-lg bg-slate-950/60 border border-white/10 p-4 text-sm text-slate-200 overflow-x-auto my-3">{`.claude/skills/[nom-du-skill]/
├── SKILL.md        la fiche : quand l'utiliser, comment faire
├── references/     les principes détaillés, des exemples
├── assets/         un gabarit de document (si utile)
└── scripts/        seulement pour une tâche répétée à l'identique`}</pre>
        <Liste
          items={[
            <><strong className="text-white">SKILL.md</strong> commence par un nom et une <strong className="text-white">description</strong>. C&apos;est la description que l&apos;agent lit pour décider d&apos;utiliser le skill : elle doit citer vos vraies façons de demander.</>,
            <>Le corps de SKILL.md donne la marche à suivre. skill-creator le garde sous 500 lignes et renvoie le détail vers <C>references/</C>.</>,
            <>Seul le dossier du skill compte. Les autres fichiers du projet (votre cours, vos essais) n&apos;en font pas partie.</>,
          ]}
        />
        <Encadre type="info" titre="skill-creator propose souvent des tests">
          <p>
            Il peut lancer des essais avec et sans le skill, puis ouvrir une page pour les comparer. Vous pouvez accepter
            ou passer : l&apos;étape 4 propose un test plus simple. Ces essais sont rangés dans un dossier{' '}
            <C>[nom-du-skill]-workspace/</C>, à supprimer ensuite.
          </p>
        </Encadre>

        <Sous>Le relire en cinq minutes</Sous>
        <PromptACopier titre="Se faire présenter le skill" texte={PROMPT_PRESENTER} />
        <Liste
          items={[
            'La description se déclencherait-elle sur vos demandes réelles (« le cours sur les fractions », « mon chapitre 3 ») ?',
            'Retrouvez-vous les principes de votre cours, et vos décisions de l\'interview ?',
            'Rien d\'inventé que vous n\'auriez pas dit ?',
            'Aucune information personnelle, si vous comptez le partager ?',
          ]}
        />
        <Encadre type="astuce" titre="Le skill n'apparaît pas ?">
          <p>
            Tapez <C>/</C> puis le nom du skill. S&apos;il n&apos;apparaît pas, quittez Claude Code (<C>/exit</C>) et
            relancez <C>claude</C> dans le même dossier.
          </p>
        </Encadre>
      </>
    ),
  },
  {
    id: 'tester',
    titre: 'Tester sur un cas connu',
    resume: 'Faire refaire votre cours modèle, comparer au vrai, corriger le skill.',
    duree: '20 min',
    couleur: 'violet',
    contenu: (
      <>
        <P>
          Le meilleur test : un cours dont vous connaissez déjà la bonne réponse, le vôtre. On demande au skill de le
          refaire sans le regarder, puis on compare.
        </P>
        <PromptACopier titre="1. Refaire le cours modèle" texte={PROMPT_TEST} />
        <PromptACopier titre="2. Comparer au vrai" texte={PROMPT_COMPARER} className="mt-4" />

        <Sous>Quoi regarder</Sous>
        <div className="overflow-x-auto my-3">
          <table className="w-full text-sm text-white/70 border-collapse">
            <thead>
              <tr className="text-left text-white">
                <th className="border-b border-white/10 py-2 pr-4">Critère</th>
                <th className="border-b border-white/10 py-2">La question à se poser</th>
              </tr>
            </thead>
            <tbody>
              {[
                ['Structure', 'Les mêmes blocs, dans le même ordre ?'],
                ['Ton et vocabulaire', 'Les mots du programme, votre façon de vous adresser aux élèves ?'],
                ['Mise en forme', 'Vos encadrés, vos couleurs, votre longueur ?'],
                ['Exactitude', 'Définitions et propriétés justes, exemples corrects ?'],
                ['Exigence', 'Le niveau de difficulté de vos exemples et exercices ?'],
                ['Copie', 'Le contenu est-il nouveau, ou recopié de votre cours ?'],
              ].map(([c, q]) => (
                <tr key={c}>
                  <td className="border-b border-white/5 py-2 pr-4 font-medium text-white/85 whitespace-nowrap">{c}</td>
                  <td className="border-b border-white/5 py-2">{q}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Sous>Demander les corrections</Sous>
        <Encadre type="attention" titre="Corriger le skill, pas le document">
          <p>
            Retoucher l&apos;essai ne sert à rien pour la suite. Ce qu&apos;il faut corriger, ce sont les consignes du
            skill : la prochaine fois, il fera juste du premier coup.
          </p>
        </Encadre>
        <PromptACopier titre="3. Corriger le skill et refaire le test" texte={PROMPT_CORRIGER} />
        <P>
          Quand l&apos;essai vous convient, vérifiez qu&apos;il ne sait pas faire que votre cours : testez une autre
          notion que vous connaissez bien.
        </P>
        <PromptACopier titre="4. Une autre notion" texte={PROMPT_TEST_2} />
      </>
    ),
  },
  {
    id: 'ameliorer',
    titre: 'Le rendre auto-améliorable',
    resume: 'Ajouter au skill un journal de vos retours, relu à chaque usage.',
    duree: '5 min',
    couleur: 'teal',
    contenu: (
      <>
        <P>
          Un skill n&apos;est jamais fini du premier coup. Plutôt que de le corriger de mémoire, on lui donne un carnet :
          il note vos remarques, les relit à chaque usage, et vous propose de mettre à jour ses consignes quand une
          remarque revient.
        </P>
        <PromptACopier titre="Ajouter le mécanisme d'amélioration" texte={PROMPT_AUTO} />

        <Sous>Comment il fonctionnera</Sous>
        <div className="grid gap-2 sm:grid-cols-5 my-3 text-sm">
          {[
            ['Usage', 'Il relit retours.md, puis rédige.'],
            ['Question', '« Quelque chose à corriger ? »'],
            ['Journal', 'Votre remarque est notée, datée.'],
            ['Proposition', 'Une remarque revient : avant / après du SKILL.md.'],
            ['Accord', 'Vous validez ; une sauvegarde est faite avant.'],
          ].map(([t, d], i) => (
            <div key={t} className="rounded-lg border border-teal-500/30 bg-teal-950/20 p-3">
              <div className="font-semibold text-teal-200">{i + 1}. {t}</div>
              <div className="text-white/65 mt-1">{d}</div>
            </div>
          ))}
        </div>
        <P>Un extrait de journal, après quelques semaines :</P>
        <pre className="rounded-lg bg-slate-950/60 border border-white/10 p-4 text-sm text-slate-200 overflow-x-auto whitespace-pre-wrap my-3">{`- 2026-11-04 · Pas de « on » dans les définitions, toujours « nous ». · intégré
- 2026-11-12 · Exemples avec des nombres simples avant les décimaux. · intégré
- 2026-11-20 · Ajouter une méthode « je vérifie » après chaque propriété. · à traiter`}</pre>
        <Encadre type="info" titre="Vous gardez la main">
          <p>
            Le skill ne modifie jamais ses consignes seul : il propose, vous décidez. Les petites préférences restent
            dans le journal ; seules les règles durables montent dans SKILL.md, qui reste court.
          </p>
        </Encadre>
      </>
    ),
  },
  {
    id: 'quotidien',
    titre: 'L\'utiliser au jour le jour',
    resume: 'Demander, relire, signaler ; le skill s\'affine au fil des cours.',
    duree: 'au fil de l\'année',
    couleur: 'slate',
    contenu: (
      <>
        <Sous>La routine</Sous>
        <Liste
          ordonnee
          items={[
            'Demander, en une phrase.',
            'Relire le cours produit : l\'exactitude mathématique reste votre affaire.',
            'Signaler ce qui ne va pas, à la question finale ou à tout moment.',
            'De temps en temps, faire le bilan du journal et valider les mises à jour proposées.',
          ]}
        />
        <PromptACopier titre="Demander un cours" texte={PROMPT_USAGE} />
        <PromptACopier titre="Signaler un défaut" texte={PROMPT_REMARQUE} className="mt-4" />
        <PromptACopier titre="Faire le bilan du journal" texte={PROMPT_BILAN} className="mt-4" />

        <Sous>Les signes qu&apos;il faut le retoucher</Sous>
        <Liste
          items={[
            'Vous corrigez deux fois la même chose dans des cours différents.',
            'Il ne se déclenche pas quand vous le demandez, ou se déclenche hors de propos : c\'est sa description qu\'il faut revoir.',
            'Il recopie votre cours modèle au lieu d\'en écrire un nouveau.',
            'SKILL.md dépasse quelques centaines de lignes : demandez de ranger le détail dans references/.',
          ]}
        />
        <P>
          Pour une retouche plus large, repassez par skill-creator : « améliore le skill [nom-du-skill] : [ce qui ne va
          pas] ».
        </P>

        <Sous>Garder une version de secours</Sous>
        <P>Avant une grosse modification, ou quand le skill vous donne entière satisfaction :</P>
        <PromptACopier titre="Sauvegarder" texte={PROMPT_SAUVEGARDE} />
        <Encadre type="attention" titre="Jamais dans .claude/skills/">
          <p>
            Une copie rangée dans <C>.claude/skills/</C> serait chargée comme un second skill, au même nom : l&apos;agent
            ne saurait plus lequel utiliser.
          </p>
        </Encadre>
        <PromptACopier titre="Revenir en arrière" texte={PROMPT_RESTAURER} />
        <P>
          Pour partager votre skill avec un collègue, voyez la capsule{' '}
          <Lien href="/claude-code/tutorials/parcours/avance/av-share">Partager sa configuration</Lien>.
        </P>
      </>
    ),
  },
]
