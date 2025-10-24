import Link from "next/link"
import { ArrowRight } from "lucide-react"
import { Scope } from "@/types"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface ScopeCardProps {
  scope: Scope
}

/**
 * Carte de présentation d'un scope
 */
export function ScopeCard({ scope }: ScopeCardProps) {
  return (
    <Link href={scope.path} className="block">
      <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full">
        <CardHeader>
          <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${scope.gradient} flex items-center justify-center mb-3`}>
            <div className="text-2xl">📚</div>
          </div>
          <CardTitle className="group-hover:text-cosmic-400 transition-colors">{scope.title}</CardTitle>
          <CardDescription>{scope.description}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between text-muted-foreground group-hover:text-cosmic-400 transition-colors">
            <span className="font-medium">Explorer</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
