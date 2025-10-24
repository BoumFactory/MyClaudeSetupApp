export function useLorenzAttractor() {
  // Paramètres de l'attracteur de Lorenz
  const sigma = 10;
  const rho = 28;
  const beta = 8 / 3;

  interface Point {
    x: number;
    y: number;
    z: number;
  }

  let points: Point[] = [];
  let currentPoint: Point = { x: 0.1, y: 0, z: 0 };

  // Calculer le prochain point de l'attracteur
  const lorenzStep = (point: Point, dt: number): Point => {
    const dx = sigma * (point.y - point.x) * dt;
    const dy = (point.x * (rho - point.z) - point.y) * dt;
    const dz = (point.x * point.y - beta * point.z) * dt;

    return {
      x: point.x + dx,
      y: point.y + dy,
      z: point.z + dz,
    };
  };

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();

    // Calculer de nouveaux points de l'attracteur
    const dt = 0.005;
    const stepsPerFrame = 5;

    for (let i = 0; i < stepsPerFrame; i++) {
      currentPoint = lorenzStep(currentPoint, dt);
      points.push({ ...currentPoint });
    }

    // Limiter le nombre de points pour optimiser les performances et créer l'effet de trace
    const maxPoints = 3000;
    if (points.length > maxPoints) {
      points = points.slice(points.length - maxPoints);
    }

    // Rotation pour visualiser la structure 3D
    const rotationAngle = time * 0.15;

    // Dessiner les trajectoires avec des traces plus visibles
    // Créer un gradient de couleur le long de la trajectoire
    for (let i = 1; i < points.length; i++) {
      const point = points[i];
      const prevPoint = points[i - 1];

      // Rotation autour de l'axe Y
      const rotatedX = point.x * Math.cos(rotationAngle) - point.z * Math.sin(rotationAngle);
      const prevRotatedX = prevPoint.x * Math.cos(rotationAngle) - prevPoint.z * Math.sin(rotationAngle);

      // Projection sur le plan 2D
      const scale = 8;
      const screenX = centerX + rotatedX * scale;
      const screenY = centerY + point.y * scale;
      const prevScreenX = centerX + prevRotatedX * scale;
      const prevScreenY = centerY + prevPoint.y * scale;

      // Opacité basée sur l'âge de la trace
      const age = i / points.length;
      const alpha = 0.1 + age * 0.3; // Traces plus visibles

      ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(prevScreenX, prevScreenY);
      ctx.lineTo(screenX, screenY);
      ctx.stroke();
    }

    // Dessiner des points lumineux le long de la trajectoire
    const pulsation = Math.sin(time * 0.5) * 0.3 + 0.7;

    points.forEach((point, index) => {
      if (index % 50 === 0) {
        const rotatedX = point.x * Math.cos(rotationAngle) - point.z * Math.sin(rotationAngle);

        const scale = 8;
        const screenX = centerX + rotatedX * scale;
        const screenY = centerY + point.y * scale;

        const age = (points.length - index) / points.length;
        const alpha = age * pulsation * 0.4;

        ctx.fillStyle = `rgba(168, 85, 247, ${alpha})`;
        ctx.beginPath();
        ctx.arc(screenX, screenY, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // Dessiner les deux attracteurs (les "ailes du papillon")
    const attractorScale = 8;
    const attractorRadius = rho * attractorScale;

    ctx.strokeStyle = 'rgba(99, 102, 241, 0.2)';
    ctx.lineWidth = 2;

    // Attracteur gauche
    ctx.beginPath();
    ctx.arc(
      centerX - attractorRadius * 0.5 * Math.cos(rotationAngle),
      centerY,
      attractorRadius * 0.3,
      0,
      Math.PI * 2
    );
    ctx.stroke();

    // Attracteur droit
    ctx.beginPath();
    ctx.arc(
      centerX + attractorRadius * 0.5 * Math.cos(rotationAngle),
      centerY,
      attractorRadius * 0.3,
      0,
      Math.PI * 2
    );
    ctx.stroke();

    // Ajouter des lignes de liaison pour souligner la structure
    ctx.strokeStyle = 'rgba(168, 85, 247, 0.1)';
    ctx.lineWidth = 1;

    for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 4) {
      const x1 = centerX - attractorRadius * 0.5 * Math.cos(rotationAngle) + Math.cos(angle) * attractorRadius * 0.3;
      const y1 = centerY + Math.sin(angle) * attractorRadius * 0.3;
      const x2 = centerX + attractorRadius * 0.5 * Math.cos(rotationAngle) + Math.cos(angle + Math.PI) * attractorRadius * 0.3;
      const y2 = centerY + Math.sin(angle + Math.PI) * attractorRadius * 0.3;

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }

    ctx.restore();
  };
}
