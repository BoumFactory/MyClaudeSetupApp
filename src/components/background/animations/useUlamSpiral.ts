export function useUlamSpiral() {
  // Test de primalité simple (optimisé pour les petits nombres)
  const isPrime = (n: number): boolean => {
    if (n < 2) return false;
    if (n === 2) return true;
    if (n % 2 === 0) return false;

    const sqrt = Math.sqrt(n);
    for (let i = 3; i <= sqrt; i += 2) {
      if (n % i === 0) return false;
    }
    return true;
  };

  // Pré-calculer les nombres premiers jusqu'à un certain nombre
  const maxNumber = 2000;
  const primes = new Set<number>();
  for (let i = 2; i <= maxNumber; i++) {
    if (isPrime(i)) {
      primes.add(i);
    }
  }

  return (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => {
    const centerX = width / 2;
    const centerY = height / 2;

    ctx.save();

    // Rotation de la spirale
    const rotation = time * 0.1;
    ctx.translate(centerX, centerY);
    ctx.rotate(rotation);

    const cellSize = 8;
    let x = 0;
    let y = 0;
    let dx = 0;
    let dy = -1;

    // Dessiner la spirale d'Ulam
    for (let n = 1; n <= maxNumber; n++) {
      const screenX = x * cellSize;
      const screenY = y * cellSize;

      // Vérifier si le point est visible à l'écran
      if (
        Math.abs(screenX) < width / 2 + 100 &&
        Math.abs(screenY) < height / 2 + 100
      ) {
        if (primes.has(n)) {
          // Nombre premier - point lumineux
          const pulsation = Math.sin(time * 0.5 + n * 0.01) * 0.3 + 0.7;
          const distance = Math.sqrt(screenX * screenX + screenY * screenY);
          const maxDistance = Math.sqrt(width * width + height * height) / 2;
          const distanceFactor = 1 - Math.min(distance / maxDistance, 1);

          ctx.fillStyle = `rgba(168, 85, 247, ${pulsation * 0.4 * distanceFactor})`;
          ctx.beginPath();
          ctx.arc(screenX, screenY, 3, 0, Math.PI * 2);
          ctx.fill();

          // Souligner les diagonales de nombres premiers
          if (n > 10 && Math.abs(x) === Math.abs(y)) {
            ctx.strokeStyle = `rgba(99, 102, 241, ${0.3 * distanceFactor})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(screenX, screenY);
            ctx.stroke();
          }
        } else {
          // Nombre composé - point très subtil
          ctx.fillStyle = 'rgba(99, 102, 241, 0.05)';
          ctx.fillRect(screenX - 1, screenY - 1, 2, 2);
        }
      }

      // Mouvement en spirale (algorithme classique)
      if (x === y || (x < 0 && x === -y) || (x > 0 && x === 1 - y)) {
        const temp = dx;
        dx = -dy;
        dy = temp;
      }

      x += dx;
      y += dy;
    }

    // Dessiner des cercles pour souligner la structure
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.1)';
    ctx.lineWidth = 1;

    for (let r = 50; r < Math.min(width, height); r += 100) {
      const pulsation = Math.sin(time * 0.2 + r * 0.01) * 5;
      ctx.beginPath();
      ctx.arc(0, 0, r + pulsation, 0, Math.PI * 2);
      ctx.stroke();
    }

    ctx.restore();
  };
}
