export function useFibonacciSpiral() {
  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const PHI = 1.618033988749895; // Nombre d'or
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();

    // Rotation de la spirale
    const rotation = time * 0.15; // Rotation accélérée

    ctx.translate(centerX, centerY);
    ctx.rotate(rotation);

    // Dessiner plusieurs spirales pour remplir l'espace
    for (let spiralOffset = 0; spiralOffset < Math.PI * 2; spiralOffset += Math.PI * 2 / 3) {
      ctx.save();
      ctx.rotate(spiralOffset);

      // Gradient pour la spirale
      const gradient = ctx.createLinearGradient(-width / 2, 0, width / 2, 0);
      gradient.addColorStop(0, 'rgba(99, 102, 241, 0.1)');
      gradient.addColorStop(0.5, 'rgba(168, 85, 247, 0.2)');
      gradient.addColorStop(1, 'rgba(99, 102, 241, 0.1)');

      ctx.strokeStyle = gradient;
      ctx.lineWidth = 2;
      ctx.beginPath();

      // Dessiner la spirale dorée
      const maxRadius = Math.max(width, height) * 0.8;
      const steps = 300;

      for (let i = 0; i < steps; i++) {
        const angle = (i / steps) * Math.PI * 6; // 3 tours
        const radius = (i / steps) * maxRadius * Math.pow(PHI, angle / (Math.PI * 2));

        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.stroke();
      ctx.restore();
    }

    // Ajouter des points dorés le long de la spirale pour souligner le rapport
    const pulsation = Math.sin(time * 0.5) * 0.3 + 0.7;

    ctx.fillStyle = `rgba(168, 85, 247, ${pulsation * 0.4})`;

    for (let spiralOffset = 0; spiralOffset < Math.PI * 2; spiralOffset += Math.PI * 2 / 3) {
      ctx.save();
      ctx.rotate(spiralOffset);

      for (let i = 0; i < 30; i++) {
        const angle = (i / 30) * Math.PI * 6;
        const maxRadius = Math.max(width, height) * 0.8;
        const radius = (i / 30) * maxRadius * Math.pow(PHI, angle / (Math.PI * 2));

        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        const size = (i / 30) * 3 + 1;

        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.restore();
    }

    ctx.restore();
  };
}
