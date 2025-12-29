/**
 * Scenes - Récupération des scènes depuis le registre
 *
 * Les scènes sont définies dans js/scenarios/*.js
 * Chaque fichier de scène s'enregistre dans window.SCENE_REGISTRY
 */

// Récupérer les scènes du registre (remplies par les fichiers scenarios/*.js)
const SCENES = window.SCENE_REGISTRY || [];

// Ancien code conservé pour référence - SUPPRIMER si le registre fonctionne
const SCENES_OLD = [
    // ============================================
    // SCÈNE 1 : INTRODUCTION
    // ============================================
    {
        id: 'intro',
        title: 'Introduction',
        duration: 4000,

        animate(localTime, progress, renderer, state) {
            const opacity = MathUtils.ease(progress, 'easeOutQuad');

            renderer.drawText('Le Produit Scalaire', 0, 0, {
                font: 'bold 48px Arial',
                color: `rgba(37, 99, 235, ${opacity})`,
                align: 'center'
            });
        }
    },

    // ============================================
    // SCÈNE 2 : NORME D'UN VECTEUR
    // ============================================
    {
        id: 'norme',
        title: 'Norme d\'un vecteur',
        duration: 8000,

        animate(localTime, progress, renderer, state) {
            // Coordonnées du vecteur u
            const ux = 4, uy = 3;

            // Phase 1 : Apparition du vecteur (0-30%)
            if (progress < 0.3) {
                const p = progress / 0.3;
                const len = MathUtils.ease(p, 'easeOutQuad');

                renderer.drawVector(0, 0, ux * len, uy * len, {
                    color: '#ef4444',
                    width: 3
                });

                if (p > 0.5) {
                    const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    renderer.drawText('u', ux + 0.3, uy + 0.3, {
                        color: `rgba(239, 68, 68, ${labelOpacity})`,
                        font: 'bold 24px Arial'
                    });
                }
            }
            // Phase 2 : Triangle rectangle (30-60%)
            else if (progress < 0.6) {
                const p = (progress - 0.3) / 0.3;

                // Vecteur complet
                renderer.drawVector(0, 0, ux, uy, {
                    color: '#ef4444',
                    width: 3
                });
                renderer.drawText('u', ux + 0.3, uy + 0.3, {
                    color: '#ef4444',
                    font: 'bold 24px Arial'
                });

                // Triangle rectangle progressif
                const triangleOpacity = MathUtils.ease(p, 'easeOutQuad');

                // Côté horizontal
                renderer.drawSegment(0, 0, ux, 0, {
                    color: `rgba(59, 130, 246, ${triangleOpacity})`,
                    width: 2,
                    dashed: true
                });

                // Côté vertical
                renderer.drawSegment(ux, 0, ux, uy, {
                    color: `rgba(59, 130, 246, ${triangleOpacity})`,
                    width: 2,
                    dashed: true
                });

                // Labels des côtés
                if (p > 0.3) {
                    const labelOp = MathUtils.ease((p - 0.3) / 0.7, 'easeOutQuad');
                    renderer.drawText('4', ux / 2, -0.5, {
                        color: `rgba(59, 130, 246, ${labelOp})`,
                        font: '18px Arial',
                        align: 'center'
                    });
                    renderer.drawText('3', ux + 0.5, uy / 2, {
                        color: `rgba(59, 130, 246, ${labelOp})`,
                        font: '18px Arial'
                    });
                }
            }
            // Phase 3 : Formule et calcul (60-100%)
            else {
                const p = (progress - 0.6) / 0.4;

                // Tout le contenu précédent
                renderer.drawVector(0, 0, ux, uy, {
                    color: '#ef4444',
                    width: 3
                });
                renderer.drawText('u', ux + 0.3, uy + 0.3, {
                    color: '#ef4444',
                    font: 'bold 24px Arial'
                });

                renderer.drawSegment(0, 0, ux, 0, {
                    color: 'rgba(59, 130, 246, 0.7)',
                    width: 2,
                    dashed: true
                });
                renderer.drawSegment(ux, 0, ux, uy, {
                    color: 'rgba(59, 130, 246, 0.7)',
                    width: 2,
                    dashed: true
                });
                renderer.drawText('4', ux / 2, -0.5, {
                    color: '#3b82f6',
                    font: '18px Arial',
                    align: 'center'
                });
                renderer.drawText('3', ux + 0.5, uy / 2, {
                    color: '#3b82f6',
                    font: '18px Arial'
                });

                // Formule et calcul apparaissent ligne par ligne
                const lines = [
                    '||u|| = √(x² + y²)',
                    '||u|| = √(4² + 3²)',
                    '||u|| = √(16 + 9)',
                    '||u|| = √25 = 5'
                ];

                const lineDelay = 0.2;
                lines.forEach((line, i) => {
                    const lineStart = i * lineDelay;
                    if (p > lineStart) {
                        const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                        const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                        renderer.drawText(line, 0, -2.5 - i * 0.6, {
                            color: `rgba(37, 99, 235, ${opacity})`,
                            font: i === 3 ? 'bold 22px Arial' : '20px Arial',
                            align: 'center'
                        });
                    }
                });
            }

            // Stocker pour la suite
            state.uNorm = 5;
        }
    },

    // ============================================
    // SCÈNE 3 : DEUX VECTEURS
    // ============================================
    {
        id: 'deux-vecteurs',
        title: 'Deux vecteurs',
        duration: 6000,

        animate(localTime, progress, renderer, state) {
            const ux = 4, uy = 0;
            const vx = 3, vy = 3;

            // Phase 1 : Vecteur u (0-40%)
            if (progress < 0.4) {
                const p = progress / 0.4;
                const len = MathUtils.ease(p, 'easeOutQuad');

                renderer.drawVector(0, 0, ux * len, uy * len, {
                    color: '#ef4444',
                    width: 3
                });

                if (p > 0.5) {
                    const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    renderer.drawText('u', ux + 0.3, 0.3, {
                        color: `rgba(239, 68, 68, ${labelOpacity})`,
                        font: 'bold 24px Arial'
                    });
                }
            }
            // Phase 2 : Vecteur v apparaît (40-100%)
            else {
                const p = (progress - 0.4) / 0.6;

                // Vecteur u complet
                renderer.drawVector(0, 0, ux, uy, {
                    color: '#ef4444',
                    width: 3
                });
                renderer.drawText('u', ux + 0.3, 0.3, {
                    color: '#ef4444',
                    font: 'bold 24px Arial'
                });

                // Vecteur v avec rotation depuis l'axe x
                const len = MathUtils.ease(Math.min(p * 2, 1), 'easeOutQuad');
                const angle = MathUtils.ease(Math.min(p * 1.5, 1), 'easeOutQuad') * Math.PI / 4;

                const currentVx = len * vx * MathUtils.cos(angle) / Math.sqrt(vx * vx + vy * vy);
                const currentVy = len * vx * MathUtils.sin(angle) / Math.sqrt(vx * vx + vy * vy);
                const scaledLen = len * Math.sqrt(vx * vx + vy * vy);

                renderer.drawVector(0, 0, scaledLen * MathUtils.cos(angle), scaledLen * MathUtils.sin(angle), {
                    color: '#3b82f6',
                    width: 3
                });

                if (p > 0.5) {
                    const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    const finalVx = scaledLen * MathUtils.cos(angle);
                    const finalVy = scaledLen * MathUtils.sin(angle);
                    renderer.drawText('v', finalVx + 0.3, finalVy + 0.3, {
                        color: `rgba(59, 130, 246, ${labelOpacity})`,
                        font: 'bold 24px Arial'
                    });
                }
            }

            // Stocker les vecteurs
            state.ux = ux;
            state.uy = uy;
            state.vx = vx;
            state.vy = vy;
        }
    },

    // ============================================
    // SCÈNE 4 : ANGLE ENTRE LES VECTEURS
    // ============================================
    {
        id: 'angle',
        title: 'Angle θ',
        duration: 6000,

        animate(localTime, progress, renderer, state) {
            const ux = state.ux || 4;
            const uy = state.uy || 0;
            const vx = state.vx || 3;
            const vy = state.vy || 3;
            const angle = Math.PI / 4; // 45°

            // Vecteurs complets
            renderer.drawVector(0, 0, ux, uy, {
                color: '#ef4444',
                width: 3
            });
            renderer.drawText('u', ux + 0.3, 0.3, {
                color: '#ef4444',
                font: 'bold 24px Arial'
            });

            renderer.drawVector(0, 0, vx, vy, {
                color: '#3b82f6',
                width: 3
            });
            renderer.drawText('v', vx + 0.3, vy + 0.3, {
                color: '#3b82f6',
                font: 'bold 24px Arial'
            });

            // Phase 1 : Arc de l'angle (0-50%)
            if (progress < 0.5) {
                const p = progress / 0.5;
                const arcProgress = MathUtils.ease(p, 'easeOutQuad');
                const arcAngle = angle * arcProgress;

                renderer.drawArc(0, 0, 1.5, 0, arcAngle, {
                    color: '#10b981',
                    lineWidth: 2
                });

                if (p > 0.5) {
                    const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    renderer.drawText('θ', 1.2, 0.4, {
                        color: `rgba(16, 185, 129, ${labelOpacity})`,
                        font: 'bold 20px Arial'
                    });
                }
            }
            // Phase 2 : Affichage de l'angle et formule (50-100%)
            else {
                const p = (progress - 0.5) / 0.5;

                // Arc complet
                renderer.drawArc(0, 0, 1.5, 0, angle, {
                    color: '#10b981',
                    lineWidth: 2
                });
                renderer.drawText('θ', 1.2, 0.4, {
                    color: '#10b981',
                    font: 'bold 20px Arial'
                });

                // Label de l'angle
                if (p > 0.2) {
                    const angleOpacity = MathUtils.ease((p - 0.2) / 0.3, 'easeOutQuad');
                    renderer.drawText('θ = 45°', 2, 0.8, {
                        color: `rgba(16, 185, 129, ${angleOpacity})`,
                        font: 'bold 20px Arial'
                    });
                }

                // Formule géométrique
                if (p > 0.5) {
                    const formulaOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    renderer.drawText('u · v = ||u|| × ||v|| × cos(θ)', 0, -3, {
                        color: `rgba(37, 99, 235, ${formulaOpacity})`,
                        font: 'bold 24px Arial',
                        align: 'center'
                    });
                }
            }

            state.angle = angle;
        }
    },

    // ============================================
    // SCÈNE 5 : CALCUL GÉOMÉTRIQUE
    // ============================================
    {
        id: 'calcul-geometrique',
        title: 'Calcul géométrique',
        duration: 10000,

        animate(localTime, progress, renderer, state) {
            const ux = state.ux || 4;
            const uy = state.uy || 0;
            const vx = state.vx || 3;
            const vy = state.vy || 3;
            const angle = state.angle || Math.PI / 4;

            // Éléments graphiques (toujours visibles)
            renderer.drawVector(0, 0, ux, uy, {
                color: '#ef4444',
                width: 3
            });
            renderer.drawText('u', ux + 0.3, 0.3, {
                color: '#ef4444',
                font: 'bold 24px Arial'
            });

            renderer.drawVector(0, 0, vx, vy, {
                color: '#3b82f6',
                width: 3
            });
            renderer.drawText('v', vx + 0.3, vy + 0.3, {
                color: '#3b82f6',
                font: 'bold 24px Arial'
            });

            renderer.drawArc(0, 0, 1.5, 0, angle, {
                color: '#10b981',
                lineWidth: 2
            });
            renderer.drawText('θ', 1.2, 0.4, {
                color: '#10b981',
                font: 'bold 20px Arial'
            });

            // Calcul étape par étape
            const vNorm = Math.sqrt(vx * vx + vy * vy);
            const lines = [
                'u · v = ||u|| × ||v|| × cos(θ)',
                `u · v = 4 × ${MathUtils.format(vNorm, 2)} × cos(45°)`,
                `u · v = ${MathUtils.format(4 * vNorm, 2)} × (√2/2)`,
                `u · v = 12`
            ];

            const lineDelay = 0.2;
            lines.forEach((line, i) => {
                const lineStart = i * lineDelay;
                if (progress > lineStart) {
                    const lineProgress = Math.min((progress - lineStart) / lineDelay, 1);
                    const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                    renderer.drawText(line, 0, -2.5 - i * 0.7, {
                        color: `rgba(37, 99, 235, ${opacity})`,
                        font: i === 3 ? 'bold 26px Arial' : '20px Arial',
                        align: 'center'
                    });
                }
            });

            state.dotProduct = 12;
        }
    },

    // ============================================
    // SCÈNE 6 : PROJECTION ORTHOGONALE
    // ============================================
    {
        id: 'projection',
        title: 'Projection orthogonale',
        duration: 8000,

        animate(localTime, progress, renderer, state) {
            const ux = state.ux || 4;
            const uy = state.uy || 0;
            const vx = state.vx || 3;
            const vy = state.vy || 3;

            // Vecteurs
            renderer.drawVector(0, 0, ux, uy, {
                color: '#ef4444',
                width: 3
            });
            renderer.drawText('u', ux + 0.3, 0.3, {
                color: '#ef4444',
                font: 'bold 24px Arial'
            });

            renderer.drawVector(0, 0, vx, vy, {
                color: '#3b82f6',
                width: 3
            });
            renderer.drawText('v', vx + 0.3, vy + 0.3, {
                color: '#3b82f6',
                font: 'bold 24px Arial'
            });

            // Phase 1 : Point H apparaît (0-30%)
            const dotProduct = ux * vx + uy * vy;
            const uNormSq = ux * ux + uy * uy;
            const projScalar = dotProduct / uNormSq;
            const hx = projScalar * ux;
            const hy = projScalar * uy;

            if (progress > 0.1) {
                const p = Math.min((progress - 0.1) / 0.3, 1);
                const pointProgress = MathUtils.ease(p, 'easeOutQuad');

                // Segment perpendiculaire
                const perpOpacity = pointProgress;
                renderer.drawSegment(vx, vy, hx, hy, {
                    color: `rgba(155, 89, 182, ${perpOpacity})`,
                    width: 2,
                    dashed: true
                });

                // Point H
                renderer.drawPoint(hx, hy, {
                    radius: 6,
                    color: '#9b59b6'
                });

                if (p > 0.5) {
                    const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    renderer.drawText('H', hx, hy - 0.5, {
                        color: `rgba(155, 89, 182, ${labelOpacity})`,
                        font: 'bold 20px Arial',
                        align: 'center'
                    });
                }
            }

            // Phase 2 : Vecteur OH (40-60%)
            if (progress > 0.4) {
                const p = Math.min((progress - 0.4) / 0.2, 1);
                const vectorProgress = MathUtils.ease(p, 'easeOutQuad');

                const currentHx = hx * vectorProgress;
                const currentHy = hy * vectorProgress;

                renderer.drawVector(0, 0, currentHx, currentHy, {
                    color: '#9b59b6',
                    width: 3
                });

                if (p > 0.5) {
                    const labelOpacity = MathUtils.ease((p - 0.5) / 0.5, 'easeOutQuad');
                    renderer.drawText('OH', currentHx / 2, currentHy / 2 - 0.4, {
                        color: `rgba(155, 89, 182, ${labelOpacity})`,
                        font: 'bold 20px Arial',
                        align: 'center'
                    });
                }
            }

            // Phase 3 : Formules (60-100%)
            if (progress > 0.6) {
                const p = (progress - 0.6) / 0.4;

                const lines = [
                    'u · v = ||u|| × OH',
                    `u · v = 4 × 3 = 12`,
                    `(avec OH = ||v||cos(θ) = 3)`
                ];

                const lineDelay = 0.25;
                lines.forEach((line, i) => {
                    const lineStart = i * lineDelay;
                    if (p > lineStart) {
                        const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                        const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                        renderer.drawText(line, 0, -3 - i * 0.7, {
                            color: `rgba(155, 89, 182, ${opacity})`,
                            font: i === 1 ? 'bold 24px Arial' : '18px Arial',
                            align: 'center'
                        });
                    }
                });
            }
        }
    },

    // ============================================
    // SCÈNE 7 : FORMULE ANALYTIQUE
    // ============================================
    {
        id: 'analytique',
        title: 'Formule analytique',
        duration: 8000,

        animate(localTime, progress, renderer, state) {
            const ux = state.ux || 4;
            const uy = state.uy || 0;
            const vx = state.vx || 3;
            const vy = state.vy || 3;

            // Vecteurs
            renderer.drawVector(0, 0, ux, uy, {
                color: '#ef4444',
                width: 3
            });
            renderer.drawVector(0, 0, vx, vy, {
                color: '#3b82f6',
                width: 3
            });

            // Phase 1 : Coordonnées apparaissent (0-30%)
            if (progress > 0) {
                const p = Math.min(progress / 0.3, 1);
                const coordOpacity = MathUtils.ease(p, 'easeOutQuad');

                renderer.drawText(`u(${ux}, ${uy})`, ux + 0.5, 0.3, {
                    color: `rgba(239, 68, 68, ${coordOpacity})`,
                    font: 'bold 22px Arial'
                });

                renderer.drawText(`v(${vx}, ${vy})`, vx + 0.5, vy + 0.3, {
                    color: `rgba(59, 130, 246, ${coordOpacity})`,
                    font: 'bold 22px Arial'
                });
            }

            // Phase 2 : Formule générale (30-50%)
            if (progress > 0.3) {
                const p = Math.min((progress - 0.3) / 0.2, 1);
                const formulaOpacity = MathUtils.ease(p, 'easeOutQuad');

                renderer.drawText('u · v = xu × xv + yu × yv', 0, -2.5, {
                    color: `rgba(37, 99, 235, ${formulaOpacity})`,
                    font: 'bold 24px Arial',
                    align: 'center'
                });
            }

            // Phase 3 : Calcul étape par étape (50-100%)
            if (progress > 0.5) {
                const p = (progress - 0.5) / 0.5;

                const lines = [
                    'u · v = xu × xv + yu × yv',
                    `u · v = ${ux} × ${vx} + ${uy} × ${vy}`,
                    `u · v = 12 + 0`,
                    `u · v = 12`
                ];

                const lineDelay = 0.2;
                lines.forEach((line, i) => {
                    const lineStart = i * lineDelay;
                    if (p > lineStart) {
                        const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                        const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                        renderer.drawText(line, 0, -2.5 - i * 0.7, {
                            color: `rgba(37, 99, 235, ${opacity})`,
                            font: i === 3 ? 'bold 26px Arial' : '20px Arial',
                            align: 'center'
                        });
                    }
                });

                // Message "Même résultat !"
                if (p > 0.8) {
                    const msgOpacity = MathUtils.ease((p - 0.8) / 0.2, 'easeOutQuad');
                    renderer.drawText('✓ Même résultat !', 0, -6, {
                        color: `rgba(16, 185, 129, ${msgOpacity})`,
                        font: 'bold 22px Arial',
                        align: 'center'
                    });
                }
            }
        }
    },

    // ============================================
    // SCÈNE 8 : ORTHOGONALITÉ
    // ============================================
    {
        id: 'orthogonalite',
        title: 'Orthogonalité',
        duration: 10000,

        animate(localTime, progress, renderer, state) {
            // Nouveaux vecteurs orthogonaux
            const ux = 3, uy = 2;
            const vx = -2, vy = 3;

            // Phase 1 : Transition - nouveaux vecteurs apparaissent (0-25%)
            if (progress < 0.25) {
                const p = progress / 0.25;
                const len = MathUtils.ease(p, 'easeOutQuad');

                renderer.drawVector(0, 0, ux * len, uy * len, {
                    color: '#ef4444',
                    width: 3
                });

                if (p > 0.3) {
                    const vProgress = MathUtils.ease((p - 0.3) / 0.7, 'easeOutQuad');
                    renderer.drawVector(0, 0, vx * vProgress, vy * vProgress, {
                        color: '#3b82f6',
                        width: 3
                    });
                }
            }
            // Phase 2 : Calcul du produit scalaire (25-60%)
            else if (progress < 0.6) {
                const p = (progress - 0.25) / 0.35;

                // Vecteurs complets
                renderer.drawVector(0, 0, ux, uy, {
                    color: '#ef4444',
                    width: 3
                });
                renderer.drawText(`u(${ux}, ${uy})`, ux + 0.3, uy + 0.3, {
                    color: '#ef4444',
                    font: 'bold 20px Arial'
                });

                renderer.drawVector(0, 0, vx, vy, {
                    color: '#3b82f6',
                    width: 3
                });
                renderer.drawText(`v(${vx}, ${vy})`, vx - 1.2, vy + 0.3, {
                    color: '#3b82f6',
                    font: 'bold 20px Arial'
                });

                // Calcul
                const lines = [
                    `u · v = ${ux} × (${vx}) + ${uy} × ${vy}`,
                    `u · v = ${ux * vx} + ${uy * vy}`,
                    `u · v = 0`
                ];

                const lineDelay = 0.25;
                lines.forEach((line, i) => {
                    const lineStart = i * lineDelay;
                    if (p > lineStart) {
                        const lineProgress = Math.min((p - lineStart) / lineDelay, 1);
                        const opacity = MathUtils.ease(lineProgress, 'easeOutQuad');

                        renderer.drawText(line, 0, -3 - i * 0.7, {
                            color: `rgba(37, 99, 235, ${opacity})`,
                            font: i === 2 ? 'bold 26px Arial' : '20px Arial',
                            align: 'center'
                        });
                    }
                });
            }
            // Phase 3 : Angle droit visible (60-100%)
            else {
                const p = (progress - 0.6) / 0.4;

                // Vecteurs
                renderer.drawVector(0, 0, ux, uy, {
                    color: '#ef4444',
                    width: 3
                });
                renderer.drawVector(0, 0, vx, vy, {
                    color: '#3b82f6',
                    width: 3
                });

                // Carré de l'angle droit
                if (p > 0.1) {
                    const squareSize = 0.5;
                    const squareOpacity = MathUtils.ease((p - 0.1) / 0.2, 'easeOutQuad');

                    const uNorm = Math.sqrt(ux * ux + uy * uy);
                    const vNorm = Math.sqrt(vx * vx + vy * vy);

                    const ux_norm = ux / uNorm * squareSize;
                    const uy_norm = uy / uNorm * squareSize;
                    const vx_norm = vx / vNorm * squareSize;
                    const vy_norm = vy / vNorm * squareSize;

                    renderer.drawSegment(ux_norm, uy_norm, ux_norm + vx_norm, uy_norm + vy_norm, {
                        color: `rgba(16, 185, 129, ${squareOpacity})`,
                        width: 2
                    });
                    renderer.drawSegment(ux_norm + vx_norm, uy_norm + vy_norm, vx_norm, vy_norm, {
                        color: `rgba(16, 185, 129, ${squareOpacity})`,
                        width: 2
                    });
                    renderer.drawSegment(ux_norm, uy_norm, 0, 0, {
                        color: `rgba(16, 185, 129, ${squareOpacity})`,
                        width: 2
                    });
                    renderer.drawSegment(vx_norm, vy_norm, 0, 0, {
                        color: `rgba(16, 185, 129, ${squareOpacity})`,
                        width: 2
                    });
                }

                // Message "ORTHOGONAUX"
                if (p > 0.3) {
                    const msgOpacity = MathUtils.ease((p - 0.3) / 0.2, 'easeOutQuad');
                    renderer.drawText('Vecteurs ORTHOGONAUX', 0, -3, {
                        color: `rgba(59, 130, 246, ${msgOpacity})`,
                        font: 'bold 28px Arial',
                        align: 'center'
                    });
                }

                // Encadré de la propriété
                if (p > 0.5) {
                    const boxOpacity = MathUtils.ease((p - 0.5) / 0.3, 'easeOutQuad');
                    renderer.drawText('u ⊥ v  ⟺  u · v = 0', 0, -4.5, {
                        color: `rgba(37, 99, 235, ${boxOpacity})`,
                        font: 'bold 24px Arial',
                        align: 'center'
                    });
                }
            }
        }
    },

    // ============================================
    // SCÈNE 9 : SIGNE DU PRODUIT SCALAIRE
    // ============================================
    {
        id: 'signe',
        title: 'Signe du produit scalaire',
        duration: 12000,

        animate(localTime, progress, renderer, state) {
            const ux = 3, uy = 0;

            // Vecteur u fixe
            renderer.drawVector(0, 0, ux, uy, {
                color: '#ef4444',
                width: 3
            });
            renderer.drawText('u', ux + 0.3, 0.3, {
                color: '#ef4444',
                font: 'bold 24px Arial'
            });

            // Vecteur v tourne autour de l'origine
            const angle = progress * 2 * Math.PI;
            const vLen = 2.5;
            const vx = vLen * MathUtils.cos(angle);
            const vy = vLen * MathUtils.sin(angle);

            renderer.drawVector(0, 0, vx, vy, {
                color: '#3b82f6',
                width: 3
            });
            renderer.drawText('v', vx + 0.3, vy + 0.3, {
                color: '#3b82f6',
                font: 'bold 24px Arial'
            });

            // Calcul du produit scalaire
            const dotProduct = ux * vx + uy * vy;
            const angleDeg = (angle * 180 / Math.PI) % 360;

            // Déterminer la couleur et le message
            let color, message, bgColor;
            if (Math.abs(dotProduct) < 0.3) {
                color = '#3b82f6';
                message = 'Angle droit (θ = 90°)';
                bgColor = 'rgba(59, 130, 246, 0.1)';
            } else if (dotProduct > 0) {
                color = '#10b981';
                message = 'Angle aigu (θ < 90°)';
                bgColor = 'rgba(16, 185, 129, 0.1)';
            } else {
                color = '#f97316';
                message = 'Angle obtus (θ > 90°)';
                bgColor = 'rgba(249, 115, 22, 0.1)';
            }

            // Zone colorée de fond
            if (progress > 0.1) {
                const sectors = [
                    { start: -Math.PI / 2, end: Math.PI / 2, color: 'rgba(16, 185, 129, 0.15)' }, // vert
                    { start: Math.PI / 2 - 0.1, end: Math.PI / 2 + 0.1, color: 'rgba(59, 130, 246, 0.2)' }, // bleu
                    { start: Math.PI / 2, end: 3 * Math.PI / 2, color: 'rgba(249, 115, 22, 0.15)' }, // orange
                    { start: 3 * Math.PI / 2 - 0.1, end: 3 * Math.PI / 2 + 0.1, color: 'rgba(59, 130, 246, 0.2)' }, // bleu
                ];

                sectors.forEach(sector => {
                    for (let a = sector.start; a < sector.end; a += 0.05) {
                        const r = 5;
                        const x1 = r * MathUtils.cos(a);
                        const y1 = r * MathUtils.sin(a);
                        renderer.drawSegment(0, 0, x1, y1, {
                            color: sector.color,
                            width: 20,
                            alpha: 0.3
                        });
                    }
                });
            }

            // Affichage des informations
            renderer.drawText(`u · v = ${MathUtils.format(dotProduct, 2)}`, 0, -3.5, {
                color: color,
                font: 'bold 28px Arial',
                align: 'center'
            });

            renderer.drawText(`θ = ${MathUtils.format(angleDeg, 1)}°`, 0, -4.5, {
                color: '#64748b',
                font: '20px Arial',
                align: 'center'
            });

            renderer.drawText(message, 0, -5.5, {
                color: color,
                font: 'bold 22px Arial',
                align: 'center'
            });
        }
    },

    // ============================================
    // SCÈNE 10 : RÉCAPITULATIF
    // ============================================
    {
        id: 'recap',
        title: 'Récapitulatif',
        duration: 6000,

        animate(localTime, progress, renderer, state) {
            const formulas = [
                {
                    title: 'Formule géométrique',
                    formula: 'u · v = ||u|| × ||v|| × cos(θ)',
                    y: 1.5,
                    color: '#10b981'
                },
                {
                    title: 'Formule analytique',
                    formula: 'u · v = xu × xv + yu × yv',
                    y: -0.5,
                    color: '#3b82f6'
                },
                {
                    title: 'Critère d\'orthogonalité',
                    formula: 'u ⊥ v  ⟺  u · v = 0',
                    y: -2.5,
                    color: '#ef4444'
                }
            ];

            formulas.forEach((item, i) => {
                const startTime = i * 0.25;
                if (progress > startTime) {
                    const p = Math.min((progress - startTime) / 0.2, 1);
                    const opacity = MathUtils.ease(p, 'easeOutQuad');
                    const offset = (1 - p) * 0.3;

                    // Titre
                    renderer.drawText(item.title, 0, item.y + offset, {
                        color: `rgba(100, 116, 139, ${opacity})`,
                        font: 'bold 18px Arial',
                        align: 'center'
                    });

                    // Formule encadrée
                    renderer.drawText(item.formula, 0, item.y - 0.6 + offset, {
                        color: `${item.color.replace(')', `, ${opacity})`).replace('rgb', 'rgba')}`,
                        font: 'bold 24px Arial',
                        align: 'center'
                    });

                    // Ligne de séparation
                    if (i < formulas.length - 1 && p > 0.8) {
                        const lineOpacity = MathUtils.ease((p - 0.8) / 0.2, 'easeOutQuad') * opacity;
                        renderer.drawSegment(-3, item.y - 1.3, 3, item.y - 1.3, {
                            color: `rgba(226, 232, 240, ${lineOpacity})`,
                            width: 1
                        });
                    }
                }
            });
        }
    }
];

/**
 * Gestionnaire de scènes
 * Coordonne l'exécution des scènes avec la timeline
 */
const SceneManager = {
    scenes: [],
    currentState: {},
    renderer: null,

    /**
     * Initialiser avec les scènes
     */
    init(scenes, renderer) {
        this.scenes = scenes;
        this.renderer = renderer;
        this.currentState = {};
        return this;
    },

    /**
     * Obtenir les scènes formatées pour la timeline
     */
    getScenesForTimeline() {
        return this.scenes.map(scene => ({
            id: scene.id,
            title: scene.title,
            duration: scene.duration
        }));
    },

    /**
     * Rendre la frame actuelle
     * Appelé par la timeline à chaque mise à jour
     */
    render(currentTime, sceneData) {
        if (!this.renderer || !sceneData || !sceneData.scene) return;

        const scene = this.scenes.find(s => s.id === sceneData.scene.id);
        if (!scene || !scene.animate) return;

        // Appeler la fonction d'animation de la scène
        scene.animate(
            sceneData.localTime,
            sceneData.progress,
            this.renderer,
            this.currentState
        );
    },

    /**
     * Réinitialiser l'état
     */
    reset() {
        this.currentState = {};
    }
};

/**
 * Helpers pour créer des animations complexes
 */
const AnimationHelpers = {
    /**
     * Animation de morphing entre deux valeurs
     */
    morph(from, to, progress, easing = 'easeInOutQuad') {
        const t = MathUtils.ease(progress, easing);
        if (typeof from === 'number') {
            return MathUtils.lerp(from, to, t);
        }
        // Pour les objets {x, y}
        return {
            x: MathUtils.lerp(from.x, to.x, t),
            y: MathUtils.lerp(from.y, to.y, t)
        };
    },

    /**
     * Animation séquencée (plusieurs étapes dans une scène)
     * @param progress - Progression totale (0-1)
     * @param steps - Array de {at, duration, fn}
     */
    sequence(progress, steps) {
        const totalDuration = steps.reduce((sum, s) => sum + (s.duration || 1), 0);
        let currentTime = progress * totalDuration;

        for (const step of steps) {
            const stepDuration = step.duration || 1;
            if (currentTime <= stepDuration) {
                const stepProgress = currentTime / stepDuration;
                return step.fn(stepProgress);
            }
            currentTime -= stepDuration;
        }
    },

    /**
     * Délai avant de commencer (retourne 0 puis progress ajusté)
     */
    delay(progress, delayRatio) {
        if (progress < delayRatio) return 0;
        return (progress - delayRatio) / (1 - delayRatio);
    },

    /**
     * Animation qui se répète
     */
    loop(progress, count = 1) {
        return (progress * count) % 1;
    },

    /**
     * Animation qui va et vient
     */
    pingPong(progress) {
        return progress < 0.5
            ? progress * 2
            : 2 - progress * 2;
    },

    /**
     * Apparition progressive (fade in)
     */
    fadeIn(progress, start = 0, end = 0.3) {
        if (progress < start) return 0;
        if (progress > end) return 1;
        return (progress - start) / (end - start);
    },

    /**
     * Disparition progressive (fade out)
     */
    fadeOut(progress, start = 0.7, end = 1) {
        if (progress < start) return 1;
        if (progress > end) return 0;
        return 1 - (progress - start) / (end - start);
    },

    /**
     * Écriture progressive d'un texte
     */
    typewriter(text, progress) {
        const len = Math.floor(text.length * progress);
        return text.substring(0, len);
    },

    /**
     * Tracé progressif d'une courbe (pour les fonctions)
     */
    drawProgressively(fn, progress, renderer, options = {}) {
        const { minX = -5, maxX = 5, color = '#2563eb', lineWidth = 2 } = options;
        const effectiveMaxX = MathUtils.lerp(minX, maxX, progress);

        renderer.drawFunction(fn, {
            minX,
            maxX: effectiveMaxX,
            color,
            lineWidth
        });
    }
};
