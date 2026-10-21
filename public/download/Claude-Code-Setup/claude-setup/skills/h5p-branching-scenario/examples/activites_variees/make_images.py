#!/usr/bin/env python3
"""
Figures de l'exemple « activités variées » (arbre pondéré de probabilités).

Le repère de dessin couvre EXACTEMENT l'image, de 0 à 100 sur chaque axe, axe
vertical orienté vers le bas : une coordonnée de dessin EST donc un pourcentage
du cadre de l'image, celui qu'attend le preplan pour les zones (glisser-déposer)
et les points (image à zones cliquables). Les constantes ZONES et HOTSPOTS
ci-dessous sont recopiées dans activites_variees.json.

Usage :
  python make_images.py
Produit arbre_a_completer.png (cases vides sur les branches, bande du bas
libre pour les étiquettes) et arbre_complet.png (arbre renseigné).
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).parent
W_PX, H_PX = 1000, 625

ROOT = (6, 40)
L1 = {'A': (40, 18), 'Abar': (40, 62)}
L2 = {('A', 'B'): (80, 5), ('A', 'Bbar'): (80, 31),
      ('Abar', 'B'): (80, 49), ('Abar', 'Bbar'): (80, 75)}
PROBAS = {'A': '0,3', 'Abar': '0,7', ('A', 'B'): '0,6', ('A', 'Bbar'): '0,4',
          ('Abar', 'B'): '0,2', ('Abar', 'Bbar'): '0,8'}
NOMS = {'A': r'$A$', 'Abar': r'$\overline{A}$', 'B': r'$B$', 'Bbar': r'$\overline{B}$'}

#: Case d'une branche : largeur et hauteur en % du cadre de l'image.
ZONE_W, ZONE_H = 11, 8


def milieu(p, q):
    """Point de la branche où poser la case : au milieu pour le premier niveau,
    aux 3/5 pour le second (les deux branches issues d'un nœud s'y écartent
    davantage, les cases ne se touchent plus)."""
    t = 0.5 if p == ROOT else 0.6
    return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))


def branches():
    """(clé, départ, arrivée) de chaque branche, dans l'ordre de lecture."""
    out = [(k, ROOT, v) for k, v in L1.items()]
    out += [(k, L1[k[0]], v) for k, v in L2.items()]
    return out


def zones():
    """Cases des branches : coin haut gauche + taille, en %."""
    res = {}
    for key, p, q in branches():
        cx, cy = milieu(p, q)
        res[key] = (round(cx - ZONE_W / 2, 2), round(cy - ZONE_H / 2, 2), ZONE_W, ZONE_H)
    return res


def dessiner(nom_fichier, complet):
    fig = plt.figure(figsize=(W_PX / 100, H_PX / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(100, 0)          # y vers le bas, comme les % de H5P
    ax.axis('off')

    for key, p, q in branches():
        fin = (q[0] - 3.2, q[1])
        ax.plot([p[0] + 2.5, fin[0]], [p[1], fin[1]], color='#1f3b73', lw=2.2, zorder=1)

    for key, (x, y, w, h) in zones().items():
        if complet:
            cx, cy = x + w / 2, y + h / 2
            ax.text(cx, cy, PROBAS[key], ha='center', va='center', fontsize=17,
                    color='#b3261e', zorder=3,
                    bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='none'))
        else:
            ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.3',
                                        fc='white', ec='#6b7280', lw=1.6,
                                        ls=(0, (4, 3)), zorder=3))

    ax.text(*ROOT, '•', ha='center', va='center', fontsize=22, color='#1f3b73')
    for k, (x, y) in L1.items():
        ax.text(x, y, NOMS[k], ha='center', va='center', fontsize=22, zorder=4,
                bbox=dict(boxstyle='circle,pad=0.2', fc='#e8eefc', ec='#1f3b73'))
    for (a, b), (x, y) in L2.items():
        ax.text(x, y, NOMS[b], ha='center', va='center', fontsize=20, zorder=4)

    if not complet:
        # Bande du bas laissée libre : le générateur y range les étiquettes.
        ax.add_patch(FancyBboxPatch((1.5, 88.5), 97, 10.5, boxstyle='round,pad=0.4',
                                    fc='#f3f4f6', ec='#d1d5db', lw=1, zorder=0))
    fig.savefig(HERE / nom_fichier, dpi=100)
    plt.close(fig)


if __name__ == '__main__':
    dessiner('arbre_a_completer.png', complet=False)
    dessiner('arbre_complet.png', complet=True)
    for key, box in zones().items():
        print(key, box)
