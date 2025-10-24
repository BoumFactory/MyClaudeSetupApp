export function useDragonCurve() {
  interface Point {
    x: number;
    y: number;
  }

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
    angle: number,
    time: number
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

    // Dessiner les segments avec des couleurs changeantes
    for (let i = 1; i < points.length; i++) {
      const age = i / points.length;
      const hue = (age * 360 + time * 50) % 360;
      const alpha = 0.2 + age * 0.3;
      const pulsation = Math.sin(time * 0.6 + i * 0.01) * 0.3 + 0.7;

      ctx.strokeStyle = `hsla(${hue}, 75%, 60%, ${alpha * pulsation})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(points[i - 1].x, points[i - 1].y);
      ctx.lineTo(points[i].x, points[i].y);
      ctx.stroke();
    }

    // Ajouter des points lumineux aux extrémités
    const vertexPulsation = Math.sin(time * 0.9) * 0.5 + 0.5;
    [0, Math.floor(points.length / 2), points.length - 1].forEach((index, i) => {
      if (index < points.length) {
        const point = points[index];
        const hue = (i * 120 + time * 40) % 360;

        // Halo
        const gradient = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, 20);
        gradient.addColorStop(0, `hsla(${hue}, 85%, 65%, ${0.5 * vertexPulsation})`);
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 20, 0, Math.PI * 2);
        ctx.fill();

        // Point central
        ctx.fillStyle = `hsla(${hue}, 90%, 70%, ${vertexPulsation})`;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    });
  };

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();
    ctx.translate(centerX, centerY);

    // Rotation
    const rotation = time * 0.12;
    ctx.rotate(rotation);

    // Générer la courbe du dragon (nombre d'itérations ajusté pour performance/détail)
    const iterations = 12;
    const sequence = generateDragonCurve(iterations);

    // Calculer la longueur des segments pour bien remplir l'écran
    const totalSegments = Math.pow(2, iterations);
    const desiredTotalLength = Math.min(width, height) * 0.7;
    const segmentLength = desiredTotalLength / Math.sqrt(totalSegments);

    // Dessiner la courbe
    drawDragonCurve(ctx, sequence, 0, 0, segmentLength, 0, time);

    ctx.restore();
  };
}
