/**
 * Scenes - Récupération des scènes depuis le registre
 *
 * Les scènes sont définies dans js/scenarios/*.js
 * Chaque fichier de scène s'enregistre dans window.SCENE_REGISTRY
 *
 * Structure d'une scène :
 * {
 *     id: 'intro',           // Identifiant unique
 *     title: 'Introduction', // Titre affiché
 *     duration: 5000,        // Durée en ms
 *     animate: (localTime, progress, renderer, state) => { ... }
 * }
 */

// Récupérer les scènes du registre (remplies par les fichiers scenarios/*.js)
const SCENES = window.SCENE_REGISTRY || [];

/**
 * Gestionnaire de scènes
 * Coordonne l'exécution des scènes avec la timeline
 */
const SceneManager = {
    scenes: [],
    currentState: {},
    renderer: null,

    /**
     * Initialiser avec les scènes
     */
    init(scenes, renderer) {
        this.scenes = scenes;
        this.renderer = renderer;
        this.currentState = {};
        return this;
    },

    /**
     * Obtenir les scènes formatées pour la timeline
     */
    getScenesForTimeline() {
        return this.scenes.map(scene => ({
            id: scene.id,
            title: scene.title,
            duration: scene.duration
        }));
    },

    /**
     * Rendre la frame actuelle
     * Appelé par la timeline à chaque mise à jour
     */
    render(currentTime, sceneData) {
        if (!this.renderer || !sceneData || !sceneData.scene) return;

        const scene = this.scenes.find(s => s.id === sceneData.scene.id);
        if (!scene || !scene.animate) return;

        // Appeler la fonction d'animation de la scène
        scene.animate(
            sceneData.localTime,
            sceneData.progress,
            this.renderer,
            this.currentState
        );
    },

    /**
     * Réinitialiser l'état
     */
    reset() {
        this.currentState = {};
    }
};

/**
 * Helpers pour créer des animations complexes
 */
const AnimationHelpers = {
    /**
     * Animation de morphing entre deux valeurs
     */
    morph(from, to, progress, easing = 'easeInOutQuad') {
        const t = MathUtils.ease(progress, easing);
        if (typeof from === 'number') {
            return MathUtils.lerp(from, to, t);
        }
        // Pour les objets {x, y}
        return {
            x: MathUtils.lerp(from.x, to.x, t),
            y: MathUtils.lerp(from.y, to.y, t)
        };
    },

    /**
     * Animation séquencée (plusieurs étapes dans une scène)
     * @param progress - Progression totale (0-1)
     * @param steps - Array de {at, duration, fn}
     */
    sequence(progress, steps) {
        const totalDuration = steps.reduce((sum, s) => sum + (s.duration || 1), 0);
        let currentTime = progress * totalDuration;

        for (const step of steps) {
            const stepDuration = step.duration || 1;
            if (currentTime <= stepDuration) {
                const stepProgress = currentTime / stepDuration;
                return step.fn(stepProgress);
            }
            currentTime -= stepDuration;
        }
    },

    /**
     * Délai avant de commencer (retourne 0 puis progress ajusté)
     */
    delay(progress, delayRatio) {
        if (progress < delayRatio) return 0;
        return (progress - delayRatio) / (1 - delayRatio);
    },

    /**
     * Animation qui se répète
     */
    loop(progress, count = 1) {
        return (progress * count) % 1;
    },

    /**
     * Animation qui va et vient
     */
    pingPong(progress) {
        return progress < 0.5
            ? progress * 2
            : 2 - progress * 2;
    },

    /**
     * Apparition progressive (fade in)
     */
    fadeIn(progress, start = 0, end = 0.3) {
        if (progress < start) return 0;
        if (progress > end) return 1;
        return (progress - start) / (end - start);
    },

    /**
     * Disparition progressive (fade out)
     */
    fadeOut(progress, start = 0.7, end = 1) {
        if (progress < start) return 1;
        if (progress > end) return 0;
        return 1 - (progress - start) / (end - start);
    },

    /**
     * Écriture progressive d'un texte
     */
    typewriter(text, progress) {
        const len = Math.floor(text.length * progress);
        return text.substring(0, len);
    },

    /**
     * Tracé progressif d'une courbe (pour les fonctions)
     */
    drawProgressively(fn, progress, renderer, options = {}) {
        const { minX = -5, maxX = 5, color = '#2563eb', lineWidth = 2 } = options;
        const effectiveMaxX = MathUtils.lerp(minX, maxX, progress);

        renderer.drawFunction(fn, {
            minX,
            maxX: effectiveMaxX,
            color,
            lineWidth
        });
    }
};
