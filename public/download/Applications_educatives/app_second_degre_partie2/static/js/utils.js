// Utilitaires JavaScript pour l'application

/**
 * Affiche un message de log formaté
 */
function log(message, type = 'info') {
    const emoji = {
        info: 'ℹ️',
        success: '✅',
        error: '❌',
        warning: '⚠️'
    };
    console.log(`${emoji[type] || 'ℹ️'} ${message}`);
}

/**
 * Formater un temps en minutes et secondes
 */
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Sauvegarder dans localStorage
 */
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error);
        return false;
    }
}

/**
 * Charger depuis localStorage
 */
function loadFromLocalStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Erreur lors du chargement:', error);
        return defaultValue;
    }
}

/**
 * Debounce function pour optimiser les événements
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Normaliser une chaîne pour la comparaison
 */
function normalizeString(str) {
    if (typeof str !== 'string') {
        str = String(str);
    }
    return str
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '')
        .replace(/,/g, '.');
}

/**
 * Vérifier si MathJax est chargé
 */
function isMathJaxReady() {
    return typeof MathJax !== 'undefined' && MathJax.typesetPromise;
}

/**
 * Re-render MathJax sur un élément
 */
async function renderMath(element) {
    if (isMathJaxReady()) {
        try {
            await MathJax.typesetPromise([element]);
            log('MathJax rendu avec succès', 'success');
        } catch (error) {
            console.error('Erreur MathJax:', error);
        }
    }
}

/**
 * Animer l'apparition d'un élément
 */
function animateElement(element, animation = 'fadeIn') {
    element.style.opacity = '0';
    element.style.transform = 'translateY(10px)';

    setTimeout(() => {
        element.style.transition = 'all 0.3s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 10);
}

/**
 * Scroller doucement vers un élément
 */
function smoothScrollTo(element, offset = 0) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

/**
 * Classe pour gérer une API
 */
class APIClient {
    constructor(baseURL = window.location.origin) {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };

        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, finalOptions);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erreur API:', error);
            throw error;
        }
    }

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
}

/**
 * Afficher une notification temporaire
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Créer l'élément de notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    // Styles inline pour la notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10B981' : type === 'error' ? '#EF4444' : '#3B82F6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
        font-weight: 600;
    `;

    document.body.appendChild(notification);

    // Retirer après la durée spécifiée
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}

// Ajouter les animations CSS pour les notifications
if (!document.getElementById('notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Export des fonctions (pour utilisation dans d'autres scripts)
window.AppUtils = {
    log,
    formatTime,
    saveToLocalStorage,
    loadFromLocalStorage,
    debounce,
    normalizeString,
    isMathJaxReady,
    renderMath,
    animateElement,
    smoothScrollTo,
    APIClient,
    showNotification
};

log('Utilitaires chargés', 'success');
