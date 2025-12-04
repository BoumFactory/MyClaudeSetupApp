/**
 * ANIMATION CORE
 * Gestion de la boucle d'animation, des états et des transitions
 */

class AnimationCore {
    constructor(renderer) {
        this.renderer = renderer;

        // État de l'animation
        this.isRunning = false;
        this.isPaused = false;
        this.animationId = null;

        // Timing
        this.lastTime = 0;
        this.deltaTime = 0;
        this.elapsedTime = 0;
        this.fps = 60;
        this.frameInterval = 1000 / this.fps;

        // Callbacks
        this.onUpdate = null;
        this.onRender = null;

        // Animations programmées
        this.animations = new Map();
        this.animationIdCounter = 0;

        // Transitions
        this.transitions = new Map();

        // Fonctions d'easing
        this.easingFunctions = {
            linear: t => t,
            easeInQuad: t => t * t,
            easeOutQuad: t => t * (2 - t),
            easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
            easeInCubic: t => t * t * t,
            easeOutCubic: t => (--t) * t * t + 1,
            easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
            easeInQuart: t => t * t * t * t,
            easeOutQuart: t => 1 - (--t) * t * t * t,
            easeInOutQuart: t => t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t,
            easeInSine: t => 1 - Math.cos(t * Math.PI / 2),
            easeOutSine: t => Math.sin(t * Math.PI / 2),
            easeInOutSine: t => -(Math.cos(Math.PI * t) - 1) / 2,
            easeInExpo: t => t === 0 ? 0 : Math.pow(2, 10 * t - 10),
            easeOutExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
            easeInOutExpo: t => {
                if (t === 0) return 0;
                if (t === 1) return 1;
                if (t < 0.5) return Math.pow(2, 20 * t - 10) / 2;
                return (2 - Math.pow(2, -20 * t + 10)) / 2;
            },
            easeInElastic: t => {
                if (t === 0) return 0;
                if (t === 1) return 1;
                return -Math.pow(2, 10 * t - 10) * Math.sin((t * 10 - 10.75) * (2 * Math.PI) / 3);
            },
            easeOutElastic: t => {
                if (t === 0) return 0;
                if (t === 1) return 1;
                return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI) / 3) + 1;
            },
            easeOutBounce: t => {
                const n1 = 7.5625;
                const d1 = 2.75;
                if (t < 1 / d1) return n1 * t * t;
                if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
                if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
                return n1 * (t -= 2.625 / d1) * t + 0.984375;
            }
        };
    }

    // ==========================================
    // CONTRÔLE DE LA BOUCLE
    // ==========================================

    start() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.isPaused = false;
        this.lastTime = performance.now();

        this.loop();
    }

    stop() {
        this.isRunning = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }

    pause() {
        this.isPaused = true;
    }

    resume() {
        if (!this.isRunning) {
            this.start();
        } else {
            this.isPaused = false;
            this.lastTime = performance.now();
        }
    }

    toggle() {
        if (this.isPaused) {
            this.resume();
        } else {
            this.pause();
        }
    }

    reset() {
        this.elapsedTime = 0;
        this.animations.clear();
        this.transitions.clear();
    }

    loop() {
        if (!this.isRunning) return;

        this.animationId = requestAnimationFrame(() => this.loop());

        const currentTime = performance.now();
        this.deltaTime = currentTime - this.lastTime;

        // Limiter le frame rate si nécessaire
        if (this.deltaTime < this.frameInterval) return;

        this.lastTime = currentTime - (this.deltaTime % this.frameInterval);

        if (!this.isPaused) {
            this.elapsedTime += this.deltaTime;

            // Mise à jour des animations
            this.updateAnimations();

            // Mise à jour des transitions
            this.updateTransitions();

            // Callback de mise à jour personnalisé
            if (this.onUpdate) {
                this.onUpdate(this.deltaTime, this.elapsedTime);
            }
        }

        // Rendu
        this.render();
    }

    render() {
        // Clear et dessiner la grille/axes
        this.renderer.clear();
        this.renderer.drawGrid();
        this.renderer.drawAxes();

        // Callback de rendu personnalisé
        if (this.onRender) {
            this.onRender(this.renderer);
        }
    }

    // ==========================================
    // ANIMATIONS PROGRAMMÉES
    // ==========================================

    /**
     * Crée une animation
     * @param {Object} options Configuration de l'animation
     * @returns {number} ID de l'animation
     */
    animate(options) {
        const {
            from,
            to,
            duration = 1000,
            easing = 'easeInOutQuad',
            delay = 0,
            loop = false,
            yoyo = false,
            onUpdate,
            onComplete
        } = options;

        const id = ++this.animationIdCounter;

        const animation = {
            id,
            from,
            to,
            duration,
            easing: typeof easing === 'function' ? easing : this.easingFunctions[easing],
            delay,
            loop,
            yoyo,
            onUpdate,
            onComplete,
            startTime: this.elapsedTime + delay,
            direction: 1,
            completed: false
        };

        this.animations.set(id, animation);

        return id;
    }

    /**
     * Annule une animation
     */
    cancelAnimation(id) {
        this.animations.delete(id);
    }

    /**
     * Met à jour toutes les animations actives
     */
    updateAnimations() {
        for (const [id, anim] of this.animations) {
            if (anim.completed) continue;

            const elapsed = this.elapsedTime - anim.startTime;

            if (elapsed < 0) continue; // Pas encore démarré (delay)

            let progress = Math.min(elapsed / anim.duration, 1);

            // Appliquer le yoyo
            if (anim.yoyo && anim.direction === -1) {
                progress = 1 - progress;
            }

            // Appliquer l'easing
            const easedProgress = anim.easing(progress);

            // Calculer la valeur interpolée
            const value = this.interpolateValue(anim.from, anim.to, easedProgress);

            // Callback de mise à jour
            if (anim.onUpdate) {
                anim.onUpdate(value, progress);
            }

            // Vérifier si terminé
            if (elapsed >= anim.duration) {
                if (anim.loop) {
                    if (anim.yoyo) {
                        anim.direction *= -1;
                    }
                    anim.startTime = this.elapsedTime;
                } else {
                    anim.completed = true;
                    if (anim.onComplete) {
                        anim.onComplete();
                    }
                    this.animations.delete(id);
                }
            }
        }
    }

    /**
     * Interpole une valeur (supporte nombres, objets, tableaux)
     */
    interpolateValue(from, to, t) {
        // Nombre
        if (typeof from === 'number' && typeof to === 'number') {
            return MathUtils.lerp(from, to, t);
        }

        // Tableau
        if (Array.isArray(from) && Array.isArray(to)) {
            return from.map((v, i) => this.interpolateValue(v, to[i], t));
        }

        // Objet
        if (typeof from === 'object' && typeof to === 'object') {
            const result = {};
            for (const key of Object.keys(from)) {
                if (to.hasOwnProperty(key)) {
                    result[key] = this.interpolateValue(from[key], to[key], t);
                }
            }
            return result;
        }

        return from;
    }

    // ==========================================
    // TRANSITIONS SIMPLES
    // ==========================================

    /**
     * Crée une transition simple sur une propriété
     */
    transition(target, property, toValue, duration = 500, easing = 'easeOutQuad') {
        const key = `${target.constructor.name}_${property}`;

        // Annuler transition existante
        if (this.transitions.has(key)) {
            this.transitions.delete(key);
        }

        const fromValue = target[property];

        this.animate({
            from: fromValue,
            to: toValue,
            duration,
            easing,
            onUpdate: (value) => {
                target[property] = value;
            },
            onComplete: () => {
                this.transitions.delete(key);
            }
        });

        this.transitions.set(key, true);
    }

    /**
     * Met à jour les transitions
     */
    updateTransitions() {
        // Géré par updateAnimations
    }

    // ==========================================
    // SÉQUENCES D'ANIMATION
    // ==========================================

    /**
     * Crée une séquence d'animations
     * @param {Array} steps Tableau d'objets d'animation
     * @returns {Promise} Promesse résolue à la fin de la séquence
     */
    sequence(steps) {
        return new Promise(async (resolve) => {
            for (const step of steps) {
                await this.animateAsync(step);
            }
            resolve();
        });
    }

    /**
     * Version async de animate
     */
    animateAsync(options) {
        return new Promise((resolve) => {
            const originalOnComplete = options.onComplete;
            options.onComplete = () => {
                if (originalOnComplete) originalOnComplete();
                resolve();
            };
            this.animate(options);
        });
    }

    /**
     * Attend un délai
     */
    wait(duration) {
        return new Promise(resolve => {
            setTimeout(resolve, duration);
        });
    }

    /**
     * Exécute des animations en parallèle
     */
    parallel(animations) {
        return Promise.all(animations.map(anim => this.animateAsync(anim)));
    }

    // ==========================================
    // UTILITAIRES
    // ==========================================

    setFPS(fps) {
        this.fps = fps;
        this.frameInterval = 1000 / fps;
    }

    getElapsedTime() {
        return this.elapsedTime;
    }

    getElapsedSeconds() {
        return this.elapsedTime / 1000;
    }

    /**
     * Obtient une fonction d'easing par nom
     */
    getEasing(name) {
        return this.easingFunctions[name] || this.easingFunctions.linear;
    }

    /**
     * Ajoute une fonction d'easing personnalisée
     */
    addEasing(name, fn) {
        this.easingFunctions[name] = fn;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AnimationCore;
}
