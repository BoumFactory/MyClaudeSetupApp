# Publication QF-Studio — zone de mise à jour

> Backend d'auto-update de l'application desktop **QF-Studio** (Tauri v2).
> Servi en statique par Vercel depuis `public/`, **totalement séparé** du
> système de téléchargement du site (panier / FileExplorer / `/api/download`).

## Arborescence d'URL — GELÉE (ne jamais changer)

Le token est **gravé dans le binaire distribué**. Le modifier casse l'updater
de tous les utilisateurs déjà installés.

```
https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/latest.json              # manifeste updater (machine)
https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/QF-Studio_<ver>_x64-setup.nsis.zip   # artefact updater
https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/QF-Studio_<ver>_x64-setup.exe        # installeur humain
https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/inputs-manifest.json     # manifeste contenu (machine)
https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/inputs-officiels-r<N>.zip            # archives de contenu
```

Dossier disque correspondant **1:1** :
`public/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/`

### Côté application Tauri (`tauri.conf.json`)

```jsonc
"plugins": {
  "updater": {
    "endpoints": ["https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/latest.json"],
    "pubkey": "<CLE_PUBLIQUE_MINISIGN>"   // la clé PRIVÉE reste sur la machine de build, jamais sur le site
  }
}
```

---

## Publier une nouvelle version de l'APPLICATION

1. **Builder** l'app signée sur la machine de build :
   `tauri build` produit dans `src-tauri/target/release/bundle/nsis/` :
   - `QF-Studio_<ver>_x64-setup.exe`
   - `QF-Studio_<ver>_x64-setup.nsis.zip`
   - `QF-Studio_<ver>_x64-setup.nsis.zip.sig`  (signature minisign)

2. **Copier** les deux premiers fichiers dans la zone :
   ```sh
   cp QF-Studio_<ver>_x64-setup.exe       "public/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/"
   cp QF-Studio_<ver>_x64-setup.nsis.zip  "public/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/"
   ```

3. **Mettre à jour `latest.json`** (même dossier) :
   - `version` → la nouvelle version (ex. `0.2.0`)
   - `pub_date` → date ISO 8601
   - `notes` → résumé des changements
   - `platforms.windows-x86_64.url` → URL du nouveau `.nsis.zip`
   - `platforms.windows-x86_64.signature` → **contenu** du fichier `.sig`
     (`cat QF-Studio_<ver>_x64-setup.nsis.zip.sig`)

4. **Mettre à jour la page humaine** (facultatif mais conseillé) :
   `src/app/claude-code/applications/logiciels/page.tsx`
   - `QFSTUDIO_VERSION` → nouvelle version
   - ajouter une entrée en tête de `QFSTUDIO_CHANGELOG`

5. **Déposer** = commit + push :
   ```sh
   git add public/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio src/app/claude-code/applications/logiciels/page.tsx
   git commit -m "QF-Studio <ver>"
   git push      # Vercel redéploie automatiquement bfcours.dev
   ```

---

## Publier une nouvelle archive de CONTENU (inputs officiels)

1. Construire `inputs-officiels-r<N>.zip` (N = numéro de release incrémenté).
2. Calculer son empreinte : `sha256sum inputs-officiels-r<N>.zip`.
3. Copier le zip dans la zone, puis mettre à jour `inputs-manifest.json` :
   - `release` → `<N>`, `updated` → date ISO
   - `archive.url` → URL du nouveau zip
   - `archive.sha256` → l'empreinte calculée
   - `archive.bytes` → taille exacte en octets (`wc -c`)
4. Commit + push (idem ci-dessus).

> L'app vérifie le `sha256` après téléchargement : **ne jamais** recompresser
> ou altérer le zip après calcul de l'empreinte.

---

## Garde-fous

- **Token GELÉ** : `7gOdepBMu5OY2QBKBcd7mGyA`. Communiqué une seule fois, jamais modifié.
- **noindex** : en-tête `X-Robots-Tag: noindex, nofollow` posé sur toute la zone
  (`next.config.js`). Le token n'est **pas** mis dans `robots.txt` (qui est public).
- **Manifestes** : servis en `application/json` + `Cache-Control: no-cache, no-store`
  (les clients voient toujours la dernière version).
- **Binaires** : servis en octets bruts par le CDN Vercel (pas de recompression des
  `.zip`/`.exe`), intégrité vérifiée côté app par sha256.
- **Clé privée de signature** : jamais déposée sur le site. Seule la clé publique
  est dans `tauri.conf.json` (embarquée dans le binaire).
- **Taille du dépôt** : les binaires sont versionnés dans git. Élaguer les anciennes
  versions de temps en temps (`git rm` des `.exe`/`.nsis.zip` obsolètes) ;
  garder au moins la version pointée par `latest.json`.
