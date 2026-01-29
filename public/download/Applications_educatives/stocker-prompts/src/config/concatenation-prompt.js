/**
 * Prompt prédéfini pour demander à une IA de concaténer les messages utilisateur
 */

export const CONCATENATION_PROMPT = `Tu es un assistant qui aide à résumer et organiser des demandes.

**Ta mission :** Analyse tous les messages que je t'ai envoyés pendant cette conversation et crée UN SEUL prompt qui résume tout ce que j'ai demandé.

**Instructions :**
1. Relis tous mes messages depuis le début de cette conversation
2. Identifie l'objectif principal de ma demande
3. Note tous les détails, précisions et modifications que j'ai apportés
4. Rédige un prompt unique et complet qui intègre tout

**Format de ta réponse :**

---
**📋 PROMPT RÉSUMÉ**

[Le prompt complet qui résume toute ma demande, prêt à être copié et réutilisé]

---

**Ce prompt doit être :**
- Autonome (compréhensible sans contexte)
- Complet (tous les détails importants)
- Clair (bien structuré)
- Réutilisable (je peux le coller dans une nouvelle conversation)`;

export const CONCATENATION_VARIANTS = [
  {
    id: 'standard',
    label: 'Standard',
    description: 'Résumé complet de la conversation',
    prompt: CONCATENATION_PROMPT
  },
  {
    id: 'court',
    label: 'Version courte',
    description: 'Résumé condensé',
    prompt: `Fais-moi un résumé très court de tout ce que je t'ai demandé dans cette conversation. Donne-moi juste le prompt essentiel en 2-3 phrases maximum.`
  },
  {
    id: 'structure',
    label: 'Version structurée',
    description: 'Avec sections claires',
    prompt: `Analyse notre conversation et crée un prompt structuré avec :
- **Contexte :** [qui je suis, ma situation]
- **Objectif :** [ce que je veux obtenir]
- **Détails :** [précisions importantes]
- **Format souhaité :** [comment je veux la réponse]

Rends ce prompt réutilisable dans une nouvelle conversation.`
  }
];
