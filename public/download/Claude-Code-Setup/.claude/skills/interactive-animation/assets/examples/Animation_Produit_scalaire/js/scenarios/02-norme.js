/**
 * Scene 2 : Norme d'un vecteur
 * Vecteur u(4,3), triangle rectangle, calcul de ||u|| = 5
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'norme',
    title: 'Norme d\'un vecteur',
    duration: 14000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        const ux = 4, uy = 3;

        // Phase 1 : Apparition du vecteur (0-30%)
        if (contentProgress < 0.3) {
            const p = contentProgress / 0.3;
            const len = MathUtils.ease(p, 'easeOutQuad');

            renderer.drawVector(0, 0, ux * len, uy * len, {
                color: '#ef4444',
                width: 3
            });

            if (p > 0.5) {
                const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                drawMathBox('vec-u-label', '\\vec{u}', ux * len + 0.4, uy * len + 0.4, {
                    opacity: labelOpacity, fontSize: '1.3em', color: '#ef4444',
                    bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
                });
            }
        }
        // Phase 2 : Triangle rectangle (30-60%)
        else if (contentProgress < 0.6) {
            const p = (contentProgress - 0.3) / 0.3;

            // Vecteur complet
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u-label', '\\vec{u}', ux + 0.4, uy + 0.4, {
                fontSize: '1.3em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });

            // Triangle rectangle
            const triangleOpacity = MathUtils.ease(p, 'easeOutQuad');
            renderer.drawSegment(0, 0, ux, 0, {
                color: `rgba(59, 130, 246, ${triangleOpacity})`,
                width: 2, dashed: true
            });
            renderer.drawSegment(ux, 0, ux, uy, {
                color: `rgba(59, 130, 246, ${triangleOpacity})`,
                width: 2, dashed: true
            });

            // Labels des cotes
            if (p > 0.3) {
                const labelOp = MathUtils.ease((p - 0.3) / 0.7, 'easeOutQuad');
                drawMathBox('side-x', '4', ux / 2, -0.6, {
                    opacity: labelOp, fontSize: '1.1em', color: '#3b82f6'
                });
                drawMathBox('side-y', '3', ux + 0.7, uy / 2, {
                    opacity: labelOp, fontSize: '1.1em', color: '#3b82f6'
                });
            }
        }
        // Phase 3 : Formule et calcul (60-100%)
        else {
            const p = (contentProgress - 0.6) / 0.4;

            // Elements graphiques
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u-label', '\\vec{u}', ux + 0.4, uy + 0.4, {
                fontSize: '1.3em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });
            renderer.drawSegment(0, 0, ux, 0, { color: 'rgba(59, 130, 246, 0.7)', width: 2, dashed: true });
            renderer.drawSegment(ux, 0, ux, uy, { color: 'rgba(59, 130, 246, 0.7)', width: 2, dashed: true });
            drawMathBox('side-x', '4', ux / 2, -0.6, { fontSize: '1.1em', color: '#3b82f6' });
            drawMathBox('side-y', '3', ux + 0.7, uy / 2, { fontSize: '1.1em', color: '#3b82f6' });

            // Formules LaTeX a GAUCHE
            const formulas = [
                { latex: '\\|\\vec{u}\\| = \\sqrt{x^2 + y^2}', isFormula: true },
                { latex: '\\|\\vec{u}\\| = \\sqrt{4^2 + 3^2}', isFormula: false },
                { latex: '\\|\\vec{u}\\| = \\sqrt{16 + 9}', isFormula: false },
                { latex: '\\|\\vec{u}\\| = \\sqrt{25} = 5', isResult: true }
            ];

            const lineDelay = 0.2;
            formulas.forEach((formula, i) => {
                const lineStart = i * lineDelay;
                if (p > lineStart) {
                    const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                    if (formula.isResult) {
                        drawMathResult(`norm-${i}`, formula.latex, -9, 3 - i * 1.5, {
                            opacity, align: 'left'
                        });
                    } else {
                        drawMathBox(`norm-${i}`, formula.latex, -9, 3 - i * 1.5, {
                            opacity, align: 'left',
                            fontSize: formula.isFormula ? '1.3em' : '1.2em',
                            color: formula.isFormula ? '#1e3a8a' : '#374151',
                            bgColor: formula.isFormula ? 'rgba(219, 234, 254, 0.95)' : 'rgba(255, 255, 255, 0.95)'
                        });
                    }
                }
            });
        }

        state.uNorm = 5;
    }
});
