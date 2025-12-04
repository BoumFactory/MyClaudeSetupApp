/**
 * Scene 5 : Calcul avec la formule geometrique
 * Calcul etape par etape jusqu'a u.v = 12
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'calcul-geometrique',
    title: 'Calcul geometrique',
    duration: 14000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);

        const ux = state.ux || 4;
        const uy = state.uy || 0;
        const vx = state.vx || 3;
        const vy = state.vy || 3;
        const angle = state.angle || Math.PI / 4;

        // Elements graphiques (au centre-droit)
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

        // Arc de l'angle
        renderer.drawArc(0, 0, 1.2, 0, angle, {
            strokeColor: '#10b981',
            fillColor: 'rgba(16, 185, 129, 0.1)',
            lineWidth: 2
        });
        drawMathBox('theta-label', '\\theta', 1.0, 0.55, {
            fontSize: '1.2em', color: '#10b981',
            bgColor: 'rgba(209, 250, 229, 0.9)', padding: '4px 8px'
        });

        // Calcul etape par etape a GAUCHE avec LaTeX
        const vNorm = Math.sqrt(vx * vx + vy * vy);
        const vNormFormatted = MathUtils.format(vNorm, 1);
        const productFormatted = MathUtils.format(4 * vNorm, 1);

        // Formules LaTeX
        const formulas = [
            { latex: '\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times \\|\\vec{v}\\| \\times \\cos(\\theta)', y: 3.5, isFormula: true },
            { latex: `\\vec{u} \\cdot \\vec{v} = 4 \\times ${vNormFormatted} \\times \\cos(45^\\circ)`, y: 2, isFormula: false },
            { latex: `\\vec{u} \\cdot \\vec{v} = ${productFormatted} \\times \\frac{\\sqrt{2}}{2}`, y: 0.5, isFormula: false },
            { latex: '\\vec{u} \\cdot \\vec{v} = 12', y: -1, isResult: true }
        ];

        const lineDelay = 0.20;
        formulas.forEach((formula, i) => {
            const lineStart = i * lineDelay;
            if (contentProgress > lineStart) {
                const lineProgress = Math.min((contentProgress - lineStart) / lineDelay, 1);
                const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                if (formula.isResult) {
                    drawMathResult(`calc-${i}`, formula.latex, -9, formula.y, {
                        opacity,
                        align: 'left'
                    });
                } else {
                    drawMathBox(`calc-${i}`, formula.latex, -9, formula.y, {
                        opacity,
                        fontSize: formula.isFormula ? '1.3em' : '1.2em',
                        color: formula.isFormula ? '#1e3a8a' : '#374151',
                        bgColor: formula.isFormula ? 'rgba(219, 234, 254, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                        align: 'left'
                    });
                }
            }
        });

        state.dotProduct = 12;
    }
});
