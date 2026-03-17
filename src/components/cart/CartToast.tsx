'use client'

import { useState, useEffect, useCallback } from 'react'
import { cn } from '@/lib/utils'

interface ToastData {
  message: string
  id: number
}

let toastId = 0
let showToastFn: ((message: string) => void) | null = null

/**
 * Fonction globale pour afficher un toast depuis n'importe quel composant
 * Le CartToast doit etre monte dans l'arbre pour que cela fonctionne
 */
export function triggerCartToast(message: string) {
  showToastFn?.(message)
}

/**
 * Composant toast temporaire (3s) avec animation slide-up + fade-out
 * A monter une seule fois dans le layout
 */
export function CartToast() {
  const [toast, setToast] = useState<ToastData | null>(null)
  const [visible, setVisible] = useState(false)

  const showToast = useCallback((message: string) => {
    const id = ++toastId
    setToast({ message, id })
    setVisible(true)

    // Demarrer le fade-out apres 2.5s
    setTimeout(() => {
      setVisible(false)
    }, 2500)

    // Retirer completement apres 3s
    setTimeout(() => {
      setToast(prev => (prev?.id === id ? null : prev))
    }, 3000)
  }, [])

  // Enregistrer la fonction globale
  useEffect(() => {
    showToastFn = showToast
    return () => {
      showToastFn = null
    }
  }, [showToast])

  if (!toast) return null

  return (
    <div
      className={cn(
        'fixed bottom-20 left-1/2 -translate-x-1/2 z-50',
        'px-4 py-2 rounded-lg',
        'glass-card text-white text-sm font-medium',
        'transition-all duration-500 ease-out',
        visible
          ? 'opacity-100 translate-y-0'
          : 'opacity-0 translate-y-4'
      )}
    >
      {toast.message}
    </div>
  )
}
