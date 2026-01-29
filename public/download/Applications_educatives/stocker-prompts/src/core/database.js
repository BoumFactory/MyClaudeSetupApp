/**
 * Module de gestion de la base de données JSON
 * Mode Tauri : gestion multi-fichiers dans le dossier data/
 */

class Database {
  constructor() {
    this.data = {
      prompts: [],
      settings: {},
      customBricks: [],
      customStructures: [],
      brickOverrides: {},      // Modifications des briques par défaut (id -> override)
      structureOverrides: {}   // Modifications des structures par défaut (id -> override)
    };
    this.currentFile = null;
    this.dataDirectory = null;
    this.initialized = false;
    this.isTauri = false;
  }

  /**
   * Détecte si on est dans Tauri
   */
  detectTauri() {
    return window.__TAURI__ && window.__TAURI__.core;
  }

  /**
   * Initialise la connexion (vérifie Tauri, récupère le chemin data/)
   */
  async init() {
    if (this.initialized) return;

    this.isTauri = this.detectTauri();

    if (!this.isTauri) {
      throw new Error('Cette application nécessite Tauri pour fonctionner.');
    }

    try {
      const { invoke } = window.__TAURI__.core;
      this.dataDirectory = await invoke('get_data_directory');
      console.log('Dossier data:', this.dataDirectory);
      this.initialized = true;
    } catch (err) {
      console.error('Erreur init Tauri:', err);
      throw new Error('Impossible d\'initialiser le dossier data/');
    }
  }

  /**
   * Liste tous les fichiers JSON disponibles dans data/
   */
  async listFiles() {
    if (!this.isTauri) throw new Error('Tauri requis');

    const { invoke } = window.__TAURI__.core;
    return await invoke('list_databases');
  }

  /**
   * Charge un fichier spécifique
   */
  async loadFile(filename) {
    if (!this.isTauri) throw new Error('Tauri requis');

    const { invoke } = window.__TAURI__.core;
    const content = await invoke('load_database', { filename });

    this.data = JSON.parse(content);
    this.currentFile = filename;

    // Assurer la structure de base
    this.data.prompts = this.data.prompts || [];
    this.data.settings = this.data.settings || this._getDefaultSettings();
    this.data.customBricks = this.data.customBricks || [];
    this.data.customStructures = this.data.customStructures || [];
    this.data.brickOverrides = this.data.brickOverrides || {};
    this.data.structureOverrides = this.data.structureOverrides || {};

    console.log('Fichier chargé:', filename, '-', this.data.prompts.length, 'prompts');
    return this.data;
  }

  /**
   * Crée un nouveau fichier
   */
  async createFile(filename) {
    if (!this.isTauri) throw new Error('Tauri requis');

    const { invoke } = window.__TAURI__.core;
    await invoke('create_database', { filename });

    // Charger le nouveau fichier
    return await this.loadFile(filename.endsWith('.json') ? filename : `${filename}.json`);
  }

  /**
   * Supprime un fichier
   */
  async deleteFile(filename) {
    if (!this.isTauri) throw new Error('Tauri requis');

    const { invoke } = window.__TAURI__.core;
    await invoke('delete_database', { filename });

    // Si c'était le fichier actif, le décharger
    if (this.currentFile === filename) {
      this.currentFile = null;
      this.data = {
        prompts: [],
        settings: this._getDefaultSettings(),
        customBricks: [],
        customStructures: []
      };
    }
  }

  /**
   * Renomme un fichier
   */
  async renameFile(oldName, newName) {
    if (!this.isTauri) throw new Error('Tauri requis');

    const { invoke } = window.__TAURI__.core;
    await invoke('rename_database', { oldName, newName });

    // Mettre à jour le nom si c'était le fichier actif
    if (this.currentFile === oldName) {
      this.currentFile = newName.endsWith('.json') ? newName : `${newName}.json`;
    }
  }

  _getDefaultSettings() {
    return {
      defaultLevel: null,
      enabledSubjects: ['maths', 'francais', 'histoire', 'geo', 'physique', 'svt', 'anglais', 'autre'],
      enabledActions: ['creer', 'reviser', 'expliquer', 'corriger', 'resumer', 'comparer'],
      theme: 'light'
    };
  }

  /**
   * Sauvegarde la base de données dans le fichier actif
   */
  async save() {
    if (!this.currentFile) {
      throw new Error('Aucun fichier sélectionné');
    }

    const { invoke } = window.__TAURI__.core;
    const content = JSON.stringify(this.data, null, 2);
    await invoke('save_database', { filename: this.currentFile, content });
  }

  // ===== PROMPTS =====

  addPrompt(prompt) {
    const newPrompt = {
      id: this._generateId(),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      ...prompt
    };
    this.data.prompts.push(newPrompt);
    this.save();
    return newPrompt;
  }

  updatePrompt(id, updates) {
    const index = this.data.prompts.findIndex(p => p.id === id);
    if (index === -1) return null;

    this.data.prompts[index] = {
      ...this.data.prompts[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };
    this.save();
    return this.data.prompts[index];
  }

  deletePrompt(id) {
    const index = this.data.prompts.findIndex(p => p.id === id);
    if (index === -1) return false;

    this.data.prompts.splice(index, 1);
    this.save();
    return true;
  }

  getAllPrompts() {
    return [...this.data.prompts];
  }

  getPrompts(filters = {}) {
    let prompts = [...this.data.prompts];

    if (filters.action) {
      prompts = prompts.filter(p => p.action === filters.action);
    }
    if (filters.subject) {
      prompts = prompts.filter(p => p.subject === filters.subject);
    }
    if (filters.level) {
      prompts = prompts.filter(p => p.level === filters.level);
    }
    if (filters.theme) {
      prompts = prompts.filter(p =>
        p.theme && p.theme.toLowerCase().includes(filters.theme.toLowerCase())
      );
    }
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      prompts = prompts.filter(p =>
        p.title?.toLowerCase().includes(searchLower) ||
        p.content?.toLowerCase().includes(searchLower) ||
        p.description?.toLowerCase().includes(searchLower)
      );
    }

    return prompts;
  }

  getPromptById(id) {
    return this.data.prompts.find(p => p.id === id) || null;
  }

  // ===== SETTINGS =====

  getSettings() {
    return { ...this.data.settings };
  }

  updateSettings(updates) {
    this.data.settings = { ...this.data.settings, ...updates };
    this.save();
    return this.data.settings;
  }

  // ===== CUSTOM BRICKS =====

  addCustomBrick(brick) {
    const newBrick = {
      id: 'custom_' + this._generateId(),
      ...brick,
      isCustom: true
    };
    this.data.customBricks.push(newBrick);
    this.save();
    return newBrick;
  }

  getCustomBricks() {
    return [...this.data.customBricks];
  }

  deleteCustomBrick(id) {
    const index = this.data.customBricks.findIndex(b => b.id === id);
    if (index === -1) return false;
    this.data.customBricks.splice(index, 1);
    this.save();
    return true;
  }

  // ===== CUSTOM STRUCTURES =====

  addCustomStructure(structure) {
    const newStructure = {
      id: 'custom_' + this._generateId(),
      ...structure,
      isCustom: true
    };
    this.data.customStructures.push(newStructure);
    this.save();
    return newStructure;
  }

  getCustomStructures() {
    return [...this.data.customStructures];
  }

  deleteCustomStructure(id) {
    const index = this.data.customStructures.findIndex(s => s.id === id);
    if (index === -1) return false;
    this.data.customStructures.splice(index, 1);
    this.save();
    return true;
  }

  // ===== BRICK OVERRIDES (modifications des briques par défaut) =====

  setBrickOverride(brickId, override) {
    this.data.brickOverrides[brickId] = {
      ...override,
      modifiedAt: new Date().toISOString()
    };
    this.save();
    return this.data.brickOverrides[brickId];
  }

  getBrickOverride(brickId) {
    return this.data.brickOverrides[brickId] || null;
  }

  getAllBrickOverrides() {
    return { ...this.data.brickOverrides };
  }

  deleteBrickOverride(brickId) {
    if (!this.data.brickOverrides[brickId]) return false;
    delete this.data.brickOverrides[brickId];
    this.save();
    return true;
  }

  resetAllBrickOverrides() {
    this.data.brickOverrides = {};
    this.save();
  }

  // ===== STRUCTURE OVERRIDES (modifications des structures par défaut) =====

  setStructureOverride(structureId, override) {
    this.data.structureOverrides[structureId] = {
      ...override,
      modifiedAt: new Date().toISOString()
    };
    this.save();
    return this.data.structureOverrides[structureId];
  }

  getStructureOverride(structureId) {
    return this.data.structureOverrides[structureId] || null;
  }

  getAllStructureOverrides() {
    return { ...this.data.structureOverrides };
  }

  deleteStructureOverride(structureId) {
    if (!this.data.structureOverrides[structureId]) return false;
    delete this.data.structureOverrides[structureId];
    this.save();
    return true;
  }

  resetAllStructureOverrides() {
    this.data.structureOverrides = {};
    this.save();
  }

  // ===== RESET COMPLET BRIQUES/STRUCTURES =====

  resetAllBricksAndStructures() {
    this.data.customBricks = [];
    this.data.customStructures = [];
    this.data.brickOverrides = {};
    this.data.structureOverrides = {};
    this.save();
  }

  // ===== EXPORT / IMPORT BRIQUES/STRUCTURES =====

  exportBricksAndStructures() {
    return JSON.stringify({
      customBricks: this.data.customBricks,
      customStructures: this.data.customStructures,
      brickOverrides: this.data.brickOverrides,
      structureOverrides: this.data.structureOverrides
    }, null, 2);
  }

  importBricksAndStructures(jsonString, merge = false) {
    try {
      const imported = JSON.parse(jsonString);

      if (merge) {
        if (imported.customBricks) {
          this.data.customBricks = [...this.data.customBricks, ...imported.customBricks];
        }
        if (imported.customStructures) {
          this.data.customStructures = [...this.data.customStructures, ...imported.customStructures];
        }
        if (imported.brickOverrides) {
          this.data.brickOverrides = { ...this.data.brickOverrides, ...imported.brickOverrides };
        }
        if (imported.structureOverrides) {
          this.data.structureOverrides = { ...this.data.structureOverrides, ...imported.structureOverrides };
        }
      } else {
        this.data.customBricks = imported.customBricks || [];
        this.data.customStructures = imported.customStructures || [];
        this.data.brickOverrides = imported.brickOverrides || {};
        this.data.structureOverrides = imported.structureOverrides || {};
      }

      this.save();
      return true;
    } catch (e) {
      console.error('Erreur d\'import briques/structures:', e);
      return false;
    }
  }

  // ===== EXPORT / IMPORT =====

  exportAll() {
    return JSON.stringify(this.data, null, 2);
  }

  exportPrompts() {
    return JSON.stringify(this.data.prompts, null, 2);
  }

  importData(jsonString, merge = false) {
    try {
      const imported = JSON.parse(jsonString);

      if (merge) {
        if (imported.prompts) {
          this.data.prompts = [...this.data.prompts, ...imported.prompts];
        }
        if (imported.customBricks) {
          this.data.customBricks = [...this.data.customBricks, ...imported.customBricks];
        }
        if (imported.customStructures) {
          this.data.customStructures = [...this.data.customStructures, ...imported.customStructures];
        }
      } else {
        this.data = imported;
      }

      this.save();
      return true;
    } catch (e) {
      console.error('Erreur d\'import:', e);
      return false;
    }
  }

  // ===== UTILS =====

  _generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
  }

  clear() {
    this.data = {
      prompts: [],
      settings: this._getDefaultSettings(),
      customBricks: [],
      customStructures: []
    };
    this.save();
  }

  /**
   * Retourne le nom du fichier actuellement utilisé
   */
  getCurrentFile() {
    return this.currentFile;
  }

  /**
   * Retourne le chemin du dossier data/
   */
  getDataDirectory() {
    return this.dataDirectory;
  }

  /**
   * Retourne le statut
   */
  getStatus() {
    return {
      initialized: this.initialized,
      currentFile: this.currentFile,
      dataDirectory: this.dataDirectory,
      promptCount: this.data.prompts.length
    };
  }
}

// Export singleton
export const db = new Database();
