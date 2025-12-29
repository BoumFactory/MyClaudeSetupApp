/**
 * Index des scènes - Produit Scalaire
 *
 * Helpers et registre pour les scènes
 */

// Registre global des scènes
window.SCENE_REGISTRY = window.SCENE_REGISTRY || [];

/**
 * Helper pour dessiner une boîte de texte avec fond
 * Garantit la lisibilité sur projection
 */
function drawTextBox(renderer, text, x, y, options = {}) {
    const {
        font = '20px Arial',
        color = '#1e3a8a',
        bgColor = 'rgba(255, 255, 255, 0.92)',
        padding = 10,
        borderRadius = 6,
        align = 'center',
        opacity = 1
    } = options;

    const ctx = renderer.ctx;
    ctx.save();

    // Appliquer l'opacité globale
    ctx.globalAlpha = opacity;

    ctx.font = font;
    const metrics = ctx.measureText(text);
    const textWidth = metrics.width;
    const textHeight = parseInt(font) * 1.2;

    // Convertir coordonnées math → canvas
    const canvasPos = renderer.toPixel(x, y);

    // Ajuster selon l'alignement
    let boxX;
    if (align === 'left') {
        boxX = canvasPos.x - padding;
    } else if (align === 'right') {
        boxX = canvasPos.x - textWidth - padding;
    } else {
        boxX = canvasPos.x - textWidth / 2 - padding;
    }
    const boxY = canvasPos.y - textHeight / 2 - padding;

    // Dessiner le fond avec coins arrondis
    ctx.fillStyle = bgColor;
    ctx.beginPath();
    ctx.roundRect(boxX, boxY, textWidth + 2 * padding, textHeight + 2 * padding, borderRadius);
    ctx.fill();

    // Bordure subtile
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.restore();

    // Dessiner le texte
    renderer.drawText(text, x, y, { font, color: opacity < 1 ? color.replace(')', `, ${opacity})`).replace('rgb', 'rgba') : color, align });
}

/**
 * Helper pour dessiner plusieurs lignes de texte dans une boîte
 */
function drawMultilineTextBox(renderer, lines, x, y, options = {}) {
    const {
        font = '20px Arial',
        color = '#1e3a8a',
        bgColor = 'rgba(255, 255, 255, 0.92)',
        padding = 12,
        borderRadius = 6,
        lineSpacing = 1.3,
        align = 'left',
        opacity = 1
    } = options;

    const ctx = renderer.ctx;
    ctx.save();
    ctx.globalAlpha = opacity;
    ctx.font = font;

    const fontSize = parseInt(font);
    let maxWidth = 0;
    lines.forEach(line => {
        const w = ctx.measureText(line).width;
        if (w > maxWidth) maxWidth = w;
    });
    const totalHeight = lines.length * fontSize * lineSpacing;

    const canvasPos = renderer.toPixel(x, y);

    // Position de la boîte
    let boxX;
    if (align === 'left') {
        boxX = canvasPos.x - padding;
    } else if (align === 'right') {
        boxX = canvasPos.x - maxWidth - padding;
    } else {
        boxX = canvasPos.x - maxWidth / 2 - padding;
    }
    const boxY = canvasPos.y - padding;

    // Dessiner le fond
    ctx.fillStyle = bgColor;
    ctx.beginPath();
    ctx.roundRect(boxX, boxY, maxWidth + 2 * padding, totalHeight + 2 * padding, borderRadius);
    ctx.fill();

    ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.restore();

    // Dessiner chaque ligne
    lines.forEach((line, i) => {
        const lineY = y - (i * fontSize * lineSpacing) / renderer.config.scale;
        renderer.drawText(line, x, lineY, {
            font,
            color: opacity < 1 ? `rgba(30, 58, 138, ${opacity})` : color,
            align
        });
    });
}

// Exposer les helpers globalement
window.TextBoxHelpers = {
    drawTextBox,
    drawMultilineTextBox
};

// Raccourcis pratiques
window.drawTextBox = drawTextBox;
window.drawMultilineTextBox = drawMultilineTextBox;
