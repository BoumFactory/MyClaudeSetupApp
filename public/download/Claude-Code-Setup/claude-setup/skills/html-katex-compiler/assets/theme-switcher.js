/**
 * Theme Switcher - Contrôle de l'univers visuel et du mode light/dark
 * Permet de changer dynamiquement le style du document
 *
 * IMPORTANT: Pour le forçage light/dark, on injecte un style qui override
 * les media queries en dupliquant les variables CSS.
 */

(function() {
    'use strict';

    // Configuration des univers disponibles
    const UNIVERSES = {
        'standard': { name: 'Standard', icon: '📚', description: 'Style classique et professionnel' },
        'minimal': { name: 'Minimal', icon: '◻️', description: 'Design épuré et moderne' },
        'paper': { name: 'Cahier', icon: '📓', description: 'Style cahier d\'écolier' },
        'nature': { name: 'Nature', icon: '🌿', description: 'Tons naturels et apaisants' },
        'retro': { name: 'Rétro', icon: '📜', description: 'Style vintage et nostalgique' },
        'manga': { name: 'Manga', icon: '⚡', description: 'Style manga dynamique' },
        'futuriste': { name: 'Futuriste', icon: '🔮', description: 'Style cyberpunk néon' },
        'gaming': { name: 'Gaming', icon: '🎮', description: 'Style jeu vidéo RGB' }
    };

    const STORAGE_KEY_UNIVERSE = 'cours-universe';
    const STORAGE_KEY_THEME = 'cours-theme';

    let currentUniverse = window.DEFAULT_UNIVERSE || 'standard';
    let currentTheme = 'auto'; // 'light', 'dark', 'auto'

    /**
     * Initialise le theme switcher
     */
    function init() {
        loadPreferences();
        injectStyles();
        createControlPanel();
        applyUniverse(currentUniverse);
        applyTheme(currentTheme);

        console.log(`[ThemeSwitcher] Init: univers=${currentUniverse}, theme=${currentTheme}`);
    }

    /**
     * Charge les préférences depuis localStorage
     */
    function loadPreferences() {
        try {
            const savedUniverse = localStorage.getItem(STORAGE_KEY_UNIVERSE);
            const savedTheme = localStorage.getItem(STORAGE_KEY_THEME);

            if (savedUniverse && UNIVERSES[savedUniverse]) {
                currentUniverse = savedUniverse;
            }

            if (savedTheme && ['light', 'dark', 'auto'].includes(savedTheme)) {
                currentTheme = savedTheme;
            }
        } catch (e) {
            console.warn('[ThemeSwitcher] Cannot load preferences:', e);
        }
    }

    /**
     * Sauvegarde les préférences
     */
    function savePreferences() {
        try {
            localStorage.setItem(STORAGE_KEY_UNIVERSE, currentUniverse);
            localStorage.setItem(STORAGE_KEY_THEME, currentTheme);
        } catch (e) {
            console.warn('[ThemeSwitcher] Cannot save preferences:', e);
        }
    }

    /**
     * Injecte les styles CSS du panneau de contrôle
     */
    function injectStyles() {
        const styles = `
            /* === PANNEAU DE CONTROLE === */
            .theme-control-panel {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 100000;
                font-family: system-ui, -apple-system, sans-serif;
            }

            /* Bouton toggle */
            .theme-toggle-btn {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                border: none;
                cursor: pointer;
                font-size: 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                background: #ffffff;
                color: #333;
            }

            .theme-control-panel.dark-mode .theme-toggle-btn {
                background: #2a2a2a;
                color: #fff;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            }

            .theme-toggle-btn:hover {
                transform: scale(1.1);
            }

            /* Panneau deroulant */
            .theme-dropdown {
                position: absolute;
                top: 60px;
                right: 0;
                width: 280px;
                border-radius: 12px;
                padding: 1rem;
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                background: #ffffff;
                border: 1px solid rgba(0,0,0,0.1);
                color: #333;
            }

            .theme-control-panel.dark-mode .theme-dropdown {
                background: #1e1e1e;
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                color: #e8e8e8;
            }

            .theme-dropdown.open {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }

            /* Titre section */
            .theme-section-title {
                font-size: 0.7rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 0.5rem;
                opacity: 0.6;
            }

            /* Toggle Light/Dark/Auto */
            .theme-mode-selector {
                display: flex;
                gap: 0.5rem;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid rgba(128,128,128,0.2);
            }

            .theme-mode-btn {
                flex: 1;
                padding: 0.5rem;
                border: 1px solid rgba(128,128,128,0.3);
                border-radius: 8px;
                background: transparent;
                cursor: pointer;
                font-size: 0.85rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.25rem;
                transition: all 0.2s ease;
                color: inherit;
            }

            .theme-mode-btn:hover {
                border-color: rgba(128,128,128,0.5);
            }

            .theme-mode-btn.active {
                background: rgba(0, 120, 255, 0.1);
                border-color: #0078ff;
                color: #0078ff;
            }

            .theme-control-panel.dark-mode .theme-mode-btn.active {
                background: rgba(100, 180, 255, 0.15);
                border-color: #64b4ff;
                color: #64b4ff;
            }

            .theme-mode-btn span.icon {
                font-size: 1.2rem;
            }

            .theme-mode-btn span.label {
                font-size: 0.7rem;
            }

            /* Grille des univers */
            .theme-universe-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 0.5rem;
            }

            .theme-universe-btn {
                padding: 0.75rem 0.5rem;
                border: 1px solid rgba(128,128,128,0.3);
                border-radius: 8px;
                background: transparent;
                cursor: pointer;
                font-size: 0.85rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.25rem;
                transition: all 0.2s ease;
                color: inherit;
            }

            .theme-universe-btn:hover {
                border-color: rgba(128,128,128,0.5);
                transform: translateY(-2px);
            }

            .theme-universe-btn.active {
                background: rgba(0, 120, 255, 0.1);
                border-color: #0078ff;
            }

            .theme-control-panel.dark-mode .theme-universe-btn.active {
                background: rgba(100, 180, 255, 0.15);
                border-color: #64b4ff;
            }

            .theme-universe-btn span.icon {
                font-size: 1.5rem;
            }

            .theme-universe-btn span.name {
                font-size: 0.75rem;
                font-weight: 500;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .theme-control-panel {
                    top: 10px;
                    right: 10px;
                }

                .theme-toggle-btn {
                    width: 44px;
                    height: 44px;
                    font-size: 1.3rem;
                }

                .theme-dropdown {
                    width: 260px;
                    right: -10px;
                }
            }

            /* Animation de transition pour le body */
            body {
                transition: background-color 0.3s ease, color 0.3s ease;
            }

            /* Print: masquer le panneau */
            @media print {
                .theme-control-panel {
                    display: none !important;
                }
            }
        `;

        const styleSheet = document.createElement('style');
        styleSheet.id = 'theme-switcher-styles';
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }

    /**
     * Cree le panneau de controle
     */
    function createControlPanel() {
        const panel = document.createElement('div');
        panel.className = 'theme-control-panel';
        panel.innerHTML = `
            <button class="theme-toggle-btn" title="Parametres d'affichage">
                <span style="font-size: 1.3rem;">&#9881;</span>
            </button>
            <div class="theme-dropdown">
                <div class="theme-section-title">Mode d'affichage</div>
                <div class="theme-mode-selector">
                    <button class="theme-mode-btn" data-mode="light">
                        <span class="icon">&#9728;</span>
                        <span class="label">Clair</span>
                    </button>
                    <button class="theme-mode-btn" data-mode="dark">
                        <span class="icon">&#9790;</span>
                        <span class="label">Sombre</span>
                    </button>
                    <button class="theme-mode-btn" data-mode="auto">
                        <span class="icon">&#128187;</span>
                        <span class="label">Auto</span>
                    </button>
                </div>

                <div class="theme-section-title">Style visuel</div>
                <div class="theme-universe-grid">
                    ${Object.entries(UNIVERSES).map(([id, data]) => `
                        <button class="theme-universe-btn" data-universe="${id}" title="${data.description}">
                            <span class="icon">${data.icon}</span>
                            <span class="name">${data.name}</span>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        document.body.appendChild(panel);

        // Event listeners
        const toggleBtn = panel.querySelector('.theme-toggle-btn');
        const dropdown = panel.querySelector('.theme-dropdown');

        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('open');
        });

        document.addEventListener('click', (e) => {
            if (!panel.contains(e.target)) {
                dropdown.classList.remove('open');
            }
        });

        // Boutons de mode
        panel.querySelectorAll('.theme-mode-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const mode = btn.dataset.mode;
                applyTheme(mode);
                currentTheme = mode;
                savePreferences();
                updateModeButtons(panel);
            });
        });

        // Boutons d'univers
        panel.querySelectorAll('.theme-universe-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const universe = btn.dataset.universe;
                applyUniverse(universe);
                currentUniverse = universe;
                savePreferences();
                updateUniverseButtons(panel);
                // Re-appliquer le theme car l'univers a ses propres variables
                applyTheme(currentTheme);
            });
        });

        updateModeButtons(panel);
        updateUniverseButtons(panel);
        updatePanelDarkMode(panel);
    }

    /**
     * Met a jour l'etat des boutons de mode
     */
    function updateModeButtons(panel) {
        panel.querySelectorAll('.theme-mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === currentTheme);
        });
    }

    /**
     * Met a jour l'etat des boutons d'univers
     */
    function updateUniverseButtons(panel) {
        panel.querySelectorAll('.theme-universe-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.universe === currentUniverse);
        });
    }

    /**
     * Met a jour le mode sombre du panneau
     */
    function updatePanelDarkMode(panel) {
        const isDark = currentTheme === 'dark' ||
            (currentTheme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        panel.classList.toggle('dark-mode', isDark);
    }

    /**
     * Applique un univers visuel
     */
    function applyUniverse(universe) {
        // Desactiver tous les styles d'univers
        document.querySelectorAll('style[data-universe]').forEach(style => {
            style.disabled = true;
        });

        // Activer le style demande
        const targetStyle = document.querySelector(`style[data-universe="${universe}"]`);
        if (targetStyle) {
            targetStyle.disabled = false;
        }

        // Mettre a jour l'attribut sur le body
        document.body.dataset.universe = universe;

        // Rafraichir le vocabulaire si present
        if (window.VocabularyTooltips && window.VocabularyTooltips.refresh) {
            setTimeout(() => VocabularyTooltips.refresh(), 100);
        }
    }

    /**
     * Applique un mode (light/dark/auto)
     * Pour forcer le mode, on extrait les variables CSS du style actif
     * et on les re-injecte avec les bonnes valeurs.
     */
    function applyTheme(mode) {
        const html = document.documentElement;

        // Supprimer l'ancien style de forcage
        const oldForceStyle = document.getElementById('theme-force-style');
        if (oldForceStyle) {
            oldForceStyle.remove();
        }

        // Determiner si on doit forcer
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const shouldBeDark = mode === 'dark' || (mode === 'auto' && systemDark);

        // Mettre a jour l'attribut data-theme
        if (mode === 'auto') {
            html.removeAttribute('data-theme');
        } else {
            html.setAttribute('data-theme', mode);
        }

        // Si on force un mode different du systeme, injecter un style
        if (mode !== 'auto') {
            const forceStyle = document.createElement('style');
            forceStyle.id = 'theme-force-style';

            if (mode === 'dark' && !systemDark) {
                // Forcer le dark mode - simuler prefers-color-scheme: dark
                forceStyle.textContent = `
                    /* Force dark mode */
                    :root {
                        color-scheme: dark;
                    }
                `;
            } else if (mode === 'light' && systemDark) {
                // Forcer le light mode - override les styles dark
                forceStyle.textContent = `
                    /* Force light mode - reset dark variables */
                    :root {
                        color-scheme: light;
                    }
                `;
            }

            if (forceStyle.textContent.trim()) {
                document.head.appendChild(forceStyle);
            }
        }

        // Recharger le style de l'univers actif pour appliquer le bon mode
        const activeStyle = document.querySelector(`style[data-universe="${currentUniverse}"]`);
        if (activeStyle && mode !== 'auto') {
            // Forcer le recalcul en desactivant/reactivant
            activeStyle.disabled = true;

            // Cloner le contenu et modifier selon le mode
            let cssContent = activeStyle.textContent;

            if (mode === 'light' && systemDark) {
                // On est en systeme dark mais on veut light
                // Supprimer les media queries dark pour ne garder que le light
                cssContent = removeDarkMediaQueries(cssContent);
            } else if (mode === 'dark' && !systemDark) {
                // On est en systeme light mais on veut dark
                // Extraire les regles du @media dark et les appliquer directement
                cssContent = extractAndApplyDarkRules(cssContent);
            }

            // Creer un nouveau style avec le contenu modifie
            const newStyle = document.createElement('style');
            newStyle.id = 'theme-universe-override';
            newStyle.textContent = cssContent;

            // Supprimer l'ancien override s'il existe
            const oldOverride = document.getElementById('theme-universe-override');
            if (oldOverride) oldOverride.remove();

            document.head.appendChild(newStyle);
        } else if (mode === 'auto') {
            // Supprimer l'override et reactiver le style original
            const oldOverride = document.getElementById('theme-universe-override');
            if (oldOverride) oldOverride.remove();

            if (activeStyle) {
                activeStyle.disabled = false;
            }
        }

        // Mettre a jour le panneau
        const panel = document.querySelector('.theme-control-panel');
        if (panel) {
            updatePanelDarkMode(panel);
        }
    }

    /**
     * Supprime les media queries dark du CSS
     */
    function removeDarkMediaQueries(css) {
        // Pattern pour matcher @media (prefers-color-scheme: dark) { ... }
        return css.replace(/@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{([^{}]*(\{[^{}]*\}[^{}]*)*)\}/g, '');
    }

    /**
     * Extrait les regles dark et les applique directement
     */
    function extractAndApplyDarkRules(css) {
        let result = css;

        // Trouver toutes les media queries dark
        const darkMediaRegex = /@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{([\s\S]*?)\}(?=\s*(?:\/\*|@media|$|\n\s*\n))/g;

        let match;
        let darkRules = '';

        // Utiliser une approche plus simple: chercher le pattern et extraire le contenu
        const matches = css.match(/@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{/g);
        if (matches) {
            matches.forEach((m, idx) => {
                const startIdx = css.indexOf(m);
                if (startIdx !== -1) {
                    // Trouver la fin du bloc
                    let braceCount = 1;
                    let i = startIdx + m.length;
                    while (i < css.length && braceCount > 0) {
                        if (css[i] === '{') braceCount++;
                        if (css[i] === '}') braceCount--;
                        i++;
                    }
                    // Extraire le contenu entre les accolades
                    const blockContent = css.substring(startIdx + m.length, i - 1);
                    darkRules += blockContent + '\n';
                }
            });
        }

        // Ajouter les regles dark directement (sans media query)
        if (darkRules) {
            result += '\n/* Dark mode forced */\n' + darkRules;
        }

        return result;
    }

    // Ecouter les changements de preference systeme
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (currentTheme === 'auto') {
            const panel = document.querySelector('.theme-control-panel');
            if (panel) {
                updatePanelDarkMode(panel);
            }
        }
    });

    // Exposer l'API
    window.ThemeSwitcher = {
        init: init,
        setUniverse: applyUniverse,
        setTheme: applyTheme,
        getUniverse: () => currentUniverse,
        getTheme: () => currentTheme,
        UNIVERSES: UNIVERSES
    };

    // Auto-init au chargement
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
