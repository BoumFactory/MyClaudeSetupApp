export function useFlowField() {
  interface Particle {
    x: number;
    y: number;
    vx: number;
    vy: number;
    age: number;
    maxAge: number;
    hue: number;
  }

  let particles: Particle[] = [];

  // Initialiser les particules
  const initParticles = (width: number, height: number, count: number) => {
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: 0,
        vy: 0,
        age: 0,
        maxAge: 200 + Math.random() * 200,
        hue: Math.random() * 360,
      });
    }
  };

  // Calculer le champ vectoriel à une position donnée
  const getFlowVector = (x: number, y: number, time: number, width: number, height: number) => {
    // Utiliser plusieurs fonctions sinus/cosinus pour créer un champ complexe
    const scale = 0.003;
    const angle1 = Math.sin(x * scale + time * 0.2) * Math.cos(y * scale);
    const angle2 = Math.cos(x * scale * 1.5 - time * 0.15) * Math.sin(y * scale * 1.5);
    const angle3 = Math.sin((x + y) * scale * 0.5 + time * 0.3);

    const angle = angle1 + angle2 + angle3;

    return {
      vx: Math.cos(angle) * 2,
      vy: Math.sin(angle) * 2,
    };
  };

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    // Initialiser si nécessaire
    if (particles.length === 0) {
      initParticles(width, height, 300);
    }

    ctx.save();

    // Dessiner le champ vectoriel avec des lignes de flux subtiles
    const gridSize = 50;
    for (let x = 0; x < width; x += gridSize) {
      for (let y = 0; y < height; y += gridSize) {
        const flow = getFlowVector(x, y, time, width, height);

        ctx.strokeStyle = 'rgba(99, 102, 241, 0.08)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + flow.vx * 10, y + flow.vy * 10);
        ctx.stroke();

        // Point au centre
        ctx.fillStyle = 'rgba(168, 85, 247, 0.15)';
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Mettre à jour et dessiner les particules
    particles.forEach((p, index) => {
      // Obtenir la force du champ vectoriel
      const flow = getFlowVector(p.x, p.y, time, width, height);

      // Appliquer la force
      p.vx += (flow.vx - p.vx) * 0.1;
      p.vy += (flow.vy - p.vy) * 0.1;

      // Mettre à jour la position
      p.x += p.vx;
      p.y += p.vy;

      // Vieillir la particule
      p.age++;

      // Réinitialiser si trop vieille ou hors écran
      if (p.age > p.maxAge || p.x < 0 || p.x > width || p.y < 0 || p.y > height) {
        p.x = Math.random() * width;
        p.y = Math.random() * height;
        p.vx = 0;
        p.vy = 0;
        p.age = 0;
        p.maxAge = 200 + Math.random() * 200;
        p.hue = Math.random() * 360;
      }

      // Dessiner la particule
      const alpha = (1 - p.age / p.maxAge) * 0.6;
      const hue = (p.hue + time * 20) % 360;

      // Traînée de la particule
      ctx.strokeStyle = `hsla(${hue}, 70%, 60%, ${alpha * 0.5})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(p.x, p.y);
      ctx.lineTo(p.x - p.vx * 5, p.y - p.vy * 5);
      ctx.stroke();

      // Point de la particule
      const pulsation = Math.sin(time * 2 + index * 0.1) * 0.3 + 0.7;
      ctx.fillStyle = `hsla(${hue}, 80%, 70%, ${alpha * pulsation})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
      ctx.fill();
    });

    ctx.restore();
  };
}
