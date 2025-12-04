/**
 * SCENARIOS
 * Gestion des scénarios d'animation guidés
 * Chaque scénario est une séquence d'étapes avec animations et descriptions
 */

class ScenarioManager {
    constructor(renderer, animation) {
        this.renderer = renderer;
        this.animation = animation;

        // Scénarios disponibles
        this.scenarios = [];

        // État courant
        this.currentScenario = null;
        this.currentStepIndex = 0;
        this.isPlaying = false;
        this.isPaused = false;

        // Contrôles en temps réel pendant le scénario
        this.realtimeParams = {};

        // Éléments DOM
        this.scenarioList = document.getElementById('scenario-list');
        this.scenarioCanvas = document.getElementById('scenario-canvas');
        this.scenarioDescription = document.getElementById('scenario-description');
        this.stepDisplay = document.getElementById('scenario-step');
        this.totalDisplay = document.getElementById('scenario-total');
        this.prevBtn = document.getElementById('scenario-prev');
        this.nextBtn = document.getElementById('scenario-next');

        // Renderer dédié aux scénarios
        if (this.scenarioCanvas) {
            this.scenarioRenderer = new CanvasRenderer('scenario-canvas');
        }

        // Initialisation
        this.init();
    }

    // ==========================================
    // INITIALISATION
    // ==========================================

    init() {
        this.setupNavigation();
        this.setupKeyboardShortcuts();
    }

    setupNavigation() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.previousStep());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.nextStep());
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Seulement si la vue scénarios est active
            const view = document.getElementById('view-scenarios');
            if (!view || !view.classList.contains('active')) return;

            switch (e.key) {
                case 'ArrowLeft':
                    this.previousStep();
                    break;
                case 'ArrowRight':
                    this.nextStep();
                    break;
                case ' ':
                    e.preventDefault();
                    this.togglePlayPause();
                    break;
                case 'r':
                case 'R':
                    this.restartScenario();
                    break;
            }
        });
    }

    // ==========================================
    // GESTION DES SCÉNARIOS
    // ==========================================

    /**
     * Ajoute un scénario
     * @param {Object} scenario Configuration du scénario
     */
    addScenario(scenario) {
        const validatedScenario = {
            id: scenario.id || `scenario-${this.scenarios.length}`,
            title: scenario.title || 'Scénario sans titre',
            description: scenario.description || '',
            level: scenario.level || 'basic', // basic, intermediate, advanced
            steps: scenario.steps || [],
            realtimeControls: scenario.realtimeControls || [],
            onEnter: scenario.onEnter || null,
            onExit: scenario.onExit || null
        };

        this.scenarios.push(validatedScenario);
        this.updateScenarioList();

        return validatedScenario.id;
    }

    /**
     * Définit plusieurs scénarios à la fois
     */
    setScenarios(scenarios) {
        this.scenarios = [];
        scenarios.forEach(s => this.addScenario(s));
    }

    /**
     * Met à jour l'affichage de la liste des scénarios
     */
    updateScenarioList() {
        if (!this.scenarioList) return;

        this.scenarioList.innerHTML = '';

        this.scenarios.forEach((scenario, index) => {
            const item = document.createElement('li');
            item.className = 'scenario-item';
            item.setAttribute('data-scenario-id', scenario.id);

            const badgeClass = {
                basic: 'badge-basic',
                intermediate: 'badge-intermediate',
                advanced: 'badge-advanced'
            }[scenario.level] || 'badge-basic';

            const levelLabel = {
                basic: 'Basique',
                intermediate: 'Intermédiaire',
                advanced: 'Avancé'
            }[scenario.level] || 'Basique';

            item.innerHTML = `
                <div class="scenario-item-title">${scenario.title}</div>
                <div class="scenario-item-desc">${scenario.description}</div>
                <span class="scenario-item-badge ${badgeClass}">${levelLabel}</span>
            `;

            item.addEventListener('click', () => this.selectScenario(scenario.id));

            this.scenarioList.appendChild(item);
        });
    }

    /**
     * Sélectionne et démarre un scénario
     */
    selectScenario(scenarioId) {
        const scenario = this.scenarios.find(s => s.id === scenarioId);
        if (!scenario) return;

        // Mettre à jour l'UI
        document.querySelectorAll('.scenario-item').forEach(item => {
            item.classList.toggle('active', item.getAttribute('data-scenario-id') === scenarioId);
        });

        this.currentScenario = scenario;
        this.currentStepIndex = 0;

        // Callback d'entrée
        if (scenario.onEnter) {
            scenario.onEnter();
        }

        // Configurer les contrôles en temps réel
        this.setupRealtimeControls(scenario.realtimeControls);

        // Afficher la première étape
        this.showStep(0);

        // Démarrer l'animation du scénario
        this.startScenarioAnimation();
    }

    // ==========================================
    // NAVIGATION DANS LES ÉTAPES
    // ==========================================

    showStep(index) {
        if (!this.currentScenario) return;

        const steps = this.currentScenario.steps;
        if (index < 0 || index >= steps.length) return;

        this.currentStepIndex = index;
        const step = steps[index];

        // Mettre à jour l'affichage
        this.updateStepDisplay(step);

        // Mettre à jour les boutons
        if (this.prevBtn) {
            this.prevBtn.disabled = index === 0;
        }
        if (this.nextBtn) {
            this.nextBtn.disabled = index === steps.length - 1;
        }

        // Exécuter l'animation de l'étape
        if (step.animation) {
            this.executeStepAnimation(step);
        }

        // Callback de l'étape
        if (step.onEnter) {
            step.onEnter();
        }
    }

    updateStepDisplay(step) {
        // Numéro de l'étape
        if (this.stepDisplay) {
            this.stepDisplay.textContent = `Étape ${this.currentStepIndex + 1}`;
        }
        if (this.totalDisplay) {
            this.totalDisplay.textContent = this.currentScenario.steps.length;
        }

        // Description
        if (this.scenarioDescription) {
            this.scenarioDescription.innerHTML = `
                <div class="step-title">${step.title || ''}</div>
                <div class="step-content">${step.description || ''}</div>
            `;
        }
    }

    nextStep() {
        if (!this.currentScenario) return;

        const nextIndex = this.currentStepIndex + 1;
        if (nextIndex < this.currentScenario.steps.length) {
            this.showStep(nextIndex);
        }
    }

    previousStep() {
        if (!this.currentScenario) return;

        const prevIndex = this.currentStepIndex - 1;
        if (prevIndex >= 0) {
            this.showStep(prevIndex);
        }
    }

    restartScenario() {
        if (this.currentScenario) {
            this.showStep(0);
        }
    }

    // ==========================================
    // ANIMATIONS DES ÉTAPES
    // ==========================================

    executeStepAnimation(step) {
        if (!step.animation) return;

        const anim = step.animation;

        // Configurer les paramètres initiaux
        if (anim.initialParams) {
            Object.assign(this.realtimeParams, anim.initialParams);
        }

        // Exécuter les animations séquentielles ou parallèles
        if (anim.sequence) {
            this.animation.sequence(anim.sequence);
        } else if (anim.parallel) {
            this.animation.parallel(anim.parallel);
        } else if (anim.animate) {
            this.animation.animate(anim.animate);
        }
    }

    startScenarioAnimation() {
        if (!this.scenarioRenderer) return;

        // Utiliser un renderer et animation dédiés pour les scénarios
        const scenarioAnimation = new AnimationCore(this.scenarioRenderer);

        scenarioAnimation.onUpdate = (dt, elapsed) => {
            this.updateScenarioState(dt, elapsed);
        };

        scenarioAnimation.onRender = (renderer) => {
            this.renderScenario(renderer);
        };

        scenarioAnimation.start();
        this.scenarioAnimation = scenarioAnimation;
    }

    updateScenarioState(deltaTime, elapsedTime) {
        // Mise à jour de l'état du scénario
        // À surcharger dans AnimationLogic si besoin
    }

    renderScenario(renderer) {
        // Rendu du scénario
        // Appeler la méthode de rendu d'AnimationLogic avec les paramètres du scénario
        if (typeof AnimationLogic !== 'undefined' && AnimationLogic.renderScenario) {
            AnimationLogic.renderScenario(renderer, this.currentStepIndex, this.realtimeParams);
        } else if (typeof AnimationLogic !== 'undefined' && AnimationLogic.render) {
            AnimationLogic.render(renderer);
        }
    }

    // ==========================================
    // CONTRÔLES EN TEMPS RÉEL
    // ==========================================

    setupRealtimeControls(controls) {
        const container = document.querySelector('.scenario-realtime-controls');
        if (!container || !controls || controls.length === 0) {
            if (container) container.style.display = 'none';
            return;
        }

        container.style.display = 'block';
        container.innerHTML = '<h4>Ajustements</h4>';

        controls.forEach(ctrl => {
            const div = document.createElement('div');
            div.className = 'realtime-control';

            switch (ctrl.type) {
                case 'range':
                    div.innerHTML = `
                        <label>${ctrl.label}</label>
                        <input type="range"
                               id="rt-${ctrl.param}"
                               min="${ctrl.min || 0}"
                               max="${ctrl.max || 100}"
                               step="${ctrl.step || 1}"
                               value="${ctrl.default || 50}">
                    `;
                    container.appendChild(div);

                    const rangeInput = div.querySelector('input');
                    this.realtimeParams[ctrl.param] = ctrl.default || 50;
                    rangeInput.addEventListener('input', () => {
                        this.realtimeParams[ctrl.param] = parseFloat(rangeInput.value);
                    });
                    break;

                case 'checkbox':
                    div.innerHTML = `
                        <label class="checkbox-label">
                            <input type="checkbox" id="rt-${ctrl.param}" ${ctrl.default ? 'checked' : ''}>
                            <span>${ctrl.label}</span>
                        </label>
                    `;
                    container.appendChild(div);

                    const checkbox = div.querySelector('input');
                    this.realtimeParams[ctrl.param] = ctrl.default || false;
                    checkbox.addEventListener('change', () => {
                        this.realtimeParams[ctrl.param] = checkbox.checked;
                    });
                    break;
            }
        });
    }

    // ==========================================
    // CONTRÔLE LECTURE/PAUSE
    // ==========================================

    togglePlayPause() {
        if (this.scenarioAnimation) {
            if (this.isPaused) {
                this.scenarioAnimation.resume();
                this.isPaused = false;
            } else {
                this.scenarioAnimation.pause();
                this.isPaused = true;
            }
        }
    }

    setSpeed(speed) {
        // 0.5x, 1x, 2x
        if (this.scenarioAnimation) {
            // Ajuster le timing des animations
        }
    }

    // ==========================================
    // UTILITAIRES
    // ==========================================

    getCurrentScenario() {
        return this.currentScenario;
    }

    getCurrentStep() {
        if (!this.currentScenario) return null;
        return this.currentScenario.steps[this.currentStepIndex];
    }

    getRealtimeParams() {
        return { ...this.realtimeParams };
    }
}

// ==========================================
// DÉFINITION DES SCÉNARIOS
// ==========================================

/**
 * SCÉNARIOS À DÉFINIR ICI
 * Ajouter vos scénarios dans cette constante
 */
const SCENARIOS = [
    /*
    // Exemple de scénario basique
    {
        id: 'intro',
        title: 'Introduction',
        description: 'Découverte des concepts de base',
        level: 'basic',
        steps: [
            {
                title: 'Étape 1 - Présentation',
                description: 'Voici le repère orthonormé avec les axes <span class="math-highlight">x</span> et <span class="math-highlight">y</span>.',
                animation: {
                    initialParams: { showGrid: true, showAxes: true }
                }
            },
            {
                title: 'Étape 2 - Un point',
                description: 'Plaçons le point <span class="math-highlight">A(2, 3)</span> dans le repère.',
                animation: {
                    animate: {
                        from: { x: 0, y: 0 },
                        to: { x: 2, y: 3 },
                        duration: 1500,
                        easing: 'easeOutQuad'
                    }
                }
            }
        ],
        realtimeControls: [
            {
                type: 'range',
                param: 'pointSize',
                label: 'Taille du point',
                min: 3,
                max: 15,
                default: 8
            }
        ]
    },

    // Exemple de scénario intermédiaire
    {
        id: 'vectors',
        title: 'Les vecteurs',
        description: 'Construction et manipulation de vecteurs',
        level: 'intermediate',
        steps: [
            // ...
        ]
    },

    // Exemple de scénario avancé
    {
        id: 'transformations',
        title: 'Transformations',
        description: 'Rotations, translations, homothéties',
        level: 'advanced',
        steps: [
            // ...
        ]
    }
    */
];

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ScenarioManager, SCENARIOS };
}
