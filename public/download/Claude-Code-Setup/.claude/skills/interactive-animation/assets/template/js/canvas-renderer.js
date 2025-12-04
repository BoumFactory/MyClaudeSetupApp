/**
 * CANVAS RENDERER
 * Système de rendu optimisé pour les animations mathématiques
 * avec gestion du repère, du zoom et des transformations
 */

class CanvasRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');

        // Configuration du repère mathématique
        this.config = {
            // Origine au centre par défaut
            originX: 0.5,
            originY: 0.5,

            // Échelle (pixels par unité)
            scale: 50,
            minScale: 10,
            maxScale: 200,

            // Grille
            showGrid: true,
            gridColor: '#e5e7eb',
            gridColorMajor: '#d1d5db',
            gridStep: 1,
            gridMajorStep: 5,

            // Axes
            showAxes: true,
            axisColor: '#374151',
            axisWidth: 2,
            axisArrowSize: 10,

            // Labels
            showLabels: true,
            labelColor: '#6b7280',
            labelFont: '14px sans-serif',
            labelFontLarge: '18px sans-serif',

            // Valeurs numériques
            showValues: true,
            valueColor: '#374151',
            valueFont: '12px monospace',

            // Styles de dessin
            defaultStrokeColor: '#2563eb',
            defaultFillColor: 'rgba(37, 99, 235, 0.1)',
            defaultLineWidth: 2,

            // Points
            pointRadius: 5,
            pointColor: '#2563eb',

            // Texte
            fontSize: 16,

            // Animation
            antialias: true
        };

        // État du viewport
        this.viewport = {
            panX: 0,
            panY: 0
        };

        // Initialisation
        this.setupCanvas();
        this.setupResizeObserver();
    }

    // ==========================================
    // INITIALISATION
    // ==========================================

    setupCanvas() {
        this.resize();

        // Activer l'antialiasing
        if (this.config.antialias) {
            this.ctx.imageSmoothingEnabled = true;
            this.ctx.imageSmoothingQuality = 'high';
        }
    }

    setupResizeObserver() {
        const observer = new ResizeObserver(() => {
            this.resize();
        });
        observer.observe(this.canvas.parentElement);
    }

    resize() {
        const rect = this.canvas.parentElement.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;

        // Taille CSS
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';

        // Taille réelle (haute résolution)
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;

        // Scale pour haute résolution
        this.ctx.scale(dpr, dpr);

        // Stocker les dimensions CSS
        this.width = rect.width;
        this.height = rect.height;

        // Calculer l'origine
        this.originX = this.width * this.config.originX + this.viewport.panX;
        this.originY = this.height * this.config.originY + this.viewport.panY;
    }

    // ==========================================
    // CONVERSION DE COORDONNÉES
    // ==========================================

    /**
     * Convertit coordonnées mathématiques → pixels
     */
    toPixel(x, y) {
        return {
            x: this.originX + x * this.config.scale,
            y: this.originY - y * this.config.scale // Y inversé
        };
    }

    /**
     * Convertit pixels → coordonnées mathématiques
     */
    toMath(px, py) {
        return {
            x: (px - this.originX) / this.config.scale,
            y: (this.originY - py) / this.config.scale
        };
    }

    /**
     * Convertit une longueur math → pixels
     */
    toPixelLength(length) {
        return length * this.config.scale;
    }

    /**
     * Convertit une longueur pixels → math
     */
    toMathLength(pixels) {
        return pixels / this.config.scale;
    }

    // ==========================================
    // VIEWPORT
    // ==========================================

    setScale(scale) {
        this.config.scale = MathUtils.clamp(scale, this.config.minScale, this.config.maxScale);
        this.resize();
    }

    zoom(factor, centerX = this.width / 2, centerY = this.height / 2) {
        const oldScale = this.config.scale;
        const newScale = MathUtils.clamp(
            oldScale * factor,
            this.config.minScale,
            this.config.maxScale
        );

        // Zoom vers le point centre
        const mathPoint = this.toMath(centerX, centerY);
        this.config.scale = newScale;
        const newPixel = this.toPixel(mathPoint.x, mathPoint.y);

        this.viewport.panX += centerX - newPixel.x;
        this.viewport.panY += centerY - newPixel.y;

        this.resize();
    }

    pan(dx, dy) {
        this.viewport.panX += dx;
        this.viewport.panY += dy;
        this.resize();
    }

    resetViewport() {
        this.viewport.panX = 0;
        this.viewport.panY = 0;
        this.config.scale = 50;
        this.resize();
    }

    // ==========================================
    // DESSIN DE BASE
    // ==========================================

    clear(color = '#ffffff') {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(0, 0, this.width, this.height);
    }

    // ==========================================
    // GRILLE ET AXES
    // ==========================================

    drawGrid() {
        if (!this.config.showGrid) return;

        const bounds = this.getViewBounds();
        const step = this.config.gridStep;
        const majorStep = this.config.gridMajorStep;

        // Lignes verticales
        const startX = Math.floor(bounds.minX / step) * step;
        for (let x = startX; x <= bounds.maxX; x += step) {
            const px = this.toPixel(x, 0).x;
            const isMajor = MathUtils.isZero(x % majorStep);

            this.ctx.beginPath();
            this.ctx.strokeStyle = isMajor ? this.config.gridColorMajor : this.config.gridColor;
            this.ctx.lineWidth = isMajor ? 1 : 0.5;
            this.ctx.moveTo(px, 0);
            this.ctx.lineTo(px, this.height);
            this.ctx.stroke();
        }

        // Lignes horizontales
        const startY = Math.floor(bounds.minY / step) * step;
        for (let y = startY; y <= bounds.maxY; y += step) {
            const py = this.toPixel(0, y).y;
            const isMajor = MathUtils.isZero(y % majorStep);

            this.ctx.beginPath();
            this.ctx.strokeStyle = isMajor ? this.config.gridColorMajor : this.config.gridColor;
            this.ctx.lineWidth = isMajor ? 1 : 0.5;
            this.ctx.moveTo(0, py);
            this.ctx.lineTo(this.width, py);
            this.ctx.stroke();
        }
    }

    drawAxes() {
        if (!this.config.showAxes) return;

        const ctx = this.ctx;
        const origin = this.toPixel(0, 0);

        ctx.strokeStyle = this.config.axisColor;
        ctx.lineWidth = this.config.axisWidth;
        ctx.lineCap = 'round';

        // Axe X
        ctx.beginPath();
        ctx.moveTo(0, origin.y);
        ctx.lineTo(this.width, origin.y);
        ctx.stroke();

        // Flèche X
        this.drawArrow(this.width - 10, origin.y, 0);

        // Axe Y
        ctx.beginPath();
        ctx.moveTo(origin.x, this.height);
        ctx.lineTo(origin.x, 0);
        ctx.stroke();

        // Flèche Y
        this.drawArrow(origin.x, 10, -Math.PI / 2);

        // Labels des axes
        if (this.config.showLabels) {
            ctx.fillStyle = this.config.labelColor;
            ctx.font = this.config.labelFontLarge;
            ctx.textAlign = 'left';
            ctx.textBaseline = 'top';
            ctx.fillText('x', this.width - 25, origin.y + 8);

            ctx.textAlign = 'left';
            ctx.textBaseline = 'bottom';
            ctx.fillText('y', origin.x + 10, 25);
        }

        // Graduations et valeurs
        if (this.config.showValues) {
            this.drawAxisValues();
        }
    }

    drawArrow(x, y, angle) {
        const ctx = this.ctx;
        const size = this.config.axisArrowSize;

        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angle);

        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(-size, -size / 2);
        ctx.lineTo(-size, size / 2);
        ctx.closePath();
        ctx.fillStyle = this.config.axisColor;
        ctx.fill();

        ctx.restore();
    }

    drawAxisValues() {
        const ctx = this.ctx;
        const bounds = this.getViewBounds();
        const step = this.config.gridMajorStep;

        ctx.fillStyle = this.config.valueColor;
        ctx.font = this.config.valueFont;

        // Valeurs sur X
        const startX = Math.ceil(bounds.minX / step) * step;
        for (let x = startX; x <= bounds.maxX; x += step) {
            if (MathUtils.isZero(x)) continue;
            const px = this.toPixel(x, 0);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'top';
            ctx.fillText(MathUtils.format(x, 0), px.x, px.y + 8);
        }

        // Valeurs sur Y
        const startY = Math.ceil(bounds.minY / step) * step;
        for (let y = startY; y <= bounds.maxY; y += step) {
            if (MathUtils.isZero(y)) continue;
            const py = this.toPixel(0, y);
            ctx.textAlign = 'right';
            ctx.textBaseline = 'middle';
            ctx.fillText(MathUtils.format(y, 0), py.x - 8, py.y);
        }

        // Origine
        const origin = this.toPixel(0, 0);
        ctx.textAlign = 'right';
        ctx.textBaseline = 'top';
        ctx.fillText('O', origin.x - 8, origin.y + 8);
    }

    getViewBounds() {
        const topLeft = this.toMath(0, 0);
        const bottomRight = this.toMath(this.width, this.height);

        return {
            minX: topLeft.x,
            maxX: bottomRight.x,
            minY: bottomRight.y,
            maxY: topLeft.y
        };
    }

    // ==========================================
    // PRIMITIVES DE DESSIN
    // ==========================================

    /**
     * Dessine un point
     */
    drawPoint(x, y, options = {}) {
        const {
            radius = this.config.pointRadius,
            color = this.config.pointColor,
            label = null,
            labelOffset = { x: 10, y: -10 }
        } = options;

        const p = this.toPixel(x, y);

        // Point
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, radius, 0, MathUtils.TAU);
        this.ctx.fillStyle = color;
        this.ctx.fill();

        // Label
        if (label && this.config.showLabels) {
            this.ctx.fillStyle = color;
            this.ctx.font = this.config.labelFont;
            this.ctx.textAlign = 'left';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(label, p.x + labelOffset.x, p.y + labelOffset.y);
        }
    }

    /**
     * Dessine un segment
     */
    drawSegment(x1, y1, x2, y2, options = {}) {
        const {
            color = this.config.defaultStrokeColor,
            width = this.config.defaultLineWidth,
            dashed = false,
            dashPattern = [5, 5]
        } = options;

        const p1 = this.toPixel(x1, y1);
        const p2 = this.toPixel(x2, y2);

        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = width;
        this.ctx.setLineDash(dashed ? dashPattern : []);
        this.ctx.moveTo(p1.x, p1.y);
        this.ctx.lineTo(p2.x, p2.y);
        this.ctx.stroke();
        this.ctx.setLineDash([]);
    }

    /**
     * Dessine une droite (infinie)
     */
    drawLine(x1, y1, x2, y2, options = {}) {
        const bounds = this.getViewBounds();
        const dx = x2 - x1;
        const dy = y2 - y1;

        // Trouver les intersections avec les bords du viewport
        let tMin = -Infinity;
        let tMax = Infinity;

        if (!MathUtils.isZero(dx)) {
            const t1 = (bounds.minX - x1) / dx;
            const t2 = (bounds.maxX - x1) / dx;
            tMin = Math.max(tMin, Math.min(t1, t2));
            tMax = Math.min(tMax, Math.max(t1, t2));
        }

        if (!MathUtils.isZero(dy)) {
            const t1 = (bounds.minY - y1) / dy;
            const t2 = (bounds.maxY - y1) / dy;
            tMin = Math.max(tMin, Math.min(t1, t2));
            tMax = Math.min(tMax, Math.max(t1, t2));
        }

        if (tMin < tMax) {
            const startX = x1 + tMin * dx;
            const startY = y1 + tMin * dy;
            const endX = x1 + tMax * dx;
            const endY = y1 + tMax * dy;

            this.drawSegment(startX, startY, endX, endY, options);
        }
    }

    /**
     * Dessine un vecteur avec flèche
     */
    drawVector(x1, y1, x2, y2, options = {}) {
        const {
            color = this.config.defaultStrokeColor,
            width = this.config.defaultLineWidth,
            arrowSize = 12
        } = options;

        const p1 = this.toPixel(x1, y1);
        const p2 = this.toPixel(x2, y2);

        // Ligne
        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = width;
        this.ctx.moveTo(p1.x, p1.y);
        this.ctx.lineTo(p2.x, p2.y);
        this.ctx.stroke();

        // Flèche
        const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);

        this.ctx.save();
        this.ctx.translate(p2.x, p2.y);
        this.ctx.rotate(angle);

        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(-arrowSize, -arrowSize / 2);
        this.ctx.lineTo(-arrowSize, arrowSize / 2);
        this.ctx.closePath();
        this.ctx.fillStyle = color;
        this.ctx.fill();

        this.ctx.restore();
    }

    /**
     * Dessine un cercle
     */
    drawCircle(cx, cy, radius, options = {}) {
        const {
            strokeColor = this.config.defaultStrokeColor,
            fillColor = null,
            lineWidth = this.config.defaultLineWidth,
            dashed = false
        } = options;

        const center = this.toPixel(cx, cy);
        const r = this.toPixelLength(radius);

        this.ctx.beginPath();
        this.ctx.arc(center.x, center.y, r, 0, MathUtils.TAU);

        if (fillColor) {
            this.ctx.fillStyle = fillColor;
            this.ctx.fill();
        }

        this.ctx.strokeStyle = strokeColor;
        this.ctx.lineWidth = lineWidth;
        this.ctx.setLineDash(dashed ? [5, 5] : []);
        this.ctx.stroke();
        this.ctx.setLineDash([]);
    }

    /**
     * Dessine un arc de cercle
     */
    drawArc(cx, cy, radius, startAngle, endAngle, options = {}) {
        const {
            strokeColor = this.config.defaultStrokeColor,
            fillColor = null,
            lineWidth = this.config.defaultLineWidth,
            counterClockwise = false
        } = options;

        const center = this.toPixel(cx, cy);
        const r = this.toPixelLength(radius);

        // Convertir les angles (y inversé)
        const start = -startAngle;
        const end = -endAngle;

        this.ctx.beginPath();
        this.ctx.arc(center.x, center.y, r, start, end, !counterClockwise);

        if (fillColor) {
            this.ctx.lineTo(center.x, center.y);
            this.ctx.closePath();
            this.ctx.fillStyle = fillColor;
            this.ctx.fill();
        }

        this.ctx.strokeStyle = strokeColor;
        this.ctx.lineWidth = lineWidth;
        this.ctx.stroke();
    }

    /**
     * Dessine un angle (arc avec éventuellement la valeur)
     */
    drawAngle(cx, cy, startAngle, endAngle, options = {}) {
        const {
            radius = 0.5,
            strokeColor = this.config.defaultStrokeColor,
            fillColor = 'rgba(37, 99, 235, 0.1)',
            showValue = true,
            valueOffset = 1.5
        } = options;

        // Dessiner l'arc
        this.drawArc(cx, cy, radius, startAngle, endAngle, { strokeColor, fillColor });

        // Afficher la valeur
        if (showValue && this.config.showValues) {
            const midAngle = (startAngle + endAngle) / 2;
            const labelPos = MathUtils.pointOnCircle(cx, cy, radius * valueOffset, midAngle);
            const angleDeg = MathUtils.radToDeg(Math.abs(endAngle - startAngle));

            this.drawText(
                MathUtils.format(angleDeg, 0) + '°',
                labelPos.x, labelPos.y,
                { color: strokeColor, align: 'center' }
            );
        }
    }

    /**
     * Dessine un polygone
     */
    drawPolygon(points, options = {}) {
        const {
            strokeColor = this.config.defaultStrokeColor,
            fillColor = null,
            lineWidth = this.config.defaultLineWidth,
            closed = true
        } = options;

        if (points.length < 2) return;

        this.ctx.beginPath();
        const start = this.toPixel(points[0].x, points[0].y);
        this.ctx.moveTo(start.x, start.y);

        for (let i = 1; i < points.length; i++) {
            const p = this.toPixel(points[i].x, points[i].y);
            this.ctx.lineTo(p.x, p.y);
        }

        if (closed) {
            this.ctx.closePath();
        }

        if (fillColor) {
            this.ctx.fillStyle = fillColor;
            this.ctx.fill();
        }

        this.ctx.strokeStyle = strokeColor;
        this.ctx.lineWidth = lineWidth;
        this.ctx.stroke();
    }

    /**
     * Dessine une fonction y = f(x)
     */
    drawFunction(fn, options = {}) {
        const {
            color = this.config.defaultStrokeColor,
            lineWidth = this.config.defaultLineWidth,
            minX = null,
            maxX = null,
            step = null
        } = options;

        const bounds = this.getViewBounds();
        const xMin = minX !== null ? minX : bounds.minX;
        const xMax = maxX !== null ? maxX : bounds.maxX;
        const pixelStep = step || 2;
        const mathStep = this.toMathLength(pixelStep);

        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = lineWidth;

        let started = false;

        for (let x = xMin; x <= xMax; x += mathStep) {
            try {
                const y = fn(x);

                if (!isFinite(y) || isNaN(y)) {
                    started = false;
                    continue;
                }

                const p = this.toPixel(x, y);

                if (!started) {
                    this.ctx.moveTo(p.x, p.y);
                    started = true;
                } else {
                    this.ctx.lineTo(p.x, p.y);
                }
            } catch {
                started = false;
            }
        }

        this.ctx.stroke();
    }

    /**
     * Dessine du texte
     */
    drawText(text, x, y, options = {}) {
        const {
            color = this.config.labelColor,
            font = this.config.labelFont,
            align = 'left',
            baseline = 'middle',
            inMathCoords = true
        } = options;

        const pos = inMathCoords ? this.toPixel(x, y) : { x, y };

        this.ctx.fillStyle = color;
        this.ctx.font = font;
        this.ctx.textAlign = align;
        this.ctx.textBaseline = baseline;
        this.ctx.fillText(text, pos.x, pos.y);
    }

    /**
     * Dessine une image à une position donnée
     */
    drawImage(img, x, y, width, height, options = {}) {
        const {
            inMathCoords = true,
            centered = false
        } = options;

        let pos = inMathCoords ? this.toPixel(x, y) : { x, y };
        const w = inMathCoords ? this.toPixelLength(width) : width;
        const h = inMathCoords ? this.toPixelLength(height) : height;

        if (centered) {
            pos.x -= w / 2;
            pos.y -= h / 2;
        }

        this.ctx.drawImage(img, pos.x, pos.y, w, h);
    }

    // ==========================================
    // UTILITAIRES DE STYLE
    // ==========================================

    setStyle(options) {
        Object.assign(this.config, options);
    }

    getStyle() {
        return { ...this.config };
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CanvasRenderer;
}
