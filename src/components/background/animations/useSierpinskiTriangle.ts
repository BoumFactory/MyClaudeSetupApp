export function useSierpinskiTriangle() {
  interface Point {
    x: number;
    y: number;
  }

  // Angle aléatoire fixe pour cette instance
  const randomRotation = Math.random() * Math.PI * 2;

  // Générer les points du triangle de Sierpinski par le jeu du chaos
  const generatePoints = (numPoints: number, vertices: Point[], scale: number): Point[] => {
    const points: Point[] = [];
    let current: Point = { x: Math.random() * scale, y: Math.random() * scale };

    for (let i = 0; i < numPoints; i++) {
      const targetVertex = vertices[Math.floor(Math.random() * vertices.length)];
      current = {
        x: (current.x + targetVertex.x) / 2,
        y: (current.y + targetVertex.y) / 2,
      };
      points.push({ ...current });
    }

    return points;
  };

  // Cache pour l'image statique
  let cachedCanvas: HTMLCanvasElement | null = null;
  let cachedWidth = 0;
  let cachedHeight = 0;

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    // Si l'image est déjà en cache et que la taille n'a pas changé, la réutiliser
    if (cachedCanvas && cachedWidth === width && cachedHeight === height) {
      ctx.drawImage(cachedCanvas, 0, 0);
      return;
    }

    // Créer un nouveau canvas pour le cache
    cachedCanvas = document.createElement('canvas');
    cachedCanvas.width = width;
    cachedCanvas.height = height;
    cachedWidth = width;
    cachedHeight = height;

    const cacheCtx = cachedCanvas.getContext('2d');
    if (!cacheCtx) return;

    const centerX = width / 2;
    const centerY = height / 2;

    cacheCtx.save();
    cacheCtx.translate(centerX, centerY);

    // Rotation aléatoire fixe
    cacheCtx.rotate(randomRotation);

    // Taille du triangle
    const size = Math.min(width, height) * 0.8;

    // Définir les trois sommets du triangle équilatéral
    const vertices: Point[] = [
      { x: 0, y: -size / 2 },
      { x: -size / 2 * Math.sqrt(3) / 2, y: size / 4 },
      { x: size / 2 * Math.sqrt(3) / 2, y: size / 4 },
    ];

    // Générer les points du triangle de Sierpinski
    const numPoints = 15000;
    const points = generatePoints(numPoints, vertices, size);

    // Dessiner les points avec des couleurs spectaculaires et plus lumineuses
    points.forEach((point, index) => {
      const age = index / numPoints;
      const hue = age * 360;
      const alpha = 0.4 + age * 0.5;

      cacheCtx.fillStyle = `hsla(${hue}, 85%, 70%, ${alpha})`;
      cacheCtx.beginPath();
      cacheCtx.arc(point.x, point.y, 1.5, 0, Math.PI * 2);
      cacheCtx.fill();
    });

    // Dessiner les sommets du triangle avec des halos
    vertices.forEach((vertex, index) => {
      const hue = index * 120;

      // Halo
      const gradient = cacheCtx.createRadialGradient(vertex.x, vertex.y, 0, vertex.x, vertex.y, 40);
      gradient.addColorStop(0, `hsla(${hue}, 90%, 70%, 0.7)`);
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      cacheCtx.fillStyle = gradient;
      cacheCtx.beginPath();
      cacheCtx.arc(vertex.x, vertex.y, 40, 0, Math.PI * 2);
      cacheCtx.fill();

      // Point central brillant
      cacheCtx.fillStyle = `hsla(${hue}, 95%, 75%, 0.9)`;
      cacheCtx.beginPath();
      cacheCtx.arc(vertex.x, vertex.y, 4, 0, Math.PI * 2);
      cacheCtx.fill();
    });

    // Dessiner les arêtes du triangle
    cacheCtx.strokeStyle = `rgba(168, 85, 247, 0.7)`;
    cacheCtx.lineWidth = 2;
    cacheCtx.beginPath();
    vertices.forEach((vertex, index) => {
      const nextVertex = vertices[(index + 1) % vertices.length];
      cacheCtx.moveTo(vertex.x, vertex.y);
      cacheCtx.lineTo(nextVertex.x, nextVertex.y);
    });
    cacheCtx.stroke();

    cacheCtx.restore();

    // Dessiner le canvas caché sur le canvas principal
    ctx.drawImage(cachedCanvas, 0, 0);
  };
}
