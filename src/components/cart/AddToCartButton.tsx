'use client'

import { useCart } from '@/contexts/CartContext'
import { useCartTheme } from '@/contexts/CartThemeContext'
import { Button, type ButtonProps } from '@/components/ui/button'
import { triggerCartToast } from '@/components/cart/CartToast'
import { cn } from '@/lib/utils'
import type { CartItem } from '@/types/cart-theme'

interface AddToCartButtonProps {
  /** Item à ajouter au panier */
  item: CartItem
  /** Classes CSS additionnelles */
  className?: string
  /** Variant du bouton shadcn */
  variant?: ButtonProps['variant']
}

/**
 * Bouton pour ajouter un item au panier
 * Affiche le verbAdd du thème actif ou "Déjà ajouté" si déjà présent
 */
export function AddToCartButton({ item, className, variant = 'default' }: AddToCartButtonProps) {
  const { addItem, isInCart } = useCart()
  const { theme } = useCartTheme()

  const alreadyInCart = isInCart(item.id)

  const handleClick = () => {
    if (alreadyInCart) return
    addItem(item)
    triggerCartToast(`${theme.notification} ${item.name}`)
  }

  return (
    <Button
      variant={alreadyInCart ? 'secondary' : variant}
      className={cn('text-white', className)}
      disabled={alreadyInCart}
      onClick={handleClick}
    >
      {alreadyInCart ? 'Déjà ajouté ✓' : `${theme.icon} ${theme.verbAdd}`}
    </Button>
  )
}
