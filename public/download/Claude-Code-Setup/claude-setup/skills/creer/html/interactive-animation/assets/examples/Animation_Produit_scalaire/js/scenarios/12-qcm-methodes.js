/**
 * Scene 12 : QCM - Choisir la methode adaptee
 * 3 enonces a associer a la bonne methode
 * Pause pour reflexion puis correction avec fleches
 */

window.SCENE_REGISTRY.push({
    id: 'qcm-methodes',
    title: 'Quelle methode choisir ?',
    duration: 35000,
    hideGrid: true,
    hideAxes: true,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);

        // Fond degrade
        const ctx = renderer.ctx;
        const gradient = ctx.createLinearGradient(0, 0, 0, renderer.height);
        gradient.addColorStop(0, 'rgba(248, 250, 252, 1)');
        gradient.addColorStop(1, 'rgba(241, 245, 249, 1)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, renderer.width, renderer.height);

        // Enonces (a gauche)
        const enonces = [
            {
                id: 'E1',
                text: 'On connait les coordonnees',
                subtext: 'des deux vecteurs',
                y: 2.5,
                solution: 'analytique',
                color: '#ef4444'
            },
            {
                id: 'E2',
                text: 'On connait les normes et',
                subtext: 'l\'angle entre les vecteurs',
                y: 0,
                solution: 'geometrique',
                color: '#3b82f6'
            },
            {
                id: 'E3',
                text: 'On veut savoir si deux',
                subtext: 'vecteurs sont orthogonaux',
                y: -2.5,
                solution: 'orthogonalite',
                color: '#10b981'
            }
        ];

        // Methodes (a droite)
        const methodes = [
            {
                id: 'M1',
                name: 'Geometrique',
                latex: '\\|\\vec{u}\\| \\times \\|\\vec{v}\\| \\times \\cos\\theta',
                y: 2.5,
                color: '#059669',
                bgColor: 'rgba(209, 250, 229, 0.98)'
            },
            {
                id: 'M2',
                name: 'Analytique',
                latex: 'x_u \\times x_v + y_u \\times y_v',
                y: 0,
                color: '#1d4ed8',
                bgColor: 'rgba(219, 234, 254, 0.98)'
            },
            {
                id: 'M3',
                name: 'Test orthogonalite',
                latex: '\\vec{u} \\cdot \\vec{v} = 0 \\,?',
                y: -2.5,
                color: '#d97706',
                bgColor: 'rgba(254, 243, 199, 0.98)'
            }
        ];

        // Phase 1 : Titre (0-8%)
        if (contentProgress > 0) {
            const titleOpacity = MathUtils.ease(Math.min(contentProgress / 0.08, 1), 'easeOutQuad');
            drawMathBox('qcm-title', '\\textbf{Quelle methode utiliser ?}', 0, 4.5, {
                opacity: titleOpacity,
                fontSize: '1.8em',
                color: '#1e3a8a',
                bgColor: 'rgba(219, 234, 254, 0.98)',
                borderColor: '#3b82f6',
                borderWidth: 2
            });
        }

        // Phase 2 : Apparition des enonces (8-25%)
        enonces.forEach((enonce, i) => {
            const startTime = 0.08 + i * 0.06;
            if (contentProgress > startTime) {
                const p = Math.min((contentProgress - startTime) / 0.08, 1);
                const opacity = MathUtils.ease(p, 'easeOutCubic');
                const slideX = (1 - MathUtils.ease(p, 'easeOutBack')) * 1.5;

                // Numero
                renderer.drawText(enonce.id, -10 - slideX, enonce.y + 0.3, {
                    font: 'bold 24px Arial',
                    color: `rgba(${enonce.color === '#ef4444' ? '239,68,68' : enonce.color === '#3b82f6' ? '59,130,246' : '16,185,129'}, ${opacity})`,
                    align: 'center'
                });

                // Texte
                drawTextBox(renderer, enonce.text, -7 - slideX, enonce.y + 0.3, {
                    font: '18px Arial', color: '#374151', opacity,
                    bgColor: 'rgba(255, 255, 255, 0.95)', align: 'left'
                });
                drawTextBox(renderer, enonce.subtext, -7 - slideX, enonce.y - 0.4, {
                    font: '18px Arial', color: '#374151', opacity,
                    bgColor: 'rgba(255, 255, 255, 0.95)', align: 'left'
                });
            }
        });

        // Phase 3 : Apparition des methodes (25-40%)
        methodes.forEach((methode, i) => {
            const startTime = 0.25 + i * 0.05;
            if (contentProgress > startTime) {
                const p = Math.min((contentProgress - startTime) / 0.08, 1);
                const opacity = MathUtils.ease(p, 'easeOutCubic');
                const slideX = (1 - MathUtils.ease(p, 'easeOutBack')) * 1.5;

                // Nom de la methode
                renderer.drawText(methode.name, 6 + slideX, methode.y + 0.6, {
                    font: 'bold 16px Arial',
                    color: `rgba(100, 116, 139, ${opacity})`,
                    align: 'center'
                });

                // Formule
                drawMathBox(`methode-${i}`, methode.latex, 6 + slideX, methode.y - 0.2, {
                    opacity,
                    fontSize: '1.2em',
                    color: methode.color,
                    bgColor: methode.bgColor,
                    borderColor: methode.color,
                    borderWidth: 1
                });
            }
        });

        // Phase 4 : Pause reflexion (40-55%)
        if (contentProgress > 0.40 && contentProgress < 0.55) {
            const p = (contentProgress - 0.40) / 0.15;
            const pulseOpacity = 0.6 + 0.4 * Math.sin(p * Math.PI * 4);

            renderer.drawText('Associez chaque enonce a la methode adaptee...', 0, -4, {
                font: 'italic 20px Arial',
                color: `rgba(100, 116, 139, ${pulseOpacity})`,
                align: 'center'
            });
        }

        // Phase 5 : Correction avec fleches (55-100%)
        if (contentProgress > 0.55) {
            const correctionProgress = (contentProgress - 0.55) / 0.45;

            // Mapping : E1 -> M2 (analytique), E2 -> M1 (geometrique), E3 -> M3 (orthogonalite)
            const associations = [
                { from: enonces[0], to: methodes[1], delay: 0, color: '#1d4ed8' },      // E1 -> Analytique
                { from: enonces[1], to: methodes[0], delay: 0.25, color: '#059669' },   // E2 -> Geometrique
                { from: enonces[2], to: methodes[2], delay: 0.50, color: '#d97706' }    // E3 -> Orthogonalite
            ];

            associations.forEach((assoc, i) => {
                if (correctionProgress > assoc.delay) {
                    const p = Math.min((correctionProgress - assoc.delay) / 0.2, 1);
                    const arrowProgress = MathUtils.ease(p, 'easeOutCubic');
                    const opacity = arrowProgress;

                    // Points de depart et arrivee (ajustes pour eviter le texte)
                    const x1 = -2.5;  // Apres les enonces
                    const y1 = assoc.from.y;
                    const x2 = 3.5;   // Avant les methodes
                    const y2 = assoc.to.y;

                    // Dessiner la fleche progressivement
                    const currentX = x1 + (x2 - x1) * arrowProgress;
                    const currentY = y1 + (y2 - y1) * arrowProgress;

                    // Ligne courbe (bezier simplifie en segments)
                    ctx.save();
                    ctx.globalAlpha = opacity;
                    ctx.strokeStyle = assoc.color;
                    ctx.lineWidth = 3;
                    ctx.setLineDash([]);

                    const startPixel = renderer.toPixel(x1, y1);
                    const endPixel = renderer.toPixel(currentX, currentY);
                    const midY = (y1 + y2) / 2;
                    // Courbure moderee vers le haut
                    const curveOffset = Math.abs(y2 - y1) > 1 ? 0.8 : 0.3;
                    const controlPixel = renderer.toPixel((x1 + x2) / 2, midY + curveOffset);

                    ctx.beginPath();
                    ctx.moveTo(startPixel.x, startPixel.y);
                    ctx.quadraticCurveTo(controlPixel.x, controlPixel.y, endPixel.x, endPixel.y);
                    ctx.stroke();

                    // Pointe de fleche si complete
                    if (arrowProgress > 0.9) {
                        const angle = Math.atan2(y2 - midY - curveOffset, x2 - (x1 + x2) / 2);
                        const arrowSize = 12;

                        ctx.beginPath();
                        ctx.moveTo(endPixel.x, endPixel.y);
                        ctx.lineTo(
                            endPixel.x - arrowSize * Math.cos(angle - Math.PI / 6),
                            endPixel.y + arrowSize * Math.sin(angle - Math.PI / 6)
                        );
                        ctx.moveTo(endPixel.x, endPixel.y);
                        ctx.lineTo(
                            endPixel.x - arrowSize * Math.cos(angle + Math.PI / 6),
                            endPixel.y + arrowSize * Math.sin(angle + Math.PI / 6)
                        );
                        ctx.stroke();
                    }

                    ctx.restore();

                    // Badge "correct" sur l'enonce
                    if (p > 0.8) {
                        const checkOpacity = (p - 0.8) / 0.2;
                        renderer.drawText('✓', -10.8, assoc.from.y + 0.3, {
                            font: 'bold 20px Arial',
                            color: `rgba(16, 185, 129, ${checkOpacity})`,
                            align: 'center'
                        });
                    }
                }
            });

            // Message final
            if (correctionProgress > 0.85) {
                const finalOpacity = MathUtils.ease((correctionProgress - 0.85) / 0.15, 'easeOutQuad');
                drawMathBox('final-msg', '\\text{Choisissez toujours la methode la plus adaptee !}', 0, -4, {
                    opacity: finalOpacity,
                    fontSize: '1.3em',
                    color: '#059669',
                    bgColor: 'rgba(209, 250, 229, 0.98)',
                    borderColor: '#10b981',
                    borderWidth: 2
                });
            }
        }
    }
});
