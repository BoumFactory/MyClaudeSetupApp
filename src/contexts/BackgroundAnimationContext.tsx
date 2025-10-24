'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type AnimationId = 'fibonacci' | 'fourier' | 'lissajous' | 'ulam' | 'lorenz' | 'flowfield' | 'rossler' | 'sierpinski' | 'dragon';

export type AnimationInfo = {
  id: AnimationId;
  name: string;
  secret: string;
};

export const ANIMATIONS: AnimationInfo[] = [
  {
    id: 'fibonacci',
    name: 'Spirale de Fibonacci',
    secret: 'Le nombre d\'or φ ≈ 1.618 apparaît dans la nature',
  },
  {
    id: 'fourier',
    name: 'Épicycles de Fourier',
    secret: 'Cercles tournant sur des cercles dessinent des formes complexes',
  },
  {
    id: 'flowfield',
    name: 'Champ Vectoriel',
    secret: 'Particules suivant les lignes invisibles d\'un champ de forces',
  },
  {
    id: 'lissajous',
    name: 'Courbes de Lissajous',
    secret: 'Les harmonies cachées entre fréquences produisent des formes élégantes',
  },
  {
    id: 'ulam',
    name: 'Spirale d\'Ulam',
    secret: 'Les nombres premiers forment des diagonales mystérieuses',
  },
  {
    id: 'lorenz',
    name: 'Attracteur de Lorenz',
    secret: 'Le chaos déterministe : sensibilité extrême aux conditions initiales',
  },
  {
    id: 'rossler',
    name: 'Attracteur de Rössler',
    secret: 'Système chaotique continu créant une bande de Möbius étrange',
  },
  {
    id: 'sierpinski',
    name: 'Triangle de Sierpiński',
    secret: 'Fractale auto-similaire générée par le jeu du chaos',
  },
  {
    id: 'dragon',
    name: 'Courbe du Dragon',
    secret: 'Fractale créée par pliage de papier, complexité émergente',
  },
];

const ANIMATION_KEY = 'math-background-animation';

type BackgroundAnimationContextType = {
  currentAnimation: AnimationId | null;
  setAnimation: (id: AnimationId) => void;
  animations: AnimationInfo[];
  cycleAnimation: () => void;
};

const BackgroundAnimationContext = createContext<BackgroundAnimationContextType | undefined>(undefined);

export function BackgroundAnimationProvider({ children }: { children: ReactNode }) {
  const [currentAnimation, setCurrentAnimationState] = useState<AnimationId | null>(null);

  // Initialiser l'animation au chargement
  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Vérifier si une animation est déjà stockée en session
    const storedId = sessionStorage.getItem(ANIMATION_KEY) as AnimationId | null;

    if (storedId && ANIMATIONS.find(a => a.id === storedId)) {
      setCurrentAnimationState(storedId);
    } else {
      // Sélectionner une animation au hasard
      const randomIndex = Math.floor(Math.random() * ANIMATIONS.length);
      const randomId = ANIMATIONS[randomIndex].id;
      sessionStorage.setItem(ANIMATION_KEY, randomId);
      setCurrentAnimationState(randomId);
    }
  }, []);

  const setAnimation = (id: AnimationId) => {
    sessionStorage.setItem(ANIMATION_KEY, id);
    setCurrentAnimationState(id);
  };

  const cycleAnimation = () => {
    if (!currentAnimation) return;

    const currentIndex = ANIMATIONS.findIndex(a => a.id === currentAnimation);
    const nextIndex = (currentIndex + 1) % ANIMATIONS.length;
    const nextId = ANIMATIONS[nextIndex].id;

    setAnimation(nextId);
  };

  return (
    <BackgroundAnimationContext.Provider
      value={{
        currentAnimation,
        setAnimation,
        animations: ANIMATIONS,
        cycleAnimation,
      }}
    >
      {children}
    </BackgroundAnimationContext.Provider>
  );
}

export function useBackgroundAnimation() {
  const context = useContext(BackgroundAnimationContext);
  if (context === undefined) {
    throw new Error('useBackgroundAnimation must be used within a BackgroundAnimationProvider');
  }
  return context;
}
