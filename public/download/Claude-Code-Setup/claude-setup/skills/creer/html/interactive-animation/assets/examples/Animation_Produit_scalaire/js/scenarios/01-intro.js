/**
 * Scène 1 : Introduction
 * Titre "Le Produit Scalaire" qui apparaît progressivement
 */

window.SCENE_REGISTRY.push({
    id: 'intro',
    title: 'Introduction',
    duration: 6000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        const opacity = MathUtils.ease(contentProgress, 'easeOutQuad');

        // Titre principal au centre
        drawTextBox(renderer, 'Le Produit Scalaire', 0, 0.5, {
            font: 'bold 52px Arial',
            color: '#2563eb',
            align: 'center',
            opacity
        });

        // Sous-titre
        if (contentProgress > 0.5) {
            const subOpacity = MathUtils.ease((contentProgress - 0.5) / 0.5, 'easeOutQuad');
            drawTextBox(renderer, 'Première Specialite', 0, -0.8, {
                font: '24px Arial',
                color: '#64748b',
                align: 'center',
                opacity: subOpacity
            });
        }
    }
});
