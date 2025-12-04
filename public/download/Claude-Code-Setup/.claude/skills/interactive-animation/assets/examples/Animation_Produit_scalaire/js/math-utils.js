/**
 * UTILITAIRES MATHÉMATIQUES
 * Fonctions de haute précision pour les calculs mathématiques
 *
 * IMPORTANT: Toutes les fonctions utilisent une précision contrôlée
 * pour éviter les erreurs d'arrondi flottant.
 */

const MathUtils = {
    // ==========================================
    // CONSTANTES
    // ==========================================
    PI: Math.PI,
    TAU: 2 * Math.PI,
    E: Math.E,
    SQRT2: Math.SQRT2,
    SQRT3: Math.sqrt(3),
    PHI: (1 + Math.sqrt(5)) / 2, // Nombre d'or

    // Précision par défaut pour les arrondis
    DEFAULT_PRECISION: 10,

    // Tolérance pour les comparaisons
    EPSILON: 1e-10,

    // ==========================================
    // FONCTIONS DE BASE AVEC PRÉCISION
    // ==========================================

    /**
     * Arrondit un nombre à n décimales
     */
    round(value, decimals = this.DEFAULT_PRECISION) {
        const factor = Math.pow(10, decimals);
        return Math.round(value * factor) / factor;
    },

    /**
     * Vérifie si deux nombres sont égaux (avec tolérance)
     */
    equals(a, b, epsilon = this.EPSILON) {
        return Math.abs(a - b) < epsilon;
    },

    /**
     * Vérifie si un nombre est proche de zéro
     */
    isZero(value, epsilon = this.EPSILON) {
        return Math.abs(value) < epsilon;
    },

    /**
     * Signe d'un nombre (-1, 0, 1)
     */
    sign(value) {
        if (this.isZero(value)) return 0;
        return value > 0 ? 1 : -1;
    },

    /**
     * Clamp une valeur entre min et max
     */
    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    },

    /**
     * Interpolation linéaire
     */
    lerp(a, b, t) {
        return a + (b - a) * t;
    },

    /**
     * Inverse de l'interpolation linéaire
     */
    inverseLerp(a, b, value) {
        if (this.equals(a, b)) return 0;
        return (value - a) / (b - a);
    },

    /**
     * Map une valeur d'un intervalle à un autre
     */
    map(value, inMin, inMax, outMin, outMax) {
        return this.lerp(outMin, outMax, this.inverseLerp(inMin, inMax, value));
    },

    // ==========================================
    // TRIGONOMÉTRIE
    // ==========================================

    /**
     * Convertit degrés en radians
     */
    degToRad(degrees) {
        return degrees * (this.PI / 180);
    },

    /**
     * Convertit radians en degrés
     */
    radToDeg(radians) {
        return radians * (180 / this.PI);
    },

    /**
     * Sinus avec précision
     */
    sin(angle, inDegrees = false) {
        const rad = inDegrees ? this.degToRad(angle) : angle;
        return this.round(Math.sin(rad));
    },

    /**
     * Cosinus avec précision
     */
    cos(angle, inDegrees = false) {
        const rad = inDegrees ? this.degToRad(angle) : angle;
        return this.round(Math.cos(rad));
    },

    /**
     * Tangente avec précision
     */
    tan(angle, inDegrees = false) {
        const rad = inDegrees ? this.degToRad(angle) : angle;
        return this.round(Math.tan(rad));
    },

    /**
     * Arc sinus
     */
    asin(value) {
        return this.round(Math.asin(this.clamp(value, -1, 1)));
    },

    /**
     * Arc cosinus
     */
    acos(value) {
        return this.round(Math.acos(this.clamp(value, -1, 1)));
    },

    /**
     * Arc tangente
     */
    atan(value) {
        return this.round(Math.atan(value));
    },

    /**
     * Arc tangente 2 (angle d'un point)
     */
    atan2(y, x) {
        return this.round(Math.atan2(y, x));
    },

    /**
     * Normalise un angle en radians dans [0, 2π)
     */
    normalizeAngle(angle) {
        angle = angle % this.TAU;
        if (angle < 0) angle += this.TAU;
        return this.round(angle);
    },

    /**
     * Normalise un angle en degrés dans [0, 360)
     */
    normalizeAngleDeg(angle) {
        angle = angle % 360;
        if (angle < 0) angle += 360;
        return this.round(angle);
    },

    // ==========================================
    // VECTEURS 2D
    // ==========================================

    /**
     * Crée un vecteur 2D
     */
    vec2(x = 0, y = 0) {
        return { x, y };
    },

    /**
     * Addition de vecteurs
     */
    vec2Add(v1, v2) {
        return { x: v1.x + v2.x, y: v1.y + v2.y };
    },

    /**
     * Soustraction de vecteurs
     */
    vec2Sub(v1, v2) {
        return { x: v1.x - v2.x, y: v1.y - v2.y };
    },

    /**
     * Multiplication par un scalaire
     */
    vec2Scale(v, scalar) {
        return { x: v.x * scalar, y: v.y * scalar };
    },

    /**
     * Produit scalaire
     */
    vec2Dot(v1, v2) {
        return this.round(v1.x * v2.x + v1.y * v2.y);
    },

    /**
     * Produit vectoriel (composante z)
     */
    vec2Cross(v1, v2) {
        return this.round(v1.x * v2.y - v1.y * v2.x);
    },

    /**
     * Norme d'un vecteur
     */
    vec2Length(v) {
        return this.round(Math.sqrt(v.x * v.x + v.y * v.y));
    },

    /**
     * Normalise un vecteur
     */
    vec2Normalize(v) {
        const len = this.vec2Length(v);
        if (this.isZero(len)) return { x: 0, y: 0 };
        return { x: v.x / len, y: v.y / len };
    },

    /**
     * Distance entre deux points
     */
    distance(p1, p2) {
        return this.vec2Length(this.vec2Sub(p2, p1));
    },

    /**
     * Angle d'un vecteur
     */
    vec2Angle(v) {
        return this.atan2(v.y, v.x);
    },

    /**
     * Rotation d'un vecteur
     */
    vec2Rotate(v, angle) {
        const cos = this.cos(angle);
        const sin = this.sin(angle);
        return {
            x: this.round(v.x * cos - v.y * sin),
            y: this.round(v.x * sin + v.y * cos)
        };
    },

    /**
     * Projection d'un vecteur sur un autre
     */
    vec2Project(v, onto) {
        const dot = this.vec2Dot(v, onto);
        const len2 = this.vec2Dot(onto, onto);
        if (this.isZero(len2)) return { x: 0, y: 0 };
        const scalar = dot / len2;
        return this.vec2Scale(onto, scalar);
    },

    /**
     * Interpolation linéaire entre deux vecteurs
     */
    vec2Lerp(v1, v2, t) {
        return {
            x: this.lerp(v1.x, v2.x, t),
            y: this.lerp(v1.y, v2.y, t)
        };
    },

    // ==========================================
    // GÉOMÉTRIE
    // ==========================================

    /**
     * Point sur un cercle
     */
    pointOnCircle(cx, cy, radius, angle) {
        return {
            x: this.round(cx + radius * this.cos(angle)),
            y: this.round(cy + radius * this.sin(angle))
        };
    },

    /**
     * Point sur une ellipse
     */
    pointOnEllipse(cx, cy, rx, ry, angle) {
        return {
            x: this.round(cx + rx * this.cos(angle)),
            y: this.round(cy + ry * this.sin(angle))
        };
    },

    /**
     * Intersection de deux droites (format paramétrique)
     * Droite 1: P1 + t * D1
     * Droite 2: P2 + s * D2
     */
    lineLineIntersection(p1, d1, p2, d2) {
        const cross = this.vec2Cross(d1, d2);
        if (this.isZero(cross)) return null; // Droites parallèles

        const diff = this.vec2Sub(p2, p1);
        const t = this.vec2Cross(diff, d2) / cross;

        return {
            x: this.round(p1.x + t * d1.x),
            y: this.round(p1.y + t * d1.y),
            t: this.round(t)
        };
    },

    /**
     * Intersection droite-cercle
     */
    lineCircleIntersection(linePoint, lineDir, cx, cy, radius) {
        const d = this.vec2Normalize(lineDir);
        const f = this.vec2Sub(linePoint, { x: cx, y: cy });

        const a = this.vec2Dot(d, d);
        const b = 2 * this.vec2Dot(f, d);
        const c = this.vec2Dot(f, f) - radius * radius;

        const discriminant = b * b - 4 * a * c;

        if (discriminant < 0) return [];

        const sqrtDisc = Math.sqrt(discriminant);
        const t1 = (-b - sqrtDisc) / (2 * a);
        const t2 = (-b + sqrtDisc) / (2 * a);

        const points = [];
        if (!this.equals(t1, t2)) {
            points.push({
                x: this.round(linePoint.x + t1 * d.x),
                y: this.round(linePoint.y + t1 * d.y)
            });
        }
        points.push({
            x: this.round(linePoint.x + t2 * d.x),
            y: this.round(linePoint.y + t2 * d.y)
        });

        return points;
    },

    /**
     * Point le plus proche sur une droite
     */
    closestPointOnLine(point, linePoint, lineDir) {
        const proj = this.vec2Project(
            this.vec2Sub(point, linePoint),
            lineDir
        );
        return this.vec2Add(linePoint, proj);
    },

    /**
     * Distance point-droite
     */
    distancePointToLine(point, linePoint, lineDir) {
        const closest = this.closestPointOnLine(point, linePoint, lineDir);
        return this.distance(point, closest);
    },

    /**
     * Aire d'un triangle (formule de Héron)
     */
    triangleArea(a, b, c) {
        // a, b, c sont les longueurs des côtés
        const s = (a + b + c) / 2;
        return this.round(Math.sqrt(s * (s - a) * (s - b) * (s - c)));
    },

    /**
     * Aire d'un triangle à partir des coordonnées
     */
    triangleAreaFromPoints(p1, p2, p3) {
        return this.round(Math.abs(
            (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)
        ) / 2);
    },

    // ==========================================
    // COURBES
    // ==========================================

    /**
     * Point sur une courbe de Bézier quadratique
     */
    bezierQuadratic(p0, p1, p2, t) {
        const mt = 1 - t;
        return {
            x: this.round(mt * mt * p0.x + 2 * mt * t * p1.x + t * t * p2.x),
            y: this.round(mt * mt * p0.y + 2 * mt * t * p1.y + t * t * p2.y)
        };
    },

    /**
     * Point sur une courbe de Bézier cubique
     */
    bezierCubic(p0, p1, p2, p3, t) {
        const mt = 1 - t;
        const mt2 = mt * mt;
        const mt3 = mt2 * mt;
        const t2 = t * t;
        const t3 = t2 * t;

        return {
            x: this.round(mt3 * p0.x + 3 * mt2 * t * p1.x + 3 * mt * t2 * p2.x + t3 * p3.x),
            y: this.round(mt3 * p0.y + 3 * mt2 * t * p1.y + 3 * mt * t2 * p2.y + t3 * p3.y)
        };
    },

    // ==========================================
    // ALGÈBRE
    // ==========================================

    /**
     * Résout une équation du second degré ax² + bx + c = 0
     */
    solveQuadratic(a, b, c) {
        if (this.isZero(a)) {
            // Équation du premier degré
            if (this.isZero(b)) return [];
            return [this.round(-c / b)];
        }

        const discriminant = b * b - 4 * a * c;

        if (discriminant < 0) return [];
        if (this.isZero(discriminant)) {
            return [this.round(-b / (2 * a))];
        }

        const sqrtDisc = Math.sqrt(discriminant);
        return [
            this.round((-b - sqrtDisc) / (2 * a)),
            this.round((-b + sqrtDisc) / (2 * a))
        ].sort((x, y) => x - y);
    },

    /**
     * PGCD de deux nombres
     */
    gcd(a, b) {
        a = Math.abs(Math.round(a));
        b = Math.abs(Math.round(b));
        while (b !== 0) {
            const temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    },

    /**
     * PPCM de deux nombres
     */
    lcm(a, b) {
        return Math.abs(a * b) / this.gcd(a, b);
    },

    /**
     * Simplifie une fraction
     */
    simplifyFraction(numerator, denominator) {
        const g = this.gcd(numerator, denominator);
        const sign = denominator < 0 ? -1 : 1;
        return {
            numerator: sign * Math.round(numerator / g),
            denominator: Math.abs(Math.round(denominator / g))
        };
    },

    // ==========================================
    // FORMATAGE
    // ==========================================

    /**
     * Formate un nombre pour affichage
     */
    format(value, decimals = 2) {
        if (this.isZero(value)) return '0';
        const rounded = this.round(value, decimals);
        // Supprime les zéros trailing
        return parseFloat(rounded.toFixed(decimals)).toString();
    },

    /**
     * Formate une fraction
     */
    formatFraction(numerator, denominator) {
        const { numerator: n, denominator: d } = this.simplifyFraction(numerator, denominator);
        if (d === 1) return n.toString();
        return `${n}/${d}`;
    },

    /**
     * Formate un angle en notation degré
     */
    formatAngle(radians, decimals = 1) {
        const degrees = this.radToDeg(radians);
        return `${this.format(degrees, decimals)}°`;
    },

    /**
     * Formate des coordonnées
     */
    formatPoint(x, y, decimals = 2) {
        return `(${this.format(x, decimals)} ; ${this.format(y, decimals)})`;
    },

    // ==========================================
    // FONCTIONS D'EASING POUR ANIMATIONS
    // ==========================================

    /**
     * Applique une fonction d'easing à une valeur t (0-1)
     * @param {number} t - Progression (0 à 1)
     * @param {string} type - Type d'easing
     * @returns {number} - Valeur easée (0 à 1)
     */
    ease(t, type = 'linear') {
        t = this.clamp(t, 0, 1);

        const easings = {
            // Linéaire
            linear: t => t,

            // Quadratique
            easeInQuad: t => t * t,
            easeOutQuad: t => t * (2 - t),
            easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,

            // Cubique
            easeInCubic: t => t * t * t,
            easeOutCubic: t => (--t) * t * t + 1,
            easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,

            // Quartique
            easeInQuart: t => t * t * t * t,
            easeOutQuart: t => 1 - (--t) * t * t * t,
            easeInOutQuart: t => t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t,

            // Sinusoïdal
            easeInSine: t => 1 - Math.cos(t * Math.PI / 2),
            easeOutSine: t => Math.sin(t * Math.PI / 2),
            easeInOutSine: t => -(Math.cos(Math.PI * t) - 1) / 2,

            // Exponentiel
            easeInExpo: t => t === 0 ? 0 : Math.pow(2, 10 * (t - 1)),
            easeOutExpo: t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t),
            easeInOutExpo: t => {
                if (t === 0 || t === 1) return t;
                return t < 0.5
                    ? Math.pow(2, 20 * t - 10) / 2
                    : (2 - Math.pow(2, -20 * t + 10)) / 2;
            },

            // Circulaire
            easeInCirc: t => 1 - Math.sqrt(1 - t * t),
            easeOutCirc: t => Math.sqrt(1 - (--t) * t),
            easeInOutCirc: t => t < 0.5
                ? (1 - Math.sqrt(1 - 4 * t * t)) / 2
                : (Math.sqrt(1 - Math.pow(-2 * t + 2, 2)) + 1) / 2,

            // Élastique
            easeInElastic: t => {
                if (t === 0 || t === 1) return t;
                return -Math.pow(2, 10 * t - 10) * Math.sin((t * 10 - 10.75) * (2 * Math.PI) / 3);
            },
            easeOutElastic: t => {
                if (t === 0 || t === 1) return t;
                return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * (2 * Math.PI) / 3) + 1;
            },
            easeInOutElastic: t => {
                if (t === 0 || t === 1) return t;
                return t < 0.5
                    ? -(Math.pow(2, 20 * t - 10) * Math.sin((20 * t - 11.125) * (2 * Math.PI) / 4.5)) / 2
                    : (Math.pow(2, -20 * t + 10) * Math.sin((20 * t - 11.125) * (2 * Math.PI) / 4.5)) / 2 + 1;
            },

            // Rebond
            easeOutBounce: t => {
                const n1 = 7.5625;
                const d1 = 2.75;
                if (t < 1 / d1) return n1 * t * t;
                if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
                if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
                return n1 * (t -= 2.625 / d1) * t + 0.984375;
            },
            easeInBounce: t => 1 - easings.easeOutBounce(1 - t),
            easeInOutBounce: t => t < 0.5
                ? (1 - easings.easeOutBounce(1 - 2 * t)) / 2
                : (1 + easings.easeOutBounce(2 * t - 1)) / 2,

            // Back (dépassement)
            easeInBack: t => {
                const c1 = 1.70158;
                const c3 = c1 + 1;
                return c3 * t * t * t - c1 * t * t;
            },
            easeOutBack: t => {
                const c1 = 1.70158;
                const c3 = c1 + 1;
                return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
            },
            easeInOutBack: t => {
                const c1 = 1.70158;
                const c2 = c1 * 1.525;
                return t < 0.5
                    ? (Math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
                    : (Math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2;
            }
        };

        const fn = easings[type] || easings.linear;
        return this.round(fn(t), 6);
    },

    /**
     * Interpolation avec easing entre deux valeurs
     */
    lerpEase(a, b, t, easing = 'easeInOutQuad') {
        return this.lerp(a, b, this.ease(t, easing));
    }
};

// Export pour utilisation modulaire
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MathUtils;
}
