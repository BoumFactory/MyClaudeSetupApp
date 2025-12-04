/**
 * Scène 1 : Introduction
 *
 * Exemple de scène - À personnaliser selon l'animation
 *
 * STRUCTURE D'UNE SCÈNE :
 * - id: identifiant unique
 * - title: titre affiché dans la timeline
 * - duration: durée en ms
 * - animate(localTime, progress, renderer, state): fonction d'animation
 */

// Raccourcis vers les helpers
const { drawTextBox, drawMultilineTextBox } = window.TextBoxHelpers || {};

// Enregistrer la scène dans le registre global
window.SCENE_REGISTRY.push({
    id: 'intro',
    title: 'Introduction',
    duration: 4000,

    /**
     * Fonction d'animation appelée à chaque frame
     * @param {number} localTime - Temps en ms depuis le début de la scène
     * @param {number} progress - Ratio d'avancement (0 à 1)
     * @param {CanvasRenderer} renderer - Instance pour dessiner
     * @param {object} state - État partagé entre les scènes
     */
    animate(localTime, progress, renderer, state) {
        // Titre qui apparaît progressivement au centre
        const opacity = MathUtils.ease(progress, 'easeOutQuad');

        renderer.drawText('Titre de l\'animation', 0, 0, {
            font: 'bold 48px Arial',
            color: `rgba(37, 99, 235, ${opacity})`,
            align: 'center'
        });
    }
});
