/**
 * Application principale - Prompt Manager
 * Point d'entrée de l'application
 */

import { db } from './core/database.js';
import { PromptList } from './ui/components/prompt-list.js';
import { BuilderPanel } from './ui/components/builder-panel.js';
import { ConcatenationPanel } from './ui/components/concatenation-panel.js';
import { SettingsPanel } from './ui/components/settings-panel.js';
import { SaveModal } from './ui/components/save-modal.js';
import { Wizard } from './ui/components/wizard.js';
import { DEFAULT_BRICKS, BRICK_CATEGORIES } from './config/bricks.js';
import { DEFAULT_STRUCTURES } from './config/structures.js';

class App {
  constructor() {
    this.currentView = 'prompts';
    this.promptList = null;
    this.builderPanel = null;
    this.concatenationPanel = null;
    this.settingsPanel = null;
    this.saveModal = new SaveModal();
    this.files = [];
  }

  /**
   * Initialise l'application
   */
  async init() {
    try {
      // Initialiser la connexion DB
      await db.init();

      // Charger la liste des fichiers
      this.files = await db.listFiles();

      // Si des fichiers existent, charger le premier
      if (this.files.length > 0) {
        await db.loadFile(this.files[0].name);
      }

      // Appliquer le thème
      const settings = db.getSettings();
      document.documentElement.setAttribute('data-theme', settings.theme || 'light');

      // Rendre le layout principal
      this.renderLayout();

      // Bind des événements
      this.bindNavigation();
      this.bindFileSelector();

      // Afficher la vue par défaut
      this.showView('prompts');

    } catch (err) {
      console.error('Erreur initialisation:', err);
      this.showError(err.message);
    }
  }

  /**
   * Affiche un écran d'erreur
   */
  async showError(message) {
    let debugInfo = '';
    try {
      if (window.__TAURI__ && window.__TAURI__.core) {
        const { invoke } = window.__TAURI__.core;
        debugInfo = await invoke('debug_paths');
      }
    } catch (e) {
      debugInfo = 'Impossible de récupérer les chemins: ' + e;
    }

    document.body.innerHTML = `
      <div class="error-screen">
        <div class="error-card">
          <div class="error-icon">⚠️</div>
          <h1>Erreur</h1>
          <p>${message}</p>
          <p class="error-hint">Vérifiez que le dossier <code>data/</code> existe à côté de l'application.</p>
          <pre class="error-debug">${debugInfo}</pre>
        </div>
      </div>
    `;
    this.addErrorStyles();
  }

  addErrorStyles() {
    const styles = document.createElement('style');
    styles.textContent = `
      .error-screen {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
      }
      .error-card {
        background: white;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        max-width: 400px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
      }
      .error-icon { font-size: 4rem; margin-bottom: 1rem; }
      .error-card h1 { margin-bottom: 1rem; color: #e74c3c; }
      .error-card p { color: #666; margin-bottom: 1rem; }
      .error-hint { font-size: 0.9rem; background: #f5f5f5; padding: 1rem; border-radius: 8px; }
      .error-hint code { background: #e0e0e0; padding: 0.2rem 0.5rem; border-radius: 4px; }
      .error-debug { text-align: left; background: #2d2d2d; color: #0f0; padding: 1rem; border-radius: 8px; font-size: 0.8rem; overflow-x: auto; margin-top: 1rem; white-space: pre-wrap; word-break: break-all; }
    `;
    document.head.appendChild(styles);
  }

  /**
   * Rendu du layout principal
   */
  renderLayout() {
    const currentFile = db.getCurrentFile();
    const dataDir = db.getDataDirectory();

    const appHtml = `
      <div class="app-container">
        <header class="app-header">
          <div class="app-header-left">
            <h1>🎯 Prompt Manager</h1>
            <div class="file-selector">
              <select id="file-select" title="Fichier actif">
                ${this.files.length === 0 ? '<option value="">Aucun fichier</option>' : ''}
                ${this.files.map(f => `
                  <option value="${f.name}" ${f.name === currentFile ? 'selected' : ''}>
                    📄 ${f.name.replace('.json', '')}
                  </option>
                `).join('')}
              </select>
              <button class="btn-icon" id="btn-new-file" title="Nouveau fichier">➕</button>
              <button class="btn-icon" id="btn-delete-file" title="Supprimer ce fichier" ${!currentFile ? 'disabled' : ''}>🗑️</button>
            </div>
          </div>
          <nav class="app-nav">
            <button class="nav-btn active" data-view="prompts">
              📚 Mes Prompts
            </button>
            <button class="nav-btn" data-view="builder">
              🧱 Fabricateur
            </button>
            <button class="nav-btn" data-view="concat">
              🔗 Résumer
            </button>
            <button class="nav-btn" data-view="new">
              ➕ Nouveau
            </button>
            <div class="nav-dropdown">
              <button class="nav-btn nav-dropdown-btn">
                🛠️ Créer ▾
              </button>
              <div class="nav-dropdown-menu">
                <button class="dropdown-item" id="quick-add-brick">🧱 Nouvelle brique</button>
                <button class="dropdown-item" id="quick-add-structure">🏗️ Nouvelle structure</button>
                <hr>
                <button class="dropdown-item" id="quick-manage-bricks">📋 Gérer les briques</button>
                <button class="dropdown-item" id="quick-manage-structures">📋 Gérer les structures</button>
              </div>
            </div>
            <button class="nav-btn" data-view="settings">
              ⚙️
            </button>
          </nav>
        </header>
        <main class="app-content" id="main-content">
          <!-- Contenu dynamique -->
        </main>
      </div>
    `;

    document.body.innerHTML = appHtml;
    this.addFileSelectorStyles();
  }

  addFileSelectorStyles() {
    if (document.getElementById('file-selector-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'file-selector-styles';
    styles.textContent = `
      .file-selector {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-left: 1rem;
      }
      .file-selector select {
        padding: 0.4rem 0.8rem;
        border: 1px solid #ddd;
        border-radius: 6px;
        background: white;
        font-size: 0.9rem;
        cursor: pointer;
        min-width: 150px;
      }
      .file-selector select:focus {
        outline: none;
        border-color: #4361ee;
      }
      .btn-icon {
        padding: 0.4rem 0.6rem;
        border: 1px solid #ddd;
        border-radius: 6px;
        background: white;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.2s;
      }
      .btn-icon:hover:not(:disabled) {
        background: #f0f0f0;
        border-color: #ccc;
      }
      .btn-icon:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      .app-header-left {
        display: flex;
        align-items: center;
      }
      /* Dropdown menu */
      .nav-dropdown {
        position: relative;
        display: inline-block;
      }
      .nav-dropdown-menu {
        display: none;
        position: absolute;
        top: 100%;
        right: 0;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        min-width: 220px;
        z-index: 1000;
        padding: 0.5rem 0;
        margin-top: 0.25rem;
      }
      .nav-dropdown.open .nav-dropdown-menu {
        display: block;
      }
      .nav-dropdown-btn.active {
        background: var(--primary);
        color: white;
      }
      .dropdown-item {
        display: block;
        width: 100%;
        padding: 0.6rem 1rem;
        border: none;
        background: none;
        text-align: left;
        cursor: pointer;
        font-size: 0.9rem;
        color: #333;
        transition: all 0.15s;
      }
      .dropdown-item:hover {
        background: #f0f0f0;
      }
      .nav-dropdown-menu hr {
        margin: 0.5rem 0;
        border: none;
        border-top: 1px solid #eee;
      }
    `;
    document.head.appendChild(styles);
  }

  /**
   * Bind des événements du sélecteur de fichier
   */
  bindFileSelector() {
    const select = document.getElementById('file-select');
    const btnNew = document.getElementById('btn-new-file');
    const btnDelete = document.getElementById('btn-delete-file');

    select?.addEventListener('change', async (e) => {
      const filename = e.target.value;
      if (filename) {
        await db.loadFile(filename);
        const settings = db.getSettings();
        document.documentElement.setAttribute('data-theme', settings.theme || 'light');
        this.showView(this.currentView);
        this.updateDeleteButton();
      }
    });

    btnNew?.addEventListener('click', () => this.showNewFileModal());
    btnDelete?.addEventListener('click', () => this.confirmDeleteFile());
  }

  updateDeleteButton() {
    const btnDelete = document.getElementById('btn-delete-file');
    if (btnDelete) {
      btnDelete.disabled = !db.getCurrentFile();
    }
  }

  /**
   * Modal pour créer un nouveau fichier
   */
  showNewFileModal() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal-card">
        <h2>📄 Nouveau fichier de prompts</h2>
        <div class="form-group">
          <label for="new-file-name">Nom du fichier</label>
          <input type="text" id="new-file-name" placeholder="ex: maths-terminale" autofocus>
          <small>L'extension .json sera ajoutée automatiquement</small>
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" id="modal-cancel">Annuler</button>
          <button class="btn btn-success" id="modal-create">Créer</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    this.addModalStyles();

    const input = modal.querySelector('#new-file-name');
    const btnCancel = modal.querySelector('#modal-cancel');
    const btnCreate = modal.querySelector('#modal-create');

    btnCancel.addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });

    btnCreate.addEventListener('click', async () => {
      const name = input.value.trim();
      if (!name) {
        input.focus();
        return;
      }

      try {
        await db.createFile(name);
        this.files = await db.listFiles();
        this.renderLayout();
        this.bindNavigation();
        this.bindFileSelector();
        this.showView('prompts');
        modal.remove();
        this.showToast(`Fichier "${name}.json" créé !`);
      } catch (err) {
        alert(err.message || 'Erreur lors de la création');
      }
    });

    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') btnCreate.click();
    });
  }

  /**
   * Confirmer la suppression du fichier actif
   */
  confirmDeleteFile() {
    const currentFile = db.getCurrentFile();
    if (!currentFile) return;

    const confirmed = confirm(`Supprimer définitivement "${currentFile}" ?\n\nCette action est irréversible.`);
    if (!confirmed) return;

    this.deleteCurrentFile();
  }

  async deleteCurrentFile() {
    const currentFile = db.getCurrentFile();
    try {
      await db.deleteFile(currentFile);
      this.files = await db.listFiles();

      // Charger un autre fichier s'il en reste
      if (this.files.length > 0) {
        await db.loadFile(this.files[0].name);
      }

      this.renderLayout();
      this.bindNavigation();
      this.bindFileSelector();
      this.showView('prompts');
      this.showToast(`Fichier "${currentFile}" supprimé`);
    } catch (err) {
      alert(err.message || 'Erreur lors de la suppression');
    }
  }

  addModalStyles() {
    if (document.getElementById('modal-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'modal-styles';
    styles.textContent = `
      .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
      }
      .modal-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        min-width: 350px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
      }
      .modal-card h2 {
        margin-bottom: 1.5rem;
      }
      .modal-card .form-group {
        margin-bottom: 1.5rem;
      }
      .modal-card label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
      }
      .modal-card input {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        font-size: 1rem;
      }
      .modal-card input:focus {
        outline: none;
        border-color: #4361ee;
      }
      .modal-card small {
        display: block;
        margin-top: 0.5rem;
        color: #888;
        font-size: 0.85rem;
      }
      .modal-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
      }
    `;
    document.head.appendChild(styles);
  }

  /**
   * Gère la navigation entre les vues
   */
  bindNavigation() {
    document.querySelectorAll('.nav-btn[data-view]').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.dataset.view;
        if (view) this.showView(view);
      });
    });

    // Dropdown menu - toggle on click
    const dropdown = document.querySelector('.nav-dropdown');
    const dropdownBtn = document.querySelector('.nav-dropdown-btn');

    if (dropdownBtn && dropdown) {
      dropdownBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('open');
        dropdownBtn.classList.toggle('active');
      });

      // Fermer quand on clique ailleurs
      document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) {
          dropdown.classList.remove('open');
          dropdownBtn.classList.remove('active');
        }
      });
    }

    // Dropdown menu actions - fermer le menu après action
    const closeDropdown = () => {
      dropdown?.classList.remove('open');
      dropdownBtn?.classList.remove('active');
    };

    const quickAddBrick = document.getElementById('quick-add-brick');
    const quickAddStructure = document.getElementById('quick-add-structure');
    const quickManageBricks = document.getElementById('quick-manage-bricks');
    const quickManageStructures = document.getElementById('quick-manage-structures');

    if (quickAddBrick) {
      quickAddBrick.addEventListener('click', () => { closeDropdown(); this.openBrickModal(); });
    }
    if (quickAddStructure) {
      quickAddStructure.addEventListener('click', () => { closeDropdown(); this.openStructureModal(); });
    }
    if (quickManageBricks) {
      quickManageBricks.addEventListener('click', () => { closeDropdown(); this.openBricksManager(); });
    }
    if (quickManageStructures) {
      quickManageStructures.addEventListener('click', () => { closeDropdown(); this.openStructuresManager(); });
    }
  }

  /**
   * Affiche une vue spécifique
   */
  showView(viewName) {
    // Vérifier qu'un fichier est chargé
    if (!db.getCurrentFile() && viewName !== 'settings') {
      const content = document.getElementById('main-content');
      content.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">📂</div>
          <h2>Aucun fichier sélectionné</h2>
          <p>Créez un nouveau fichier pour commencer à stocker vos prompts.</p>
          <button class="btn btn-primary" id="btn-create-first">➕ Créer mon premier fichier</button>
        </div>
      `;
      document.getElementById('btn-create-first')?.addEventListener('click', () => this.showNewFileModal());
      this.addEmptyStateStyles();
      return;
    }

    this.currentView = viewName;

    // Mettre à jour les boutons de navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === viewName);
    });

    const content = document.getElementById('main-content');

    switch (viewName) {
      case 'prompts':
        content.innerHTML = '<div id="prompt-list-container"></div>';
        this.promptList = new PromptList('prompt-list-container');
        this.promptList.init({
          onEdit: (prompt) => this.editPrompt(prompt),
          onCopy: (prompt) => console.log('Copié:', prompt.id),
          onDelete: (id) => console.log('Supprimé:', id)
        });
        break;

      case 'builder':
        content.innerHTML = '<div id="builder-container"></div>';
        this.builderPanel = new BuilderPanel('builder-container');
        this.builderPanel.init({
          onPromptGenerated: (promptContent, builderValues) => {
            this.saveModal.open(promptContent, {
              onSaved: (prompt) => {
                this.showView('prompts');
              },
              prefill: builderValues  // Pré-remplir avec les valeurs du fabricateur
            });
          }
        });
        break;

      case 'concat':
        content.innerHTML = '<div id="concat-container"></div>';
        this.concatenationPanel = new ConcatenationPanel('concat-container');
        this.concatenationPanel.init();
        break;

      case 'new':
        this.showNewPromptView(content);
        break;

      case 'settings':
        content.innerHTML = '<div id="settings-container"></div>';
        this.settingsPanel = new SettingsPanel('settings-container');
        this.settingsPanel.init({
          onSettingsChanged: () => {
            const settings = db.getSettings();
            document.documentElement.setAttribute('data-theme', settings.theme || 'light');
          }
        });
        break;
    }
  }

  addEmptyStateStyles() {
    if (document.getElementById('empty-state-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'empty-state-styles';
    styles.textContent = `
      .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        text-align: center;
      }
      .empty-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
      }
      .empty-state h2 {
        margin-bottom: 0.5rem;
        color: #333;
      }
      .empty-state p {
        color: #666;
        margin-bottom: 2rem;
      }
    `;
    document.head.appendChild(styles);
  }

  /**
   * Vue pour ajouter un nouveau prompt
   */
  showNewPromptView(content) {
    content.innerHTML = `
      <div class="new-prompt-container" style="max-width: 800px; margin: 0 auto;">
        <div class="card" style="margin-bottom: 1.5rem; text-align: center;">
          <h2>➕ Ajouter un nouveau prompt</h2>
          <p class="hint">Colle ici un prompt que tu as utilisé ou créé</p>
        </div>

        <div class="card">
          <div class="form-group">
            <label for="new-prompt-content">Contenu du prompt</label>
            <textarea id="new-prompt-content" rows="10"
                      placeholder="Colle ton prompt ici..."></textarea>
          </div>
          <div style="display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1rem;">
            <button class="btn btn-secondary" id="cancel-new">Annuler</button>
            <button class="btn btn-success" id="save-new" disabled>💾 Catégoriser et sauvegarder</button>
          </div>
        </div>
      </div>
    `;

    const textarea = content.querySelector('#new-prompt-content');
    const saveBtn = content.querySelector('#save-new');
    const cancelBtn = content.querySelector('#cancel-new');

    textarea.addEventListener('input', () => {
      saveBtn.disabled = !textarea.value.trim();
    });

    cancelBtn.addEventListener('click', () => {
      this.showView('prompts');
    });

    saveBtn.addEventListener('click', () => {
      const promptContent = textarea.value.trim();
      if (promptContent) {
        this.saveModal.open(promptContent, {
          onSaved: (prompt) => {
            this.showView('prompts');
          }
        });
      }
    });

    setTimeout(() => textarea.focus(), 100);
  }

  /**
   * Édite un prompt existant
   */
  editPrompt(prompt) {
    const content = document.getElementById('main-content');
    content.innerHTML = `
      <div class="edit-prompt-container" style="max-width: 800px; margin: 0 auto;">
        <div class="card" style="margin-bottom: 1.5rem;">
          <h2>✏️ Modifier le prompt</h2>
        </div>

        <div class="card">
          <div class="form-group">
            <label for="edit-title">Titre</label>
            <input type="text" id="edit-title" value="${prompt.title || ''}" placeholder="Titre du prompt">
          </div>

          <div class="form-group">
            <label for="edit-content">Contenu</label>
            <textarea id="edit-content" rows="10">${prompt.content}</textarea>
          </div>

          <div class="form-group">
            <label for="edit-description">Description</label>
            <textarea id="edit-description" rows="2"
                      placeholder="Note personnelle">${prompt.description || ''}</textarea>
          </div>

          <div class="form-group">
            <label for="edit-theme">Thème</label>
            <input type="text" id="edit-theme" value="${prompt.theme || ''}" placeholder="Thème ou chapitre">
          </div>

          <div style="display: flex; gap: 1rem; justify-content: flex-end; margin-top: 1rem;">
            <button class="btn btn-secondary" id="cancel-edit">Annuler</button>
            <button class="btn btn-success" id="save-edit">💾 Sauvegarder</button>
          </div>
        </div>
      </div>
    `;

    const cancelBtn = content.querySelector('#cancel-edit');
    const saveBtn = content.querySelector('#save-edit');

    cancelBtn.addEventListener('click', () => {
      this.showView('prompts');
    });

    saveBtn.addEventListener('click', () => {
      const updates = {
        title: content.querySelector('#edit-title').value.trim() || null,
        content: content.querySelector('#edit-content').value.trim(),
        description: content.querySelector('#edit-description').value.trim() || null,
        theme: content.querySelector('#edit-theme').value.trim() || null
      };

      if (updates.content) {
        db.updatePrompt(prompt.id, updates);
        this.showToast('Prompt mis à jour !');
        this.showView('prompts');
      }
    });
  }

  // ===== MODALS BRIQUES/STRUCTURES =====

  /**
   * Extrait les paramètres d'un template
   */
  extractParams(template) {
    const matches = template.match(/\{(\w+)\}/g) || [];
    return [...new Set(matches.map(m => m.slice(1, -1)))];
  }

  /**
   * Ouvre la modal de création/édition de brique
   * @param {Object} existingBrick - Brique existante à modifier
   * @param {boolean} existingBrick.isCustom - true si c'est une brique personnalisée
   * @param {boolean} existingBrick.isDefault - true si c'est une brique par défaut
   */
  openBrickModal(existingBrick = null) {
    const isEdit = !!existingBrick;
    const isDefault = existingBrick?.isDefault === true;
    const isCustom = existingBrick?.isCustom === true;
    const isOverridden = existingBrick?.isOverridden === true;

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <h3>${isEdit ? '✏️ Modifier la brique' : '➕ Nouvelle brique'}</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          ${isDefault ? '<p class="hint" style="color: var(--info); margin-bottom: 1rem;">ℹ️ Modification d\'une brique par défaut. Les changements seront sauvegardés comme personnalisation.</p>' : ''}

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
          <button class="btn btn-success modal-save">Enregistrer</button>
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

      if (isDefault) {
        // Sauvegarder comme override de la brique par défaut
        db.setBrickOverride(existingBrick.id, { label, category, template, params });
        this.showToast('Brique modifiée !');
      } else if (isCustom) {
        // Modifier une brique personnalisée
        db.deleteCustomBrick(existingBrick.id);
        db.addCustomBrick({ label, category, template, params, enabled: true });
        this.showToast('Brique modifiée !');
      } else {
        // Nouvelle brique personnalisée
        db.addCustomBrick({ label, category, template, params, enabled: true });
        this.showToast('Brique créée !');
      }

      modal.remove();

      // Rafraîchir la vue si on est dans les paramètres
      if (this.currentView === 'settings' && this.settingsPanel) {
        this.settingsPanel.render();
      }
    });
  }

  /**
   * Ouvre la modal de création/édition de structure
   */
  openStructureModal(existingStructure = null) {
    const isEdit = !!existingStructure;
    const isDefault = existingStructure?.isDefault === true;
    const isCustom = existingStructure?.isCustom === true;
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
          ${isDefault ? '<p class="hint" style="color: var(--info); margin-bottom: 1rem;">ℹ️ Modification d\'une structure par défaut. Les changements seront sauvegardés comme personnalisation.</p>' : ''}

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
          <button class="btn btn-success modal-save">Enregistrer</button>
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

      if (isDefault) {
        // Sauvegarder comme override de la structure par défaut
        db.setStructureOverride(existingStructure.id, { label, description, icon, bricks });
        this.showToast('Structure modifiée !');
      } else if (isCustom) {
        // Modifier une structure personnalisée
        db.deleteCustomStructure(existingStructure.id);
        db.addCustomStructure({ label, description, icon, bricks, enabled: true });
        this.showToast('Structure modifiée !');
      } else {
        // Nouvelle structure personnalisée
        db.addCustomStructure({ label, description, icon, bricks, enabled: true });
        this.showToast('Structure créée !');
      }

      modal.remove();

      if (this.currentView === 'settings' && this.settingsPanel) {
        this.settingsPanel.render();
      }
    });
  }

  /**
   * Ouvre le gestionnaire de briques (toutes les briques)
   */
  openBricksManager() {
    const customBricks = db.getCustomBricks();
    const brickOverrides = db.getAllBrickOverrides();

    // Construire la liste des briques avec statut
    const allBricks = [
      ...DEFAULT_BRICKS.map(b => {
        const override = brickOverrides[b.id];
        return {
          ...b,
          ...(override || {}),
          isDefault: true,
          isOverridden: !!override
        };
      }),
      ...customBricks.map(b => ({...b, isCustom: true}))
    ];

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>📋 Gérer les briques</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          <div class="manager-toolbar">
            <button class="btn btn-primary" id="manager-add-brick">➕ Nouvelle brique</button>
            <div class="manager-toolbar-right">
              <button class="btn btn-secondary" id="manager-export-bricks">📤 Exporter</button>
              <button class="btn btn-secondary" id="manager-import-bricks">📥 Importer</button>
              <button class="btn btn-danger" id="manager-reset-bricks">🔄 Réinitialiser tout</button>
            </div>
          </div>
          <input type="file" id="import-bricks-file" accept=".json" style="display: none">

          <div class="manager-list">
            ${Object.entries(BRICK_CATEGORIES).map(([catId, cat]) => {
              const catBricks = allBricks.filter(b => b.category === catId);
              if (catBricks.length === 0) return '';
              return `
                <div class="manager-category">
                  <h4 style="color: ${cat.color}">${cat.icon} ${cat.label}</h4>
                  <div class="manager-items">
                    ${catBricks.map(brick => `
                      <div class="manager-item ${brick.isDefault ? (brick.isOverridden ? 'is-overridden' : 'is-default') : 'is-custom'}">
                        <div class="manager-item-info">
                          <strong>${brick.label}</strong>
                          ${brick.isDefault
                            ? (brick.isOverridden
                              ? '<span class="badge-overridden">Modifié</span>'
                              : '<span class="badge-default">Par défaut</span>')
                            : '<span class="badge-custom">Personnalisé</span>'}
                          <div class="manager-item-preview">${brick.template}</div>
                        </div>
                        <div class="manager-item-actions">
                          <button class="btn btn-small btn-secondary manager-edit-brick" data-brick-id="${brick.id}" data-is-default="${brick.isDefault}" data-is-custom="${brick.isCustom || false}">
                            ✏️ Modifier
                          </button>
                          ${brick.isOverridden ? `<button class="btn btn-small btn-warning manager-reset-brick" data-brick-id="${brick.id}" title="Restaurer la version d'origine">↩️</button>` : ''}
                          ${brick.isCustom ? `<button class="btn btn-small btn-danger manager-delete-brick" data-brick-id="${brick.id}">🗑️</button>` : ''}
                        </div>
                      </div>
                    `).join('')}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary modal-close-btn">Fermer</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);
    this.addManagerStyles();

    // Événements
    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('.modal-close-btn').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    modal.querySelector('#manager-add-brick').addEventListener('click', () => {
      modal.remove();
      this.openBrickModal();
    });

    // Export
    modal.querySelector('#manager-export-bricks').addEventListener('click', () => {
      const data = db.exportBricksAndStructures();
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `briques-structures-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      this.showToast('Export réussi !');
    });

    // Import
    const importFile = modal.querySelector('#import-bricks-file');
    modal.querySelector('#manager-import-bricks').addEventListener('click', () => importFile.click());
    importFile.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (evt) => {
          const merge = confirm('Fusionner avec les données existantes ?\n\nOK = Fusionner\nAnnuler = Remplacer');
          if (db.importBricksAndStructures(evt.target.result, merge)) {
            this.showToast('Import réussi !');
            modal.remove();
            this.openBricksManager();
          } else {
            this.showToast('Erreur d\'import');
          }
        };
        reader.readAsText(file);
      }
    });

    // Réinitialiser tout
    modal.querySelector('#manager-reset-bricks').addEventListener('click', () => {
      if (confirm('Réinitialiser TOUTES les briques et structures ?\n\nCela supprimera toutes les modifications et briques personnalisées.')) {
        db.resetAllBricksAndStructures();
        this.showToast('Réinitialisation effectuée');
        modal.remove();
        this.openBricksManager();
      }
    });

    // Modifier une brique
    modal.querySelectorAll('.manager-edit-brick').forEach(btn => {
      btn.addEventListener('click', () => {
        const brickId = btn.dataset.brickId;
        const isDefault = btn.dataset.isDefault === 'true';
        const isCustom = btn.dataset.isCustom === 'true';

        let brick;
        if (isDefault) {
          // Récupérer la brique par défaut avec son éventuel override
          const defaultBrick = DEFAULT_BRICKS.find(b => b.id === brickId);
          const override = brickOverrides[brickId];
          brick = { ...defaultBrick, ...(override || {}), isDefault: true };
        } else {
          brick = customBricks.find(b => b.id === brickId);
          if (brick) brick = { ...brick, isCustom: true };
        }

        if (brick) {
          modal.remove();
          this.openBrickModal(brick);
        }
      });
    });

    // Réinitialiser une brique individuelle
    modal.querySelectorAll('.manager-reset-brick').forEach(btn => {
      btn.addEventListener('click', () => {
        const brickId = btn.dataset.brickId;
        if (confirm('Restaurer cette brique à sa version d\'origine ?')) {
          db.deleteBrickOverride(brickId);
          modal.remove();
          this.openBricksManager();
          this.showToast('Brique restaurée');
        }
      });
    });

    // Supprimer une brique personnalisée
    modal.querySelectorAll('.manager-delete-brick').forEach(btn => {
      btn.addEventListener('click', () => {
        const brickId = btn.dataset.brickId;
        if (confirm('Supprimer cette brique ?')) {
          db.deleteCustomBrick(brickId);
          modal.remove();
          this.openBricksManager();
          this.showToast('Brique supprimée');
        }
      });
    });
  }

  /**
   * Ouvre le gestionnaire de structures (toutes les structures)
   */
  openStructuresManager() {
    const customStructures = db.getCustomStructures();
    const structureOverrides = db.getAllStructureOverrides();
    const allBricks = [...DEFAULT_BRICKS, ...db.getCustomBricks()];

    // Construire la liste des structures avec statut
    const allStructures = [
      ...DEFAULT_STRUCTURES.map(s => {
        const override = structureOverrides[s.id];
        return {
          ...s,
          ...(override || {}),
          isDefault: true,
          isOverridden: !!override
        };
      }),
      ...customStructures.map(s => ({...s, isCustom: true}))
    ];

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>📋 Gérer les structures</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          <div class="manager-toolbar">
            <button class="btn btn-primary" id="manager-add-structure">➕ Nouvelle structure</button>
            <div class="manager-toolbar-right">
              <button class="btn btn-secondary" id="manager-export-structures">📤 Exporter</button>
              <button class="btn btn-secondary" id="manager-import-structures">📥 Importer</button>
              <button class="btn btn-danger" id="manager-reset-structures">🔄 Réinitialiser tout</button>
            </div>
          </div>
          <input type="file" id="import-structures-file" accept=".json" style="display: none">

          <div class="manager-list">
            ${allStructures.map(structure => `
              <div class="manager-item ${structure.isDefault ? (structure.isOverridden ? 'is-overridden' : 'is-default') : 'is-custom'}">
                <div class="manager-item-info">
                  <span style="font-size: 1.5rem; margin-right: 0.5rem;">${structure.icon || '📋'}</span>
                  <strong>${structure.label}</strong>
                  ${structure.isDefault
                    ? (structure.isOverridden
                      ? '<span class="badge-overridden">Modifié</span>'
                      : '<span class="badge-default">Par défaut</span>')
                    : '<span class="badge-custom">Personnalisé</span>'}
                  <div class="manager-item-preview">${structure.description || ''}</div>
                  <div class="manager-item-bricks">
                    ${structure.bricks.map(bId => {
                      const b = allBricks.find(br => br.id === bId);
                      return b ? `<span class="mini-tag">${b.label}</span>` : '';
                    }).join('')}
                  </div>
                </div>
                <div class="manager-item-actions">
                  <button class="btn btn-small btn-secondary manager-edit-structure" data-structure-id="${structure.id}" data-is-default="${structure.isDefault}" data-is-custom="${structure.isCustom || false}">
                    ✏️ Modifier
                  </button>
                  ${structure.isOverridden ? `<button class="btn btn-small btn-warning manager-reset-structure" data-structure-id="${structure.id}" title="Restaurer la version d'origine">↩️</button>` : ''}
                  ${structure.isCustom ? `<button class="btn btn-small btn-danger manager-delete-structure" data-structure-id="${structure.id}">🗑️</button>` : ''}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary modal-close-btn">Fermer</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);
    this.addManagerStyles();

    // Événements
    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('.modal-close-btn').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

    modal.querySelector('#manager-add-structure').addEventListener('click', () => {
      modal.remove();
      this.openStructureModal();
    });

    // Export
    modal.querySelector('#manager-export-structures').addEventListener('click', () => {
      const data = db.exportBricksAndStructures();
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `briques-structures-${new Date().toISOString().split('T')[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
      this.showToast('Export réussi !');
    });

    // Import
    const importFile = modal.querySelector('#import-structures-file');
    modal.querySelector('#manager-import-structures').addEventListener('click', () => importFile.click());
    importFile.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (evt) => {
          const merge = confirm('Fusionner avec les données existantes ?\n\nOK = Fusionner\nAnnuler = Remplacer');
          if (db.importBricksAndStructures(evt.target.result, merge)) {
            this.showToast('Import réussi !');
            modal.remove();
            this.openStructuresManager();
          } else {
            this.showToast('Erreur d\'import');
          }
        };
        reader.readAsText(file);
      }
    });

    // Réinitialiser tout
    modal.querySelector('#manager-reset-structures').addEventListener('click', () => {
      if (confirm('Réinitialiser TOUTES les briques et structures ?\n\nCela supprimera toutes les modifications et briques/structures personnalisées.')) {
        db.resetAllBricksAndStructures();
        this.showToast('Réinitialisation effectuée');
        modal.remove();
        this.openStructuresManager();
      }
    });

    // Modifier une structure
    modal.querySelectorAll('.manager-edit-structure').forEach(btn => {
      btn.addEventListener('click', () => {
        const structureId = btn.dataset.structureId;
        const isDefault = btn.dataset.isDefault === 'true';
        const isCustom = btn.dataset.isCustom === 'true';

        let structure;
        if (isDefault) {
          // Récupérer la structure par défaut avec son éventuel override
          const defaultStructure = DEFAULT_STRUCTURES.find(s => s.id === structureId);
          const override = structureOverrides[structureId];
          structure = { ...defaultStructure, ...(override || {}), isDefault: true };
        } else {
          structure = customStructures.find(s => s.id === structureId);
          if (structure) structure = { ...structure, isCustom: true };
        }

        if (structure) {
          modal.remove();
          this.openStructureModal(structure);
        }
      });
    });

    // Réinitialiser une structure individuelle
    modal.querySelectorAll('.manager-reset-structure').forEach(btn => {
      btn.addEventListener('click', () => {
        const structureId = btn.dataset.structureId;
        if (confirm('Restaurer cette structure à sa version d\'origine ?')) {
          db.deleteStructureOverride(structureId);
          modal.remove();
          this.openStructuresManager();
          this.showToast('Structure restaurée');
        }
      });
    });

    // Supprimer une structure personnalisée
    modal.querySelectorAll('.manager-delete-structure').forEach(btn => {
      btn.addEventListener('click', () => {
        const structureId = btn.dataset.structureId;
        if (confirm('Supprimer cette structure ?')) {
          db.deleteCustomStructure(structureId);
          modal.remove();
          this.openStructuresManager();
          this.showToast('Structure supprimée');
        }
      });
    });
  }

  addManagerStyles() {
    if (document.getElementById('manager-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'manager-styles';
    styles.textContent = `
      .manager-toolbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        gap: 1rem;
        flex-wrap: wrap;
      }
      .manager-toolbar-right {
        display: flex;
        gap: 0.5rem;
      }
      .manager-list {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        max-height: 60vh;
        overflow-y: auto;
      }
      .manager-category h4 {
        margin-bottom: 0.75rem;
        font-size: 1rem;
      }
      .manager-items {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      .manager-item {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        padding: 0.75rem 1rem;
        background: var(--bg-hover);
        border-radius: var(--radius-sm);
        border-left: 3px solid var(--border);
      }
      .manager-item.is-default {
        border-left-color: var(--text-muted);
      }
      .manager-item.is-custom {
        border-left-color: var(--success);
      }
      .manager-item.is-overridden {
        border-left-color: var(--warning, #f39c12);
        background: rgba(243, 156, 18, 0.05);
      }
      .manager-item-info {
        flex: 1;
        min-width: 0;
      }
      .manager-item-info strong {
        margin-right: 0.5rem;
      }
      .manager-item-preview {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .manager-item-bricks {
        display: flex;
        flex-wrap: wrap;
        gap: 0.25rem;
        margin-top: 0.5rem;
      }
      .manager-item-actions {
        display: flex;
        gap: 0.5rem;
        flex-shrink: 0;
      }
      .badge-default, .badge-custom, .badge-overridden {
        display: inline-block;
        padding: 0.15rem 0.4rem;
        border-radius: 3px;
        font-size: 0.7rem;
        vertical-align: middle;
      }
      .badge-default {
        background: var(--text-muted);
        color: white;
      }
      .badge-custom {
        background: var(--success);
        color: white;
      }
      .badge-overridden {
        background: var(--warning, #f39c12);
        color: white;
      }
      .btn-warning {
        background: var(--warning, #f39c12);
        color: white;
        border-color: var(--warning, #f39c12);
      }
      .btn-warning:hover {
        background: #e67e22;
        border-color: #e67e22;
      }
      .mini-tag {
        display: inline-block;
        padding: 0.1rem 0.35rem;
        background: var(--bg-hover);
        border-radius: 3px;
        font-size: 0.75rem;
        color: var(--text-muted);
      }
    `;
    document.head.appendChild(styles);
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

// Démarrer l'application au chargement
document.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});

export { App };
