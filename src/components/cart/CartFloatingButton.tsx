'use client'

import { useState } from 'react'
import { useCart } from '@/contexts/CartContext'
import { useCartTheme } from '@/contexts/CartThemeContext'
import { CartDrawer } from '@/components/cart/CartDrawer'
import { cn } from '@/lib/utils'

/**
 * Bouton flottant en bas à droite affichant le panier
 * Visible uniquement si le panier contient des items
 * Ouvre le CartDrawer au clic
 */
export function CartFloatingButton() {
  const { count } = useCart()
  const { theme } = useCartTheme()
  const [drawerOpen, setDrawerOpen] = useState(false)

  return (
    <>
      {/* Bouton flottant */}
      <button
        onClick={() => setDrawerOpen(true)}
        className={cn(
          'fixed bottom-6 right-6 z-40',
          'flex items-center gap-2',
          'px-4 py-3 rounded-full',
          'glass-card cursor-pointer',
          'shadow-lg shadow-indigo-500/20',
          'transition-all duration-300 ease-out',
          'hover:scale-105 hover:shadow-xl hover:shadow-indigo-500/30',
          'active:scale-95',
          count > 0
            ? 'opacity-100 scale-100 pointer-events-auto'
            : 'opacity-0 scale-75 pointer-events-none'
        )}
        aria-label={`${theme.name} - ${count} élément${count > 1 ? 's' : ''}`}
      >
        <span className="text-xl">{theme.icon}</span>
        {count > 0 && (
          <span
            className={cn(
              'flex items-center justify-center',
              'min-w-[1.25rem] h-5 px-1.5',
              'rounded-full text-xs font-bold',
              'bg-indigo-500 text-white'
            )}
          >
            {count}
          </span>
        )}
      </button>

      {/* Drawer */}
      <CartDrawer open={drawerOpen} onOpenChange={setDrawerOpen} />
    </>
  )
}
