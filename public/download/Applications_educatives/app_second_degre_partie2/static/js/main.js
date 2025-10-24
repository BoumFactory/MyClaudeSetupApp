// Script principal pour toutes les pages

document.addEventListener('DOMContentLoaded', () => {
    const { log, renderMath, isMathJaxReady } = window.AppUtils;

    log('Application initialisée');

    // Attendre que MathJax soit prêt pour re-render les formules
    const waitForMathJax = setInterval(() => {
        if (isMathJaxReady()) {
            clearInterval(waitForMathJax);
            log('MathJax est prêt', 'success');

            // Re-render toutes les formules mathématiques
            if (MathJax && MathJax.typesetPromise) {
                MathJax.typesetPromise().then(() => {
                    log('Formules mathématiques rendues', 'success');
                }).catch((err) => {
                    console.error('Erreur lors du rendu MathJax:', err);
                });
            }
        }
    }, 100);

    // Timeout de sécurité
    setTimeout(() => {
        clearInterval(waitForMathJax);
    }, 10000);

    // Gérer les liens d'ancrage avec scroll smooth
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const offset = 100; // Offset pour le header sticky
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animations au scroll
    const observeElements = () => {
        const elements = document.querySelectorAll('.content-block, .competence-card, .exercise-card');

        if (elements.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        elements.forEach(element => observer.observe(element));
    };

    observeElements();

    // Gestion du bouton "retour en haut"
    createBackToTopButton();

    log('Scripts principaux chargés', 'success');
});

/**
 * Créer un bouton "retour en haut"
 */
function createBackToTopButton() {
    const button = document.createElement('button');
    button.id = 'backToTop';
    button.innerHTML = '↑';
    button.setAttribute('aria-label', 'Retour en haut');

    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--primary);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
    `;

    document.body.appendChild(button);

    // Afficher/cacher le bouton selon le scroll
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            button.style.opacity = '1';
            button.style.visibility = 'visible';
        } else {
            button.style.opacity = '0';
            button.style.visibility = 'hidden';
        }
    });

    // Action au clic
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Effet hover
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'scale(1.1)';
        button.style.background = 'var(--primary-dark)';
    });

    button.addEventListener('mouseleave', () => {
        button.style.transform = 'scale(1)';
        button.style.background = 'var(--primary)';
    });
}

// Gestion des erreurs globales
window.addEventListener('error', (event) => {
    console.error('Erreur globale:', event.error);
});

// Prévenir la perte de données lors de la fermeture (si des exercices sont en cours)
window.addEventListener('beforeunload', (event) => {
    const hasUnsavedProgress = sessionStorage.getItem('exercisesInProgress');
    if (hasUnsavedProgress) {
        event.preventDefault();
        event.returnValue = '';
    }
});
