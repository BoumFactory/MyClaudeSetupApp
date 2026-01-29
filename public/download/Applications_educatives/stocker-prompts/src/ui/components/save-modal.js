/**
 * Composant Modal de Sauvegarde
 * Affiche le wizard de catégorisation puis sauvegarde le prompt
 */

import { Wizard } from './wizard.js';
import { db } from '../../core/database.js';

class SaveModal {
  constructor() {
    this.modal = null;
    this.promptContent = '';
    this.onSaved = null;
    this.wizard = null;
    this.prefillValues = null;
  }

  /**
   * Ouvre la modal pour sauvegarder un prompt
   * @param {string} promptContent - Le contenu du prompt
   * @param {Object} options - Options
   * @param {Function} options.onSaved - Callback après sauvegarde
   * @param {Object} options.prefill - Valeurs pré-remplies {level, subject, theme}
   */
  open(promptContent, options = {}) {
    this.promptContent = promptContent;
    this.onSaved = options.onSaved || (() => {});
    this.prefillValues = options.prefill || null;

    // Créer la modal
    this.modal = document.createElement('div');
    this.modal.className = 'modal-overlay';
    this.modal.innerHTML = `
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>💾 Sauvegarder le prompt</h3>
          <button class="modal-close">✖</button>
        </div>
        <div class="modal-body">
          <div class="save-modal-content">
            <div class="prompt-preview-section">
              <h4>Prompt à sauvegarder :</h4>
              <div class="prompt-preview-box">
                <pre>${promptContent.length > 300 ? promptContent.substring(0, 300) + '...' : promptContent}</pre>
              </div>
            </div>
            <div class="wizard-section" id="save-wizard"></div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(this.modal);

    // Initialiser le wizard avec les valeurs pré-remplies
    this.wizard = new Wizard('save-wizard');
    this.wizard.start({
      onComplete: (selection) => this.handleWizardComplete(selection),
      onCancel: () => this.close(),
      prefill: this.prefillValues
    });

    // Fermer la modal
    this.modal.querySelector('.modal-close').addEventListener('click', () => this.close());
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });
  }

  /**
   * Gère la fin du wizard
   */
  handleWizardComplete(selection) {
    // Afficher le formulaire de finalisation
    const wizardSection = this.modal.querySelector('.wizard-section');
    wizardSection.innerHTML = `
      <div class="finalize-form">
        <h4>✏️ Informations complémentaires</h4>

        <div class="form-group">
          <label for="prompt-title">Titre (optionnel)</label>
          <input type="text" id="prompt-title" placeholder="Ex: Aide pour résoudre des équations"
                 maxlength="100">
        </div>

        <div class="form-group">
          <label for="prompt-description">Description courte (optionnel)</label>
          <textarea id="prompt-description" rows="2"
                    placeholder="Note personnelle pour te souvenir de ce prompt"></textarea>
        </div>

        <div class="selection-summary">
          <h4>📋 Récapitulatif</h4>
          <div class="summary-tags">
            <span class="tag">${this.wizard.getSelectionLabels().action}</span>
            <span class="tag">${this.wizard.getSelectionLabels().subject}</span>
            <span class="tag">${this.wizard.getSelectionLabels().level}</span>
            ${selection.theme ? `<span class="tag">📌 ${selection.theme}</span>` : ''}
          </div>
        </div>

        <div class="finalize-actions">
          <button class="btn btn-secondary" id="back-to-wizard">← Modifier</button>
          <button class="btn btn-success" id="confirm-save">💾 Sauvegarder</button>
        </div>
      </div>
    `;

    // Événements
    this.modal.querySelector('#back-to-wizard').addEventListener('click', () => {
      this.wizard.currentStep = 0;
      this.wizard.render();
    });

    this.modal.querySelector('#confirm-save').addEventListener('click', () => {
      const title = this.modal.querySelector('#prompt-title').value.trim();
      const description = this.modal.querySelector('#prompt-description').value.trim();

      const prompt = db.addPrompt({
        content: this.promptContent,
        title: title || null,
        description: description || null,
        action: selection.action,
        subject: selection.subject,
        level: selection.level,
        theme: selection.theme || null
      });

      this.showToast('Prompt sauvegardé !');
      this.onSaved(prompt);
      this.close();
    });
  }

  /**
   * Ferme la modal
   */
  close() {
    if (this.modal) {
      this.modal.remove();
      this.modal = null;
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
}

export { SaveModal };
