/**
 * Composant Panneau des Paramètres
 * Permet de configurer les actions, matières, briques personnalisées et structures
 */

import { db } from '../../core/database.js';
import { ACTIONS, ACTION_CATEGORIES } from '../../config/actions.js';
import { DEFAULT_SUBJECTS, DEFAULT_LEVELS } from '../../config/subjects.js';
import { DEFAULT_BRICKS, BRICK_CATEGORIES } from '../../config/bricks.js';
import { DEFAULT_STRUCTURES } from '../../config/structures.js';

class SettingsPanel {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.onSettingsChanged = null;
  }

  /**
   * Initialise le panneau
   */
  init(options = {}) {
    this.onSettingsChanged = options.onSettingsChanged || (() => {});
    this.render();
  }

  /**
   * Rendu principal
   */
  render() {
    const settings = db.getSettings();

    let html = `
      <div class="settings-panel">
        <div class="settings-header">
          <h2>⚙️ Paramètres</h2>
          <p class="hint">Configure l'application selon tes besoins</p>
        </div>

        <div class="settings-section">
          <h3>📊 Niveau par défaut</h3>
          <p class="hint">Si tu es toujours au même niveau, définis-le ici pour gagner du temps</p>
          <select id="default-level">
            <option value="">Aucun (demander à chaque fois)</option>
            ${DEFAULT_LEVELS.map(l => `
              <option value="${l.id}" ${settings.defaultLevel === l.id ? 'selected' : ''}>${l.label}</option>
            `).join('')}
          </select>
        </div>

        <div class="settings-section">
          <h3>✨ Actions disponibles</h3>
          <p class="hint">Coche les actions que tu veux voir dans le wizard</p>
          <div class="checkbox-grid">
            ${ACTIONS.map(a => `
              <label class="checkbox-item">
                <input type="checkbox" data-action="${a.id}"
                       ${settings.enabledActions?.includes(a.id) ? 'checked' : ''}>
                <span>${a.emoji} ${a.label}</span>
              </label>
            `).join('')}
          </div>
          <div class="settings-actions">
            <button class="btn btn-small" id="actions-select-all">Tout cocher</button>
            <button class="btn btn-small" id="actions-select-none">Tout décocher</button>
            <button class="btn btn-small" id="actions-reset">Par défaut</button>
          </div>
        </div>

        <div class="settings-section">
          <h3>📚 Matières disponibles</h3>
          <p class="hint">Coche les matières que tu étudies</p>
          <div class="checkbox-grid">
            ${DEFAULT_SUBJECTS.map(s => `
              <label class="checkbox-item">
                <input type="checkbox" data-subject="${s.id}"
                       ${settings.enabledSubjects?.includes(s.id) ? 'checked' : ''}>
                <span>${s.emoji} ${s.label}</span>
              </label>
            `).join('')}
          </div>
        </div>

        <div class="settings-section">
          <h3>🎨 Apparence</h3>
          <div class="theme-selector">
            <button class="theme-btn ${settings.theme === 'light' ? 'selected' : ''}" data-theme="light">
              ☀️ Clair
            </button>
            <button class="theme-btn ${settings.theme === 'dark' ? 'selected' : ''}" data-theme="dark">
              🌙 Sombre
            </button>
          </div>
        </div>

        ${this.renderCustomBricksSection()}

        ${this.renderCustomStructuresSection()}

        <div class="settings-section danger-zone">
          <h3>⚠️ Zone de danger</h3>
          <div class="danger-actions">
            <button class="btn btn-danger" id="export-data">
              📤 Exporter mes données
            </button>
            <button class="btn btn-danger" id="import-data">
              📥 Importer des données
            </button>
            <button class="btn btn-danger" id="clear-data">
              🗑️ Tout effacer
            </button>
          </div>
          <input type="file" id="import-file" accept=".json" style="display: none">
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    this.bindEvents();
  }

  /**
   * Rendu de la section briques personnalisées
   */
  renderCustomBricksSection() {
    const customBricks = db.getCustomBricks();

    return `
      <div class="settings-section">
        <h3>🧱 Mes briques personnalisées</h3>
        <p class="hint">Crée tes propres briques de texte réutilisables</p>

        ${customBricks.length > 0 ? `
          <div class="custom-items-list">
            ${customBricks.map(brick => `
              <div class="custom-item" data-brick-id="${brick.id}">
                <div class="custom-item-info">
                  <span class="custom-item-category" style="background: ${BRICK_CATEGORIES[brick.category]?.color || '#888'}">
                    ${BRICK_CATEGORIES[brick.category]?.icon || '📦'} ${BRICK_CATEGORIES[brick.category]?.label || brick.category}
                  </span>
                  <strong>${brick.label}</strong>
                  <div class="custom-item-preview">${brick.template}</div>
                </div>
                <div class="custom-item-actions">
                  <button class="btn btn-small btn-secondary edit-brick" data-brick-id="${brick.id}">✏️</button>
                  <button class="btn btn-small btn-danger delete-brick" data-brick-id="${brick.id}">🗑️</button>
                </div>
              </div>
            `).join('')}
          </div>
        ` : `
          <p class="empty-hint">Aucune brique personnalisée. Crée ta première !</p>
        `}

        <button class="btn btn-primary" id="add-brick">
          ➕ Créer une brique
        </button>
      </div>
    `;
  }

  /**
   * Rendu de la section structures personnalisées
   */
  renderCustomStructuresSection() {
    const customStructures = db.getCustomStructures();
    const allBricks = [...DEFAULT_BRICKS, ...db.getCustomBricks()];

    return `
      <div class="settings-section">
        <h3>🏗️ Mes structures personnalisées</h3>
        <p class="hint">Combine des briques pour créer des structures réutilisables</p>

        ${customStructures.length > 0 ? `
          <div class="custom-items-list">
            ${customStructures.map(structure => `
              <div class="custom-item" data-structure-id="${structure.id}">
                <div class="custom-item-info">
                  <span class="custom-item-icon">${structure.icon || '📋'}</span>
                  <strong>${structure.label}</strong>
                  <div class="custom-item-preview">${structure.description || ''}</div>
                  <div class="custom-item-bricks">
                    ${structure.bricks.map(brickId => {
                      const brick = allBricks.find(b => b.id === brickId);
                      return brick ? `<span class="mini-tag">${brick.label}</span>` : '';
                    }).join('')}
                  </div>
                </div>
                <div class="custom-item-actions">
                  <button class="btn btn-small btn-secondary edit-structure" data-structure-id="${structure.id}">✏️</button>
                  <button class="btn btn-small btn-danger delete-structure" data-structure-id="${structure.id}">🗑️</button>
                </div>
              </div>
            `).join('')}
          </div>
        ` : `
          <p class="empty-hint">Aucune structure personnalisée. Crée ta première !</p>
        `}

        <button class="btn btn-primary" id="add-structure">
          ➕ Créer une structure
        </button>
      </div>
    `;
  }

  /**
   * Ouvre la modal de création/édition de brique
   */
  openBrickModal(existingBrick = null) {
    const isEdit = !!existingBrick;
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <h3>${isEdit ? '✏️ Modifier la brique' : '➕ Nouvelle brique'}</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="brick-label">Nom de la brique *</label>
            <input type="text" id="brick-label" value="${existingBrick?.label || ''}" placeholder="Ex: Ma demande personnalisée" required>
          </div>

          <div class="form-group">
            <label for="brick-category">Catégorie *</label>
            <select id="brick-category">
              ${Object.entries(BRICK_CATEGORIES).map(([id, cat]) => `
                <option value="${id}" ${existingBrick?.category === id ? 'selected' : ''}>
                  ${cat.icon} ${cat.label}
                </option>
              `).join('')}
            </select>
          </div>

          <div class="form-group">
            <label for="brick-template">Texte du prompt *</label>
            <textarea id="brick-template" rows="3" placeholder="Utilise {parametre} pour les variables">${existingBrick?.template || ''}</textarea>
            <small>Astuce : utilise <code>{niveau}</code>, <code>{matiere}</code>, <code>{theme}</code> pour des paramètres</small>
          </div>

          <div class="form-group">
            <label>Aperçu des paramètres détectés</label>
            <div id="params-preview" class="params-preview">
              ${this.extractParams(existingBrick?.template || '').map(p => `<span class="param-tag">{${p}}</span>`).join('') || '<em>Aucun paramètre</em>'}
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary modal-cancel">Annuler</button>
          <button class="btn btn-success modal-save">${isEdit ? 'Enregistrer' : 'Créer'}</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Mise à jour en temps réel des paramètres
    const templateInput = modal.querySelector('#brick-template');
    const paramsPreview = modal.querySelector('#params-preview');
    templateInput.addEventListener('input', () => {
      const params = this.extractParams(templateInput.value);
      paramsPreview.innerHTML = params.length > 0
        ? params.map(p => `<span class="param-tag">{${p}}</span>`).join('')
        : '<em>Aucun paramètre</em>';
    });

    // Événements
    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('.modal-cancel').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    modal.querySelector('.modal-save').addEventListener('click', () => {
      const label = modal.querySelector('#brick-label').value.trim();
      const category = modal.querySelector('#brick-category').value;
      const template = modal.querySelector('#brick-template').value.trim();

      if (!label || !template) {
        this.showToast('Remplis tous les champs obligatoires');
        return;
      }

      const params = this.extractParams(template);

      if (isEdit) {
        // Supprimer l'ancienne et créer la nouvelle (simple update)
        db.deleteCustomBrick(existingBrick.id);
      }

      db.addCustomBrick({ label, category, template, params, enabled: true });
      this.showToast(isEdit ? 'Brique modifiée !' : 'Brique créée !');
      modal.remove();
      this.render();
    });
  }

  /**
   * Ouvre la modal de création/édition de structure
   */
  openStructureModal(existingStructure = null) {
    const isEdit = !!existingStructure;
    const allBricks = [...DEFAULT_BRICKS, ...db.getCustomBricks()];

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>${isEdit ? '✏️ Modifier la structure' : '➕ Nouvelle structure'}</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label for="structure-icon">Icône</label>
              <input type="text" id="structure-icon" value="${existingStructure?.icon || '📋'}" maxlength="2" style="width: 60px; text-align: center; font-size: 1.5rem;">
            </div>
            <div class="form-group" style="flex: 1;">
              <label for="structure-label">Nom de la structure *</label>
              <input type="text" id="structure-label" value="${existingStructure?.label || ''}" placeholder="Ex: Ma révision personnalisée">
            </div>
          </div>

          <div class="form-group">
            <label for="structure-description">Description</label>
            <input type="text" id="structure-description" value="${existingStructure?.description || ''}" placeholder="Courte description de l'utilité">
          </div>

          <div class="form-group">
            <label>Sélectionne les briques à inclure *</label>
            <div class="brick-selector">
              ${Object.entries(BRICK_CATEGORIES).map(([catId, cat]) => `
                <div class="brick-selector-category">
                  <h4 style="color: ${cat.color}">${cat.icon} ${cat.label}</h4>
                  <div class="brick-selector-list">
                    ${allBricks.filter(b => b.category === catId).map(brick => `
                      <label class="brick-selector-item">
                        <input type="checkbox" value="${brick.id}"
                               ${existingStructure?.bricks?.includes(brick.id) ? 'checked' : ''}>
                        <span>${brick.label}</span>
                        ${brick.isCustom ? '<span class="custom-badge">Perso</span>' : ''}
                      </label>
                    `).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="form-group">
            <label>Briques sélectionnées</label>
            <div id="selected-bricks-preview" class="selected-bricks-preview">
              ${existingStructure?.bricks?.length > 0
                ? existingStructure.bricks.map(bId => {
                    const b = allBricks.find(br => br.id === bId);
                    return b ? `<span class="mini-tag">${b.label}</span>` : '';
                  }).join('')
                : '<em>Aucune brique sélectionnée</em>'}
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary modal-cancel">Annuler</button>
          <button class="btn btn-success modal-save">${isEdit ? 'Enregistrer' : 'Créer'}</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    // Mise à jour en temps réel de la prévisualisation
    const updatePreview = () => {
      const selected = Array.from(modal.querySelectorAll('.brick-selector input:checked')).map(cb => cb.value);
      const preview = modal.querySelector('#selected-bricks-preview');
      preview.innerHTML = selected.length > 0
        ? selected.map(bId => {
            const b = allBricks.find(br => br.id === bId);
            return b ? `<span class="mini-tag">${b.label}</span>` : '';
          }).join('')
        : '<em>Aucune brique sélectionnée</em>';
    };

    modal.querySelectorAll('.brick-selector input').forEach(cb => {
      cb.addEventListener('change', updatePreview);
    });

    // Événements
    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('.modal-cancel').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    modal.querySelector('.modal-save').addEventListener('click', () => {
      const label = modal.querySelector('#structure-label').value.trim();
      const description = modal.querySelector('#structure-description').value.trim();
      const icon = modal.querySelector('#structure-icon').value.trim() || '📋';
      const bricks = Array.from(modal.querySelectorAll('.brick-selector input:checked')).map(cb => cb.value);

      if (!label) {
        this.showToast('Donne un nom à ta structure');
        return;
      }

      if (bricks.length === 0) {
        this.showToast('Sélectionne au moins une brique');
        return;
      }

      if (isEdit) {
        db.deleteCustomStructure(existingStructure.id);
      }

      db.addCustomStructure({ label, description, icon, bricks, enabled: true });
      this.showToast(isEdit ? 'Structure modifiée !' : 'Structure créée !');
      modal.remove();
      this.render();
    });
  }

  /**
   * Extrait les paramètres d'un template
   */
  extractParams(template) {
    const matches = template.match(/\{(\w+)\}/g) || [];
    return [...new Set(matches.map(m => m.slice(1, -1)))];
  }

  bindEvents() {
    const settings = db.getSettings();

    // Niveau par défaut
    const defaultLevel = this.container.querySelector('#default-level');
    if (defaultLevel) {
      defaultLevel.addEventListener('change', (e) => {
        db.updateSettings({ defaultLevel: e.target.value || null });
        this.onSettingsChanged();
      });
    }

    // Actions
    this.container.querySelectorAll('input[data-action]').forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        const enabledActions = [];
        this.container.querySelectorAll('input[data-action]:checked').forEach(cb => {
          enabledActions.push(cb.dataset.action);
        });
        db.updateSettings({ enabledActions });
        this.onSettingsChanged();
      });
    });

    // Boutons actions
    const selectAll = this.container.querySelector('#actions-select-all');
    const selectNone = this.container.querySelector('#actions-select-none');
    const resetActions = this.container.querySelector('#actions-reset');

    if (selectAll) {
      selectAll.addEventListener('click', () => {
        const allActions = ACTIONS.map(a => a.id);
        db.updateSettings({ enabledActions: allActions });
        this.render();
        this.onSettingsChanged();
      });
    }

    if (selectNone) {
      selectNone.addEventListener('click', () => {
        db.updateSettings({ enabledActions: [] });
        this.render();
        this.onSettingsChanged();
      });
    }

    if (resetActions) {
      resetActions.addEventListener('click', () => {
        const defaultActions = ACTIONS.filter(a => a.enabled).map(a => a.id);
        db.updateSettings({ enabledActions: defaultActions });
        this.render();
        this.onSettingsChanged();
      });
    }

    // Matières
    this.container.querySelectorAll('input[data-subject]').forEach(checkbox => {
      checkbox.addEventListener('change', () => {
        const enabledSubjects = [];
        this.container.querySelectorAll('input[data-subject]:checked').forEach(cb => {
          enabledSubjects.push(cb.dataset.subject);
        });
        db.updateSettings({ enabledSubjects });
        this.onSettingsChanged();
      });
    });

    // Thème
    this.container.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const theme = btn.dataset.theme;
        db.updateSettings({ theme });
        document.documentElement.setAttribute('data-theme', theme);
        this.render();
        this.onSettingsChanged();
      });
    });

    // Export
    const exportBtn = this.container.querySelector('#export-data');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        const data = db.exportAll();
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `prompts-backup-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
        this.showToast('Données exportées !');
      });
    }

    // Import
    const importBtn = this.container.querySelector('#import-data');
    const importFile = this.container.querySelector('#import-file');
    if (importBtn && importFile) {
      importBtn.addEventListener('click', () => importFile.click());
      importFile.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (evt) => {
            const merge = confirm('Fusionner avec les données existantes ?\n\nOK = Fusionner\nAnnuler = Remplacer');
            if (db.importData(evt.target.result, merge)) {
              this.showToast('Données importées !');
              this.render();
              this.onSettingsChanged();
            } else {
              this.showToast('Erreur d\'import');
            }
          };
          reader.readAsText(file);
        }
      });
    }

    // Clear
    const clearBtn = this.container.querySelector('#clear-data');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (confirm('Supprimer TOUTES les données ? Cette action est irréversible !')) {
          if (confirm('Vraiment sûr ? Dernière chance...')) {
            db.clear();
            this.showToast('Toutes les données ont été effacées');
            this.render();
            this.onSettingsChanged();
          }
        }
      });
    }

    // ===== Briques personnalisées =====
    const addBrickBtn = this.container.querySelector('#add-brick');
    if (addBrickBtn) {
      addBrickBtn.addEventListener('click', () => this.openBrickModal());
    }

    this.container.querySelectorAll('.edit-brick').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const brickId = btn.dataset.brickId;
        const brick = db.getCustomBricks().find(b => b.id === brickId);
        if (brick) this.openBrickModal(brick);
      });
    });

    this.container.querySelectorAll('.delete-brick').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const brickId = btn.dataset.brickId;
        if (confirm('Supprimer cette brique ?')) {
          db.deleteCustomBrick(brickId);
          this.showToast('Brique supprimée');
          this.render();
        }
      });
    });

    // ===== Structures personnalisées =====
    const addStructureBtn = this.container.querySelector('#add-structure');
    if (addStructureBtn) {
      addStructureBtn.addEventListener('click', () => this.openStructureModal());
    }

    this.container.querySelectorAll('.edit-structure').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const structureId = btn.dataset.structureId;
        const structure = db.getCustomStructures().find(s => s.id === structureId);
        if (structure) this.openStructureModal(structure);
      });
    });

    this.container.querySelectorAll('.delete-structure').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const structureId = btn.dataset.structureId;
        if (confirm('Supprimer cette structure ?')) {
          db.deleteCustomStructure(structureId);
          this.showToast('Structure supprimée');
          this.render();
        }
      });
    });
  }

  showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 2000);
  }
}

export { SettingsPanel };
