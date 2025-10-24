import { Loader2 } from "lucide-react"

/**
 * Page de chargement globale
 */
export default function Loading() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="text-center space-y-4">
        <Loader2 className="w-12 h-12 animate-spin mx-auto text-cosmic-400" />
        <p className="text-muted-foreground">Chargement en cours...</p>
      </div>
    </div>
  )
}
