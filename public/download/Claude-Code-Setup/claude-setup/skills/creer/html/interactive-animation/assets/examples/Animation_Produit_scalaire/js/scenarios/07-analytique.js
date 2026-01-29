/**
 * Scene 7 : Formule analytique
 * u.v = xu x xv + yu x yv, verification du resultat
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'analytique',
    title: 'Formule analytique',
    duration: 18000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        const ux = state.ux || 4;
        const uy = state.uy || 0;
        const vx = state.vx || 3;
        const vy = state.vy || 3;

        // Vecteurs (au centre)
        renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
        drawMathBox('vec-u-label', '\\vec{u}', ux + 0.5, 0.5, {
            fontSize: '1.2em', color: '#ef4444',
            bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
        });
        renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
        drawMathBox('vec-v-label', '\\vec{v}', vx + 0.5, vy + 0.4, {
            fontSize: '1.2em', color: '#3b82f6',
            bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
        });

        // Phase 1 : Coordonnees apparaissent a cote des vecteurs
        if (contentProgress > 0) {
            const p = Math.min(contentProgress / 0.3, 1);
            const coordOpacity = MathUtils.ease(p, 'easeOutQuad');

            drawMathBox('coord-u', `\\vec{u}(${ux}; ${uy})`, ux + 0.5, 0.4, {
                opacity: coordOpacity,
                fontSize: '1.15em',
                color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.95)'
            });

            drawMathBox('coord-v', `\\vec{v}(${vx}; ${vy})`, vx + 0.5, vy + 0.4, {
                opacity: coordOpacity,
                fontSize: '1.15em',
                color: '#3b82f6',
                bgColor: 'rgba(219, 234, 254, 0.95)'
            });
        }

        // Phase 2 : Formule generale a GAUCHE (30-50%)
        if (contentProgress > 0.3) {
            const p = Math.min((contentProgress - 0.3) / 0.2, 1);
            const formulaOpacity = MathUtils.ease(p, 'easeOutQuad');

            drawMathBox('formula-ana', '\\vec{u} \\cdot \\vec{v} = x_u \\times x_v + y_u \\times y_v', -9, 3, {
                opacity: formulaOpacity, align: 'left',
                fontSize: '1.3em',
                color: '#1e3a8a',
                bgColor: 'rgba(219, 234, 254, 0.95)'
            });
        }

        // Phase 3 : Calcul etape par etape (50-100%)
        if (contentProgress > 0.5) {
            const p = (contentProgress - 0.5) / 0.5;

            const formulas = [
                { latex: `\\vec{u} \\cdot \\vec{v} = ${ux} \\times ${vx} + ${uy} \\times ${vy}`, isFormula: false },
                { latex: `\\vec{u} \\cdot \\vec{v} = ${ux * vx} + ${uy * vy}`, isFormula: false },
                { latex: '\\vec{u} \\cdot \\vec{v} = 12', isResult: true }
            ];

            const lineDelay = 0.25;
            formulas.forEach((formula, i) => {
                const lineStart = i * lineDelay;
                if (p > lineStart) {
                    const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                    if (formula.isResult) {
                        drawMathResult(`ana-${i}`, formula.latex, -9, 2 - i * 1.5, {
                            opacity, align: 'left'
                        });
                    } else {
                        drawMathBox(`ana-${i}`, formula.latex, -9, 2 - i * 1.5, {
                            opacity, align: 'left',
                            fontSize: '1.2em',
                            color: '#374151',
                            bgColor: 'rgba(255, 255, 255, 0.95)'
                        });
                    }
                }
            });

            // Message "Meme resultat !" en BAS centre
            if (p > 0.8) {
                const msgOpacity = MathUtils.ease((p - 0.8) / 0.2, 'easeOutQuad');
                drawMathBox('same-result', '\\checkmark \\text{ Meme resultat !}', 0, -3.5, {
                    opacity: msgOpacity,
                    fontSize: '1.4em',
                    color: '#059669',
                    bgColor: 'rgba(209, 250, 229, 0.98)',
                    borderColor: '#10b981',
                    borderWidth: 2
                });
            }
        }
    }
});
