export function useSierpinskiTriangle() {
  interface Point {
    x: number;
    y: number;
  }

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

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();
    ctx.translate(centerX, centerY);

    // Rotation
    const rotation = time * 0.1;
    ctx.rotate(rotation);

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

    // Dessiner les points avec des couleurs spectaculaires
    points.forEach((point, index) => {
      const age = index / numPoints;
      const hue = (age * 360 + time * 40) % 360;
      const alpha = 0.1 + age * 0.3;
      const pulsation = Math.sin(time * 0.5 + index * 0.001) * 0.2 + 0.8;

      ctx.fillStyle = `hsla(${hue}, 70%, 60%, ${alpha * pulsation})`;
      ctx.beginPath();
      ctx.arc(point.x, point.y, 1.5, 0, Math.PI * 2);
      ctx.fill();
    });

    // Dessiner les sommets du triangle avec des halos
    const vertexPulsation = Math.sin(time * 0.8) * 0.5 + 0.5;
    vertices.forEach((vertex, index) => {
      const hue = (index * 120 + time * 30) % 360;

      // Halo
      const gradient = ctx.createRadialGradient(vertex.x, vertex.y, 0, vertex.x, vertex.y, 40);
      gradient.addColorStop(0, `hsla(${hue}, 80%, 60%, ${0.4 * vertexPulsation})`);
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(vertex.x, vertex.y, 40, 0, Math.PI * 2);
      ctx.fill();

      // Point central brillant
      ctx.fillStyle = `hsla(${hue}, 90%, 70%, ${0.8 * vertexPulsation})`;
      ctx.beginPath();
      ctx.arc(vertex.x, vertex.y, 4, 0, Math.PI * 2);
      ctx.fill();
    });

    // Dessiner les arêtes du triangle
    ctx.strokeStyle = `rgba(168, 85, 247, ${0.3 + vertexPulsation * 0.2})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    vertices.forEach((vertex, index) => {
      const nextVertex = vertices[(index + 1) % vertices.length];
      ctx.moveTo(vertex.x, vertex.y);
      ctx.lineTo(nextVertex.x, nextVertex.y);
    });
    ctx.stroke();

    ctx.restore();
  };
}
