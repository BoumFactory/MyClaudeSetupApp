# Pannes concrètes

À consulter au premier échec technique, pas avant. Chaque entrée donne le
symptôme réel, la cause, et la conduite.

## Sommaire

- [Extraction vidéo](#extraction-vidéo)
- [Transcription](#transcription)
- [PDF](#pdf)
- [Web](#web)
- [Python et environnement Windows](#python-et-environnement-windows)
- [Rapport HTML](#rapport-html)

---

## Extraction vidéo

**`yt-dlp` échoue avec « Sign in to confirm you're not a bot » ou « Private video »**
YouTube exige une session. Relancer en passant les cookies du navigateur :

```bash
yt-dlp --cookies-from-browser chrome --dump-json "<url>"
```

Si l'utilisateur n'a pas la vidéo en accès libre, le dire — ne pas tourner en
rond sur des tentatives d'accès.

**`yt-dlp` échoue avec « Requested format is not available »**
Le format demandé (720p max) n'existe pas pour cette vidéo. La méthode retombe
déjà sur `b` (meilleur format disponible) ; si l'échec persiste, forcer
`--method video_youtube` après avoir ajusté le sélecteur dans
`m_video_youtube.py`.

**Aucune image extraite alors que la vidéo en contient**
La détection de changement de scène n'a rien trouvé au-dessus du seuil : c'est
typique d'une conférence filmée en plan fixe. Le complément par échantillonnage
régulier prend normalement le relais ; sinon, relancer avec `--visual deep`
(seuil abaissé à 0,18).

**Les écrans importants défilent trop vite et sont manqués**
`--visual deep` monte à 48 images. Au-delà, extraire manuellement un instant
précis repéré dans la transcription :

```bash
ffmpeg -ss 00:04:12 -i ".rts/<slug>/raw/video.mp4" -frames:v 1 -q:v 2 zoom.jpg
```

**Le téléchargement est très long**
Une vidéo d'une heure en 720p représente plusieurs centaines de mégaoctets.
Si seules les paroles comptent, `--visual off` télécharge uniquement les
sous-titres — quelques kilooctets.

## Transcription

**« Installation de faster-whisper impossible »**
Le Python du poste est en 32 bits (`Python311-32`) : `ctranslate2`, dont dépend
faster-whisper, ne publie pas de roue pour cette architecture. Trois issues, par
ordre de préférence :

1. la ressource a des sous-titres ailleurs (chaîne YouTube, fichier `.srt`
   fourni par l'utilisateur) — les utiliser ;
2. l'extraction visuelle suffit (diapos, code à l'écran) — le dire explicitement
   dans le skill produit et dans le rapport ;
3. demander à l'utilisateur une transcription, plutôt que de deviner le contenu.

Ne jamais inventer ce qui est dit dans une vidéo non transcrite.

**Transcription automatique truffée d'erreurs sur les termes techniques**
Les sous-titres automatiques transcrivent mal les noms propres et le jargon
(« LangGraph » → « lang graph », « une graphe »). Croiser systématiquement avec
les images : le terme exact est presque toujours écrit à l'écran. Le nom
correct compte : un skill qui se trompe de nom de bibliothèque est inutilisable.

## PDF

**Texte extrait vide ou dérisoire**
Le PDF est scanné. La méthode le détecte (moins de 120 caractères par page) et
rend les pages en images dans `assets/`. Les lire : c'est de la lecture d'image,
pas de l'OCR, et ça fonctionne bien — mais ça consomme du contexte, donc se
limiter aux pages qui portent la matière.

**Tableau illisible après extraction**
Le texte d'un PDF perd la structure des colonnes. Pour un tableau qui compte,
rendre la page en image et la lire :

```python
import fitz; d = fitz.open("doc.pdf"); d[11].get_pixmap(dpi=170).save("p12.png")
```

**Document de plusieurs centaines de pages**
Extraire d'abord, puis lire le sommaire dans `content.md` et ne traiter que les
sections utiles à la capacité visée. Un skill n'a pas à couvrir tout un manuel.

## Web

**`content.md` presque vide, avertissement sur JavaScript**
La page est rendue côté client. Reprendre l'URL avec l'outil `WebFetch` de
Claude, qui en obtient davantage. Si la documentation est sur GitHub, viser le
markdown source (`raw.githubusercontent.com`) plutôt que la page rendue.

**Erreur de certificat TLS**
La méthode retente déjà sans vérification. Si l'échec persiste, le site bloque
probablement l'agent : `WebFetch` reste le recours.

## Python et environnement Windows

**`UnicodeEncodeError: 'charmap' codec can't encode character`**
Toujours préfixer les appels par `PYTHONIOENCODING=utf-8`. Et ne jamais créer de
chemin contenant un accent : `ingest.py` translittère déjà les noms de dossiers
qu'il génère, mais un `--out` fourni à la main peut réintroduire le problème.

**`pip` échoue en `SSLError`**
Un certificat auto-signé se trouve dans la chaîne du poste. `pip_install()` de
`base.py` retente automatiquement avec `--trusted-host pypi.org --trusted-host
files.pythonhosted.org`. Pour une installation manuelle, reprendre ces options.

**Chemins avec espaces**
Le répertoire de travail peut contenir des espaces. Toujours
mettre les chemins entre guillemets, y compris dans les commandes qu'on écrit
dans un skill produit.

## Rapport HTML

**Rapport de plusieurs mégaoctets**
Les images sont intégrées en base64 pour que le fichier soit autonome. C'est
volontaire — il reste ouvrable sans le workspace. Pour l'alléger, régénérer
après extraction en `--visual off`, ou réduire `MAX_IMG_WIDTH` dans
`make_report.py`.

**Le navigateur ne s'ouvre pas**
Passer `--no-open` et donner le chemin du fichier à l'utilisateur. En session
distante ou sans affichage, c'est le comportement à privilégier d'emblée.
