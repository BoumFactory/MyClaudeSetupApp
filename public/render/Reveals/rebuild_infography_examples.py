#!/usr/bin/env python3
"""
Script pour reconstruire la section exemples de infography-generator-skill.html
avec toutes les infographies compressées en base64.
"""

import base64
import re
import io
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("WARNING: Pillow non installé. Images non compressées.")
    print("Installer avec: pip install Pillow")


def compress_and_encode_image(image_path: Path, quality: int = 85, max_width: int = 1200) -> tuple[str, int, int]:
    """
    Compresse une image et l'encode en base64.
    Retourne (data_uri, taille_originale, taille_compressée)
    """
    original_size = image_path.stat().st_size

    if HAS_PIL:
        # Ouvrir et redimensionner si nécessaire
        img = Image.open(image_path)

        # Convertir en RGB si nécessaire (pour JPEG)
        if img.mode in ('RGBA', 'P'):
            # Garder PNG pour les images avec transparence
            buffer = io.BytesIO()
            # Optimiser le PNG
            img.save(buffer, format='PNG', optimize=True)
            buffer.seek(0)
            b64_data = base64.b64encode(buffer.read()).decode('utf-8')
            compressed_size = len(buffer.getvalue())
            return f"data:image/png;base64,{b64_data}", original_size, compressed_size

        # Redimensionner si trop large
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Convertir en JPEG pour compression
        if img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        b64_data = base64.b64encode(buffer.read()).decode('utf-8')
        compressed_size = len(buffer.getvalue())

        return f"data:image/jpeg;base64,{b64_data}", original_size, compressed_size
    else:
        # Fallback sans compression
        with open(image_path, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode('utf-8')
        ext = image_path.suffix.lower()
        mime = {'png': 'image/png', 'jpg': 'image/jpeg'}.get(ext[1:], 'image/png')
        return f"data:{mime};base64,{b64_data}", original_size, original_size


def main():
    # Chemins
    html_file = Path(__file__).parent / "infography-generator-skill.html"
    assets_dir = Path(__file__).parent / "assets"
    mascots_dir = Path(__file__).parent.parent.parent / "download" / "Claude-Code-Setup" / ".claude" / "skills" / "infography-generator" / "assets" / "mascots"

    # Images à inclure
    images = [
        ("produit-scalaire", assets_dir / "infographie_produit_scalaire.png", "Le Produit Scalaire", "3 méthodes de calcul en une image", "#667eea"),
        ("gaia", mascots_dir / "gaia_geometrie.png", "Gaia - Géométrie", "Le monde des formes", "#3498db"),
        ("alex", mascots_dir / "alex_analyse.png", "Alex - Analyse", "Fonctions et calcul", "#27ae60"),
        ("priya", mascots_dir / "priya_probabilites.png", "Priya - Probabilités", "Hasard et statistiques", "#9b59b6"),
        ("nabil", mascots_dir / "nabil_arithmetique.png", "Nabil - Arithmétique", "Nombres et opérations", "#e67e22"),
        ("sofia", mascots_dir / "sofia_algebre.png", "Sofia - Algèbre", "Équations et variables", "#e74c3c"),
        ("sven", mascots_dir / "sven_suites.png", "Sven - Suites", "Récurrence et séries", "#1abc9c"),
    ]

    total_original = 0
    total_compressed = 0

    # Générer le HTML des slides
    slides_html = []

    # Disclaimer slide
    slides_html.append('''
        <section>
          <h2><i class="fas fa-exclamation-triangle icon" style="color: #e74c3c;"></i> Avertissement important</h2>

          <div class="warning-box" style="font-size: 0.85em;">
            <p><strong><i class="fas fa-exclamation-circle icon"></i> Contenu mathématique souvent erroné</strong></p>
            <p style="margin-top: 0.5em;">J'ai hésité à partager ces exemples car les modèles génératifs d'images <strong>manquent encore de maturité</strong> pour le contenu mathématique.</p>
          </div>

          <div class="box fragment" style="font-size: 0.85em;">
            <p><i class="fas fa-tools icon"></i> <strong>Solution :</strong> Les infographies générées doivent être <strong>relues et corrigées</strong>.</p>
            <p style="margin-top: 0.5em;">Le skill génère des prompts modifiables permettant d'itérer sur les erreurs détectées.</p>
          </div>

          <div class="example-box fragment" style="font-size: 0.8em;">
            <p><i class="fas fa-lightbulb icon"></i> <strong>Astuce :</strong> Utiliser les infographies comme <em>base de travail</em>, pas comme produit fini.</p>
          </div>

          <div class="nav-hint fragment">
            <i class="fas fa-arrow-down"></i> Voir les exemples malgré tout ↓
          </div>
        </section>''')

    # Première slide : Produit scalaire
    img_data, orig, comp = compress_and_encode_image(images[0][1])
    total_original += orig
    total_compressed += comp
    ratio = (1 - comp/orig) * 100 if orig > 0 else 0
    print(f"[{images[0][0]}] {orig/1024:.0f} Ko -> {comp/1024:.0f} Ko (-{ratio:.0f}%)")

    slides_html.append(f'''
        <section>
          <h3><i class="fas fa-star icon" style="color: #667eea;"></i> {images[0][2]}</h3>
          <p class="smaller" style="color: #666; margin-bottom: 0.5em;">{images[0][3]}</p>
          <img src="{img_data}" alt="{images[0][2]}" style="max-height: 450px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        </section>''')

    # Slides des mascottes
    for img_id, img_path, title, desc, color in images[1:]:
        img_data, orig, comp = compress_and_encode_image(img_path)
        total_original += orig
        total_compressed += comp
        ratio = (1 - comp/orig) * 100 if orig > 0 else 0
        print(f"[{img_id}] {orig/1024:.0f} Ko -> {comp/1024:.0f} Ko (-{ratio:.0f}%)")

        icons = {
            "gaia": "drafting-compass",
            "alex": "chart-line",
            "priya": "dice",
            "nabil": "calculator",
            "sofia": "superscript",
            "sven": "infinity"
        }
        icon = icons.get(img_id, "user")

        slides_html.append(f'''
        <section>
          <h3><i class="fas fa-{icon} icon" style="color: {color};"></i> {title}</h3>
          <p class="smaller" style="color: #666; margin-bottom: 0.5em;">{desc}</p>
          <img src="{img_data}" alt="{title}" style="max-height: 450px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        </section>''')

    # Nouvelle section complète
    new_section = f'''      <!-- SLIDE 5 : EXEMPLES D'INFOGRAPHIES (navigation verticale) -->
      <section>
{''.join(slides_html)}
      </section>

      <!-- SLIDE 6'''

    # Lire le fichier HTML
    html_content = html_file.read_text(encoding='utf-8')

    # Pattern pour remplacer la section exemple existante
    pattern = r'      <!-- SLIDE 5 : EXEMPLE.*?</section>\s*\n\s*<!-- SLIDE 6'

    # Remplacer
    html_content = re.sub(pattern, new_section, html_content, flags=re.DOTALL)

    # Écrire le fichier
    html_file.write_text(html_content, encoding='utf-8')

    # Stats finales
    print(f"\n{'='*50}")
    print(f"Total original:   {total_original/1024/1024:.2f} Mo")
    print(f"Total compressé:  {total_compressed/1024/1024:.2f} Mo")
    print(f"Réduction:        {(1 - total_compressed/total_original)*100:.0f}%")
    print(f"\nFichier: {html_file}")
    print(f"Taille finale: {len(html_content)/1024/1024:.2f} Mo")


if __name__ == '__main__':
    main()
