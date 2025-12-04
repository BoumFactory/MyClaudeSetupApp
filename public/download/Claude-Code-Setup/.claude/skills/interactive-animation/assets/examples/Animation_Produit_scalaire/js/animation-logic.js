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
        x_u: 4,
        y_u: 0,
        x_v: 3,
        y_v: 3,
        showProjection: true,
        formulaMode: 'analytique', // 'geometrique', 'analytique', 'projection'

        // === PARAMÈTRES D'AFFICHAGE ===
        // (gérés automatiquement par Controls)
    },

    // État interne de l'animation
    state: {
        // Valeurs calculées
        normU: 0,
        normV: 0,
        dotProduct: 0,
        angle: 0,
        angleDeg: 0,
        projectionH: { x: 0, y: 0 }
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
        // === VECTEUR U ===
        this.controls.addControlGroup('params-principaux', {
            type: 'range',
            id: 'x_u',
            param: 'x_u',
            label: 'x_u (composante x de u)',
            min: -5,
            max: 5,
            step: 0.5,
            default: this.params.x_u,
            unit: ''
        });

        this.controls.addControlGroup('params-principaux', {
            type: 'range',
            id: 'y_u',
            param: 'y_u',
            label: 'y_u (composante y de u)',
            min: -5,
            max: 5,
            step: 0.5,
            default: this.params.y_u,
            unit: ''
        });

        // === VECTEUR V ===
        this.controls.addControlGroup('params-principaux', {
            type: 'range',
            id: 'x_v',
            param: 'x_v',
            label: 'x_v (composante x de v)',
            min: -5,
            max: 5,
            step: 0.5,
            default: this.params.x_v,
            unit: ''
        });

        this.controls.addControlGroup('params-principaux', {
            type: 'range',
            id: 'y_v',
            param: 'y_v',
            label: 'y_v (composante y de v)',
            min: -5,
            max: 5,
            step: 0.5,
            default: this.params.y_v,
            unit: ''
        });

        // === OPTIONS D'AFFICHAGE ===
        this.controls.addControlGroup('params-principaux', {
            type: 'checkbox',
            id: 'show-projection',
            param: 'showProjection',
            label: 'Afficher la projection',
            default: this.params.showProjection
        });

        this.controls.addControlGroup('params-principaux', {
            type: 'select',
            id: 'formula-mode',
            param: 'formulaMode',
            label: 'Mode de formule',
            default: this.params.formulaMode,
            options: [
                { value: 'geometrique', label: 'Géométrique' },
                { value: 'analytique', label: 'Analytique' },
                { value: 'projection', label: 'Projection' }
            ]
        });

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
        // === CALCULS DES VALEURS ===
        const ux = this.params.x_u;
        const uy = this.params.y_u;
        const vx = this.params.x_v;
        const vy = this.params.y_v;

        // Normes
        this.state.normU = Math.sqrt(ux * ux + uy * uy);
        this.state.normV = Math.sqrt(vx * vx + vy * vy);

        // Produit scalaire
        this.state.dotProduct = ux * vx + uy * vy;

        // Angle (gérer le cas où les vecteurs sont nuls)
        if (this.state.normU > 0.01 && this.state.normV > 0.01) {
            const cosAngle = this.state.dotProduct / (this.state.normU * this.state.normV);
            // Borner entre -1 et 1 pour éviter les erreurs d'arrondi
            this.state.angle = Math.acos(Math.max(-1, Math.min(1, cosAngle)));
            this.state.angleDeg = this.state.angle * 180 / Math.PI;
        } else {
            this.state.angle = 0;
            this.state.angleDeg = 0;
        }

        // Projection de v sur u : H = (u·v / ||u||²) × u
        if (this.state.normU > 0.01) {
            const projScalar = this.state.dotProduct / (this.state.normU * this.state.normU);
            this.state.projectionH = {
                x: projScalar * ux,
                y: projScalar * uy
            };
        } else {
            this.state.projectionH = { x: 0, y: 0 };
        }
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
        const ux = this.params.x_u;
        const uy = this.params.y_u;
        const vx = this.params.x_v;
        const vy = this.params.y_v;

        // === DESSINER LES VECTEURS ===
        // Vecteur u (rouge)
        if (this.state.normU > 0.01) {
            renderer.drawVector(0, 0, ux, uy, {
                color: '#ef4444',
                width: 3
            });
            renderer.drawText('u', ux + 0.3, uy + 0.3, {
                color: '#ef4444',
                font: 'bold 24px Arial'
            });
        }

        // Vecteur v (bleu)
        if (this.state.normV > 0.01) {
            renderer.drawVector(0, 0, vx, vy, {
                color: '#3b82f6',
                width: 3
            });
            renderer.drawText('v', vx + 0.3, vy + 0.3, {
                color: '#3b82f6',
                font: 'bold 24px Arial'
            });
        }

        // === AFFICHER L'ANGLE ===
        if (this.state.normU > 0.01 && this.state.normV > 0.01) {
            // Calculer l'angle de départ (u) et l'angle d'arrivée (v)
            const angleU = Math.atan2(uy, ux);
            const angleV = Math.atan2(vy, vx);

            // Arc entre les deux vecteurs
            let startAngle = Math.min(angleU, angleV);
            let endAngle = Math.max(angleU, angleV);

            // Ajuster si l'arc traverse 0
            if (endAngle - startAngle > Math.PI) {
                [startAngle, endAngle] = [endAngle, startAngle + 2 * Math.PI];
            }

            renderer.drawArc(0, 0, 1, startAngle, endAngle, {
                color: '#10b981',
                lineWidth: 2
            });
        }

        // === PROJECTION ORTHOGONALE ===
        if (this.params.showProjection && this.state.normU > 0.01 && this.state.normV > 0.01) {
            const hx = this.state.projectionH.x;
            const hy = this.state.projectionH.y;

            // Segment perpendiculaire de V vers H
            renderer.drawSegment(vx, vy, hx, hy, {
                color: '#9b59b6',
                width: 2,
                dashed: true
            });

            // Point H
            renderer.drawPoint(hx, hy, {
                radius: 6,
                color: '#9b59b6'
            });
            renderer.drawText('H', hx, hy - 0.5, {
                color: '#9b59b6',
                font: 'bold 20px Arial',
                align: 'center'
            });

            // Vecteur OH
            renderer.drawVector(0, 0, hx, hy, {
                color: '#9b59b6',
                width: 2
            });
        }

        // === FORMULE SELON LE MODE ===
        let formula = '';
        let formulaColor = '#2563eb';

        if (this.state.normU > 0.01 && this.state.normV > 0.01) {
            switch (this.params.formulaMode) {
                case 'geometrique':
                    formula = `u · v = ||u|| × ||v|| × cos(θ) = ${MathUtils.format(this.state.dotProduct, 2)}`;
                    formulaColor = '#10b981';
                    break;
                case 'analytique':
                    formula = `u · v = xu × xv + yu × yv = ${MathUtils.format(this.state.dotProduct, 2)}`;
                    formulaColor = '#3b82f6';
                    break;
                case 'projection':
                    const oh = Math.sqrt(this.state.projectionH.x ** 2 + this.state.projectionH.y ** 2);
                    formula = `u · v = ||u|| × OH = ${MathUtils.format(this.state.dotProduct, 2)}`;
                    formulaColor = '#9b59b6';
                    break;
            }

            renderer.drawText(formula, 0, -5, {
                color: formulaColor,
                font: 'bold 22px Arial',
                align: 'center'
            });
        }
    },

    // ==========================================
    // AFFICHAGE D'INFORMATIONS
    // ==========================================

    /**
     * Retourne les informations à afficher dans l'overlay
     * @returns {Array} Tableau d'objets { label, value }
     */
    getInfoDisplay() {
        const info = [];

        // Coordonnées des vecteurs
        info.push({
            label: 'u',
            value: `(${MathUtils.format(this.params.x_u, 1)}, ${MathUtils.format(this.params.y_u, 1)})`
        });

        info.push({
            label: 'v',
            value: `(${MathUtils.format(this.params.x_v, 1)}, ${MathUtils.format(this.params.y_v, 1)})`
        });

        // Normes
        if (this.state.normU > 0.01) {
            info.push({
                label: '||u||',
                value: MathUtils.format(this.state.normU, 2)
            });
        }

        if (this.state.normV > 0.01) {
            info.push({
                label: '||v||',
                value: MathUtils.format(this.state.normV, 2)
            });
        }

        // Angle
        if (this.state.normU > 0.01 && this.state.normV > 0.01) {
            info.push({
                label: 'Angle θ',
                value: MathUtils.format(this.state.angleDeg, 1) + '°'
            });
        }

        // Produit scalaire avec couleur selon le signe
        if (this.state.normU > 0.01 && this.state.normV > 0.01) {
            let color, interpretation;

            if (Math.abs(this.state.dotProduct) < 0.1) {
                color = '#3b82f6'; // Bleu
                interpretation = 'Angle droit';
            } else if (this.state.dotProduct > 0) {
                color = '#10b981'; // Vert
                interpretation = 'Angle aigu';
            } else {
                color = '#f97316'; // Orange
                interpretation = 'Angle obtus';
            }

            info.push({
                label: 'u · v',
                value: MathUtils.format(this.state.dotProduct, 2),
                color: color,
                bold: true
            });

            info.push({
                label: 'Interprétation',
                value: interpretation,
                color: color
            });
        }

        return info;
    },

    /**
     * Retourne le contenu HTML de l'aide
     * @returns {string} HTML de l'aide
     */
    getHelpContent() {
        return `
            <h3>Description</h3>
            <p>
                Cette animation interactive permet d'explorer le <strong>produit scalaire</strong> entre deux vecteurs.
                Elle présente les trois définitions équivalentes : géométrique, analytique et par projection orthogonale.
            </p>

            <h3>Contrôles</h3>
            <ul>
                <li><strong>x_u, y_u</strong> : Composantes du vecteur u (rouge)</li>
                <li><strong>x_v, y_v</strong> : Composantes du vecteur v (bleu)</li>
                <li><strong>Afficher la projection</strong> : Montre la projection orthogonale de v sur u</li>
                <li><strong>Mode de formule</strong> : Choisir quelle formule afficher (géométrique, analytique ou projection)</li>
                <li><strong>Options d'affichage</strong> : Personnalisez l'apparence (grille, axes, labels...)</li>
            </ul>

            <h3>Mode Animation</h3>
            <p>
                Passez en mode "Animation" pour voir une présentation séquentielle complète :
                introduction, normes, angle, calculs, projection, orthogonalité et récapitulatif.
            </p>

            <h3>Propriétés importantes</h3>
            <ul>
                <li><strong>Formule géométrique</strong> : u · v = ||u|| × ||v|| × cos(θ)</li>
                <li><strong>Formule analytique</strong> : u · v = xu × xv + yu × yv</li>
                <li><strong>Orthogonalité</strong> : u ⊥ v si et seulement si u · v = 0</li>
                <li><strong>Signe du produit scalaire</strong> :
                    <ul>
                        <li>Positif → angle aigu (θ < 90°)</li>
                        <li>Nul → angle droit (θ = 90°)</li>
                        <li>Négatif → angle obtus (θ > 90°)</li>
                    </ul>
                </li>
            </ul>
        `;
    }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnimationLogic;
}
