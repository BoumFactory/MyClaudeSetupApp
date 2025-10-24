export function useRosslerAttractor() {
  // Paramètres de l'attracteur de Rössler
  const a = 0.2;
  const b = 0.2;
  const c = 5.7;

  interface Point {
    x: number;
    y: number;
    z: number;
  }

  let points: Point[] = [];
  let currentPoint: Point = { x: 0.1, y: 0, z: 0 };

  // Calculer le prochain point de l'attracteur
  const rosslerStep = (point: Point, dt: number): Point => {
    const dx = -(point.y + point.z) * dt;
    const dy = (point.x + a * point.y) * dt;
    const dz = (b + point.z * (point.x - c)) * dt;

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
    const dt = 0.01;
    const stepsPerFrame = 8;

    for (let i = 0; i < stepsPerFrame; i++) {
      currentPoint = rosslerStep(currentPoint, dt);
      points.push({ ...currentPoint });
    }

    // Limiter le nombre de points pour créer l'effet de trace
    const maxPoints = 3500;
    if (points.length > maxPoints) {
      points = points.slice(points.length - maxPoints);
    }

    // Rotation pour visualiser la structure 3D
    const rotationAngle = time * 0.2;
    const tiltAngle = Math.sin(time * 0.1) * 0.3;

    // Dessiner les trajectoires avec des traces colorées
    for (let i = 1; i < points.length; i++) {
      const point = points[i];
      const prevPoint = points[i - 1];

      // Rotations multiples pour une vue 3D dynamique
      let rotatedX = point.x * Math.cos(rotationAngle) - point.z * Math.sin(rotationAngle);
      let rotatedZ = point.x * Math.sin(rotationAngle) + point.z * Math.cos(rotationAngle);
      let rotatedY = point.y * Math.cos(tiltAngle) - rotatedZ * Math.sin(tiltAngle);

      let prevRotatedX = prevPoint.x * Math.cos(rotationAngle) - prevPoint.z * Math.sin(rotationAngle);
      let prevRotatedZ = prevPoint.x * Math.sin(rotationAngle) + prevPoint.z * Math.cos(rotationAngle);
      let prevRotatedY = prevPoint.y * Math.cos(tiltAngle) - prevRotatedZ * Math.sin(tiltAngle);

      // Projection sur le plan 2D
      const scale = 15;
      const screenX = centerX + rotatedX * scale;
      const screenY = centerY + rotatedY * scale;
      const prevScreenX = centerX + prevRotatedX * scale;
      const prevScreenY = centerY + prevRotatedY * scale;

      // Couleur basée sur la position Z et l'âge
      const age = i / points.length;
      const alpha = 0.15 + age * 0.35;
      const hue = (rotatedZ * 10 + time * 30) % 360;

      ctx.strokeStyle = `hsla(${hue}, 70%, 60%, ${alpha})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(prevScreenX, prevScreenY);
      ctx.lineTo(screenX, screenY);
      ctx.stroke();
    }

    // Dessiner des points lumineux le long de la trajectoire
    const pulsation = Math.sin(time * 0.7) * 0.4 + 0.6;

    points.forEach((point, index) => {
      if (index % 40 === 0) {
        let rotatedX = point.x * Math.cos(rotationAngle) - point.z * Math.sin(rotationAngle);
        let rotatedZ = point.x * Math.sin(rotationAngle) + point.z * Math.cos(rotationAngle);
        let rotatedY = point.y * Math.cos(tiltAngle) - rotatedZ * Math.sin(tiltAngle);

        const scale = 15;
        const screenX = centerX + rotatedX * scale;
        const screenY = centerY + rotatedY * scale;

        const age = (points.length - index) / points.length;
        const alpha = age * pulsation * 0.6;
        const hue = (rotatedZ * 10 + time * 30) % 360;

        ctx.fillStyle = `hsla(${hue}, 80%, 70%, ${alpha})`;
        ctx.beginPath();
        ctx.arc(screenX, screenY, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    ctx.restore();
  };
}
