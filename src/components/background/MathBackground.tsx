'use client';

import { useEffect, useRef } from 'react';
import { useFibonacciSpiral } from './animations/useFibonacciSpiral';
import { useFourierEpicycles } from './animations/useFourierEpicycles';
import { useLissajous } from './animations/useLissajous';
import { useUlamSpiral } from './animations/useUlamSpiral';
import { useLorenzAttractor } from './animations/useLorenzAttractor';
import { useFlowField } from './animations/useFlowField';
import { useRosslerAttractor } from './animations/useRosslerAttractor';
import { useSierpinskiTriangle } from './animations/useSierpinskiTriangle';
import { useDragonCurve } from './animations/useDragonCurve';
import { useBackgroundAnimation } from '@/contexts/BackgroundAnimationContext';

// Type pour une animation mathématique
export type MathAnimation = {
  id: string;
  name: string;
  secret: string;
  draw: (ctx: CanvasRenderingContext2D, width: number, height: number, time: number) => void;
};

export function MathBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number | undefined>(undefined);
  const { currentAnimation } = useBackgroundAnimation();

  // Récupérer toutes les animations disponibles
  const fibonacciDraw = useFibonacciSpiral();
  const fourierDraw = useFourierEpicycles();
  const lissajousDraw = useLissajous();
  const ulamDraw = useUlamSpiral();
  const lorenzDraw = useLorenzAttractor();
  const flowFieldDraw = useFlowField();
  const rosslerDraw = useRosslerAttractor();
  const sierpinskiDraw = useSierpinskiTriangle();
  const dragonDraw = useDragonCurve();

  const animations: MathAnimation[] = [
    {
      id: 'fibonacci',
      name: 'Spirale de Fibonacci',
      secret: 'Le nombre d\'or φ ≈ 1.618 apparaît dans la nature',
      draw: fibonacciDraw,
    },
    {
      id: 'fourier',
      name: 'Épicycles de Fourier',
      secret: 'Cercles tournant sur des cercles dessinent des formes complexes',
      draw: fourierDraw,
    },
    {
      id: 'flowfield',
      name: 'Champ Vectoriel',
      secret: 'Particules suivant les lignes invisibles d\'un champ de forces',
      draw: flowFieldDraw,
    },
    {
      id: 'lissajous',
      name: 'Courbes de Lissajous',
      secret: 'Les harmonies cachées entre fréquences produisent des formes élégantes',
      draw: lissajousDraw,
    },
    {
      id: 'ulam',
      name: 'Spirale d\'Ulam',
      secret: 'Les nombres premiers forment des diagonales mystérieuses',
      draw: ulamDraw,
    },
    {
      id: 'lorenz',
      name: 'Attracteur de Lorenz',
      secret: 'Le chaos déterministe : sensibilité extrême aux conditions initiales',
      draw: lorenzDraw,
    },
    {
      id: 'rossler',
      name: 'Attracteur de Rössler',
      secret: 'Système chaotique continu créant une bande de Möbius étrange',
      draw: rosslerDraw,
    },
    {
      id: 'sierpinski',
      name: 'Triangle de Sierpiński',
      secret: 'Fractale auto-similaire générée par le jeu du chaos',
      draw: sierpinskiDraw,
    },
    {
      id: 'dragon',
      name: 'Courbe du Dragon',
      secret: 'Fractale créée par pliage de papier, complexité émergente',
      draw: dragonDraw,
    },
  ];

  // Animation loop
  useEffect(() => {
    if (!currentAnimation) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    // Configurer le canvas avec la taille de la fenêtre
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const selectedAnimation = animations.find(a => a.id === currentAnimation);
    if (!selectedAnimation) return;

    let startTime = Date.now();

    const animate = () => {
      const currentTime = (Date.now() - startTime) / 1000; // Temps en secondes

      // Effacer le canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Dessiner l'animation
      selectedAnimation.draw(ctx, canvas.width, canvas.height, currentTime);

      animationFrameRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [currentAnimation]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
      style={{
        opacity: 0.3,
        mixBlendMode: 'screen'
      }}
    />
  );
}
