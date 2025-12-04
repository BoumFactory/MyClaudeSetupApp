/**
 * Scene 11 : Exemple avance
 * Vecteurs quelconques u(2,3) et v(4,-1)
 * On applique les 3 methodes et on verifie la coherence
 */

window.SCENE_REGISTRY.push({
    id: 'exemple-avance',
    title: 'Exemple avance',
    duration: 38000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);

        // Vecteurs quelconques (pas sur les axes)
        const ux = 2, uy = 3;
        const vx = 4, vy = -1;

        // Calculs
        const uNorm = Math.sqrt(ux * ux + uy * uy);
        const vNorm = Math.sqrt(vx * vx + vy * vy);
        const dotProduct = ux * vx + uy * vy;
        const cosTheta = dotProduct / (uNorm * vNorm);
        const theta = Math.acos(cosTheta);
        const thetaDeg = theta * 180 / Math.PI;

        // Phase 1 : Presentation des vecteurs (0-15%)
        if (contentProgress < 0.15) {
            const p = contentProgress / 0.15;
            const len = MathUtils.ease(p, 'easeOutQuad');

            renderer.drawVector(0, 0, ux * len, uy * len, { color: '#ef4444', width: 3 });
            if (p > 0.3) {
                drawMathBox('vec-u', '\\vec{u}', ux * len + 0.4, uy * len + 0.4, {
                    opacity: (p - 0.3) / 0.7, fontSize: '1.2em', color: '#ef4444',
                    bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
                });
            }

            if (p > 0.5) {
                const vProgress = (p - 0.5) / 0.5;
                renderer.drawVector(0, 0, vx * vProgress, vy * vProgress, { color: '#3b82f6', width: 3 });
                if (vProgress > 0.6) {
                    drawMathBox('vec-v', '\\vec{v}', vx * vProgress + 0.4, vy * vProgress - 0.4, {
                        opacity: (vProgress - 0.6) / 0.4, fontSize: '1.2em', color: '#3b82f6',
                        bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
                    });
                }
            }

            // Coordonnees a gauche
            if (p > 0.7) {
                const coordOpacity = (p - 0.7) / 0.3;
                drawMathBox('coord-u', `\\vec{u}(${ux}\\,;\\,${uy})`, -9, 3.5, {
                    opacity: coordOpacity, fontSize: '1.2em', color: '#ef4444',
                    bgColor: 'rgba(254, 226, 226, 0.95)', align: 'left'
                });
                drawMathBox('coord-v', `\\vec{v}(${vx}\\,;\\,${vy})`, -9, 2, {
                    opacity: coordOpacity, fontSize: '1.2em', color: '#3b82f6',
                    bgColor: 'rgba(219, 234, 254, 0.95)', align: 'left'
                });
            }
        }
        // Phase 2 : Methode analytique (15-40%)
        else if (contentProgress < 0.4) {
            const p = (contentProgress - 0.15) / 0.25;

            // Vecteurs complets
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u', '\\vec{u}', ux + 0.4, uy + 0.4, {
                fontSize: '1.2em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });
            renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
            drawMathBox('vec-v', '\\vec{v}', vx + 0.4, vy - 0.4, {
                fontSize: '1.2em', color: '#3b82f6',
                bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
            });

            // Titre methode
            if (p > 0) {
                const titleOpacity = Math.min(p / 0.15, 1);
                drawMathBox('method-title', '\\textbf{Methode analytique}', -9, 4, {
                    opacity: titleOpacity, fontSize: '1.3em', color: '#1d4ed8',
                    bgColor: 'rgba(219, 234, 254, 0.98)', align: 'left',
                    borderColor: '#3b82f6', borderWidth: 1
                });
            }

            // Calcul etape par etape
            const formulas = [
                `\\vec{u} \\cdot \\vec{v} = x_u \\times x_v + y_u \\times y_v`,
                `\\vec{u} \\cdot \\vec{v} = ${ux} \\times ${vx} + ${uy} \\times (${vy})`,
                `\\vec{u} \\cdot \\vec{v} = ${ux * vx} + (${uy * vy})`,
                `\\vec{u} \\cdot \\vec{v} = ${dotProduct}`
            ];

            const lineDelay = 0.2;
            formulas.forEach((latex, i) => {
                const lineStart = 0.1 + i * lineDelay;
                if (p > lineStart) {
                    const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');
                    const isResult = i === formulas.length - 1;

                    if (isResult) {
                        drawMathResult(`ana-${i}`, latex, -9, 2.5 - i * 1.5, {
                            opacity, align: 'left', color: '#1d4ed8'
                        });
                    } else {
                        drawMathBox(`ana-${i}`, latex, -9, 2.5 - i * 1.5, {
                            opacity, align: 'left', fontSize: '1.15em',
                            color: i === 0 ? '#1e3a8a' : '#374151',
                            bgColor: 'rgba(255, 255, 255, 0.95)'
                        });
                    }
                }
            });
        }
        // Phase 3 : Methode geometrique (40-70%)
        else if (contentProgress < 0.7) {
            const p = (contentProgress - 0.4) / 0.3;

            // Vecteurs
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u', '\\vec{u}', ux + 0.4, uy + 0.4, {
                fontSize: '1.2em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });
            renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
            drawMathBox('vec-v', '\\vec{v}', vx + 0.4, vy - 0.4, {
                fontSize: '1.2em', color: '#3b82f6',
                bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
            });

            // Arc de l'angle
            const angleU = Math.atan2(uy, ux);
            const angleV = Math.atan2(vy, vx);
            renderer.drawArc(0, 0, 1.0, Math.min(angleU, angleV), Math.max(angleU, angleV), {
                strokeColor: '#10b981', fillColor: 'rgba(16, 185, 129, 0.15)', lineWidth: 2
            });
            drawMathBox('theta-label', '\\theta', 1.3, 0.8, {
                fontSize: '1.1em', color: '#10b981', bgColor: 'rgba(209, 250, 229, 0.9)'
            });

            // Titre methode
            if (p > 0) {
                const titleOpacity = Math.min(p / 0.15, 1);
                drawMathBox('method-title-2', '\\textbf{Methode geometrique}', -9, 4, {
                    opacity: titleOpacity, fontSize: '1.3em', color: '#059669',
                    bgColor: 'rgba(209, 250, 229, 0.98)', align: 'left',
                    borderColor: '#10b981', borderWidth: 1
                });
            }

            // Calculs
            const formulas = [
                `\\|\\vec{u}\\| = \\sqrt{${ux}^2 + ${uy}^2} = \\sqrt{${ux*ux + uy*uy}} \\approx ${MathUtils.format(uNorm, 2)}`,
                `\\|\\vec{v}\\| = \\sqrt{${vx}^2 + (${vy})^2} = \\sqrt{${vx*vx + vy*vy}} \\approx ${MathUtils.format(vNorm, 2)}`,
                `\\theta \\approx ${MathUtils.format(thetaDeg, 1)}^\\circ`,
                `\\vec{u} \\cdot \\vec{v} = ${MathUtils.format(uNorm, 2)} \\times ${MathUtils.format(vNorm, 2)} \\times \\cos(${MathUtils.format(thetaDeg, 0)}^\\circ)`,
                `\\vec{u} \\cdot \\vec{v} = ${dotProduct}`
            ];

            const lineDelay = 0.15;
            formulas.forEach((latex, i) => {
                const lineStart = 0.1 + i * lineDelay;
                if (p > lineStart) {
                    const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');
                    const isResult = i === formulas.length - 1;

                    if (isResult) {
                        drawMathResult(`geom-${i}`, latex, -9, 2.5 - i * 1.3, {
                            opacity, align: 'left', color: '#059669'
                        });
                    } else {
                        drawMathBox(`geom-${i}`, latex, -9, 2.5 - i * 1.3, {
                            opacity, align: 'left', fontSize: '1.1em',
                            color: '#374151', bgColor: 'rgba(255, 255, 255, 0.95)'
                        });
                    }
                }
            });
        }
        // Phase 4 : Conclusion (70-100%)
        else {
            const p = (contentProgress - 0.7) / 0.3;

            // Vecteurs
            renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
            drawMathBox('vec-u', '\\vec{u}', ux + 0.4, uy + 0.4, {
                fontSize: '1.2em', color: '#ef4444',
                bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
            });
            renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
            drawMathBox('vec-v', '\\vec{v}', vx + 0.4, vy - 0.4, {
                fontSize: '1.2em', color: '#3b82f6',
                bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
            });

            // Arc
            const angleU = Math.atan2(uy, ux);
            const angleV = Math.atan2(vy, vx);
            renderer.drawArc(0, 0, 1.0, Math.min(angleU, angleV), Math.max(angleU, angleV), {
                strokeColor: '#10b981', fillColor: 'rgba(16, 185, 129, 0.15)', lineWidth: 2
            });

            // Conclusion
            if (p > 0.1) {
                const opacity = MathUtils.ease((p - 0.1) / 0.3, 'easeOutQuad');
                drawMathBox('conclusion-title', '\\checkmark \\textbf{ Verification}', -9, 3.5, {
                    opacity, fontSize: '1.3em', color: '#059669',
                    bgColor: 'rgba(209, 250, 229, 0.98)', align: 'left',
                    borderColor: '#10b981', borderWidth: 2
                });
            }

            if (p > 0.3) {
                const opacity = MathUtils.ease((p - 0.3) / 0.3, 'easeOutQuad');
                drawMathBox('conclusion-1', `\\text{Analytique : } \\vec{u} \\cdot \\vec{v} = ${dotProduct}`, -9, 2, {
                    opacity, fontSize: '1.2em', color: '#1d4ed8',
                    bgColor: 'rgba(219, 234, 254, 0.95)', align: 'left'
                });
            }

            if (p > 0.5) {
                const opacity = MathUtils.ease((p - 0.5) / 0.3, 'easeOutQuad');
                drawMathBox('conclusion-2', `\\text{Geometrique : } \\vec{u} \\cdot \\vec{v} \\approx ${dotProduct}`, -9, 0.5, {
                    opacity, fontSize: '1.2em', color: '#059669',
                    bgColor: 'rgba(209, 250, 229, 0.95)', align: 'left'
                });
            }

            if (p > 0.7) {
                const opacity = MathUtils.ease((p - 0.7) / 0.3, 'easeOutQuad');
                drawMathResult('same-result', '\\text{Meme resultat !}', 0, -3.5, {
                    opacity, fontSize: '1.5em', color: '#059669'
                });
            }
        }
    }
});
