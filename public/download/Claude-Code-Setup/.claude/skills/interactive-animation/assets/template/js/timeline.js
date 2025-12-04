/**
 * Timeline - Système de lecture d'animations séquentielles
 * Gère la lecture, pause, navigation et synchronisation des scènes
 */

const Timeline = {
    // État de la timeline
    state: {
        isPlaying: false,
        currentTime: 0,      // Temps actuel en ms
        totalDuration: 0,    // Durée totale en ms
        speed: 1,            // Multiplicateur de vitesse
        currentSceneIndex: 0,
        scenes: [],          // Liste des scènes
        lastFrameTime: 0
    },

    // Références DOM
    dom: {
        playBtn: null,
        progressBar: null,
        progressFill: null,
        progressHandle: null,
        timeCurrent: null,
        timeTotal: null,
        scenesBar: null,
        speedBtns: null
    },

    // Callbacks
    callbacks: {
        onTimeUpdate: null,
        onSceneChange: null,
        onPlay: null,
        onPause: null,
        onSeek: null
    },

    /**
     * Initialisation de la timeline
     */
    init(scenes, callbacks = {}) {
        this.state.scenes = scenes || [];
        this.callbacks = { ...this.callbacks, ...callbacks };

        // Calculer la durée totale
        this.state.totalDuration = this.state.scenes.reduce((total, scene) => total + scene.duration, 0);

        // Récupérer les éléments DOM
        this.dom.playBtn = document.getElementById('tl-play');
        this.dom.progressBar = document.getElementById('progress-bar');
        this.dom.progressFill = document.getElementById('progress-fill');
        this.dom.progressHandle = document.getElementById('progress-handle');
        this.dom.timeCurrent = document.getElementById('time-current');
        this.dom.timeTotal = document.getElementById('time-total');
        this.dom.scenesBar = document.getElementById('scenes-bar');
        this.dom.speedBtns = document.querySelectorAll('.speed-btn');

        // Initialiser l'affichage
        this.updateTimeDisplay();
        this.renderSceneButtons();
        this.addSceneMarkers();
        this.bindEvents();

        return this;
    },

    /**
     * Bindre les événements
     */
    bindEvents() {
        // Bouton play/pause
        this.dom.playBtn?.addEventListener('click', () => this.togglePlay());

        // Navigation
        document.getElementById('tl-prev-scene')?.addEventListener('click', () => this.prevScene());
        document.getElementById('tl-next-scene')?.addEventListener('click', () => this.nextScene());
        document.getElementById('tl-step-back')?.addEventListener('click', () => this.stepBack());
        document.getElementById('tl-step-forward')?.addEventListener('click', () => this.stepForward());

        // Barre de progression
        this.dom.progressBar?.addEventListener('click', (e) => this.seekToPosition(e));
        this.dom.progressBar?.addEventListener('mousedown', (e) => this.startDrag(e));

        // Vitesse
        this.dom.speedBtns?.forEach(btn => {
            btn.addEventListener('click', () => this.setSpeed(parseFloat(btn.dataset.speed)));
        });

        // Raccourcis clavier
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    },

    /**
     * Basculer lecture/pause
     */
    togglePlay() {
        if (this.state.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    },

    /**
     * Démarrer la lecture
     */
    play() {
        if (this.state.currentTime >= this.state.totalDuration) {
            this.seek(0);
        }

        this.state.isPlaying = true;
        this.state.lastFrameTime = performance.now();
        this.dom.playBtn?.classList.add('playing');
        this.dom.playBtn.textContent = '⏸';

        this.callbacks.onPlay?.();
        this.tick();
    },

    /**
     * Mettre en pause
     */
    pause() {
        this.state.isPlaying = false;
        this.dom.playBtn?.classList.remove('playing');
        this.dom.playBtn.textContent = '▶';

        this.callbacks.onPause?.();
    },

    /**
     * Boucle d'animation
     */
    tick() {
        if (!this.state.isPlaying) return;

        const now = performance.now();
        const delta = (now - this.state.lastFrameTime) * this.state.speed;
        this.state.lastFrameTime = now;

        this.state.currentTime = Math.min(
            this.state.currentTime + delta,
            this.state.totalDuration
        );

        this.updateProgress();
        this.updateTimeDisplay();
        this.checkSceneChange();

        this.callbacks.onTimeUpdate?.(this.state.currentTime, this.getCurrentScene());

        // Fin de l'animation
        if (this.state.currentTime >= this.state.totalDuration) {
            this.pause();
            return;
        }

        requestAnimationFrame(() => this.tick());
    },

    /**
     * Naviguer à un temps précis
     */
    seek(timeMs) {
        this.state.currentTime = MathUtils.clamp(timeMs, 0, this.state.totalDuration);
        this.updateProgress();
        this.updateTimeDisplay();
        this.checkSceneChange();

        this.callbacks.onSeek?.(this.state.currentTime);
        this.callbacks.onTimeUpdate?.(this.state.currentTime, this.getCurrentScene());
    },

    /**
     * Naviguer via clic sur la barre
     */
    seekToPosition(e) {
        const rect = this.dom.progressBar.getBoundingClientRect();
        const ratio = (e.clientX - rect.left) / rect.width;
        this.seek(ratio * this.state.totalDuration);
    },

    /**
     * Glisser-déposer sur la timeline
     */
    startDrag(e) {
        e.preventDefault();
        const wasPlaying = this.state.isPlaying;
        if (wasPlaying) this.pause();

        const onMove = (e) => {
            const rect = this.dom.progressBar.getBoundingClientRect();
            const ratio = MathUtils.clamp((e.clientX - rect.left) / rect.width, 0, 1);
            this.seek(ratio * this.state.totalDuration);
        };

        const onUp = () => {
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup', onUp);
            if (wasPlaying) this.play();
        };

        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onUp);
    },

    /**
     * Scène précédente
     */
    prevScene() {
        const sceneStart = this.getSceneStartTime(this.state.currentSceneIndex);

        // Si on est au début de la scène, aller à la précédente
        if (this.state.currentTime - sceneStart < 500 && this.state.currentSceneIndex > 0) {
            this.goToScene(this.state.currentSceneIndex - 1);
        } else {
            // Sinon, revenir au début de la scène actuelle
            this.seek(sceneStart);
        }
    },

    /**
     * Scène suivante
     */
    nextScene() {
        if (this.state.currentSceneIndex < this.state.scenes.length - 1) {
            this.goToScene(this.state.currentSceneIndex + 1);
        }
    },

    /**
     * Reculer de 5 secondes
     */
    stepBack() {
        this.seek(this.state.currentTime - 5000);
    },

    /**
     * Avancer de 5 secondes
     */
    stepForward() {
        this.seek(this.state.currentTime + 5000);
    },

    /**
     * Aller à une scène spécifique
     */
    goToScene(index) {
        if (index >= 0 && index < this.state.scenes.length) {
            const time = this.getSceneStartTime(index);
            this.seek(time);
        }
    },

    /**
     * Définir la vitesse
     */
    setSpeed(speed) {
        this.state.speed = speed;

        this.dom.speedBtns?.forEach(btn => {
            btn.classList.toggle('active', parseFloat(btn.dataset.speed) === speed);
        });
    },

    /**
     * Obtenir le temps de début d'une scène
     */
    getSceneStartTime(index) {
        let time = 0;
        for (let i = 0; i < index && i < this.state.scenes.length; i++) {
            time += this.state.scenes[i].duration;
        }
        return time;
    },

    /**
     * Obtenir la scène actuelle
     */
    getCurrentScene() {
        let time = 0;
        for (let i = 0; i < this.state.scenes.length; i++) {
            if (this.state.currentTime < time + this.state.scenes[i].duration) {
                return {
                    scene: this.state.scenes[i],
                    index: i,
                    localTime: this.state.currentTime - time,
                    progress: (this.state.currentTime - time) / this.state.scenes[i].duration
                };
            }
            time += this.state.scenes[i].duration;
        }
        // Retourner la dernière scène si on est à la fin
        const lastIndex = this.state.scenes.length - 1;
        return {
            scene: this.state.scenes[lastIndex],
            index: lastIndex,
            localTime: this.state.scenes[lastIndex]?.duration || 0,
            progress: 1
        };
    },

    /**
     * Vérifier si on a changé de scène
     */
    checkSceneChange() {
        const current = this.getCurrentScene();
        if (current.index !== this.state.currentSceneIndex) {
            this.state.currentSceneIndex = current.index;
            this.updateSceneButtons();
            this.callbacks.onSceneChange?.(current);
        }
    },

    /**
     * Mettre à jour la barre de progression
     */
    updateProgress() {
        const ratio = this.state.currentTime / this.state.totalDuration;
        const percent = (ratio * 100).toFixed(2) + '%';

        if (this.dom.progressFill) {
            this.dom.progressFill.style.width = percent;
        }
        if (this.dom.progressHandle) {
            this.dom.progressHandle.style.left = percent;
        }
    },

    /**
     * Mettre à jour l'affichage du temps
     */
    updateTimeDisplay() {
        if (this.dom.timeCurrent) {
            this.dom.timeCurrent.textContent = this.formatTime(this.state.currentTime);
        }
        if (this.dom.timeTotal) {
            this.dom.timeTotal.textContent = this.formatTime(this.state.totalDuration);
        }
    },

    /**
     * Formater le temps en mm:ss
     */
    formatTime(ms) {
        const totalSeconds = Math.floor(ms / 1000);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },

    /**
     * Rendre les boutons de scènes
     */
    renderSceneButtons() {
        if (!this.dom.scenesBar) return;

        this.dom.scenesBar.innerHTML = '';

        this.state.scenes.forEach((scene, index) => {
            const btn = document.createElement('button');
            btn.className = 'scene-btn' + (index === 0 ? ' active' : '');
            btn.textContent = scene.title;
            btn.addEventListener('click', () => this.goToScene(index));
            this.dom.scenesBar.appendChild(btn);
        });
    },

    /**
     * Mettre à jour les boutons de scènes
     */
    updateSceneButtons() {
        const buttons = this.dom.scenesBar?.querySelectorAll('.scene-btn');
        buttons?.forEach((btn, index) => {
            btn.classList.toggle('active', index === this.state.currentSceneIndex);
            btn.classList.toggle('completed', index < this.state.currentSceneIndex);
        });
    },

    /**
     * Ajouter les marqueurs de scènes sur la timeline
     */
    addSceneMarkers() {
        if (!this.dom.progressBar || this.state.scenes.length < 2) return;

        // Supprimer les anciens marqueurs
        this.dom.progressBar.querySelectorAll('.scene-marker').forEach(m => m.remove());

        let time = 0;
        for (let i = 0; i < this.state.scenes.length - 1; i++) {
            time += this.state.scenes[i].duration;
            const ratio = time / this.state.totalDuration;

            const marker = document.createElement('div');
            marker.className = 'scene-marker';
            marker.style.left = (ratio * 100) + '%';
            marker.title = this.state.scenes[i + 1].title;

            this.dom.progressBar.appendChild(marker);
        }
    },

    /**
     * Gestion des raccourcis clavier
     */
    handleKeyboard(e) {
        // Ne pas interférer avec les inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        switch (e.code) {
            case 'Space':
                e.preventDefault();
                this.togglePlay();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                if (e.shiftKey) {
                    this.prevScene();
                } else {
                    this.stepBack();
                }
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (e.shiftKey) {
                    this.nextScene();
                } else {
                    this.stepForward();
                }
                break;
            case 'Home':
                e.preventDefault();
                this.seek(0);
                break;
            case 'End':
                e.preventDefault();
                this.seek(this.state.totalDuration);
                break;
            case 'Digit1':
            case 'Digit2':
            case 'Digit3':
            case 'Digit4':
            case 'Digit5':
            case 'Digit6':
            case 'Digit7':
            case 'Digit8':
            case 'Digit9':
                const sceneIndex = parseInt(e.code.replace('Digit', '')) - 1;
                if (sceneIndex < this.state.scenes.length) {
                    e.preventDefault();
                    this.goToScene(sceneIndex);
                }
                break;
        }
    },

    /**
     * Réinitialiser la timeline
     */
    reset() {
        this.pause();
        this.seek(0);
    },

    /**
     * Obtenir l'état actuel
     */
    getState() {
        return {
            ...this.state,
            currentScene: this.getCurrentScene()
        };
    }
};
