import Link from "next/link"
import { ChevronRight, Home } from "lucide-react"

export interface BreadcrumbItem {
  label: string
  href: string
}

interface BreadcrumbProps {
  items: BreadcrumbItem[]
}

/**
 * Composant de fil d'Ariane (breadcrumb) pour la navigation
 */
export function Breadcrumb({ items }: BreadcrumbProps) {
  return (
    <nav className="flex items-center space-x-2 text-sm mb-6">
      <Link
        href="/"
        className="flex items-center gap-1 text-muted-foreground hover:text-foreground transition-colors"
      >
        <Home className="w-4 h-4" />
        <span>Accueil</span>
      </Link>

      {items.map((item, index) => {
        const isLast = index === items.length - 1

        return (
          <div key={item.href} className="flex items-center gap-2">
            <ChevronRight className="w-4 h-4 text-muted-foreground" />
            {isLast ? (
              <span className="font-medium text-foreground">{item.label}</span>
            ) : (
              <Link
                href={item.href}
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                {item.label}
              </Link>
            )}
          </div>
        )
      })}
    </nav>
  )
}
