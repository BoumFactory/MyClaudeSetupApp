'use client'

import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react'
import type { CartItem } from '@/types/cart-theme'

const STORAGE_KEY = 'bfcours-cart'

interface CartContextType {
  /** Liste des items dans le panier */
  items: CartItem[]
  /** Nombre d'items dans le panier */
  count: number
  /** Ajouter un item au panier */
  addItem: (item: CartItem) => void
  /** Retirer un item du panier par son id */
  removeItem: (id: string) => void
  /** Vider le panier */
  clearCart: () => void
  /** Vérifier si un item est dans le panier */
  isInCart: (id: string) => boolean
}

const CartContext = createContext<CartContextType | undefined>(undefined)

/**
 * Lit le panier depuis localStorage
 */
function loadCart(): CartItem[] {
  if (typeof window === 'undefined') return []
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    if (Array.isArray(parsed)) return parsed
    return []
  } catch {
    return []
  }
}

/**
 * Sauvegarde le panier dans localStorage
 */
function saveCart(items: CartItem[]): void {
  if (typeof window === 'undefined') return
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  } catch {
    // Silencieux en cas d'erreur (ex: quota dépassé)
  }
}

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([])
  const [hydrated, setHydrated] = useState(false)

  // Charger le panier au montage (côté client uniquement)
  useEffect(() => {
    setItems(loadCart())
    setHydrated(true)
  }, [])

  // Sauvegarder a chaque modification (apres hydratation)
  useEffect(() => {
    if (hydrated) {
      saveCart(items)
    }
  }, [items, hydrated])

  const addItem = useCallback((item: CartItem) => {
    setItems(prev => {
      if (prev.some(i => i.id === item.id)) return prev
      return [...prev, item]
    })
  }, [])

  const removeItem = useCallback((id: string) => {
    setItems(prev => prev.filter(i => i.id !== id))
  }, [])

  const clearCart = useCallback(() => {
    setItems([])
  }, [])

  const isInCart = useCallback((id: string) => {
    return items.some(i => i.id === id)
  }, [items])

  return (
    <CartContext.Provider
      value={{
        items,
        count: items.length,
        addItem,
        removeItem,
        clearCart,
        isInCart,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

/**
 * Hook pour accéder au panier
 * Doit être utilisé dans un CartProvider
 */
export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
