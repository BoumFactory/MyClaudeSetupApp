/**
 * Composant Liste des Prompts
 * Affiche les prompts stockés avec filtres et actions
 */

import { db } from '../../core/database.js';
import { ACTIONS } from '../../config/actions.js';
import { DEFAULT_SUBJECTS, DEFAULT_LEVELS } from '../../config/subjects.js';

class PromptList {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.filters = {
      action: null,
      subject: null,
      level: null,
      search: ''
    };
    this.onEdit = null;
    this.onCopy = null;
    this.onDelete = null;
  }

  /**
   * Initialise et affiche la liste
   */
  init(options = {}) {
    this.onEdit = options.onEdit || (() => {});
    this.onCopy = options.onCopy || (() => {});
    this.onDelete = options.onDelete || (() => {});
    this.render();
  }

  /**
   * Rendu principal
   */
  render() {
    const prompts = db.getPrompts(this.filters);
    const settings = db.getSettings();

    let html = `
      <div class="prompt-list-container">
        <div class="prompt-list-header">
          <h2>📚 Mes Prompts</h2>
          <div class="prompt-count">${prompts.length} prompt${prompts.length > 1 ? 's' : ''}</div>
        </div>

        <div class="prompt-filters">
          <div class="search-box">
            <input type="text" id="search-input" placeholder="🔍 Rechercher..."
                   value="${this.filters.search}">
          </div>
          <div class="filter-row">
            <select id="filter-action">
              <option value="">Toutes les actions</option>
              ${ACTIONS.filter(a => settings.enabledActions?.includes(a.id))
                .map(a => `<option value="${a.id}" ${this.filters.action === a.id ? 'selected' : ''}>${a.emoji} ${a.label}</option>`)
                .join('')}
            </select>
            <select id="filter-subject">
              <option value="">Toutes les matières</option>
              ${DEFAULT_SUBJECTS.filter(s => settings.enabledSubjects?.includes(s.id))
                .map(s => `<option value="${s.id}" ${this.filters.subject === s.id ? 'selected' : ''}>${s.emoji} ${s.label}</option>`)
                .join('')}
            </select>
            <select id="filter-level">
              <option value="">Tous les niveaux</option>
              ${DEFAULT_LEVELS.filter(l => l.enabled)
                .map(l => `<option value="${l.id}" ${this.filters.level === l.id ? 'selected' : ''}>${l.label}</option>`)
                .join('')}
            </select>
            <button class="btn btn-small" id="clear-filters">✖ Effacer</button>
          </div>
        </div>

        <div class="prompt-list">
          ${prompts.length === 0 ? this.renderEmpty() : prompts.map(p => this.renderPromptCard(p)).join('')}
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    this.bindEvents();
  }

  renderEmpty() {
    return `
      <div class="empty-state">
        <div class="empty-icon">📭</div>
        <h3>Aucun prompt pour le moment</h3>
        <p>Commence par créer ton premier prompt ou utilise le fabricateur !</p>
      </div>
    `;
  }

  renderPromptCard(prompt) {
    const action = ACTIONS.find(a => a.id === prompt.action);
    const subject = DEFAULT_SUBJECTS.find(s => s.id === prompt.subject);
    const level = DEFAULT_LEVELS.find(l => l.id === prompt.level);

    const truncatedContent = prompt.content.length > 150
      ? prompt.content.substring(0, 150) + '...'
      : prompt.content;

    return `
      <div class="prompt-card" data-id="${prompt.id}">
        <div class="prompt-card-header">
          <div class="prompt-tags">
            ${action ? `<span class="tag tag-action">${action.emoji} ${action.label}</span>` : ''}
            ${subject ? `<span class="tag tag-subject">${subject.emoji} ${subject.label}</span>` : ''}
            ${level ? `<span class="tag tag-level">${level.label}</span>` : ''}
          </div>
          <div class="prompt-date">${this.formatDate(prompt.createdAt)}</div>
        </div>
        <div class="prompt-card-body">
          <h4 class="prompt-title">${prompt.title || 'Sans titre'}</h4>
          ${prompt.theme ? `<div class="prompt-theme">📌 ${prompt.theme}</div>` : ''}
          <p class="prompt-preview">${truncatedContent}</p>
          ${prompt.description ? `<p class="prompt-description"><em>${prompt.description}</em></p>` : ''}
        </div>
        <div class="prompt-card-actions">
          <button class="btn btn-small btn-primary copy-btn" data-id="${prompt.id}" title="Copier">
            📋 Copier
          </button>
          <button class="btn btn-small edit-btn" data-id="${prompt.id}" title="Modifier">
            ✏️
          </button>
          <button class="btn btn-small btn-danger delete-btn" data-id="${prompt.id}" title="Supprimer">
            🗑️
          </button>
        </div>
      </div>
    `;
  }

  formatDate(isoDate) {
    const date = new Date(isoDate);
    const now = new Date();
    const diff = now - date;

    if (diff < 86400000) { // Moins de 24h
      return 'Aujourd\'hui';
    } else if (diff < 172800000) { // Moins de 48h
      return 'Hier';
    } else {
      return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
    }
  }

  bindEvents() {
    // Recherche
    const searchInput = this.container.querySelector('#search-input');
    if (searchInput) {
      let searchTimeout;
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          this.filters.search = e.target.value;
          this.render();
        }, 300);
      });
    }

    // Filtres
    const filterAction = this.container.querySelector('#filter-action');
    const filterSubject = this.container.querySelector('#filter-subject');
    const filterLevel = this.container.querySelector('#filter-level');
    const clearFilters = this.container.querySelector('#clear-filters');

    if (filterAction) {
      filterAction.addEventListener('change', (e) => {
        this.filters.action = e.target.value || null;
        this.render();
      });
    }
    if (filterSubject) {
      filterSubject.addEventListener('change', (e) => {
        this.filters.subject = e.target.value || null;
        this.render();
      });
    }
    if (filterLevel) {
      filterLevel.addEventListener('change', (e) => {
        this.filters.level = e.target.value || null;
        this.render();
      });
    }
    if (clearFilters) {
      clearFilters.addEventListener('click', () => {
        this.filters = { action: null, subject: null, level: null, search: '' };
        this.render();
      });
    }

    // Actions sur les cartes
    this.container.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        const prompt = db.getPromptById(id);
        if (prompt) {
          navigator.clipboard.writeText(prompt.content).then(() => {
            this.showToast('Prompt copié !');
            this.onCopy(prompt);
          });
        }
      });
    });

    this.container.querySelectorAll('.edit-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        const prompt = db.getPromptById(id);
        if (prompt) {
          this.onEdit(prompt);
        }
      });
    });

    this.container.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        if (confirm('Supprimer ce prompt ?')) {
          db.deletePrompt(id);
          this.render();
          this.onDelete(id);
        }
      });
    });

    // Clic sur la carte pour voir le détail
    this.container.querySelectorAll('.prompt-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = card.dataset.id;
        const prompt = db.getPromptById(id);
        if (prompt) {
          this.showPromptDetail(prompt);
        }
      });
    });
  }

  showPromptDetail(prompt) {
    const action = ACTIONS.find(a => a.id === prompt.action);
    const subject = DEFAULT_SUBJECTS.find(s => s.id === prompt.subject);
    const level = DEFAULT_LEVELS.find(l => l.id === prompt.level);

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal">
        <div class="modal-header">
          <h3>${prompt.title || 'Prompt'}</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          <div class="prompt-meta">
            ${action ? `<span class="tag tag-action">${action.emoji} ${action.label}</span>` : ''}
            ${subject ? `<span class="tag tag-subject">${subject.emoji} ${subject.label}</span>` : ''}
            ${level ? `<span class="tag tag-level">${level.label}</span>` : ''}
            ${prompt.theme ? `<span class="tag tag-theme">📌 ${prompt.theme}</span>` : ''}
          </div>
          <div class="prompt-content-full">
            <pre>${prompt.content}</pre>
          </div>
          ${prompt.description ? `<p class="prompt-description"><em>${prompt.description}</em></p>` : ''}
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" id="modal-copy">📋 Copier</button>
          <button class="btn btn-secondary" id="modal-close">Fermer</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('#modal-close').addEventListener('click', () => modal.remove());
    modal.querySelector('#modal-copy').addEventListener('click', () => {
      navigator.clipboard.writeText(prompt.content).then(() => {
        this.showToast('Prompt copié !');
        modal.remove();
      });
    });
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
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

  refresh() {
    this.render();
  }
}

export { PromptList };
