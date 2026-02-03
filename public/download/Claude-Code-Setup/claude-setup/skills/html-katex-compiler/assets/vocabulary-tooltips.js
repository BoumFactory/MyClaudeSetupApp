/**
 * Systeme d'infobulles de vocabulaire mathematique
 * Detecte automatiquement les termes definis et ajoute des infobulles interactives
 * Support KaTeX pour les formules dans les infobulles
 * STYLES ADAPTES A CHAQUE UNIVERS
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        tooltipDelay: 200,
        tooltipClass: 'vocab-tooltip',
        termClass: 'vocab-term',
        activeClass: 'vocab-active',
        katexOptions: {
            throwOnError: false,
            displayMode: false
        }
    };

    // Styles par univers (seront injectes dynamiquement)
    const UNIVERSE_STYLES = {
        'standard': {
            background: 'linear-gradient(135deg, #3498db 0%, #2980b9 100%)',
            backgroundDark: 'linear-gradient(135deg, #2980b9 0%, #1a5276 100%)',
            textColor: '#ffffff',
            borderColor: '#3498db',
            termColor: '#3498db',
            termColorDark: '#5dade2',
            formulaBg: 'rgba(255,255,255,0.15)',
            formulaBgDark: 'rgba(0,0,0,0.2)'
        },
        'minimal': {
            background: '#1a1a1a',
            backgroundDark: '#0a0a0a',
            textColor: '#f5f5f5',
            borderColor: '#333',
            termColor: '#333',
            termColorDark: '#ccc',
            formulaBg: 'rgba(255,255,255,0.1)',
            formulaBgDark: 'rgba(255,255,255,0.05)'
        },
        'paper': {
            background: 'linear-gradient(135deg, #1e3a5f 0%, #0d1f33 100%)',
            backgroundDark: 'linear-gradient(135deg, #2a4a6a 0%, #1a3050 100%)',
            textColor: '#ffffff',
            borderColor: '#1e3a5f',
            termColor: '#1e3a5f',
            termColorDark: '#6ab0ff',
            formulaBg: 'rgba(255,255,255,0.1)',
            formulaBgDark: 'rgba(255,255,255,0.08)'
        },
        'nature': {
            background: 'linear-gradient(135deg, #2d5016 0%, #1a3009 100%)',
            backgroundDark: 'linear-gradient(135deg, #3d6a1e 0%, #2d5016 100%)',
            textColor: '#ffffff',
            borderColor: '#4a8f44',
            termColor: '#2d5016',
            termColorDark: '#8bc34a',
            formulaBg: 'rgba(255,255,255,0.1)',
            formulaBgDark: 'rgba(255,255,255,0.08)'
        },
        'retro': {
            background: 'linear-gradient(135deg, #5d4e37 0%, #3d3225 100%)',
            backgroundDark: 'linear-gradient(135deg, #4a3f2e 0%, #2d261c 100%)',
            textColor: '#f5e6d3',
            borderColor: '#8b7355',
            termColor: '#5d4e37',
            termColorDark: '#d4a574',
            formulaBg: 'rgba(255,255,255,0.1)',
            formulaBgDark: 'rgba(255,255,255,0.08)'
        },
        'manga': {
            background: 'linear-gradient(135deg, #e63946 0%, #b71c1c 100%)',
            backgroundDark: 'linear-gradient(135deg, #ff5252 0%, #d32f2f 100%)',
            textColor: '#ffffff',
            borderColor: '#e63946',
            termColor: '#e63946',
            termColorDark: '#ff8a80',
            formulaBg: 'rgba(0,0,0,0.2)',
            formulaBgDark: 'rgba(0,0,0,0.3)',
            fontFamily: "'Comic Sans MS', 'Bangers', cursive",
            borderStyle: '3px solid #000'
        },
        'futuriste': {
            background: 'linear-gradient(135deg, rgba(0,20,40,0.95) 0%, rgba(0,40,80,0.95) 100%)',
            backgroundDark: 'linear-gradient(135deg, rgba(0,10,20,0.98) 0%, rgba(0,30,60,0.98) 100%)',
            textColor: '#00ffff',
            borderColor: '#00ffff',
            termColor: '#00ffff',
            termColorDark: '#00ffff',
            formulaBg: 'rgba(0,255,255,0.1)',
            formulaBgDark: 'rgba(0,255,255,0.15)',
            fontFamily: "'Orbitron', 'Rajdhani', sans-serif",
            borderStyle: '1px solid #00ffff',
            boxShadow: '0 0 20px rgba(0,255,255,0.3), inset 0 0 20px rgba(0,255,255,0.1)'
        },
        'gaming': {
            background: 'linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%)',
            backgroundDark: 'linear-gradient(135deg, #0f0f1a 0%, #050510 100%)',
            textColor: '#ffffff',
            borderColor: '#ff00ff',
            termColor: '#ff00ff',
            termColorDark: '#ff66ff',
            formulaBg: 'rgba(255,0,255,0.1)',
            formulaBgDark: 'rgba(255,0,255,0.15)',
            fontFamily: "'Press Start 2P', 'VT323', monospace",
            borderStyle: '2px solid',
            borderImage: 'linear-gradient(90deg, #ff00ff, #00ffff, #ff00ff) 1',
            boxShadow: '0 0 15px rgba(255,0,255,0.4), 0 0 30px rgba(0,255,255,0.2)'
        }
    };

    let vocabulary = null;
    let termIndex = {};
    let currentStyleSheet = null;

    /**
     * Initialise le systeme de vocabulaire
     */
    function init(vocabData) {
        if (!vocabData || !vocabData.terms) {
            console.warn('[Vocabulary] Aucune donnee de vocabulaire fournie');
            return;
        }

        vocabulary = vocabData;
        buildTermIndex();
        injectStyles();
        processDocument();
        setupTooltipEvents();
        setupUniverseListener();

        console.log(`[Vocabulary] ${Object.keys(termIndex).length} termes indexes`);
    }

    /**
     * Construit l'index inverse des termes et synonymes
     */
    function buildTermIndex() {
        termIndex = {};

        for (const [term, data] of Object.entries(vocabulary.terms)) {
            addToIndex(term, term);

            if (data.synonyms && Array.isArray(data.synonyms)) {
                for (const synonym of data.synonyms) {
                    addToIndex(synonym, term);
                }
            }
        }
    }

    function addToIndex(searchTerm, canonicalTerm) {
        const normalized = normalizeText(searchTerm);
        if (!termIndex[normalized]) {
            termIndex[normalized] = canonicalTerm;
        }
    }

    function normalizeText(text) {
        return text.toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .trim();
    }

    /**
     * Detecte l'univers actuel
     */
    function getCurrentUniverse() {
        if (window.ThemeSwitcher && window.ThemeSwitcher.getUniverse) {
            return window.ThemeSwitcher.getUniverse();
        }
        return document.body.dataset.universe || 'standard';
    }

    /**
     * Detecte si on est en mode sombre
     */
    function isDarkMode() {
        if (window.ThemeSwitcher && window.ThemeSwitcher.getTheme) {
            const theme = window.ThemeSwitcher.getTheme();
            if (theme === 'dark') return true;
            if (theme === 'light') return false;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    /**
     * Injecte les styles CSS pour les infobulles
     */
    function injectStyles() {
        updateStyles();
    }

    /**
     * Met a jour les styles selon l'univers actuel
     */
    function updateStyles() {
        const universe = getCurrentUniverse();
        const dark = isDarkMode();
        const style = UNIVERSE_STYLES[universe] || UNIVERSE_STYLES['standard'];

        const bg = dark ? style.backgroundDark : style.background;
        const termColor = dark ? style.termColorDark : style.termColor;
        const formulaBg = dark ? style.formulaBgDark : style.formulaBg;
        const fontFamily = style.fontFamily || "system-ui, -apple-system, sans-serif";
        const borderStyle = style.borderStyle || `1px solid ${style.borderColor}`;
        const boxShadow = style.boxShadow || '0 10px 40px rgba(0,0,0,0.3)';

        const styles = `
            /* === TERMES DE VOCABULAIRE === */
            .${CONFIG.termClass} {
                position: relative;
                text-decoration: underline;
                text-decoration-style: dotted;
                text-decoration-color: ${termColor};
                text-underline-offset: 3px;
                cursor: help;
                transition: all 0.2s ease;
                color: inherit;
            }

            .${CONFIG.termClass}:hover {
                text-decoration-style: solid;
                text-decoration-thickness: 2px;
                text-decoration-color: ${termColor};
            }

            /* === INFOBULLES === */
            .${CONFIG.tooltipClass} {
                position: fixed;
                z-index: 99999;
                max-width: 400px;
                min-width: 250px;
                padding: 1rem 1.2rem;
                border-radius: 12px;
                font-family: ${fontFamily};
                font-size: 0.9rem;
                line-height: 1.6;
                opacity: 0;
                visibility: hidden;
                transform: translateY(8px);
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                pointer-events: none;
                background: ${bg};
                color: ${style.textColor};
                border: ${borderStyle};
                box-shadow: ${boxShadow};
            }

            .${CONFIG.tooltipClass}.visible {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
                pointer-events: auto;
            }

            /* Titre du terme */
            .${CONFIG.tooltipClass}-title {
                font-weight: 600;
                font-size: 1rem;
                margin-bottom: 0.5rem;
                color: inherit;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .${CONFIG.tooltipClass}-title::before {
                content: '\\1F4D6';
                font-size: 1.1rem;
            }

            /* Definition */
            .${CONFIG.tooltipClass}-definition {
                margin-bottom: 0.75rem;
                opacity: 0.95;
            }

            /* Formule */
            .${CONFIG.tooltipClass}-formula {
                background: ${formulaBg};
                padding: 0.75rem 1rem;
                border-radius: 6px;
                text-align: center;
                margin-top: 0.5rem;
                overflow-x: auto;
            }

            .${CONFIG.tooltipClass}-formula .katex {
                font-size: 1.15em;
            }

            /* Categorie */
            .${CONFIG.tooltipClass}-category {
                display: inline-block;
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 0.2rem 0.5rem;
                border-radius: 3px;
                margin-top: 0.5rem;
                opacity: 0.7;
                background: rgba(255,255,255,0.1);
            }

            /* Fleche de l'infobulle */
            .${CONFIG.tooltipClass}::before {
                content: '';
                position: absolute;
                width: 12px;
                height: 12px;
                background: inherit;
                border: inherit;
                border-right: none;
                border-bottom: none;
                transform: rotate(45deg);
            }

            .${CONFIG.tooltipClass}.arrow-top::before {
                bottom: -7px;
                left: 20px;
                transform: rotate(-135deg);
            }

            .${CONFIG.tooltipClass}.arrow-bottom::before {
                top: -7px;
                left: 20px;
                transform: rotate(45deg);
            }

            /* Animation du terme actif */
            .${CONFIG.termClass}.${CONFIG.activeClass} {
                background: rgba(255, 215, 0, 0.2);
                border-radius: 3px;
                padding: 0 2px;
                margin: 0 -2px;
            }
        `;

        // Supprimer l'ancien style
        if (currentStyleSheet) {
            currentStyleSheet.remove();
        }

        // Injecter le nouveau
        const styleSheet = document.createElement('style');
        styleSheet.id = 'vocabulary-tooltip-styles';
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        currentStyleSheet = styleSheet;
    }

    /**
     * Ecoute les changements d'univers et de theme
     */
    function setupUniverseListener() {
        // Observer les changements sur body.dataset.universe
        const observer = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                if (mutation.type === 'attributes' &&
                    (mutation.attributeName === 'data-universe' ||
                     mutation.attributeName === 'data-theme')) {
                    updateStyles();
                }
            }
        });

        observer.observe(document.body, { attributes: true });
        observer.observe(document.documentElement, { attributes: true });

        // Ecouter les changements de preference systeme
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateStyles);
    }

    /**
     * Traite le document pour marquer les termes
     */
    function processDocument() {
        const containers = document.querySelectorAll(
            '.cours-container, .definition, .theoreme, .propriete, ' +
            '.exemple, .methode, .remarque, .exercice, p, li'
        );

        containers.forEach(container => {
            processNode(container);
        });
    }

    /**
     * Traite recursivement un noeud pour marquer les termes
     */
    function processNode(node) {
        if (node.classList && (
            node.classList.contains(CONFIG.tooltipClass) ||
            node.classList.contains(CONFIG.termClass) ||
            node.classList.contains('katex') ||
            node.classList.contains('katex-display')
        )) {
            return;
        }

        const walker = document.createTreeWalker(
            node,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: function(textNode) {
                    const parent = textNode.parentElement;
                    if (!parent) return NodeFilter.FILTER_REJECT;

                    const tagName = parent.tagName.toLowerCase();
                    if (['script', 'style', 'noscript', 'code', 'pre'].includes(tagName)) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    if (parent.closest('.katex, .katex-display')) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    if (parent.classList.contains(CONFIG.termClass)) {
                        return NodeFilter.FILTER_REJECT;
                    }

                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        const textNodes = [];
        let textNode;
        while (textNode = walker.nextNode()) {
            textNodes.push(textNode);
        }

        textNodes.forEach(processTextNode);
    }

    /**
     * Traite un noeud texte pour y inserer les marqueurs de termes
     */
    function processTextNode(textNode) {
        const text = textNode.textContent;
        if (!text || text.trim().length < 2) return;

        const allTerms = Object.keys(termIndex).sort((a, b) => b.length - a.length);
        if (allTerms.length === 0) return;

        const regexPattern = allTerms
            .map(t => escapeRegex(t))
            .join('|');

        const regex = new RegExp(`\\b(${regexPattern})\\b`, 'gi');

        const matches = [];
        let match;
        while ((match = regex.exec(text)) !== null) {
            const normalized = normalizeText(match[1]);
            if (termIndex[normalized]) {
                matches.push({
                    start: match.index,
                    end: match.index + match[1].length,
                    text: match[1],
                    term: termIndex[normalized]
                });
            }
        }

        if (matches.length === 0) return;

        const fragment = document.createDocumentFragment();
        let lastIndex = 0;

        matches.forEach(m => {
            if (m.start > lastIndex) {
                fragment.appendChild(
                    document.createTextNode(text.slice(lastIndex, m.start))
                );
            }

            const span = document.createElement('span');
            span.className = CONFIG.termClass;
            span.dataset.term = m.term;
            span.textContent = m.text;
            fragment.appendChild(span);

            lastIndex = m.end;
        });

        if (lastIndex < text.length) {
            fragment.appendChild(
                document.createTextNode(text.slice(lastIndex))
            );
        }

        textNode.parentNode.replaceChild(fragment, textNode);
    }

    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * Configure les evenements pour les infobulles
     */
    function setupTooltipEvents() {
        const tooltip = document.createElement('div');
        tooltip.className = CONFIG.tooltipClass;
        document.body.appendChild(tooltip);

        let hideTimeout = null;
        let showTimeout = null;
        let currentTerm = null;

        document.addEventListener('mouseenter', (e) => {
            const termElement = e.target.closest(`.${CONFIG.termClass}`);
            if (!termElement) return;

            clearTimeout(hideTimeout);
            clearTimeout(showTimeout);

            showTimeout = setTimeout(() => {
                showTooltip(termElement, tooltip);
                currentTerm = termElement;
                termElement.classList.add(CONFIG.activeClass);
            }, CONFIG.tooltipDelay);
        }, true);

        document.addEventListener('mouseleave', (e) => {
            const termElement = e.target.closest(`.${CONFIG.termClass}`);
            if (!termElement) return;

            clearTimeout(showTimeout);

            hideTimeout = setTimeout(() => {
                hideTooltip(tooltip);
                termElement.classList.remove(CONFIG.activeClass);
                currentTerm = null;
            }, 100);
        }, true);

        tooltip.addEventListener('mouseenter', () => {
            clearTimeout(hideTimeout);
        });

        tooltip.addEventListener('mouseleave', () => {
            hideTimeout = setTimeout(() => {
                hideTooltip(tooltip);
                if (currentTerm) {
                    currentTerm.classList.remove(CONFIG.activeClass);
                    currentTerm = null;
                }
            }, 100);
        });
    }

    /**
     * Affiche l'infobulle pour un terme
     */
    function showTooltip(termElement, tooltip) {
        const termKey = termElement.dataset.term;
        const termData = vocabulary.terms[termKey];

        if (!termData) {
            console.warn(`[Vocabulary] Terme non trouve: ${termKey}`);
            return;
        }

        let html = `
            <div class="${CONFIG.tooltipClass}-title">${capitalize(termKey)}</div>
            <div class="${CONFIG.tooltipClass}-definition">${termData.definition}</div>
        `;

        if (termData.formula) {
            html += `<div class="${CONFIG.tooltipClass}-formula" data-formula="${escapeHtml(termData.formula)}"></div>`;
        }

        if (termData.category) {
            html += `<div class="${CONFIG.tooltipClass}-category">${termData.category}</div>`;
        }

        tooltip.innerHTML = html;

        if (termData.formula && window.katex) {
            const formulaContainer = tooltip.querySelector(`.${CONFIG.tooltipClass}-formula`);
            try {
                katex.render(termData.formula, formulaContainer, CONFIG.katexOptions);
            } catch (e) {
                console.warn(`[Vocabulary] Erreur KaTeX: ${e.message}`);
                formulaContainer.textContent = termData.formula;
            }
        }

        positionTooltip(termElement, tooltip);
        tooltip.classList.add('visible');
    }

    function hideTooltip(tooltip) {
        tooltip.classList.remove('visible');
    }

    function positionTooltip(termElement, tooltip) {
        const rect = termElement.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        const viewportHeight = window.innerHeight;
        const viewportWidth = window.innerWidth;

        let top = rect.top - tooltipRect.height - 12;
        let left = rect.left;
        let arrowClass = 'arrow-top';

        if (top < 10) {
            top = rect.bottom + 12;
            arrowClass = 'arrow-bottom';
        }

        if (left + tooltipRect.width > viewportWidth - 10) {
            left = viewportWidth - tooltipRect.width - 10;
        }
        if (left < 10) {
            left = 10;
        }

        tooltip.style.top = `${top}px`;
        tooltip.style.left = `${left}px`;

        tooltip.classList.remove('arrow-top', 'arrow-bottom');
        tooltip.classList.add(arrowClass);
    }

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Exposer l'API
    window.VocabularyTooltips = {
        init: init,
        refresh: processDocument,
        updateStyles: updateStyles,
        getTerms: () => vocabulary ? vocabulary.terms : null
    };

    // Auto-init si les donnees sont deja presentes
    if (window.VOCABULARY_DATA) {
        document.addEventListener('DOMContentLoaded', () => {
            init(window.VOCABULARY_DATA);
        });
    }

})();
