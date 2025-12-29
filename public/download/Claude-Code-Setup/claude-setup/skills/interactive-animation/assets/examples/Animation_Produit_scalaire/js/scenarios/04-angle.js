/**
 * Scene 4 : Angle entre les vecteurs
 * Arc vert montrant theta = 45 degres, formule geometrique
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'angle',
    title: 'Angle theta',
    duration: 10000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);

        const ux = state.ux || 4;
        const uy = state.uy || 0;
        const vx = state.vx || 3;
        const vy = state.vy || 3;
        const angle = Math.PI / 4; // 45 degres

        // Vecteurs complets (toujours visibles)
        renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
        drawMathBox('vec-u-label', '\\vec{u}', ux + 0.5, 0.5, {
            fontSize: '1.3em', color: '#ef4444',
            bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
        });

        renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
        drawMathBox('vec-v-label', '\\vec{v}', vx + 0.5, vy + 0.4, {
            fontSize: '1.3em', color: '#3b82f6',
            bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
        });

        // Phase 1 : Arc de l'angle (0-40%)
        if (contentProgress < 0.4) {
            const p = contentProgress / 0.4;
            const arcProgress = MathUtils.ease(p, 'easeOutQuad');
            const arcAngle = angle * arcProgress;

            renderer.drawArc(0, 0, 1.2, 0, arcAngle, {
                strokeColor: '#10b981',
                fillColor: 'rgba(16, 185, 129, 0.1)',
                lineWidth: 3
            });

            // Label theta apparait apres l'arc
            if (p > 0.6) {
                const labelOpacity = MathUtils.ease((p - 0.6) / 0.4, 'easeOutQuad');
                drawMathBox('theta-label', '\\theta', 1.4, 0.55, {
                    opacity: labelOpacity,
                    fontSize: '1.4em',
                    color: '#10b981',
                    bgColor: 'rgba(209, 250, 229, 0.9)'
                });
            }
        }
        // Phase 2 : Affichage angle et formule (40-100%)
        else {
            const p = (contentProgress - 0.4) / 0.6;

            // Arc complet avec remplissage
            renderer.drawArc(0, 0, 1.2, 0, angle, {
                strokeColor: '#10b981',
                fillColor: 'rgba(16, 185, 129, 0.1)',
                lineWidth: 3
            });

            // Label theta (unique)
            drawMathBox('theta-label', '\\theta', 1.4, 0.55, {
                fontSize: '1.4em',
                color: '#10b981',
                bgColor: 'rgba(209, 250, 229, 0.9)'
            });

            // Valeur de l'angle a GAUCHE
            if (p > 0.15) {
                const angleOpacity = MathUtils.ease((p - 0.15) / 0.25, 'easeOutQuad');
                drawMathResult('angle-value', '\\theta = 45^\\circ', -9, 2.5, {
                    opacity: angleOpacity, align: 'left'
                });
            }

            // Formule geometrique a GAUCHE (sous l'angle)
            if (p > 0.45) {
                const formulaOpacity = MathUtils.ease((p - 0.45) / 0.35, 'easeOutQuad');
                drawMathBox('geom-formula', '\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times \\|\\vec{v}\\| \\times \\cos(\\theta)', -9, 0.8, {
                    opacity: formulaOpacity, align: 'left',
                    fontSize: '1.25em',
                    color: '#1e3a8a',
                    bgColor: 'rgba(219, 234, 254, 0.95)'
                });
            }
        }

        state.angle = angle;
    }
});
