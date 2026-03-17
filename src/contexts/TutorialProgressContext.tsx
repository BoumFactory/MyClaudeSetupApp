'use client'

import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  type ReactNode,
} from 'react'
import { TutorialProgress } from '@/types/tutorial'
import { PARCOURS } from '@/data/parcours'

const STORAGE_KEY = 'bfcours-tutorial-progress'

/** Valeur par défaut de la progression */
const defaultProgress: TutorialProgress = {
  completedCapsules: [],
  lastVisited: undefined,
  updatedAt: new Date().toISOString(),
}

interface ParcoursProgressInfo {
  completed: number
  total: number
  percent: number
}

interface TutorialProgressContextValue {
  progress: TutorialProgress
  markComplete: (capsuleId: string) => void
  isCompleted: (capsuleId: string) => boolean
  getParcoursProgress: (parcoursId: string) => ParcoursProgressInfo
  setLastVisited: (capsuleId: string) => void
  resetProgress: () => void
}

const TutorialProgressContext = createContext<TutorialProgressContextValue | null>(null)

/**
 * Charger la progression depuis localStorage
 */
function loadProgress(): TutorialProgress {
  if (typeof window === 'undefined') return defaultProgress
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return defaultProgress
    const parsed = JSON.parse(raw) as TutorialProgress
    return {
      completedCapsules: Array.isArray(parsed.completedCapsules)
        ? parsed.completedCapsules
        : [],
      lastVisited: parsed.lastVisited,
      updatedAt: parsed.updatedAt || new Date().toISOString(),
    }
  } catch {
    return defaultProgress
  }
}

/**
 * Sauvegarder la progression dans localStorage
 */
function saveProgress(progress: TutorialProgress): void {
  if (typeof window === 'undefined') return
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
  } catch {
    // localStorage plein ou indisponible
  }
}

export function TutorialProgressProvider({ children }: { children: ReactNode }) {
  const [progress, setProgress] = useState<TutorialProgress>(defaultProgress)
  const [hydrated, setHydrated] = useState(false)

  // Charger depuis localStorage au montage
  useEffect(() => {
    setProgress(loadProgress())
    setHydrated(true)
  }, [])

  // Sauvegarder a chaque changement (apres hydratation)
  useEffect(() => {
    if (hydrated) {
      saveProgress(progress)
    }
  }, [progress, hydrated])

  const markComplete = useCallback((capsuleId: string) => {
    setProgress((prev) => {
      if (prev.completedCapsules.includes(capsuleId)) return prev
      return {
        ...prev,
        completedCapsules: [...prev.completedCapsules, capsuleId],
        updatedAt: new Date().toISOString(),
      }
    })
  }, [])

  const isCompleted = useCallback(
    (capsuleId: string) => progress.completedCapsules.includes(capsuleId),
    [progress.completedCapsules]
  )

  const getParcoursProgress = useCallback(
    (parcoursId: string): ParcoursProgressInfo => {
      const parcours = PARCOURS.find((p) => p.id === parcoursId)
      if (!parcours) return { completed: 0, total: 0, percent: 0 }
      const total = parcours.capsules.length
      const completed = parcours.capsules.filter((id) =>
        progress.completedCapsules.includes(id)
      ).length
      const percent = total > 0 ? Math.round((completed / total) * 100) : 0
      return { completed, total, percent }
    },
    [progress.completedCapsules]
  )

  const setLastVisited = useCallback((capsuleId: string) => {
    setProgress((prev) => ({
      ...prev,
      lastVisited: capsuleId,
      updatedAt: new Date().toISOString(),
    }))
  }, [])

  const resetProgress = useCallback(() => {
    const reset: TutorialProgress = {
      completedCapsules: [],
      lastVisited: undefined,
      updatedAt: new Date().toISOString(),
    }
    setProgress(reset)
  }, [])

  return (
    <TutorialProgressContext.Provider
      value={{
        progress,
        markComplete,
        isCompleted,
        getParcoursProgress,
        setLastVisited,
        resetProgress,
      }}
    >
      {children}
    </TutorialProgressContext.Provider>
  )
}

/**
 * Hook pour accéder à la progression tutoriel
 */
export function useTutorialProgress(): TutorialProgressContextValue {
  const context = useContext(TutorialProgressContext)
  if (!context) {
    throw new Error(
      'useTutorialProgress doit être utilisé dans un TutorialProgressProvider'
    )
  }
  return context
}
