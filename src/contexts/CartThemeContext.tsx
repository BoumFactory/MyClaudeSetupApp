'use client'

import { createContext, useContext, useMemo, type ReactNode } from 'react'
import { useBackgroundAnimation } from '@/contexts/BackgroundAnimationContext'
import { CART_THEMES } from '@/data/cart-themes'
import type { CartTheme } from '@/types/cart-theme'

interface CartThemeContextType {
  /** Thème allégorique actif selon l'animation de fond */
  theme: CartTheme
}

const CartThemeContext = createContext<CartThemeContextType | undefined>(undefined)

/** Thème par défaut (dragon) utilisé avant l'hydratation */
const DEFAULT_THEME = CART_THEMES.dragon

export function CartThemeProvider({ children }: { children: ReactNode }) {
  const { currentAnimation } = useBackgroundAnimation()

  const theme = useMemo<CartTheme>(() => {
    if (!currentAnimation) return DEFAULT_THEME
    return CART_THEMES[currentAnimation] ?? DEFAULT_THEME
  }, [currentAnimation])

  return (
    <CartThemeContext.Provider value={{ theme }}>
      {children}
    </CartThemeContext.Provider>
  )
}

/**
 * Hook pour accéder au thème allégorique du panier
 * Doit être utilisé dans un CartThemeProvider (lui-même dans un BackgroundAnimationProvider)
 */
export function useCartTheme() {
  const context = useContext(CartThemeContext)
  if (context === undefined) {
    throw new Error('useCartTheme must be used within a CartThemeProvider')
  }
  return context
}
