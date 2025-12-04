/**
 * Scene 9 : Signe du produit scalaire
 * v tourne autour de u, zones colorees selon le signe
 * IMPORTANT: LaTeX statique + valeurs dynamiques separees pour eviter recompilation
 */

window.SCENE_REGISTRY.push({
    id: 'signe',
    title: 'Signe du produit scalaire',
    duration: 20000,

    animate(localTime, progress, renderer, state) {
        const { contentProgress } = getProgressWithDelay(progress, 0.70);
        const ux = 3, uy = 0;

        // Zones de fond colorees (toujours visibles apres 10%)
        if (contentProgress > 0.05) {
            const zoneOpacity = Math.min((contentProgress - 0.05) / 0.1, 0.15);

            // Zone verte (angle aigu) : -90 a +90 degres
            for (let a = -Math.PI / 2; a < Math.PI / 2; a += 0.05) {
                const r = 5.5;
                renderer.drawSegment(0, 0, r * MathUtils.cos(a), r * MathUtils.sin(a), {
                    color: `rgba(16, 185, 129, ${zoneOpacity})`, width: 15
                });
            }

            // Zone orange (angle obtus) : +90 a +270 degres
            for (let a = Math.PI / 2; a < 3 * Math.PI / 2; a += 0.05) {
                const r = 5.5;
                renderer.drawSegment(0, 0, r * MathUtils.cos(a), r * MathUtils.sin(a), {
                    color: `rgba(249, 115, 22, ${zoneOpacity})`, width: 15
                });
            }
        }

        // Vecteur u fixe
        renderer.drawVector(0, 0, ux, uy, { color: '#ef4444', width: 3 });
        drawMathBox('vec-u-label', '\\vec{u}', ux + 0.4, 0.5, {
            fontSize: '1.2em', color: '#ef4444',
            bgColor: 'rgba(254, 226, 226, 0.9)', padding: '4px 8px'
        });

        // Vecteur v tourne
        const angle = contentProgress * 2 * Math.PI;
        const vLen = 2.5;
        const vx = vLen * MathUtils.cos(angle);
        const vy = vLen * MathUtils.sin(angle);

        renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', width: 3 });
        drawMathBox('vec-v-label', '\\vec{v}', vx + 0.4, vy + 0.4, {
            fontSize: '1.2em', color: '#3b82f6',
            bgColor: 'rgba(219, 234, 254, 0.9)', padding: '4px 8px'
        });

        // Calculs
        const dotProduct = ux * vx + uy * vy;
        let angleDeg = (angle * 180 / Math.PI) % 360;
        if (angleDeg > 180) angleDeg = angleDeg - 360;
        angleDeg = Math.abs(angleDeg);

        // Determiner couleur et message
        let color, messageText, bgColor;
        if (Math.abs(dotProduct) < 0.5) {
            color = '#3b82f6';
            messageText = 'Angle droit (θ = 90°)';
            bgColor = 'rgba(219, 234, 254, 0.95)';
        } else if (dotProduct > 0) {
            color = '#10b981';
            messageText = 'Angle aigu (θ < 90°)';
            bgColor = 'rgba(209, 250, 229, 0.95)';
        } else {
            color = '#f97316';
            messageText = 'Angle obtus (θ > 90°)';
            bgColor = 'rgba(254, 243, 199, 0.95)';
        }

        // === DISPOSITION A GAUCHE (x = -9) ===
        // IMPORTANT: LaTeX STATIQUE uniquement (pas de recompilation)

        // Label statique "Produit scalaire :"
        drawMathBox('signe-label', '\\vec{u} \\cdot \\vec{v} =', -9, 3.5, {
            fontSize: '1.4em', color: '#1e3a8a', align: 'left',
            bgColor: 'rgba(255, 255, 255, 0.95)'
        });

        // Valeur DYNAMIQUE en drawTextBox (pas MathJax) - a cote du label
        drawTextBox(renderer, MathUtils.format(dotProduct, 1), -5.5, 3.5, {
            font: 'bold 26px Arial',
            color: color,
            bgColor: bgColor,
            borderColor: color,
            borderWidth: 2,
            padding: 10
        });

        // Angle theta (valeur dynamique en canvas)
        drawTextBox(renderer, `θ ≈ ${MathUtils.format(angleDeg, 0)}°`, -9, 1.5, {
            font: '20px Arial',
            color: '#64748b',
            bgColor: 'rgba(248, 250, 252, 0.95)',
            align: 'left'
        });

        // Message interpretation (dynamique en canvas)
        drawTextBox(renderer, messageText, -9, -0.5, {
            font: 'bold 18px Arial',
            color: color,
            bgColor: bgColor,
            align: 'left'
        });

        // Legende en BAS
        if (contentProgress > 0.3) {
            const legendOpacity = Math.min((contentProgress - 0.3) / 0.1, 1);
            drawTextBox(renderer, 'Vert = aigu | Orange = obtus', 0, -4.5, {
                font: '16px Arial', color: '#64748b', opacity: legendOpacity
            });
        }
    }
});
