/**
 * Composant Panneau de Construction de Prompts
 * Interface pour assembler des briques et générer un prompt
 */

import { promptBuilder } from '../../core/prompt-builder.js';
import { BRICK_CATEGORIES } from '../../config/bricks.js';
import { DEFAULT_SUBJECTS, DEFAULT_LEVELS } from '../../config/subjects.js';
import { db } from '../../core/database.js';

class BuilderPanel {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.paramValues = {};
    this.onPromptGenerated = null;
    // Valeurs pour pré-remplir la modale de sauvegarde
    this.builderValues = {
      level: null,
      subject: null,
      theme: ''
    };
  }

  /**
   * Initialise le panneau
   */
  init(options = {}) {
    this.onPromptGenerated = options.onPromptGenerated || (() => {});
    promptBuilder.reset();

    // Pré-sélectionner le niveau par défaut
    const settings = db.getSettings();
    if (settings.defaultLevel) {
      this.builderValues.level = settings.defaultLevel;
      promptBuilder.setParam('niveau', DEFAULT_LEVELS.find(l => l.id === settings.defaultLevel)?.label || settings.defaultLevel);
    }

    this.render();
  }

  /**
   * Rendu principal
   */
  render() {
    const structures = promptBuilder.getAllStructures();
    const bricks = promptBuilder.getAllBricks();

    let html = `
      <div class="builder-panel">
        <div class="builder-section">
          <h3>🎯 Structures prédéfinies</h3>
          <p class="hint">Clique sur une structure pour pré-remplir les briques</p>
          <div class="structure-grid">
            ${structures.filter(s => s.enabled).map(s => `
              <button class="structure-btn" data-structure="${s.id}" title="${s.description}">
                <span class="structure-icon">${s.icon}</span>
                <span class="structure-label">${s.label}</span>
              </button>
            `).join('')}
          </div>
        </div>

        <div class="builder-section">
          <h3>🧱 Briques disponibles</h3>
          <p class="hint">Sélectionne les briques pour construire ton prompt</p>

          <div class="brick-categories">
            ${Object.entries(BRICK_CATEGORIES).map(([catId, cat]) => `
              <div class="brick-category">
                <h4 style="color: ${cat.color}">${cat.icon} ${cat.label}</h4>
                <div class="brick-list">
                  ${bricks.filter(b => b.category === catId && b.enabled !== false).map(b => `
                    <label class="brick-item ${promptBuilder.selectedBricks.includes(b.id) ? 'selected' : ''}">
                      <input type="checkbox" data-brick="${b.id}"
                             ${promptBuilder.selectedBricks.includes(b.id) ? 'checked' : ''}>
                      <span class="brick-label">${b.label}</span>
                    </label>
                  `).join('')}
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        ${this.renderParamsSection()}

        <div class="builder-section">
          <h3>👁️ Aperçu du prompt</h3>
          <div class="preview-box">
            <pre id="prompt-preview">${promptBuilder.preview() || '<em>Sélectionne des briques pour voir l\'aperçu</em>'}</pre>
          </div>
          <div class="builder-actions">
            <button class="btn btn-secondary" id="builder-reset">🔄 Réinitialiser</button>
            <button class="btn btn-primary" id="builder-copy">📋 Copier</button>
            <button class="btn btn-success" id="builder-save">💾 Sauvegarder</button>
          </div>
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    this.bindEvents();
  }

  renderParamsSection() {
    const requiredParams = promptBuilder.getRequiredParams();

    if (requiredParams.length === 0) {
      return '';
    }

    const paramLabels = {
      niveau: 'Niveau',
      matiere: 'Matière',
      theme: 'Thème/Chapitre',
      sujet_difficile: 'Sujet de difficulté',
      concept: 'Concept à expliquer',
      nombre: 'Nombre',
      sujet: 'Sujet',
      difficulte: 'Difficulté',
      longueur: 'Longueur (quelques lignes, 1 page...)',
      lignes: 'Nombre de lignes max',
      temps: 'Temps disponible'
    };

    // Paramètres avec menu déroulant
    const dropdownParams = ['niveau', 'matiere', 'difficulte'];

    const settings = db.getSettings();
    const enabledSubjects = settings.enabledSubjects || [];
    const subjects = DEFAULT_SUBJECTS.filter(s => enabledSubjects.includes(s.id));
    const levels = DEFAULT_LEVELS.filter(l => l.enabled);

    const difficulties = [
      { id: 'facile', label: 'Facile' },
      { id: 'moyen', label: 'Moyen' },
      { id: 'difficile', label: 'Difficile' }
    ];

    return `
      <div class="builder-section">
        <h3>✏️ Paramètres à remplir</h3>
        <div class="params-form">
          ${requiredParams.map(param => {
            if (param === 'niveau') {
              return `
                <div class="param-field">
                  <label for="param-${param}">${paramLabels[param]}</label>
                  <select id="param-${param}" data-param="${param}" class="param-select">
                    <option value="">-- Choisir un niveau --</option>
                    ${levels.map(l => `
                      <option value="${l.label}" ${this.builderValues.level === l.id ? 'selected' : ''}>${l.label}</option>
                    `).join('')}
                  </select>
                </div>
              `;
            } else if (param === 'matiere') {
              return `
                <div class="param-field">
                  <label for="param-${param}">${paramLabels[param]}</label>
                  <select id="param-${param}" data-param="${param}" class="param-select">
                    <option value="">-- Choisir une matière --</option>
                    ${subjects.map(s => `
                      <option value="${s.label}" ${this.builderValues.subject === s.id ? 'selected' : ''}>${s.emoji} ${s.label}</option>
                    `).join('')}
                  </select>
                </div>
              `;
            } else if (param === 'difficulte') {
              return `
                <div class="param-field">
                  <label for="param-${param}">${paramLabels[param]}</label>
                  <select id="param-${param}" data-param="${param}" class="param-select">
                    <option value="">-- Choisir la difficulté --</option>
                    ${difficulties.map(d => `
                      <option value="${d.label}" ${promptBuilder.paramValues[param] === d.label ? 'selected' : ''}>${d.label}</option>
                    `).join('')}
                  </select>
                </div>
              `;
            } else {
              return `
                <div class="param-field">
                  <label for="param-${param}">${paramLabels[param] || param}</label>
                  <input type="text" id="param-${param}" data-param="${param}"
                         value="${promptBuilder.paramValues[param] || ''}"
                         placeholder="${paramLabels[param] || param}">
                </div>
              `;
            }
          }).join('')}
        </div>
      </div>
    `;
  }

  bindEvents() {
    // Structures
    this.container.querySelectorAll('.structure-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        promptBuilder.applyStructure(btn.dataset.structure);
        this.render();
      });
    });

    // Briques
    this.container.querySelectorAll('input[data-brick]').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
        if (e.target.checked) {
          promptBuilder.selectBrick(e.target.dataset.brick);
        } else {
          promptBuilder.unselectBrick(e.target.dataset.brick);
        }
        this.render();
      });
    });

    // Paramètres (inputs texte)
    this.container.querySelectorAll('input[data-param]').forEach(input => {
      input.addEventListener('input', (e) => {
        const param = e.target.dataset.param;
        promptBuilder.setParam(param, e.target.value);
        // Stocker le thème pour le pré-remplissage
        if (param === 'theme') {
          this.builderValues.theme = e.target.value;
        }
        this.updatePreview();
      });
    });

    // Paramètres (selects)
    this.container.querySelectorAll('select[data-param]').forEach(select => {
      select.addEventListener('change', (e) => {
        const param = e.target.dataset.param;
        promptBuilder.setParam(param, e.target.value);

        // Stocker les valeurs pour le pré-remplissage de la modale
        if (param === 'niveau') {
          const level = DEFAULT_LEVELS.find(l => l.label === e.target.value);
          this.builderValues.level = level ? level.id : null;
        } else if (param === 'matiere') {
          const subject = DEFAULT_SUBJECTS.find(s => s.label === e.target.value || `${s.emoji} ${s.label}` === e.target.value);
          this.builderValues.subject = subject ? subject.id : null;
        }

        this.updatePreview();
      });
    });

    // Actions
    const resetBtn = this.container.querySelector('#builder-reset');
    const copyBtn = this.container.querySelector('#builder-copy');
    const saveBtn = this.container.querySelector('#builder-save');

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        promptBuilder.reset();
        this.render();
      });
    }

    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const prompt = promptBuilder.build();
        if (prompt) {
          navigator.clipboard.writeText(prompt).then(() => {
            this.showToast('Prompt copié !');
          });
        }
      });
    }

    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        const prompt = promptBuilder.build();
        if (prompt && promptBuilder.selectedBricks.length > 0) {
          // Passer le prompt ET les valeurs pré-remplies
          this.onPromptGenerated(prompt, this.getBuilderValues());
        } else {
          this.showToast('Sélectionne au moins une brique');
        }
      });
    }
  }

  /**
   * Retourne les valeurs saisies dans le fabricateur pour pré-remplir la modale
   */
  getBuilderValues() {
    return {
      level: this.builderValues.level,
      subject: this.builderValues.subject,
      theme: promptBuilder.paramValues.theme || this.builderValues.theme || ''
    };
  }

  updatePreview() {
    const preview = this.container.querySelector('#prompt-preview');
    if (preview) {
      preview.textContent = promptBuilder.preview() || 'Sélectionne des briques pour voir l\'aperçu';
    }
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

  refresh() {
    this.render();
  }
}

export { BuilderPanel };
