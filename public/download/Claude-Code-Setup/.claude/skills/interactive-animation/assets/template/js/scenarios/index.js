/**
 * Index des scènes - Helpers et configuration
 *
 * Ce fichier est chargé EN PREMIER dans index.html.
 * Les fichiers de scènes individuels ajoutent leurs scènes à window.SCENE_REGISTRY.
 * scenes.js récupère ensuite toutes les scènes du registre.
 *
 * STRUCTURE :
 * 1. Ce fichier (index.js) - Définit les helpers et le registre
 * 2. 01-intro.js, 02-xxx.js, ... - Ajoutent les scènes au registre
 * 3. scenes.js - Récupère les scènes et crée SCENES
 */

// Registre global des scènes (chaque fichier de scène y ajoute la sienne)
window.SCENE_REGISTRY = window.SCENE_REGISTRY || [];

/**
 * Helper pour dessiner une boîte de texte avec fond
 * À utiliser dans toutes les scènes pour la lisibilité
 *
 * @param {CanvasRenderer} renderer - Instance du renderer
 * @param {string} text - Texte à afficher
 * @param {number} x - Position X en coordonnées mathématiques
 * @param {number} y - Position Y en coordonnées mathématiques
 * @param {object} options - Options de style
 */
function drawTextBox(renderer, text, x, y, options = {}) {
    const {
        font = '20px Arial',
        color = '#1e3a8a',
        bgColor = 'rgba(255, 255, 255, 0.9)',
        padding = 10,
        borderRadius = 5,
        align = 'center'
    } = options;

    const ctx = renderer.ctx;
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

    // Dessiner le texte
    renderer.drawText(text, x, y, { font, color, align });
}

/**
 * Helper pour dessiner plusieurs lignes de texte dans une boîte
 *
 * @param {CanvasRenderer} renderer - Instance du renderer
 * @param {string[]} lines - Lignes de texte
 * @param {number} x - Position X
 * @param {number} y - Position Y (coin supérieur)
 * @param {object} options - Options de style
 */
function drawMultilineTextBox(renderer, lines, x, y, options = {}) {
    const {
        font = '20px Arial',
        color = '#1e3a8a',
        bgColor = 'rgba(255, 255, 255, 0.9)',
        padding = 12,
        borderRadius = 5,
        lineHeight = 1.4,
        align = 'left'
    } = options;

    const ctx = renderer.ctx;
    ctx.font = font;

    // Calculer dimensions
    const fontSize = parseInt(font);
    let maxWidth = 0;
    lines.forEach(line => {
        const w = ctx.measureText(line).width;
        if (w > maxWidth) maxWidth = w;
    });
    const totalHeight = lines.length * fontSize * lineHeight;

    // Convertir coordonnées math → canvas
    const canvasPos = renderer.toPixel(x, y);

    // Dessiner le fond
    ctx.fillStyle = bgColor;
    ctx.beginPath();
    const boxX = canvasPos.x - padding;
    const boxY = canvasPos.y - padding;
    ctx.roundRect(boxX, boxY, maxWidth + 2 * padding, totalHeight + 2 * padding, borderRadius);
    ctx.fill();

    // Dessiner chaque ligne (de haut en bas)
    lines.forEach((line, i) => {
        const lineY = y - (i * fontSize * lineHeight) / renderer.config.scale;
        renderer.drawText(line, x, lineY, { font, color, align });
    });
}

// Exposer les helpers globalement pour les scènes
window.TextBoxHelpers = {
    drawTextBox,
    drawMultilineTextBox
};
