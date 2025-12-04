/**
 * RENDER HELPERS
 * Fonctions utilitaires pour le rendu avancé :
 * - TextBox avec fond pour la lisibilité
 * - Rendu MathJax/LaTeX
 * - Effets de transition
 */

// ==========================================
// CONFIGURATION GLOBALE
// ==========================================

const RenderConfig = {
    // Délai en ms à la fin de chaque scène avant transition
    sceneEndDelay: 1500,

    // Durée des transitions
    transitionDuration: 500,

    // Cache pour les éléments MathJax
    mathCache: new Map()
};

// ==========================================
// TEXT BOX - Boîte de texte avec fond
// ==========================================

/**
 * Dessine du texte dans une boîte avec fond pour la lisibilité
 * @param {CanvasRenderer} renderer - Instance du renderer
 * @param {string} text - Texte à afficher
 * @param {number} x - Coordonnée X (repère math)
 * @param {number} y - Coordonnée Y (repère math)
 * @param {Object} options - Options de style
 */
function drawTextBox(renderer, text, x, y, options = {}) {
    const {
        font = '20px Arial',
        color = '#1e3a8a',
        bgColor = 'rgba(255, 255, 255, 0.92)',
        padding = 12,
        borderRadius = 8,
        align = 'center',
        opacity = 1,
        borderColor = null,
        borderWidth = 0,
        shadow = true,
        maxWidth = null
    } = options;

    const ctx = renderer.ctx;
    const canvasPos = renderer.toPixel(x, y);

    // Appliquer l'opacité globale
    ctx.save();
    ctx.globalAlpha = opacity;

    // Mesurer le texte
    ctx.font = font;
    let textWidth = ctx.measureText(text).width;

    // Gérer le texte multi-lignes si nécessaire
    const lines = text.split('\n');
    const lineHeight = parseInt(font) * 1.3;
    const totalHeight = lines.length * lineHeight;

    // Calculer la largeur max si multi-lignes
    textWidth = Math.max(...lines.map(line => ctx.measureText(line).width));
    if (maxWidth && textWidth > maxWidth) {
        textWidth = maxWidth;
    }

    // Position de la boîte selon l'alignement
    let boxX = canvasPos.x - textWidth / 2 - padding;
    if (align === 'left') {
        boxX = canvasPos.x - padding;
    } else if (align === 'right') {
        boxX = canvasPos.x - textWidth - padding;
    }
    const boxY = canvasPos.y - totalHeight / 2 - padding;
    const boxWidth = textWidth + 2 * padding;
    const boxHeight = totalHeight + 2 * padding;

    // Ombre
    if (shadow) {
        ctx.shadowColor = 'rgba(0, 0, 0, 0.15)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 4;
    }

    // Dessiner le fond
    ctx.fillStyle = bgColor;
    ctx.beginPath();
    if (ctx.roundRect) {
        ctx.roundRect(boxX, boxY, boxWidth, boxHeight, borderRadius);
    } else {
        // Fallback pour navigateurs sans roundRect
        drawRoundRect(ctx, boxX, boxY, boxWidth, boxHeight, borderRadius);
    }
    ctx.fill();

    // Réinitialiser l'ombre pour le texte
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    // Bordure optionnelle
    if (borderColor && borderWidth > 0) {
        ctx.strokeStyle = borderColor;
        ctx.lineWidth = borderWidth;
        ctx.stroke();
    }

    // Dessiner le texte
    ctx.fillStyle = color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    let textX = canvasPos.x;
    if (align === 'left') {
        ctx.textAlign = 'left';
        textX = canvasPos.x;
    } else if (align === 'right') {
        ctx.textAlign = 'right';
        textX = canvasPos.x;
    }

    // Dessiner chaque ligne
    lines.forEach((line, i) => {
        const lineY = canvasPos.y - (totalHeight / 2) + (i + 0.5) * lineHeight;
        ctx.fillText(line, textX, lineY);
    });

    ctx.restore();
}

/**
 * Dessine un rectangle arrondi (fallback)
 */
function drawRoundRect(ctx, x, y, width, height, radius) {
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

// ==========================================
// RESULT BOX - Boîte de résultat mise en valeur
// ==========================================

/**
 * Dessine une boîte de résultat mise en valeur (pour les conclusions)
 * @param {CanvasRenderer} renderer - Instance du renderer
 * @param {string} text - Résultat à afficher
 * @param {number} x - Coordonnée X (repère math)
 * @param {number} y - Coordonnée Y (repère math)
 * @param {Object} options - Options de style
 */
function drawResultBox(renderer, text, x, y, options = {}) {
    const {
        font = 'bold 24px Arial',
        color = '#059669',
        bgColor = 'rgba(209, 250, 229, 0.98)',
        borderColor = '#10b981',
        opacity = 1
    } = options;

    drawTextBox(renderer, text, x, y, {
        font,
        color,
        bgColor,
        padding: 16,
        borderRadius: 10,
        align: 'center',
        opacity,
        borderColor,
        borderWidth: 3,
        shadow: true
    });
}

// ==========================================
// MATHJAX OVERLAY MANAGER
// ==========================================

const MathOverlay = {
    container: null,
    elements: new Map(),      // id -> { element, active }
    renderer: null,
    pendingTypesets: new Set(),
    currentSceneId: null,

    /**
     * Initialise l'overlay MathJax
     */
    init(renderer) {
        this.container = document.getElementById('math-overlay');
        this.renderer = renderer;
        return this;
    },

    /**
     * Debut de frame - marque tous les elements comme inactifs
     */
    beginFrame() {
        this.elements.forEach(data => {
            data.active = false;
        });
    },

    /**
     * Fin de frame - supprime les elements non utilises
     */
    endFrame() {
        const toRemove = [];
        this.elements.forEach((data, id) => {
            if (!data.active) {
                toRemove.push(id);
            }
        });
        toRemove.forEach(id => {
            const data = this.elements.get(id);
            if (data && data.element) {
                data.element.remove();
            }
            this.elements.delete(id);
        });
    },

    /**
     * Efface tous les éléments MathJax (changement de scene)
     */
    clear() {
        if (this.container) {
            this.container.innerHTML = '';
        }
        this.elements.clear();
        this.pendingTypesets.clear();
    },

    /**
     * Affiche une formule LaTeX à une position donnée
     * @param {string} id - Identifiant unique pour l'élément
     * @param {string} latex - Code LaTeX
     * @param {number} x - Coordonnée X (repère math)
     * @param {number} y - Coordonnée Y (repère math)
     * @param {Object} options - Options
     */
    showMath(id, latex, x, y, options = {}) {
        if (!this.container || !this.renderer) return;

        const {
            color = '#1e3a8a',
            fontSize = '1.4em',
            bgColor = 'rgba(255, 255, 255, 0.95)',
            padding = '12px 18px',
            borderRadius = '10px',
            opacity = 1,
            animate = false,
            isResult = false,
            borderColor = null,
            borderWidth = 0,
            shadow = true,
            align = 'center'
        } = options;

        // Convertir en pixels
        const pos = this.renderer.toPixel(x, y);

        // Verifier si l'element existe deja
        let data = this.elements.get(id);
        let element;
        const isNew = !data;

        if (isNew) {
            element = document.createElement('div');
            element.className = 'math-element';
            if (animate) element.classList.add('fade-in');
            if (isResult) element.classList.add('math-result-box');
            element.id = `math-${id}`;
            this.container.appendChild(element);
            data = { element, active: true };
            this.elements.set(id, data);
        } else {
            element = data.element;
            data.active = true; // Marquer comme actif pour cette frame
        }

        // Positionner l'élément
        element.style.left = `${pos.x}px`;
        element.style.top = `${pos.y}px`;
        element.style.opacity = opacity;
        element.style.color = color;
        element.style.fontSize = fontSize;
        element.style.background = bgColor;
        element.style.padding = padding;
        element.style.borderRadius = borderRadius;

        // Bordure optionnelle
        if (borderColor && borderWidth > 0) {
            element.style.border = `${borderWidth}px solid ${borderColor}`;
        }

        // Ombre
        if (shadow) {
            element.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        }

        // Alignement
        if (align === 'left') {
            element.style.transform = 'translateY(-50%)';
        } else if (align === 'right') {
            element.style.transform = 'translate(-100%, -50%)';
        }

        // Mettre à jour le contenu si nécessaire
        const currentLatex = element.getAttribute('data-latex');
        if (currentLatex !== latex) {
            element.setAttribute('data-latex', latex);
            element.innerHTML = `\\(${latex}\\)`;

            // Re-rendre avec MathJax (avec debounce)
            if (window.MathJax && window.MathJax.typesetPromise && !this.pendingTypesets.has(id)) {
                this.pendingTypesets.add(id);
                requestAnimationFrame(() => {
                    if (this.elements.has(id)) {
                        window.MathJax.typesetPromise([element]).then(() => {
                            this.pendingTypesets.delete(id);
                        }).catch(err => {
                            console.warn('MathJax rendering error:', err);
                            this.pendingTypesets.delete(id);
                        });
                    }
                });
            }
        }
    },

    /**
     * Affiche une formule dans une boite mise en valeur (resultat)
     */
    showResult(id, latex, x, y, options = {}) {
        this.showMath(id, latex, x, y, {
            fontSize: '1.6em',
            color: '#059669',
            bgColor: 'rgba(209, 250, 229, 0.98)',
            borderColor: '#10b981',
            borderWidth: 3,
            padding: '14px 22px',
            isResult: true,
            ...options
        });
    },

    /**
     * Cache un element MathJax
     */
    hideMath(id) {
        const data = this.elements.get(id);
        if (data && data.element) {
            data.element.classList.remove('fade-in');
            data.element.classList.add('fade-out');
            setTimeout(() => {
                data.element.remove();
                this.elements.delete(id);
            }, 300);
        }
    },

    /**
     * Met à jour les positions (après resize)
     */
    updatePositions() {
        // Peut être appelé après un redimensionnement
    }
};

// ==========================================
// DRAW MATH BOX - Formule LaTeX avec fond
// ==========================================

/**
 * Affiche une formule LaTeX avec fond via MathJax overlay
 * @param {string} id - Identifiant unique
 * @param {string} latex - Code LaTeX (sans les delimiteurs)
 * @param {number} x - Coordonnée X (repère math)
 * @param {number} y - Coordonnée Y (repère math)
 * @param {Object} options - Options de style
 */
function drawMathBox(id, latex, x, y, options = {}) {
    MathOverlay.showMath(id, latex, x, y, options);
}

/**
 * Affiche un résultat LaTeX mis en valeur
 * @param {string} id - Identifiant unique
 * @param {string} latex - Code LaTeX (sans les delimiteurs)
 * @param {number} x - Coordonnée X (repère math)
 * @param {number} y - Coordonnée Y (repère math)
 * @param {Object} options - Options de style
 */
function drawMathResult(id, latex, x, y, options = {}) {
    MathOverlay.showResult(id, latex, x, y, options);
}

// ==========================================
// GESTIONNAIRE DE TRANSITIONS
// ==========================================

const TransitionManager = {
    transitionElement: null,
    isTransitioning: false,

    init() {
        this.transitionElement = document.getElementById('scene-transition');
        return this;
    },

    /**
     * Affiche une transition vers une nouvelle scène
     * @param {string} title - Titre de la scène
     * @param {string} subtitle - Sous-titre optionnel
     * @param {number} duration - Durée en ms
     */
    show(title, subtitle = '', duration = 1000) {
        if (!this.transitionElement) return Promise.resolve();

        return new Promise(resolve => {
            const content = this.transitionElement.querySelector('.transition-content');
            content.innerHTML = `
                <div class="scene-title">${title}</div>
                ${subtitle ? `<div class="scene-subtitle">${subtitle}</div>` : ''}
            `;

            this.transitionElement.classList.remove('hidden');
            this.transitionElement.classList.add('active');
            this.isTransitioning = true;

            setTimeout(() => {
                this.hide();
                resolve();
            }, duration);
        });
    },

    /**
     * Cache la transition
     */
    hide() {
        if (!this.transitionElement) return;

        this.transitionElement.classList.remove('active');
        this.isTransitioning = false;

        setTimeout(() => {
            if (!this.isTransitioning) {
                this.transitionElement.classList.add('hidden');
            }
        }, 500);
    }
};

// ==========================================
// HELPERS D'ANIMATION AVEC TRANSITION
// ==========================================

/**
 * Calcule la progression effective avec délai de fin
 * @param {number} progress - Progression brute (0-1)
 * @param {number} contentEnd - Quand le contenu finit (0-1), ex: 0.85
 * @returns {Object} { contentProgress, isInDelay, delayProgress }
 */
function getProgressWithDelay(progress, contentEnd = 0.85) {
    if (progress < contentEnd) {
        return {
            contentProgress: progress / contentEnd,
            isInDelay: false,
            delayProgress: 0
        };
    } else {
        return {
            contentProgress: 1,
            isInDelay: true,
            delayProgress: (progress - contentEnd) / (1 - contentEnd)
        };
    }
}

/**
 * Crée un effet de fondu entrant
 * @param {number} progress - Progression (0-1)
 * @param {number} start - Début du fondu
 * @param {number} end - Fin du fondu
 * @param {string} easing - Type d'easing
 */
function fadeIn(progress, start = 0, end = 0.3, easing = 'easeOutQuad') {
    if (progress < start) return 0;
    if (progress > end) return 1;
    const p = (progress - start) / (end - start);
    return MathUtils.ease(p, easing);
}

/**
 * Crée un effet de fondu sortant
 */
function fadeOut(progress, start = 0.7, end = 1, easing = 'easeInQuad') {
    if (progress < start) return 1;
    if (progress > end) return 0;
    const p = (progress - start) / (end - start);
    return 1 - MathUtils.ease(p, easing);
}

/**
 * Crée un effet de glissement vertical
 */
function slideIn(progress, start = 0, end = 0.3, offset = 0.5, easing = 'easeOutCubic') {
    if (progress < start) return offset;
    if (progress > end) return 0;
    const p = (progress - start) / (end - start);
    return offset * (1 - MathUtils.ease(p, easing));
}

// ==========================================
// EXPORTS GLOBAUX
// ==========================================

// Rendre les fonctions disponibles globalement
window.drawTextBox = drawTextBox;
window.drawResultBox = drawResultBox;
window.drawMathBox = drawMathBox;
window.drawMathResult = drawMathResult;
window.MathOverlay = MathOverlay;
window.TransitionManager = TransitionManager;
window.RenderConfig = RenderConfig;
window.getProgressWithDelay = getProgressWithDelay;
window.fadeIn = fadeIn;
window.fadeOut = fadeOut;
window.slideIn = slideIn;
