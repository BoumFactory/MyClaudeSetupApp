/**
 * Scene 8 : Orthogonalite
 * Vecteurs u(3,2) et v(-2,3), u.v = 0
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'orthogonalite',
    title: 'Orthogonalite',
    duration: 22000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        // Nouveaux vecteurs orthogonaux
        const ux = 3, uy = 2;
        const vx = -2, vy = 3;

        // Phase 1 : Transition - nouveaux vecteurs (0-25%)
        if (contentProgress < 0.25) {
            const p = contentProgress / 0.25;
            const len = MathUtils.ease(p, 'easeOutQuad');

            renderer.drawVector(0, 0, ux * len, uy * len, { color: '#ef4444', width: 3 });

            if (p > 0.3) {
                const vProgress = MathUtils.ease((p - 0.3) / 0.7, 'easeOutQuad');
                renderer.drawVector(0, 0, vx * vProgress, vy * vProgress, { color: '#3b82f6', width: 3 });
            }
        }
        // Phase 2 : Calcul du produit scalaire (25-60%)
        else if (contentProgress < 0.6) {
            const p = (contentProgress - 0.25) / 0.35;

            // Vecteurs complets
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('orth-coord-u', `\\vec{u}(${ux}\\,;\\,${uy})`, ux + 0.5, uy + 0.4, {
                fontSize: '1.1em',
                color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.95)'
            });

            renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
            drawMathBox('orth-coord-v', `\\vec{v}(${vx}\\,;\\,${vy})`, vx - 1.5, vy + 0.4, {
                fontSize: '1.1em',
                color: '#3b82f6',
                bgColor: 'rgba(219, 234, 254, 0.95)'
            });

            // Calcul a GAUCHE avec LaTeX
            const formulas = [
                { latex: `\\vec{u} \\cdot \\vec{v} = ${ux} \\times (${vx}) + ${uy} \\times ${vy}`, isFormula: false },
                { latex: `\\vec{u} \\cdot \\vec{v} = ${ux * vx} + ${uy * vy}`, isFormula: false },
                { latex: '\\vec{u} \\cdot \\vec{v} = 0', isResult: true }
            ];

            const lineDelay = 0.25;
            formulas.forEach((formula, i) => {
                const lineStart = i * lineDelay;
                if (p > lineStart) {
                    const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                    if (formula.isResult) {
                        drawMathResult(`orth-calc-${i}`, formula.latex, -9, 3.5 - i * 1.5, {
                            opacity, align: 'left',
                            color: '#3b82f6'
                        });
                    } else {
                        drawMathBox(`orth-calc-${i}`, formula.latex, -9, 3.5 - i * 1.5, {
                            opacity, align: 'left',
                            fontSize: '1.2em',
                            color: '#374151',
                            bgColor: 'rgba(255, 255, 255, 0.95)'
                        });
                    }
                }
            });
        }
        // Phase 3 : Angle droit et conclusion (60-100%)
        else {
            const p = (contentProgress - 0.6) / 0.4;

            // Vecteurs
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u-label-3', '\\vec{u}', ux + 0.4, uy + 0.4, {
                fontSize: '1.2em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });
            renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
            drawMathBox('vec-v-label-3', '\\vec{v}', vx - 0.8, vy + 0.4, {
                fontSize: '1.2em', color: '#3b82f6',
                bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
            });

            // Carre de l'angle droit
            if (p > 0.1) {
                const squareSize = 0.5;
                const squareOpacity = MathUtils.ease((p - 0.1) / 0.2, 'easeOutQuad');

                const uNorm = Math.sqrt(ux * ux + uy * uy);
                const vNorm = Math.sqrt(vx * vx + vy * vy);

                const ux_n = ux / uNorm * squareSize;
                const uy_n = uy / uNorm * squareSize;
                const vx_n = vx / vNorm * squareSize;
                const vy_n = vy / vNorm * squareSize;

                // Dessiner le carre de l'angle droit
                renderer.drawSegment(ux_n, uy_n, ux_n + vx_n, uy_n + vy_n, {
                    color: `rgba(16, 185, 129, ${squareOpacity})`, width: 2
                });
                renderer.drawSegment(vx_n, vy_n, ux_n + vx_n, uy_n + vy_n, {
                    color: `rgba(16, 185, 129, ${squareOpacity})`, width: 2
                });
            }

            // Message "ORTHOGONAUX" en BAS avec LaTeX
            if (p > 0.3) {
                const msgOpacity = MathUtils.ease((p - 0.3) / 0.2, 'easeOutQuad');
                drawMathBox('orth-msg', '\\text{Vecteurs ORTHOGONAUX}', 0, -3, {
                    opacity: msgOpacity,
                    fontSize: '1.5em',
                    color: '#3b82f6',
                    bgColor: 'rgba(219, 234, 254, 0.98)',
                    borderColor: '#3b82f6',
                    borderWidth: 2
                });
            }

            // Propriete encadree
            if (p > 0.5) {
                const boxOpacity = MathUtils.ease((p - 0.5) / 0.3, 'easeOutQuad');
                drawMathResult('orth-property', '\\vec{u} \\perp \\vec{v} \\Leftrightarrow \\vec{u} \\cdot \\vec{v} = 0', 0, -4.5, {
                    opacity: boxOpacity,
                    fontSize: '1.4em',
                    color: '#d97706',
                    bgColor: 'rgba(254, 243, 199, 0.98)',
                    borderColor: '#f59e0b'
                });
            }
        }
    }
});
