# Métriques, score et décision de garder ou d'annuler un batch

À lire aux **Étapes 3, 5 et 7** du SKILL.md : lecture du JSON de `page_metrics.py`, comparaison entre deux versions, choix de garder, d'insister ou d'annuler.

---

## Seuils de référence (rendu à 80-100 DPI)

| Métrique | Valeur | Lecture |
|---|---|---|
| `fill_mean` | 0,10 – 0,18 | Densité saine bfcours, pas d'urgence |
| `fill_mean` | > 0,28 | Document chargé : aérer un cours, tolérable sur des énoncés denses |
| `fill_mean` | < 0,08 | Très aéré : candidat à la densification latérale |
| `density_imbalance` | > 0,40 | Mise en page hétérogène : quelques pages déséquilibrent l'ensemble |
| `sparse_tail = true` et `last_page_fill_ratio` < 0,10 | — | Dernière page quasi vide : **cas le plus fréquent** |
| Page intermédiaire `is_sparse = true` et `widow_hint = true` | — | Bloc poussé sur la page suivante : souvent gagnable par colonnage de l'EXO précédent |
| `is_dense = true` ou `fill_ratio` > 0,55 | — | Page déjà noire : ne plus compacter (voir D5 dans `figures-et-defauts.md`) |
| `low_dpi_images` non vide | — | Image raster floue à l'impression (voir D7 dans `figures-et-defauts.md`) |

**Une dernière page sous-remplie se répare rarement sur la dernière page elle-même.** Remonter en amont pour trouver l'énoncé d'EXO qui prend trop de hauteur faute de colonnage, ou le `\Needspace` surdimensionné qui pousse un bloc (D6 dans `pagination-et-bandeaux.md`).

---

## Score composite

Pénalise les défauts les plus visibles (0 = parfait, négatif sinon) :

```
score = 0
score -= 0.40 * max(0, 0.10 - last_page_fill_ratio) / 0.10
score -= 0.20 * min(1.0, density_imbalance / 0.50)
score -= 0.20 * empty_pages_count
score -= 0.10 * abs(fill_mean - 0.14) / 0.14
score -= 0.10 * (1 if pages_total > target_pages else 0)
```

Une réduction du nombre total de pages **sans dégrader les autres métriques** vaut une amélioration franche, même si la formule la récompense peu.

Enregistrer dans `runs.jsonl` une ligne par version : `version`, `pages_total`, `fill_mean`, `density_imbalance`, `score`, liste des modifications du batch.

---

## Comparer une version à la précédente (Étape 5)

| Constat | Décision |
|---|---|
| `pages_total` baisse | Gain franc : conserver, planifier l'itération suivante |
| Pages égales, `density_imbalance` baisse, pas de nouvelle page vide | Gain marginal : conserver, tenter une itération de plus |
| Pages égales, métriques équivalentes | Tenter **une** itération supplémentaire (le contenu est peut-être juste sous une frontière de page) |
| Dégradation nette | Noter dans `runs.jsonl`, **ne pas annuler tout de suite** ; l'itération suivante retire les `\newpage` devenus inutiles |
| Compilation cassée | Annuler le batch entier (restaurer depuis `v{N}/`), marquer la piste épuisée |

**Mémoire des pistes** : ne jamais retenter la même modification dans la même session.

---

## Arbitrage métrique contre lisibilité

Le score ne capture pas tout. Certaines modifications améliorent nettement la lecture (concepts parallèles côte à côte, procédure en regard de son application) sans gagner de page ; d'autres gagnent une page mais cassent une logique pédagogique.

1. Gain franc (≥ 1 page) : appliquer si la règle d'or est respectée.
2. Gain marginal (`fill_mean` < +0,01, pages inchangées) : appliquer **seulement** si le rendu est jugé plus clair.
3. Score équivalent mais rendu meilleur : **conserver**, c'est un gain réel.
4. Dégradation franche (nouvelle page sparse, `density_imbalance` > +0,02) : annuler, sauf demande explicite de l'utilisateur.

Le score est un guide, pas une fin. En cas de doute sur la sémantique pédagogique, demander à l'utilisateur.

---

## Annulation différée (Étape 6)

Une modification isolée améliore rarement le score d'un document long : elle fait remonter du contenu sans franchir de frontière de page. Le gain vient de l'**effet cumulé** d'un batch, puis de la purge des `\newpage` devenus inutiles. D'où l'annulation différée :

- annuler après **2 itérations consécutives** sans gain dont au moins une dégradante ;
- ou si la compilation est cassée et impossible à corriger ;
- ou si une zone protégée a été touchée par erreur (correction, espace réponse, activité).

On restaure la **meilleure** version rencontrée (comparer les scores de `runs.jsonl`), pas forcément la précédente.

**Plafond** : 4 itérations sans demande explicite. **Convergence** : arrêter quand le plan est épuisé ou après 2 itérations sans gain mesurable.
