/**
 * Scene 10 : Recapitulatif
 * Les 3 formules encadrees - SANS axes ni grille
 * Utilise MathJax pour un rendu LaTeX parfait
 */

window.SCENE_REGISTRY.push({
    id: 'recap',
    title: 'Recapitulatif',
    duration: 18000,
    hideGrid: true,
    hideAxes: true,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);

        // Fond legerement colore
        const ctx = renderer.ctx;
        const gradient = ctx.createLinearGradient(0, 0, 0, renderer.height);
        gradient.addColorStop(0, 'rgba(248, 250, 252, 1)');
        gradient.addColorStop(1, 'rgba(241, 245, 249, 1)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, renderer.width, renderer.height);

        // Titre
        if (contentProgress > 0) {
            const titleOpacity = MathUtils.ease(Math.min(contentProgress / 0.12, 1), 'easeOutQuad');

            drawMathBox('recap-title', '\\textbf{A RETENIR}', 0, 4.2, {
                opacity: titleOpacity,
                fontSize: '2em',
                color: '#1e3a8a',
                bgColor: 'rgba(219, 234, 254, 0.98)',
                borderColor: '#3b82f6',
                borderWidth: 2
            });
        }

        const formulas = [
            {
                title: 'Formule geometrique',
                latex: '\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times \\|\\vec{v}\\| \\times \\cos(\\theta)',
                y: 2.2,
                color: '#059669',
                bgColor: 'rgba(209, 250, 229, 0.98)',
                borderColor: '#10b981'
            },
            {
                title: 'Formule analytique',
                latex: '\\vec{u} \\cdot \\vec{v} = x_u \\times x_v + y_u \\times y_v',
                y: 0,
                color: '#1d4ed8',
                bgColor: 'rgba(219, 234, 254, 0.98)',
                borderColor: '#3b82f6'
            },
            {
                title: 'Critere d\'orthogonalite',
                latex: '\\vec{u} \\perp \\vec{v} \\Leftrightarrow \\vec{u} \\cdot \\vec{v} = 0',
                y: -2.2,
                color: '#d97706',
                bgColor: 'rgba(254, 243, 199, 0.98)',
                borderColor: '#f59e0b'
            }
        ];

        formulas.forEach((item, i) => {
            const startTime = 0.12 + i * 0.18;
            if (contentProgress > startTime) {
                const p = Math.min((contentProgress - startTime) / 0.15, 1);
                const opacity = MathUtils.ease(p, 'easeOutCubic');
                const slideOffset = (1 - MathUtils.ease(p, 'easeOutBack')) * 0.8;

                // Titre de la formule
                renderer.drawText(item.title, 0, item.y + 0.75 + slideOffset, {
                    font: 'bold 20px Arial',
                    color: `rgba(100, 116, 139, ${opacity})`,
                    align: 'center'
                });

                // Formule encadree avec LaTeX
                drawMathResult(`recap-formula-${i}`, item.latex, 0, item.y - 0.25 + slideOffset, {
                    opacity,
                    fontSize: '1.5em',
                    color: item.color,
                    bgColor: item.bgColor,
                    borderColor: item.borderColor
                });
            }
        });

        // Message de fin avec delai
        if (contentProgress > 0.75) {
            const endOpacity = MathUtils.ease((contentProgress - 0.75) / 0.25, 'easeOutQuad');
            renderer.drawText('Fin de l\'animation', 0, -4.5, {
                font: '20px Arial',
                color: `rgba(100, 116, 139, ${endOpacity})`,
                align: 'center'
            });
        }
    }
});
