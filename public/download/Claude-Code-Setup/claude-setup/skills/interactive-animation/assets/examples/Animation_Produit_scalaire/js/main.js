/**
 * MAIN - Point d'entrée de l'application
 * Gère les deux modes : Animation (capsule vidéo) et Interactif (exploration)
 */

// ==========================================
// INSTANCES GLOBALES
// ==========================================
let animationRenderer, interactiveRenderer;
let animationCore, interactiveCore;
let timeline, sceneManager, controls;
let currentMode = 'animation';

// ==========================================
// INITIALISATION
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('[Main] Initializing...');

    initRenderers();
    initModes();
    initModeSwitch();
    initGlobalControls();
    initHelp();

    // Démarrer en mode animation par défaut
    switchMode('animation');

    console.log('[Main] Ready');
});

// ==========================================
// INITIALISATION DES RENDERERS
// ==========================================

function initRenderers() {
    // Renderer pour le mode animation
    const animCanvas = document.getElementById('animation-canvas');
    if (animCanvas) {
        animationRenderer = new CanvasRenderer('animation-canvas');
    }

    // Renderer pour le mode interactif
    const interCanvas = document.getElementById('interactive-canvas');
    if (interCanvas) {
        interactiveRenderer = new CanvasRenderer('interactive-canvas');
    }
}

// ==========================================
// INITIALISATION DES MODES
// ==========================================

function initModes() {
    // ----- MODE ANIMATION -----
    if (animationRenderer && typeof SCENES !== 'undefined') {
        // Initialiser les helpers de rendu
        if (typeof MathOverlay !== 'undefined') {
            MathOverlay.init(animationRenderer);
        }
        if (typeof TransitionManager !== 'undefined') {
            TransitionManager.init();
        }

        // Initialiser le gestionnaire de scènes
        sceneManager = SceneManager.init(SCENES, animationRenderer);

        // Initialiser la timeline
        timeline = Timeline.init(sceneManager.getScenesForTimeline(), {
            onTimeUpdate: (currentTime, sceneData) => {
                // Debut de frame - marquer les elements MathJax comme inactifs
                if (typeof MathOverlay !== 'undefined') {
                    MathOverlay.beginFrame();
                }

                // Effacer et redessiner le canvas
                animationRenderer.clear();

                // Verifier si la scene actuelle desactive la grille/axes (ex: recap)
                const currentScene = sceneManager.scenes.find(s => s.id === sceneData.scene.id);
                const hideGrid = currentScene && currentScene.hideGrid;
                const hideAxes = currentScene && currentScene.hideAxes;

                if (!hideGrid) {
                    animationRenderer.drawGrid();
                }
                if (!hideAxes) {
                    animationRenderer.drawAxes();
                }

                // Rendre la scene actuelle
                sceneManager.render(currentTime, sceneData);

                // Fin de frame - supprimer les elements MathJax non utilises
                if (typeof MathOverlay !== 'undefined') {
                    MathOverlay.endFrame();
                }
            },
            onSceneChange: (sceneData) => {
                console.log(`[Scene] ${sceneData.scene.title}`);
                // Effacer l'overlay MathJax lors du changement de scène
                if (typeof MathOverlay !== 'undefined') {
                    MathOverlay.clear();
                }
            }
        });

        // Boucle de rendu pour le mode animation
        animationCore = new AnimationCore(animationRenderer);
        animationCore.onUpdate = () => {
            // La timeline gère les mises à jour
        };
        animationCore.onRender = () => {
            // Le rendu est géré par la timeline
        };
    }

    // ----- MODE INTERACTIF -----
    if (interactiveRenderer) {
        // Initialiser les contrôles
        controls = new Controls();

        // Initialiser AnimationLogic si défini
        if (typeof AnimationLogic !== 'undefined') {
            AnimationLogic.init(interactiveRenderer, null, controls);
        }

        // Boucle de rendu pour le mode interactif
        interactiveCore = new AnimationCore(interactiveRenderer);
        interactiveCore.onUpdate = (deltaTime, elapsedTime) => {
            applyDisplayParams();
            if (typeof AnimationLogic !== 'undefined') {
                AnimationLogic.update(deltaTime, elapsedTime);
            }
            updateInfoOverlay();
        };
        interactiveCore.onRender = (renderer) => {
            if (typeof AnimationLogic !== 'undefined') {
                AnimationLogic.render(renderer);
            }
        };

        // Configurer les interactions
        setupInteractiveInteractions();
    }

    // Initialiser la bulle de contrôles
    initControlsBubble();
}

// ==========================================
// CHANGEMENT DE MODE
// ==========================================

function initModeSwitch() {
    const tabs = document.querySelectorAll('.menu-tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const mode = tab.dataset.mode;
            switchMode(mode);

            // Mettre à jour l'UI
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });
}

function switchMode(mode) {
    currentMode = mode;

    // Cacher tous les conteneurs de mode
    document.querySelectorAll('.mode-container').forEach(c => {
        c.classList.remove('active');
    });

    // Afficher le mode sélectionné
    const modeContainer = document.getElementById(`mode-${mode}`);
    if (modeContainer) {
        modeContainer.classList.add('active');
    }

    // Gérer les animations
    if (mode === 'animation') {
        // Arrêter le mode interactif
        interactiveCore?.pause();

        // Le mode animation est piloté par la timeline
        // (pas besoin de démarrer animationCore, la timeline gère tout)

    } else if (mode === 'interactive') {
        // Mettre en pause la timeline
        timeline?.pause();

        // Démarrer le mode interactif
        interactiveCore?.start();
    }
}

// ==========================================
// BULLE DE CONTRÔLES (MODE INTERACTIF)
// ==========================================

function initControlsBubble() {
    const bubble = document.getElementById('controls-bubble');
    const toggle = document.getElementById('bubble-toggle');
    const close = document.getElementById('bubble-close');

    if (!bubble || !toggle) return;

    toggle.addEventListener('click', () => {
        bubble.classList.remove('collapsed');
    });

    close?.addEventListener('click', () => {
        bubble.classList.add('collapsed');
    });

    // Sections dépliables
    document.querySelectorAll('.section-header').forEach(header => {
        header.addEventListener('click', () => {
            const section = header.closest('.control-section');
            section?.classList.toggle('collapsed');
        });
    });

    // Initialiser les contrôles depuis AnimationLogic
    if (typeof AnimationLogic !== 'undefined' && AnimationLogic.setupControls) {
        AnimationLogic.setupControls();
    }
}

// ==========================================
// PARAMÈTRES D'AFFICHAGE
// ==========================================

function applyDisplayParams() {
    if (!controls || !interactiveRenderer) return;

    const params = controls.getAll();

    interactiveRenderer.config.showGrid = params.showGrid ?? true;
    interactiveRenderer.config.showAxes = params.showAxes ?? true;
    interactiveRenderer.config.showLabels = params.showLabels ?? true;
}

// ==========================================
// OVERLAY D'INFORMATIONS
// ==========================================

function updateInfoOverlay() {
    const overlay = document.getElementById('info-overlay');
    if (!overlay) return;

    let infoItems = [];

    if (typeof AnimationLogic !== 'undefined' && AnimationLogic.getInfoDisplay) {
        infoItems = AnimationLogic.getInfoDisplay();
    }

    if (infoItems.length === 0) {
        overlay.innerHTML = '';
        return;
    }

    overlay.innerHTML = infoItems.map(item => {
        let valueClass = 'value';
        if (item.positive) valueClass += ' positive';
        if (item.negative) valueClass += ' negative';
        if (item.zero) valueClass += ' zero';

        return `
            <div class="info-item">
                <span class="label">${item.label}</span>
                <span class="${valueClass}">${item.value}</span>
            </div>
        `;
    }).join('');
}

// ==========================================
// INTERACTIONS (MODE INTERACTIF)
// ==========================================

function setupInteractiveInteractions() {
    const canvas = document.getElementById('interactive-canvas');
    if (!canvas) return;

    let isDragging = false;
    let lastX, lastY;

    // Zoom avec la molette
    canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        const factor = e.deltaY > 0 ? 0.9 : 1.1;
        interactiveRenderer.zoom(factor, e.offsetX, e.offsetY);
    }, { passive: false });

    // Pan
    canvas.addEventListener('mousedown', (e) => {
        if (e.button === 2 || (e.button === 0 && e.ctrlKey)) {
            isDragging = true;
            lastX = e.clientX;
            lastY = e.clientY;
            canvas.style.cursor = 'grabbing';
        }
    });

    canvas.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const dx = e.clientX - lastX;
            const dy = e.clientY - lastY;
            interactiveRenderer.pan(dx, dy);
            lastX = e.clientX;
            lastY = e.clientY;
        }

        // Notifier AnimationLogic
        const mathPos = interactiveRenderer.toMath(e.offsetX, e.offsetY);
        if (typeof AnimationLogic !== 'undefined' && AnimationLogic.onMouseMove) {
            AnimationLogic.onMouseMove(mathPos.x, mathPos.y, e);
        }
    });

    canvas.addEventListener('mouseup', () => {
        isDragging = false;
        canvas.style.cursor = 'default';
    });

    canvas.addEventListener('mouseleave', () => {
        isDragging = false;
        canvas.style.cursor = 'default';
    });

    canvas.addEventListener('contextmenu', (e) => e.preventDefault());

    canvas.addEventListener('click', (e) => {
        const mathPos = interactiveRenderer.toMath(e.offsetX, e.offsetY);
        if (typeof AnimationLogic !== 'undefined' && AnimationLogic.onClick) {
            AnimationLogic.onClick(mathPos.x, mathPos.y, e);
        }
    });

    canvas.addEventListener('dblclick', () => {
        interactiveRenderer.resetViewport();
    });
}

// ==========================================
// CONTRÔLES GLOBAUX
// ==========================================

function initGlobalControls() {
    // Plein écran
    document.getElementById('btn-fullscreen')?.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    });

    // Reset
    document.getElementById('btn-reset')?.addEventListener('click', () => {
        if (currentMode === 'animation') {
            timeline?.reset();
            sceneManager?.reset();
        } else {
            interactiveRenderer?.resetViewport();
            if (typeof AnimationLogic !== 'undefined' && AnimationLogic.resetState) {
                AnimationLogic.resetState();
            }
        }
    });

    // Aide
    const helpModal = document.getElementById('help-modal');
    document.getElementById('btn-help')?.addEventListener('click', () => {
        helpModal?.classList.remove('hidden');
    });
    document.getElementById('modal-close')?.addEventListener('click', () => {
        helpModal?.classList.add('hidden');
    });
    helpModal?.addEventListener('click', (e) => {
        if (e.target === helpModal) helpModal.classList.add('hidden');
    });

    // Échap pour fermer modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            helpModal?.classList.add('hidden');
        }
    });
}

// ==========================================
// AIDE
// ==========================================

function initHelp() {
    const helpContent = document.getElementById('help-content');
    if (!helpContent) return;

    // Ajouter le contenu personnalisé si disponible
    if (typeof AnimationLogic !== 'undefined' && AnimationLogic.getHelpContent) {
        const customHelp = AnimationLogic.getHelpContent();
        if (customHelp) {
            helpContent.innerHTML = `<h3>À propos</h3>${customHelp}<hr>` + helpContent.innerHTML;
        }
    }
}

// ==========================================
// EXPORT GLOBAL
// ==========================================

window.AnimationApp = {
    get mode() { return currentMode; },
    switchMode,
    timeline,
    sceneManager,
    controls,
    animationRenderer,
    interactiveRenderer,

    // Mode animation
    play: () => timeline?.play(),
    pause: () => timeline?.pause(),
    seek: (time) => timeline?.seek(time),
    goToScene: (index) => timeline?.goToScene(index),

    // Mode interactif
    setParam: (name, value) => controls?.set(name, value),
    getParam: (name) => controls?.get(name),
    resetView: () => interactiveRenderer?.resetViewport()
};
