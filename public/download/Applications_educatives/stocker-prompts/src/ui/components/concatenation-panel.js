/**
 * Composant Panneau de Concaténation
 * Fournit le prompt pour résumer une conversation IA
 */

import { CONCATENATION_PROMPT, CONCATENATION_VARIANTS } from '../../config/concatenation-prompt.js';

class ConcatenationPanel {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.selectedVariant = 'standard';
  }

  /**
   * Initialise le panneau
   */
  init() {
    this.render();
  }

  /**
   * Rendu principal
   */
  render() {
    const selectedPrompt = CONCATENATION_VARIANTS.find(v => v.id === this.selectedVariant);

    let html = `
      <div class="concatenation-panel">
        <div class="concat-header">
          <h2>🔗 Résumer une conversation</h2>
          <p class="hint">Copie ce prompt et colle-le à la fin de ta conversation avec une IA pour obtenir un résumé de tout ce que tu as demandé.</p>
        </div>

        <div class="concat-section">
          <h3>Choisis le format</h3>
          <div class="variant-selector">
            ${CONCATENATION_VARIANTS.map(v => `
              <button class="variant-btn ${this.selectedVariant === v.id ? 'selected' : ''}"
                      data-variant="${v.id}">
                <strong>${v.label}</strong>
                <span>${v.description}</span>
              </button>
            `).join('')}
          </div>
        </div>

        <div class="concat-section">
          <h3>📋 Prompt à copier</h3>
          <div class="prompt-display">
            <pre id="concat-prompt">${selectedPrompt.prompt}</pre>
          </div>
          <div class="concat-actions">
            <button class="btn btn-primary btn-large" id="copy-concat">
              📋 Copier le prompt
            </button>
          </div>
        </div>

        <div class="concat-section instructions">
          <h3>📖 Comment utiliser ?</h3>
          <ol class="instruction-list">
            <li>
              <span class="step-num">1</span>
              <span class="step-text">Finis ta conversation avec l'IA (ChatGPT, Claude, etc.)</span>
            </li>
            <li>
              <span class="step-num">2</span>
              <span class="step-text">Clique sur "Copier le prompt" ci-dessus</span>
            </li>
            <li>
              <span class="step-num">3</span>
              <span class="step-text">Colle-le dans la conversation avec l'IA</span>
            </li>
            <li>
              <span class="step-num">4</span>
              <span class="step-text">L'IA te donnera un résumé de tout ce que tu as demandé</span>
            </li>
            <li>
              <span class="step-num">5</span>
              <span class="step-text">Copie ce résumé et stocke-le ici pour le réutiliser plus tard !</span>
            </li>
          </ol>
        </div>

        <div class="concat-section tip-box">
          <h4>💡 Astuce</h4>
          <p>Ce prompt fonctionne avec toutes les IA conversationnelles : ChatGPT, Claude, Gemini, Mistral, etc.</p>
          <p>Le résumé obtenu est parfait pour être stocké et réutilisé dans une nouvelle conversation !</p>
        </div>
      </div>
    `;

    this.container.innerHTML = html;
    this.bindEvents();
  }

  bindEvents() {
    // Sélection de variante
    this.container.querySelectorAll('.variant-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.selectedVariant = btn.dataset.variant;
        this.render();
      });
    });

    // Copier
    const copyBtn = this.container.querySelector('#copy-concat');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const selectedPrompt = CONCATENATION_VARIANTS.find(v => v.id === this.selectedVariant);
        navigator.clipboard.writeText(selectedPrompt.prompt).then(() => {
          this.showToast('Prompt copié ! Colle-le dans ta conversation IA');
          copyBtn.textContent = '✓ Copié !';
          setTimeout(() => {
            copyBtn.textContent = '📋 Copier le prompt';
          }, 2000);
        });
      });
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
    }, 3000);
  }
}

export { ConcatenationPanel };
