export function useDragonCurve() {
  interface Point {
    x: number;
    y: number;
  }

  // Angle aléatoire fixe pour cette instance
  const randomRotation = Math.random() * Math.PI * 2;

  // Générer la courbe du dragon de manière itérative
  const generateDragonCurve = (iterations: number): string => {
    let sequence = 'R'; // R = tourner à droite, L = tourner à gauche

    for (let i = 0; i < iterations; i++) {
      let newSequence = sequence + 'R';
      for (let j = sequence.length - 1; j >= 0; j--) {
        newSequence += sequence[j] === 'R' ? 'L' : 'R';
      }
      sequence = newSequence;
    }

    return sequence;
  };

  // Dessiner la courbe du dragon à partir de la séquence
  const drawDragonCurve = (
    ctx: CanvasRenderingContext2D,
    sequence: string,
    startX: number,
    startY: number,
    length: number,
    angle: number
  ) => {
    let x = startX;
    let y = startY;
    let currentAngle = angle;

    const points: Point[] = [{ x, y }];

    // Générer tous les points
    for (let i = 0; i < sequence.length; i++) {
      x += length * Math.cos(currentAngle);
      y += length * Math.sin(currentAngle);
      points.push({ x, y });

      if (sequence[i] === 'R') {
        currentAngle -= Math.PI / 2;
      } else {
        currentAngle += Math.PI / 2;
      }
    }

    // Dessiner les segments avec des couleurs statiques et plus lumineuses
    for (let i = 1; i < points.length; i++) {
      const age = i / points.length;
      const hue = age * 360;
      const alpha = 0.5 + age * 0.4;

      ctx.strokeStyle = `hsla(${hue}, 85%, 70%, ${alpha})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(points[i - 1].x, points[i - 1].y);
      ctx.lineTo(points[i].x, points[i].y);
      ctx.stroke();
    }

    // Ajouter des points lumineux aux extrémités
    [0, Math.floor(points.length / 2), points.length - 1].forEach((index, i) => {
      if (index < points.length) {
        const point = points[index];
        const hue = i * 120;

        // Halo
        const gradient = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, 20);
        gradient.addColorStop(0, `hsla(${hue}, 90%, 70%, 0.7)`);
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 20, 0, Math.PI * 2);
        ctx.fill();

        // Point central
        ctx.fillStyle = `hsla(${hue}, 95%, 75%, 0.9)`;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    });
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

    // Générer la courbe du dragon (nombre d'itérations ajusté pour performance/détail)
    const iterations = 12;
    const sequence = generateDragonCurve(iterations);

    // Calculer la longueur des segments pour bien remplir l'écran
    const totalSegments = Math.pow(2, iterations);
    const desiredTotalLength = Math.min(width, height) * 0.7;
    const segmentLength = desiredTotalLength / Math.sqrt(totalSegments);

    // Dessiner la courbe
    drawDragonCurve(cacheCtx, sequence, 0, 0, segmentLength, 0);

    cacheCtx.restore();

    // Dessiner le canvas caché sur le canvas principal
    ctx.drawImage(cachedCanvas, 0, 0);
  };
}
