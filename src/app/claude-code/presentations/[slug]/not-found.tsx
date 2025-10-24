import Link from "next/link"
import { BookOpen, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"

/**
 * Page 404 pour les présentations non trouvées
 */
export default function PresentationNotFound() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="text-center space-y-6 max-w-lg">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <BookOpen className="w-8 h-8 text-white" />
        </div>

        <div className="space-y-2">
          <h2 className="text-2xl font-semibold">Présentation non trouvée</h2>
          <p className="text-muted-foreground">
            Cette présentation n'existe pas ou n'est plus disponible.
          </p>
        </div>

        <Button asChild variant="cosmic">
          <Link href="/claude-code/presentations">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour aux présentations
          </Link>
        </Button>
      </div>
    </div>
  )
}
