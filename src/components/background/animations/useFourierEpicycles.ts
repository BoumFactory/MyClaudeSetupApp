export function useFourierEpicycles() {
  interface Epicycle {
    freq: number;
    amp: number;
    phase: number;
  }

  // Créer des épicycles pour dessiner une forme complexe
  const createEpicycles = (count: number): Epicycle[] => {
    const epicycles: Epicycle[] = [];
    for (let i = 0; i < count; i++) {
      epicycles.push({
        freq: i * 2 + 1, // Fréquences impaires pour symétrie
        amp: 100 / (i * 2 + 1), // Amplitude décroissante
        phase: Math.random() * Math.PI * 2,
      });
    }
    return epicycles;
  };

  const epicycles = createEpicycles(8);

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();

    // Dessiner plusieurs sets d'épicycles avec différentes orientations
    const numSets = 3;

    for (let set = 0; set < numSets; set++) {
      const rotation = (set / numSets) * Math.PI * 2;

      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(rotation);

      let x = 0;
      let y = 0;

      // Tracer le chemin des épicycles
      const pathPoints: { x: number; y: number }[] = [];

      // Dessiner chaque épicycle
      epicycles.forEach((epi, index) => {
        const angle = time * epi.freq * 0.3 + epi.phase;
        const nextX = x + Math.cos(angle) * epi.amp;
        const nextY = y + Math.sin(angle) * epi.amp;

        // Dessiner le cercle de l'épicycle
        const alpha = 0.1 + (index / epicycles.length) * 0.2;
        ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(x, y, epi.amp, 0, Math.PI * 2);
        ctx.stroke();

        // Ligne de rayon
        ctx.strokeStyle = `rgba(168, 85, 247, ${alpha * 1.5})`;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(nextX, nextY);
        ctx.stroke();

        // Point au bout du rayon
        if (index === epicycles.length - 1) {
          const pulsation = Math.sin(time * 0.8) * 0.5 + 0.5;
          ctx.fillStyle = `rgba(168, 85, 247, ${pulsation * 0.8})`;
          ctx.beginPath();
          ctx.arc(nextX, nextY, 4, 0, Math.PI * 2);
          ctx.fill();
        }

        x = nextX;
        y = nextY;
      });

      // Tracer la courbe résultante
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.4)';
      ctx.lineWidth = 2;
      ctx.beginPath();

      const steps = 200;
      for (let i = 0; i <= steps; i++) {
        const t = time * 0.3 + (i / steps) * Math.PI * 2;
        let px = 0;
        let py = 0;

        epicycles.forEach((epi) => {
          const angle = t * epi.freq + epi.phase;
          px += Math.cos(angle) * epi.amp;
          py += Math.sin(angle) * epi.amp;
        });

        if (i === 0) {
          ctx.moveTo(px, py);
        } else {
          ctx.lineTo(px, py);
        }
      }

      ctx.stroke();

      ctx.restore();
    }

    ctx.restore();
  };
}
