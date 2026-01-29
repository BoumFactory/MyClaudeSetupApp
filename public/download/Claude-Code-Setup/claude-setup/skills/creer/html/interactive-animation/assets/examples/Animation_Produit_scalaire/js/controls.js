/**
 * CONTROLS
 * Gestion des contrôles UI et des interactions utilisateur
 */

class Controls {
    constructor() {
        // Éléments DOM
        this.controlPanel = document.getElementById('control-panel');
        this.panelToggle = document.getElementById('panel-toggle');

        // État des paramètres
        this.params = {};

        // Callbacks
        this.onChange = null;
        this.onReset = null;

        // Initialisation
        this.init();
    }

    // ==========================================
    // INITIALISATION
    // ==========================================

    init() {
        this.setupPanelToggle();
        this.setupSectionCollapse();
        this.setupMenuTabs();
        this.setupMenuButtons();
        this.setupDefaultControls();
    }

    setupPanelToggle() {
        if (this.panelToggle) {
            this.panelToggle.addEventListener('click', () => {
                this.controlPanel.classList.toggle('collapsed');
            });
        }
    }

    setupSectionCollapse() {
        document.querySelectorAll('.section-title').forEach(title => {
            title.addEventListener('click', () => {
                const isCollapsed = title.getAttribute('data-collapsed') === 'true';
                title.setAttribute('data-collapsed', !isCollapsed);

                const content = title.nextElementSibling;
                if (content) {
                    content.classList.toggle('hidden', !isCollapsed);
                }

                const icon = title.querySelector('.collapse-icon');
                if (icon) {
                    icon.textContent = isCollapsed ? '▼' : '▶';
                }
            });
        });
    }

    setupMenuTabs() {
        const tabs = document.querySelectorAll('.menu-tab');
        const views = document.querySelectorAll('.view-container');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetId = tab.getAttribute('data-tab');

                // Activer l'onglet
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Afficher la vue correspondante
                views.forEach(view => {
                    view.classList.remove('active');
                    if (view.id === `view-${targetId}`) {
                        view.classList.add('active');
                    }
                });

                // Émettre un événement
                this.emitEvent('tabChange', { tab: targetId });
            });
        });
    }

    setupMenuButtons() {
        // Plein écran
        const btnFullscreen = document.getElementById('btn-fullscreen');
        if (btnFullscreen) {
            btnFullscreen.addEventListener('click', () => this.toggleFullscreen());
        }

        // Reset
        const btnReset = document.getElementById('btn-reset');
        if (btnReset) {
            btnReset.addEventListener('click', () => {
                if (this.onReset) this.onReset();
                this.resetToDefaults();
            });
        }

        // Aide
        const btnHelp = document.getElementById('btn-help');
        const helpModal = document.getElementById('help-modal');
        const modalClose = document.getElementById('modal-close');

        if (btnHelp && helpModal) {
            btnHelp.addEventListener('click', () => {
                helpModal.classList.remove('hidden');
            });
        }

        if (modalClose && helpModal) {
            modalClose.addEventListener('click', () => {
                helpModal.classList.add('hidden');
            });

            helpModal.addEventListener('click', (e) => {
                if (e.target === helpModal) {
                    helpModal.classList.add('hidden');
                }
            });
        }
    }

    setupDefaultControls() {
        // Contrôles d'affichage par défaut
        this.bindCheckbox('show-grid', 'showGrid', true);
        this.bindCheckbox('show-axes', 'showAxes', true);
        this.bindCheckbox('show-labels', 'showLabels', true);
        this.bindCheckbox('show-values', 'showValues', true);

        this.bindRange('font-size', 'fontSize', 18, 'font-size-value', 'px');
        this.bindRange('line-width', 'lineWidth', 2, 'line-width-value', 'px');
    }

    // ==========================================
    // LIAISON DES CONTRÔLES
    // ==========================================

    /**
     * Lie une checkbox à un paramètre
     */
    bindCheckbox(elementId, paramName, defaultValue = false) {
        const element = document.getElementById(elementId);
        if (!element) return;

        // Initialiser
        this.params[paramName] = defaultValue;
        element.checked = defaultValue;

        // Écouter les changements
        element.addEventListener('change', () => {
            this.params[paramName] = element.checked;
            this.notifyChange(paramName, element.checked);
        });

        return element;
    }

    /**
     * Lie un input number à un paramètre
     */
    bindNumber(elementId, paramName, defaultValue, options = {}) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const { min, max, step = 1, displayId, unit = '' } = options;

        // Appliquer les limites
        if (min !== undefined) element.min = min;
        if (max !== undefined) element.max = max;
        element.step = step;

        // Initialiser
        this.params[paramName] = defaultValue;
        element.value = defaultValue;
        this.updateDisplay(displayId, defaultValue, unit);

        // Écouter les changements
        element.addEventListener('input', () => {
            let value = parseFloat(element.value);

            // Valider
            if (isNaN(value)) value = defaultValue;
            if (min !== undefined) value = Math.max(min, value);
            if (max !== undefined) value = Math.min(max, value);

            this.params[paramName] = value;
            this.updateDisplay(displayId, value, unit);
            this.notifyChange(paramName, value);
        });

        return element;
    }

    /**
     * Lie un slider (range) à un paramètre
     */
    bindRange(elementId, paramName, defaultValue, displayId = null, unit = '') {
        const element = document.getElementById(elementId);
        if (!element) return;

        // Initialiser
        this.params[paramName] = defaultValue;
        element.value = defaultValue;
        this.updateDisplay(displayId, defaultValue, unit);

        // Écouter les changements
        element.addEventListener('input', () => {
            const value = parseFloat(element.value);
            this.params[paramName] = value;
            this.updateDisplay(displayId, value, unit);
            this.notifyChange(paramName, value);
        });

        return element;
    }

    /**
     * Lie un select à un paramètre
     */
    bindSelect(elementId, paramName, defaultValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        // Initialiser
        this.params[paramName] = defaultValue;
        element.value = defaultValue;

        // Écouter les changements
        element.addEventListener('change', () => {
            this.params[paramName] = element.value;
            this.notifyChange(paramName, element.value);
        });

        return element;
    }

    /**
     * Lie un input text à un paramètre
     */
    bindText(elementId, paramName, defaultValue = '') {
        const element = document.getElementById(elementId);
        if (!element) return;

        // Initialiser
        this.params[paramName] = defaultValue;
        element.value = defaultValue;

        // Écouter les changements
        element.addEventListener('input', () => {
            this.params[paramName] = element.value;
            this.notifyChange(paramName, element.value);
        });

        return element;
    }

    /**
     * Lie un color picker à un paramètre
     */
    bindColor(elementId, paramName, defaultValue = '#000000') {
        const element = document.getElementById(elementId);
        if (!element) return;

        // Initialiser
        this.params[paramName] = defaultValue;
        element.value = defaultValue;

        // Écouter les changements
        element.addEventListener('input', () => {
            this.params[paramName] = element.value;
            this.notifyChange(paramName, element.value);
        });

        return element;
    }

    /**
     * Lie un groupe de radio buttons à un paramètre
     */
    bindRadioGroup(name, paramName, defaultValue) {
        const elements = document.querySelectorAll(`input[name="${name}"]`);
        if (elements.length === 0) return;

        // Initialiser
        this.params[paramName] = defaultValue;
        elements.forEach(el => {
            if (el.value === defaultValue) {
                el.checked = true;
            }
        });

        // Écouter les changements
        elements.forEach(el => {
            el.addEventListener('change', () => {
                if (el.checked) {
                    this.params[paramName] = el.value;
                    this.notifyChange(paramName, el.value);
                }
            });
        });

        return elements;
    }

    // ==========================================
    // CRÉATION DYNAMIQUE DE CONTRÔLES
    // ==========================================

    /**
     * Ajoute un groupe de contrôle à une section
     */
    addControlGroup(sectionId, config) {
        const section = document.getElementById(sectionId);
        if (!section) return;

        const group = document.createElement('div');
        group.className = 'control-group';

        switch (config.type) {
            case 'checkbox':
                group.innerHTML = this.createCheckboxHTML(config);
                section.appendChild(group);
                return this.bindCheckbox(config.id, config.param, config.default);

            case 'number':
                group.innerHTML = this.createNumberHTML(config);
                section.appendChild(group);
                return this.bindNumber(config.id, config.param, config.default, config);

            case 'range':
                group.innerHTML = this.createRangeHTML(config);
                section.appendChild(group);
                return this.bindRange(config.id, config.param, config.default, `${config.id}-value`, config.unit);

            case 'select':
                group.innerHTML = this.createSelectHTML(config);
                section.appendChild(group);
                return this.bindSelect(config.id, config.param, config.default);

            case 'text':
                group.innerHTML = this.createTextHTML(config);
                section.appendChild(group);
                return this.bindText(config.id, config.param, config.default);

            case 'color':
                group.innerHTML = this.createColorHTML(config);
                section.appendChild(group);
                return this.bindColor(config.id, config.param, config.default);
        }
    }

    createCheckboxHTML(config) {
        return `
            <label class="checkbox-label">
                <input type="checkbox" id="${config.id}" ${config.default ? 'checked' : ''}>
                <span>${config.label}</span>
            </label>
        `;
    }

    createNumberHTML(config) {
        const attrs = [];
        if (config.min !== undefined) attrs.push(`min="${config.min}"`);
        if (config.max !== undefined) attrs.push(`max="${config.max}"`);
        if (config.step !== undefined) attrs.push(`step="${config.step}"`);

        return `
            <label for="${config.id}">${config.label}</label>
            <input type="number" id="${config.id}" value="${config.default}" ${attrs.join(' ')}>
        `;
    }

    createRangeHTML(config) {
        return `
            <label for="${config.id}">${config.label}</label>
            <input type="range" id="${config.id}"
                   min="${config.min || 0}"
                   max="${config.max || 100}"
                   step="${config.step || 1}"
                   value="${config.default}">
            <span class="value-display" id="${config.id}-value">${config.default}${config.unit || ''}</span>
        `;
    }

    createSelectHTML(config) {
        const options = config.options.map(opt =>
            `<option value="${opt.value}" ${opt.value === config.default ? 'selected' : ''}>${opt.label}</option>`
        ).join('');

        return `
            <label for="${config.id}">${config.label}</label>
            <select id="${config.id}">${options}</select>
        `;
    }

    createTextHTML(config) {
        return `
            <label for="${config.id}">${config.label}</label>
            <input type="text" id="${config.id}" value="${config.default || ''}"
                   placeholder="${config.placeholder || ''}">
        `;
    }

    createColorHTML(config) {
        return `
            <label for="${config.id}">${config.label}</label>
            <input type="color" id="${config.id}" value="${config.default || '#000000'}">
        `;
    }

    // ==========================================
    // GESTION DE L'ÉTAT
    // ==========================================

    /**
     * Obtient la valeur d'un paramètre
     */
    get(paramName) {
        return this.params[paramName];
    }

    /**
     * Définit la valeur d'un paramètre
     */
    set(paramName, value, updateUI = true) {
        this.params[paramName] = value;

        if (updateUI) {
            // Mettre à jour l'élément UI correspondant
            const element = document.getElementById(paramName.replace(/([A-Z])/g, '-$1').toLowerCase());
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = value;
                } else {
                    element.value = value;
                }
            }
        }

        this.notifyChange(paramName, value);
    }

    /**
     * Obtient tous les paramètres
     */
    getAll() {
        return { ...this.params };
    }

    /**
     * Définit plusieurs paramètres à la fois
     */
    setAll(params) {
        for (const [key, value] of Object.entries(params)) {
            this.set(key, value);
        }
    }

    /**
     * Réinitialise aux valeurs par défaut
     */
    resetToDefaults() {
        // Les valeurs par défaut sont stockées dans les attributs data
        document.querySelectorAll('[data-default]').forEach(el => {
            const defaultValue = el.getAttribute('data-default');
            if (el.type === 'checkbox') {
                el.checked = defaultValue === 'true';
            } else {
                el.value = defaultValue;
            }
            el.dispatchEvent(new Event('input'));
        });
    }

    // ==========================================
    // UTILITAIRES
    // ==========================================

    updateDisplay(displayId, value, unit = '') {
        if (!displayId) return;
        const display = document.getElementById(displayId);
        if (display) {
            display.textContent = MathUtils.format(value, 2) + unit;
        }
    }

    notifyChange(paramName, value) {
        if (this.onChange) {
            this.onChange(paramName, value, this.params);
        }
        this.emitEvent('paramChange', { param: paramName, value, allParams: this.params });
    }

    emitEvent(name, detail) {
        document.dispatchEvent(new CustomEvent(`controls:${name}`, { detail }));
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    /**
     * Active/désactive un groupe de contrôles
     */
    setGroupEnabled(groupId, enabled) {
        const group = document.getElementById(groupId);
        if (group) {
            if (enabled) {
                group.classList.remove('disabled');
            } else {
                group.classList.add('disabled');
            }
        }
    }

    /**
     * Affiche/cache une section
     */
    setSectionVisible(sectionId, visible) {
        const section = document.getElementById(sectionId);
        if (section) {
            const sectionParent = section.closest('.control-section');
            if (sectionParent) {
                sectionParent.style.display = visible ? 'block' : 'none';
            }
        }
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Controls;
}
