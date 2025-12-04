/**
 * Scene 6 : Projection orthogonale
 * Point H, vecteur OH, formule avec projection
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'projection',
    title: 'Projection orthogonale',
    duration: 14000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        const ux = state.ux || 4;
        const uy = state.uy || 0;
        const vx = state.vx || 3;
        const vy = state.vy || 3;

        // Vecteurs
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

        // Calcul de la projection
        const dotProduct = ux * vx + uy * vy;
        const uNormSq = ux * ux + uy * uy;
        const projScalar = dotProduct / uNormSq;
        const hx = projScalar * ux;
        const hy = projScalar * uy;

        // Phase 1 : Point H apparait (10-40%)
        if (contentProgress > 0.1) {
            const p = Math.min((contentProgress - 0.1) / 0.3, 1);
            const pointProgress = MathUtils.ease(p, 'easeOutQuad');

            // Segment perpendiculaire [BH]
            renderer.drawSegment(vx, vy, hx, hy, {
                color: `rgba(155, 89, 182, ${pointProgress})`,
                width: 2, dashed: true
            });

            // Point H
            renderer.drawPoint(hx, hy, { radius: 6, color: '#9b59b6' });

            if (p > 0.5) {
                const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                renderer.drawText('H', hx, hy - 0.5, {
                    color: `rgba(155, 89, 182, ${labelOpacity})`,
                    font: 'bold 18px Arial', align: 'center'
                });
            }
        }

        // Phase 2 : Vecteur OH (40-60%)
        if (contentProgress > 0.4) {
            const p = Math.min((contentProgress - 0.4) / 0.2, 1);
            const vectorProgress = MathUtils.ease(p, 'easeOutQuad');

            renderer.drawVector(0, 0, hx * vectorProgress, hy * vectorProgress, {
                color: '#9b59b6', width: 3
            });

            if (p > 0.5) {
                const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                drawMathBox('oh-label', '\\overrightarrow{OH}', hx / 2, -0.6, {
                    opacity: labelOpacity,
                    fontSize: '1.1em',
                    color: '#9b59b6',
                    bgColor: 'rgba(243, 232, 255, 0.95)'
                });
            }
        }

        // Phase 3 : Formules a GAUCHE avec LaTeX (60-100%)
        if (contentProgress > 0.6) {
            const p = (contentProgress - 0.6) / 0.4;

            const formulas = [
                { latex: '\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times OH', isFormula: true },
                { latex: '\\vec{u} \\cdot \\vec{v} = 4 \\times 3 = 12', isResult: true },
                { latex: 'OH = \\|\\vec{v}\\|\\cos(\\theta) = 3', isNote: true }
            ];

            const lineDelay = 0.25;
            formulas.forEach((formula, i) => {
                const lineStart = i * lineDelay;
                if (p > lineStart) {
                    const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                    if (formula.isResult) {
                        drawMathResult(`proj-${i}`, formula.latex, -9, 3 - i * 1.5, {
                            opacity, align: 'left',
                            color: '#9b59b6',
                            bgColor: 'rgba(243, 232, 255, 0.98)',
                            borderColor: '#9b59b6'
                        });
                    } else {
                        drawMathBox(`proj-${i}`, formula.latex, -9, 3 - i * 1.5, {
                            opacity, align: 'left',
                            fontSize: formula.isNote ? '1.1em' : '1.25em',
                            color: formula.isNote ? '#6b7280' : '#1e3a8a',
                            bgColor: formula.isNote ? 'rgba(243, 244, 246, 0.95)' : 'rgba(255, 255, 255, 0.95)'
                        });
                    }
                }
            });
        }
    }
});
