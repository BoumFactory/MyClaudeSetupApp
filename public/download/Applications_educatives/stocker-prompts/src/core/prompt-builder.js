/**
 * Module de construction de prompts à partir de briques
 */

import { DEFAULT_BRICKS, BRICK_CATEGORIES } from '../config/bricks.js';
import { DEFAULT_STRUCTURES } from '../config/structures.js';
import { db } from './database.js';

class PromptBuilder {
  constructor() {
    this.selectedBricks = [];
    this.paramValues = {};
  }

  /**
   * Récupère toutes les briques disponibles (par défaut avec overrides + personnalisées)
   */
  getAllBricks() {
    const customBricks = db.getCustomBricks();
    const brickOverrides = db.getAllBrickOverrides();

    // Appliquer les overrides aux briques par défaut
    const defaultBricksWithOverrides = DEFAULT_BRICKS.map(brick => {
      const override = brickOverrides[brick.id];
      if (override) {
        return { ...brick, ...override, isOverridden: true };
      }
      return brick;
    });

    return [...defaultBricksWithOverrides, ...customBricks];
  }

  /**
   * Récupère les briques par catégorie
   */
  getBricksByCategory(category) {
    return this.getAllBricks().filter(b => b.category === category && b.enabled !== false);
  }

  /**
   * Récupère toutes les structures disponibles (par défaut avec overrides + personnalisées)
   */
  getAllStructures() {
    const customStructures = db.getCustomStructures();
    const structureOverrides = db.getAllStructureOverrides();

    // Appliquer les overrides aux structures par défaut
    const defaultStructuresWithOverrides = DEFAULT_STRUCTURES.map(structure => {
      const override = structureOverrides[structure.id];
      if (override) {
        return { ...structure, ...override, isOverridden: true };
      }
      return structure;
    });

    return [...defaultStructuresWithOverrides, ...customStructures];
  }

  /**
   * Sélectionne une brique
   */
  selectBrick(brickId) {
    if (!this.selectedBricks.includes(brickId)) {
      this.selectedBricks.push(brickId);
    }
  }

  /**
   * Désélectionne une brique
   */
  unselectBrick(brickId) {
    const index = this.selectedBricks.indexOf(brickId);
    if (index > -1) {
      this.selectedBricks.splice(index, 1);
    }
  }

  /**
   * Applique une structure (sélectionne toutes ses briques)
   */
  applyStructure(structureId) {
    const structure = this.getAllStructures().find(s => s.id === structureId);
    if (structure) {
      this.selectedBricks = [...structure.bricks];
    }
  }

  /**
   * Définit une valeur de paramètre
   */
  setParam(paramName, value) {
    this.paramValues[paramName] = value;
  }

  /**
   * Récupère tous les paramètres requis par les briques sélectionnées
   */
  getRequiredParams() {
    const allBricks = this.getAllBricks();
    const params = new Set();

    for (const brickId of this.selectedBricks) {
      const brick = allBricks.find(b => b.id === brickId);
      if (brick && brick.params) {
        brick.params.forEach(p => params.add(p));
      }
    }

    return Array.from(params);
  }

  /**
   * Vérifie si tous les paramètres requis sont remplis
   */
  hasAllParams() {
    const required = this.getRequiredParams();
    return required.every(p => this.paramValues[p] && this.paramValues[p].trim() !== '');
  }

  /**
   * Génère le prompt final
   */
  build() {
    const allBricks = this.getAllBricks();
    const parts = [];

    // Trier les briques par catégorie pour un ordre logique
    const categoryOrder = ['contexte', 'demande', 'format', 'contrainte'];
    const sortedBricks = this.selectedBricks
      .map(id => allBricks.find(b => b.id === id))
      .filter(Boolean)
      .sort((a, b) => {
        const aOrder = categoryOrder.indexOf(a.category);
        const bOrder = categoryOrder.indexOf(b.category);
        return aOrder - bOrder;
      });

    for (const brick of sortedBricks) {
      let text = brick.template;

      // Remplacer les paramètres
      for (const param of (brick.params || [])) {
        const value = this.paramValues[param] || `[${param}]`;
        text = text.replace(`{${param}}`, value);
      }

      parts.push(text);
    }

    return parts.join('\n\n');
  }

  /**
   * Réinitialise le builder
   */
  reset() {
    this.selectedBricks = [];
    this.paramValues = {};
  }

  /**
   * Prévisualise le prompt avec les paramètres actuels
   */
  preview() {
    return this.build();
  }
}

export const promptBuilder = new PromptBuilder();
