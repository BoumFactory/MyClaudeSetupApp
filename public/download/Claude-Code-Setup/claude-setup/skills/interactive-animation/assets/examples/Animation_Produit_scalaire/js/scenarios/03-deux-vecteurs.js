/**
 * Scene 3 : Deux vecteurs
 * Vecteur u(4,0) puis v(3,3) qui apparait en rotation
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'deux-vecteurs',
    title: 'Deux vecteurs',
    duration: 10000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        const ux = 4, uy = 0;
        const vx = 3, vy = 3;

        // Phase 1 : Vecteur u (0-40%)
        if (contentProgress < 0.4) {
            const p = contentProgress / 0.4;
            const len = MathUtils.ease(p, 'easeOutQuad');

            renderer.drawVector(0, 0, ux * len, uy * len, {
                color: '#ef4444',
                width: 3
            });

            if (p > 0.5) {
                const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                drawMathBox('vec-u-label', '\\vec{u}', ux * len + 0.4, 0.4, {
                    opacity: labelOpacity, fontSize: '1.3em', color: '#ef4444',
                    bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
                });
            }
        }
        // Phase 2 : Vecteur v apparait (40-100%)
        else {
            const p = (contentProgress - 0.4) / 0.6;

            // Vecteur u complet
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u-label', '\\vec{u}', ux + 0.4, 0.4, {
                fontSize: '1.3em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });

            // Vecteur v avec rotation depuis l'axe x
            const vLen = Math.sqrt(vx * vx + vy * vy);
            const targetAngle = Math.atan2(vy, vx);
            const currentAngle = MathUtils.ease(Math.min(p * 1.5, 1), 'easeOutQuad') * targetAngle;
            const currentLen = MathUtils.ease(Math.min(p * 2, 1), 'easeOutQuad') * vLen;

            const currentVx = currentLen * MathUtils.cos(currentAngle);
            const currentVy = currentLen * MathUtils.sin(currentAngle);

            renderer.drawVector(0, 0, currentVx, currentVy, {
                color: '#3b82f6',
                width: 3
            });

            if (p > 0.5) {
                const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                drawMathBox('vec-v-label', '\\vec{v}', currentVx + 0.4, currentVy + 0.4, {
                    opacity: labelOpacity, fontSize: '1.3em', color: '#3b82f6',
                    bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
                });
            }

            // Coordonnees affichees a GAUCHE avec LaTeX
            if (p > 0.7) {
                const infoOpacity = MathUtils.ease((p - 0.7) / 0.3, 'easeOutQuad');
                drawMathBox('coord-u-vec', `\\vec{u}(${ux}\\,;\\, ${uy})`, -9, 2.5, {
                    opacity: infoOpacity,
                    fontSize: '1.2em',
                    color: '#ef4444',
                    bgColor: 'rgba(254, 226, 226, 0.95)',
                    align: 'left'
                });
                drawMathBox('coord-v-vec', `\\vec{v}(${vx}\\,;\\, ${vy})`, -9, 1, {
                    opacity: infoOpacity,
                    fontSize: '1.2em',
                    color: '#3b82f6',
                    bgColor: 'rgba(219, 234, 254, 0.95)',
                    align: 'left'
                });
            }
        }

        // Stocker les vecteurs
        state.ux = ux; state.uy = uy;
        state.vx = vx; state.vy = vy;
    }
});
