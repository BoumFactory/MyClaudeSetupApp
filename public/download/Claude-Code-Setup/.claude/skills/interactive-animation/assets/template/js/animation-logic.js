/**
 * ANIMATION LOGIC
 * ================
 * Ce fichier contient la logique spécifique de l'animation.
 * C'est le fichier principal à modifier pour implémenter l'animation.
 *
 * STRUCTURE À SUIVRE:
 * 1. Définir les paramètres spécifiques dans AnimationLogic.params
 * 2. Implémenter setupControls() pour créer les contrôles UI
 * 3. Implémenter update() pour la logique de mise à jour
 * 4. Implémenter render() pour le dessin sur le canvas
 * 5. Implémenter getInfoDisplay() pour les informations affichées
 */

const AnimationLogic = {
    // ==========================================
    // PARAMÈTRES DE L'ANIMATION
    // ==========================================
    params: {
        // === PARAMÈTRES PRINCIPAUX ===
        // Définir ici les paramètres spécifiques à l'animation
        // Exemple:
        // amplitude: 2,
        // frequency: 1,
        // phase: 0,

        // === PARAMÈTRES D'AFFICHAGE ===
        // (gérés automatiquement par Controls)
    },

    // État interne de l'animation
    state: {
        // Variables d'état qui évoluent dans le temps
        // Exemple:
        // time: 0,
        // position: { x: 0, y: 0 },
    },

    // Références aux objets principaux (injectés par main.js)
    renderer: null,
    animation: null,
    controls: null,

    // ==========================================
    // INITIALISATION
    // ==========================================

    /**
     * Initialise l'animation
     * Appelé une fois au démarrage
     */
    init(renderer, animation, controls) {
        this.renderer = renderer;
        this.animation = animation;
        this.controls = controls;

        // Configurer les contrôles spécifiques
        this.setupControls();

        // Initialiser l'état
        this.resetState();

        console.log('[AnimationLogic] Initialized');
    },

    /**
     * Configure les contrôles spécifiques à l'animation
     * Ajouter ici tous les contrôles de la section "Paramètres principaux"
     */
    setupControls() {
        // === EXEMPLE DE CONFIGURATION DE CONTRÔLES ===

        /*
        // Slider pour l'amplitude
        this.controls.addControlGroup('params-principaux', {
            type: 'range',
            id: 'amplitude',
            param: 'amplitude',
            label: 'Amplitude',
            min: 0,
            max: 5,
            step: 0.1,
            default: this.params.amplitude,
            unit: ''
        });

        // Champ numérique pour la fréquence
        this.controls.addControlGroup('params-principaux', {
            type: 'number',
            id: 'frequency',
            param: 'frequency',
            label: 'Fréquence (Hz)',
            min: 0.1,
            max: 10,
            step: 0.1,
            default: this.params.frequency
        });

        // Checkbox pour une option
        this.controls.addControlGroup('params-principaux', {
            type: 'checkbox',
            id: 'show-trace',
            param: 'showTrace',
            label: 'Afficher la trace',
            default: false
        });

        // Select pour un choix multiple
        this.controls.addControlGroup('params-principaux', {
            type: 'select',
            id: 'mode',
            param: 'mode',
            label: 'Mode',
            default: 'normal',
            options: [
                { value: 'normal', label: 'Normal' },
                { value: 'ralenti', label: 'Ralenti' },
                { value: 'rapide', label: 'Rapide' }
            ]
        });
        */

        // === ÉCOUTER LES CHANGEMENTS DE PARAMÈTRES ===
        this.controls.onChange = (param, value, allParams) => {
            this.onParamChange(param, value);
        };
    },

    /**
     * Réinitialise l'état de l'animation
     */
    resetState() {
        this.state = {
            // Réinitialiser toutes les variables d'état
        };
    },

    // ==========================================
    // MISE À JOUR
    // ==========================================

    /**
     * Met à jour l'animation à chaque frame
     * @param {number} deltaTime - Temps écoulé depuis la dernière frame (ms)
     * @param {number} elapsedTime - Temps total écoulé (ms)
     */
    update(deltaTime, elapsedTime) {
        // === LOGIQUE DE MISE À JOUR ===
        // Mettre à jour l'état de l'animation en fonction du temps

        /*
        // Exemple: oscillation sinusoïdale
        const t = elapsedTime / 1000; // Convertir en secondes
        const omega = 2 * Math.PI * this.params.frequency;

        this.state.position = {
            x: this.params.amplitude * MathUtils.cos(omega * t + this.params.phase),
            y: this.params.amplitude * MathUtils.sin(omega * t + this.params.phase)
        };
        */
    },

    /**
     * Appelé quand un paramètre change
     * @param {string} param - Nom du paramètre modifié
     * @param {*} value - Nouvelle valeur
     */
    onParamChange(param, value) {
        // Mettre à jour les paramètres internes
        if (this.params.hasOwnProperty(param)) {
            this.params[param] = value;
        }

        // Actions spécifiques selon le paramètre
        /*
        switch (param) {
            case 'amplitude':
                // Réagir au changement d'amplitude
                break;
            case 'frequency':
                // Réagir au changement de fréquence
                break;
        }
        */
    },

    // ==========================================
    // RENDU
    // ==========================================

    /**
     * Dessine l'animation
     * @param {CanvasRenderer} renderer - Instance du renderer
     */
    render(renderer) {
        // === RENDU PRINCIPAL ===
        // Utiliser les méthodes du renderer pour dessiner

        /*
        // Exemple: dessiner un point qui oscille
        renderer.drawPoint(
            this.state.position.x,
            this.state.position.y,
            {
                radius: 8,
                color: '#2563eb',
                label: 'P'
            }
        );

        // Exemple: dessiner un cercle
        renderer.drawCircle(0, 0, this.params.amplitude, {
            strokeColor: '#94a3b8',
            dashed: true
        });

        // Exemple: dessiner un vecteur
        renderer.drawVector(0, 0, this.state.position.x, this.state.position.y, {
            color: '#ef4444',
            width: 2
        });

        // Exemple: dessiner une fonction
        renderer.drawFunction(x => Math.sin(x), {
            color: '#10b981',
            lineWidth: 2
        });
        */
    },

    // ==========================================
    // AFFICHAGE D'INFORMATIONS
    // ==========================================

    /**
     * Retourne les informations à afficher dans l'overlay
     * @returns {Array} Tableau d'objets { label, value }
     */
    getInfoDisplay() {
        // === INFORMATIONS CONTEXTUELLES ===
        // Retourner les valeurs importantes à afficher

        /*
        return [
            {
                label: 'Position X',
                value: MathUtils.format(this.state.position.x, 2)
            },
            {
                label: 'Position Y',
                value: MathUtils.format(this.state.position.y, 2)
            },
            {
                label: 'Temps',
                value: MathUtils.format(this.animation.getElapsedSeconds(), 1) + ' s'
            }
        ];
        */

        return [];
    },

    /**
     * Retourne le contenu HTML de l'aide
     * @returns {string} HTML de l'aide
     */
    getHelpContent() {
        return `
            <h3>Description</h3>
            <p>
                [Description de l'animation et de son objectif pédagogique]
            </p>

            <h3>Contrôles</h3>
            <ul>
                <li><strong>Paramètres principaux</strong>: [Description des paramètres]</li>
                <li><strong>Options d'affichage</strong>: Personnalisez l'apparence (grille, axes, labels...)</li>
            </ul>

            <h3>Mode Scénarios</h3>
            <p>
                Utilisez l'onglet "Scénarios" pour voir des exemples guidés avec des animations étape par étape.
            </p>

            <h3>Conseils</h3>
            <ul>
                <li>[Conseil 1]</li>
                <li>[Conseil 2]</li>
            </ul>
        `;
    }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnimationLogic;
}
