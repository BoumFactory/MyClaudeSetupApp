import Link from "next/link"
import { Home, Search } from "lucide-react"
import { Button } from "@/components/ui/button"

/**
 * Page 404 personnalisée
 */
export default function NotFound() {
  return (
    <div className="flex items-center justify-center min-h-[600px]">
      <div className="text-center space-y-6 max-w-lg">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl cosmic-gradient mb-4">
          <Search className="w-10 h-10 text-white" />
        </div>

        <h1 className="text-6xl font-bold glow-text">404</h1>

        <div className="space-y-2">
          <h2 className="text-2xl font-semibold">Page non trouvée</h2>
          <p className="text-muted-foreground">
            Désolé, la page que vous recherchez n'existe pas ou a été déplacée.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/">
              <Home className="w-5 h-5 mr-2" />
              Retour à l'accueil
            </Link>
          </Button>

          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code">Explorer Claude Code</Link>
          </Button>
        </div>
      </div>
    </div>
  )
}
