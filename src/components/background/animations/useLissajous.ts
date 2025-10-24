export function useLissajous() {
  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();

    // Dessiner plusieurs courbes de Lissajous avec différents rapports de fréquences
    const curves = [
      { a: 3, b: 2, delta: 0, color: 'rgba(99, 102, 241, 0.3)', scale: 0.8 },
      { a: 5, b: 4, delta: Math.PI / 2, color: 'rgba(168, 85, 247, 0.25)', scale: 0.6 },
      { a: 7, b: 5, delta: Math.PI / 4, color: 'rgba(139, 92, 246, 0.2)', scale: 0.9 },
      { a: 2, b: 3, delta: Math.PI / 3, color: 'rgba(124, 58, 237, 0.25)', scale: 0.7 },
    ];

    curves.forEach((curve, index) => {
      ctx.strokeStyle = curve.color;
      ctx.lineWidth = 2;
      ctx.beginPath();

      const amplitude = Math.min(width, height) * 0.35 * curve.scale;
      const steps = 500;

      // Animation des paramètres
      const animatedDelta = curve.delta + time * 0.3;
      const animatedA = curve.a + Math.sin(time * 0.5 + index) * 0.3;
      const animatedB = curve.b + Math.cos(time * 0.4 + index) * 0.3;

      for (let i = 0; i <= steps; i++) {
        const t = (i / steps) * Math.PI * 2;

        const x = centerX + amplitude * Math.sin(animatedA * t + animatedDelta);
        const y = centerY + amplitude * Math.sin(animatedB * t);

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.stroke();

      // Ajouter des points lumineux le long de la courbe
      const pulsation = Math.sin(time * 0.5 + index) * 0.3 + 0.7;
      ctx.fillStyle = curve.color.replace('0.3', String(pulsation * 0.5)).replace('0.25', String(pulsation * 0.5)).replace('0.2', String(pulsation * 0.5));

      for (let i = 0; i <= steps; i += 20) {
        const t = (i / steps) * Math.PI * 2;
        const x = centerX + amplitude * Math.sin(animatedA * t + animatedDelta);
        const y = centerY + amplitude * Math.sin(animatedB * t);

        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // Dessiner des cercles concentriques pour souligner les harmonies
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.1)';
    ctx.lineWidth = 1;

    for (let r = 50; r < Math.min(width, height) / 2; r += 50) {
      const pulsation = Math.sin(time * 0.3 + r * 0.01) * 10;
      ctx.beginPath();
      ctx.arc(centerX, centerY, r + pulsation, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
  };
}
