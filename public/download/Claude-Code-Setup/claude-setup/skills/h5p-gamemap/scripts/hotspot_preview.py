#!/usr/bin/env python3
"""
Outil de prévisualisation et repositionnement interactif des hotspots sur une Game Map H5P.

Usage:
  python hotspot_preview.py --image background.png --positions positions.json [--output new_positions.json]

Fonctionnement:
  1. Affiche l'image de fond avec les hotspots positionnés
  2. Permet de déplacer les hotspots par drag & drop
  3. Quand l'utilisateur clique "Valider", sauvegarde les nouvelles positions
  4. Écrit un fichier signal pour notifier que c'est terminé

Le fichier positions.json doit avoir le format:
{
  "etapes": [
    {"title": "Étape 1", "x": 15, "y": 70},
    {"title": "Étape 2", "x": 25, "y": 45},
    ...
  ]
}
"""
import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    HAS_GUI = True
except ImportError:
    HAS_GUI = False


class HotspotPreview:
    """Interface graphique pour positionner les hotspots sur l'image de fond."""

    # Taille du hotspot (cercle)
    HOTSPOT_RADIUS = 20

    # Couleurs
    COLOR_NORMAL = "#3498db"      # Bleu
    COLOR_SELECTED = "#e74c3c"    # Rouge
    COLOR_LABEL_BG = "#2c3e50"    # Fond label
    COLOR_LABEL_FG = "#ffffff"    # Texte label

    def __init__(self, image_path: str, positions: List[Dict], output_path: str):
        self.image_path = Path(image_path)
        self.positions = positions
        self.output_path = Path(output_path)

        # État
        self.selected_index: Optional[int] = None
        self.drag_data = {"x": 0, "y": 0}
        self.hotspot_items: List[Tuple[int, int]] = []  # (circle_id, text_id)

        # Créer la fenêtre
        self.root = tk.Tk()
        self.root.title("Positionnement des Hotspots - Game Map H5P")
        self.root.protocol("WM_DELETE_WINDOW", self.on_cancel)

        # Charger l'image
        self.original_image = Image.open(self.image_path)
        self.img_width, self.img_height = self.original_image.size

        # Calculer la taille d'affichage (max 1200x800)
        self.scale = min(1200 / self.img_width, 800 / self.img_height, 1.0)
        self.display_width = int(self.img_width * self.scale)
        self.display_height = int(self.img_height * self.scale)

        # Redimensionner pour l'affichage
        display_image = self.original_image.resize(
            (self.display_width, self.display_height),
            Image.Resampling.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(display_image)

        self._setup_ui()
        self._draw_hotspots()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Instructions
        instructions = ttk.Label(
            main_frame,
            text="Glissez-déposez les hotspots pour les repositionner.\n"
                 "Les positions sont en % de l'image (0-100).",
            font=("Segoe UI", 10)
        )
        instructions.pack(pady=(0, 10))

        # Canvas pour l'image
        self.canvas = tk.Canvas(
            main_frame,
            width=self.display_width,
            height=self.display_height,
            cursor="hand2"
        )
        self.canvas.pack()

        # Afficher l'image de fond
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Bindings pour le drag & drop
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Frame pour les coordonnées en temps réel
        coord_frame = ttk.Frame(main_frame)
        coord_frame.pack(fill=tk.X, pady=10)

        self.coord_label = ttk.Label(
            coord_frame,
            text="Sélectionnez un hotspot pour voir ses coordonnées",
            font=("Consolas", 10)
        )
        self.coord_label.pack()

        # Liste des étapes avec coordonnées
        list_frame = ttk.LabelFrame(main_frame, text="Étapes", padding="5")
        list_frame.pack(fill=tk.X, pady=5)

        self.position_labels = []
        for i, pos in enumerate(self.positions):
            label = ttk.Label(
                list_frame,
                text=f"{i+1}. {pos.get('title', f'Étape {i+1}')} : x={pos['x']:.1f}%, y={pos['y']:.1f}%",
                font=("Consolas", 9)
            )
            label.pack(anchor=tk.W)
            self.position_labels.append(label)

        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="Valider",
            command=self.on_validate,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Annuler",
            command=self.on_cancel
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame,
            text="Réinitialiser",
            command=self.on_reset
        ).pack(side=tk.LEFT, padx=5)

    def _draw_hotspots(self):
        """Dessine tous les hotspots sur le canvas."""
        # Supprimer les anciens
        for circle_id, text_id in self.hotspot_items:
            self.canvas.delete(circle_id)
            self.canvas.delete(text_id)
        self.hotspot_items = []

        for i, pos in enumerate(self.positions):
            # Convertir % en pixels
            x = pos['x'] / 100 * self.display_width
            y = pos['y'] / 100 * self.display_height

            # Cercle
            r = self.HOTSPOT_RADIUS
            color = self.COLOR_SELECTED if i == self.selected_index else self.COLOR_NORMAL
            circle = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline="white", width=2,
                tags=f"hotspot_{i}"
            )

            # Numéro
            text = self.canvas.create_text(
                x, y,
                text=str(i + 1),
                fill="white",
                font=("Arial", 12, "bold"),
                tags=f"hotspot_{i}"
            )

            # Label au-dessus
            title = pos.get('title', f'Étape {i+1}')
            if len(title) > 20:
                title = title[:17] + "..."
            label = self.canvas.create_text(
                x, y - r - 15,
                text=title,
                fill=self.COLOR_LABEL_FG,
                font=("Arial", 9),
                tags=f"hotspot_{i}"
            )

            self.hotspot_items.append((circle, text))

    def _update_position_list(self):
        """Met à jour la liste des positions."""
        for i, (pos, label) in enumerate(zip(self.positions, self.position_labels)):
            text = f"{i+1}. {pos.get('title', f'Étape {i+1}')} : x={pos['x']:.1f}%, y={pos['y']:.1f}%"
            if i == self.selected_index:
                text = ">>> " + text
            label.config(text=text)

    def _find_hotspot_at(self, x: int, y: int) -> Optional[int]:
        """Trouve l'index du hotspot à la position donnée."""
        for i, pos in enumerate(self.positions):
            hx = pos['x'] / 100 * self.display_width
            hy = pos['y'] / 100 * self.display_height

            dist = ((x - hx) ** 2 + (y - hy) ** 2) ** 0.5
            if dist <= self.HOTSPOT_RADIUS:
                return i
        return None

    def on_click(self, event):
        """Gère le clic sur le canvas."""
        index = self._find_hotspot_at(event.x, event.y)

        if index is not None:
            self.selected_index = index
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self._draw_hotspots()
            self._update_position_list()

            pos = self.positions[index]
            self.coord_label.config(
                text=f"Étape {index+1} : x={pos['x']:.1f}%, y={pos['y']:.1f}%"
            )
        else:
            self.selected_index = None
            self._draw_hotspots()
            self._update_position_list()
            self.coord_label.config(text="Sélectionnez un hotspot pour voir ses coordonnées")

    def on_drag(self, event):
        """Gère le déplacement d'un hotspot."""
        if self.selected_index is None:
            return

        # Calculer le déplacement
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        # Mettre à jour la position (en %)
        pos = self.positions[self.selected_index]
        new_x = pos['x'] + (dx / self.display_width * 100)
        new_y = pos['y'] + (dy / self.display_height * 100)

        # Contraindre aux limites
        new_x = max(0, min(100, new_x))
        new_y = max(0, min(100, new_y))

        pos['x'] = new_x
        pos['y'] = new_y

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        self._draw_hotspots()
        self._update_position_list()

        self.coord_label.config(
            text=f"Étape {self.selected_index+1} : x={new_x:.1f}%, y={new_y:.1f}%"
        )

    def on_release(self, event):
        """Gère la fin du drag."""
        # Le hotspot reste sélectionné pour permettre des ajustements
        pass

    def on_validate(self):
        """Valide et sauvegarde les positions."""
        # Sauvegarder dans le fichier output
        output_data = {
            "status": "validated",
            "etapes": self.positions
        }

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        # Créer le fichier signal
        signal_file = self.output_path.with_suffix('.done')
        signal_file.write_text("OK")

        print(f"[OK] Positions sauvegardées dans : {self.output_path}")
        print(f"[OK] Signal créé : {signal_file}")

        self.root.destroy()

    def on_cancel(self):
        """Annule sans sauvegarder."""
        result = messagebox.askyesno(
            "Annuler",
            "Voulez-vous vraiment annuler sans sauvegarder ?"
        )
        if result:
            # Créer un fichier signal d'annulation
            signal_file = self.output_path.with_suffix('.cancelled')
            signal_file.write_text("CANCELLED")
            self.root.destroy()

    def on_reset(self):
        """Réinitialise les positions."""
        result = messagebox.askyesno(
            "Réinitialiser",
            "Voulez-vous réinitialiser toutes les positions ?"
        )
        if result:
            # Répartir uniformément
            n = len(self.positions)
            for i, pos in enumerate(self.positions):
                pos['x'] = 10 + (80 * i / max(n - 1, 1))
                pos['y'] = 50

            self._draw_hotspots()
            self._update_position_list()

    def run(self):
        """Lance l'interface."""
        # Centrer la fenêtre
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

        self.root.mainloop()


def extract_positions_from_preplan(preplan_path: str) -> List[Dict]:
    """Extrait les positions depuis un préplan Markdown."""
    import re

    positions = []

    with open(preplan_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern pour les étapes
    etape_pattern = r'###\s*Étape\s*\d+\s*:\s*(.+?)(?=###|\Z)'
    position_pattern = r'\*\*Position\*\*\s*:\s*x\s*=\s*([\d.]+)\s*,\s*y\s*=\s*([\d.]+)'

    for match in re.finditer(etape_pattern, content, re.DOTALL):
        title = match.group(1).strip().split('\n')[0]
        etape_content = match.group(0)

        pos_match = re.search(position_pattern, etape_content)
        if pos_match:
            x = float(pos_match.group(1))
            y = float(pos_match.group(2))
        else:
            # Position par défaut
            x = 50
            y = 50

        positions.append({
            'title': title,
            'x': x,
            'y': y
        })

    return positions


def update_preplan_positions(preplan_path: str, new_positions: List[Dict]):
    """Met à jour les positions dans un fichier préplan."""
    import re

    with open(preplan_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pour chaque position, mettre à jour
    for i, pos in enumerate(new_positions):
        # Pattern pour trouver la position de l'étape i+1
        pattern = rf'(###\s*Étape\s*{i+1}\s*:.+?\*\*Position\*\*\s*:\s*)x\s*=\s*[\d.]+\s*,\s*y\s*=\s*[\d.]+'
        replacement = rf'\1x={pos["x"]:.1f}, y={pos["y"]:.1f}'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(preplan_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Préplan mis à jour : {preplan_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Prévisualisation et repositionnement des hotspots H5P Game Map'
    )
    parser.add_argument('--image', '-i', required=True, help='Image de fond')
    parser.add_argument('--positions', '-p', required=True,
                       help='Fichier JSON des positions OU fichier préplan.md')
    parser.add_argument('--output', '-o', help='Fichier de sortie pour les nouvelles positions')
    parser.add_argument('--update-preplan', action='store_true',
                       help='Mettre à jour le préplan avec les nouvelles positions')

    args = parser.parse_args()

    if not HAS_GUI:
        print("ERREUR: Les bibliothèques GUI (tkinter, PIL) ne sont pas disponibles.")
        print("Installez-les avec: pip install pillow")
        return 1

    # Charger l'image
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"ERREUR: Image non trouvée : {image_path}")
        return 1

    # Charger les positions
    positions_path = Path(args.positions)
    if not positions_path.exists():
        print(f"ERREUR: Fichier de positions non trouvé : {positions_path}")
        return 1

    if positions_path.suffix == '.md':
        # Extraire depuis préplan
        positions = extract_positions_from_preplan(str(positions_path))
    else:
        # Charger JSON
        with open(positions_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        positions = data.get('etapes', data.get('positions', []))

    if not positions:
        print("ERREUR: Aucune position trouvée dans le fichier")
        return 1

    print(f"[INFO] {len(positions)} étapes chargées")

    # Déterminer le fichier de sortie
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = positions_path.with_name('positions_corrected.json')

    # Lancer l'interface
    app = HotspotPreview(str(image_path), positions, str(output_path))
    app.run()

    # Si demandé, mettre à jour le préplan
    if args.update_preplan and positions_path.suffix == '.md':
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data.get('status') == 'validated':
                update_preplan_positions(str(positions_path), data['etapes'])

    return 0


if __name__ == '__main__':
    sys.exit(main())
