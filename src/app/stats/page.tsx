import { Metadata } from "next"
import { BarChart3, TrendingUp, Download, Eye, Activity } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export const metadata: Metadata = {
  title: "Statistiques d'Utilisation",
  description: "Consultez les statistiques publiques d'utilisation du site : téléchargements, vues de présentations et ressources populaires.",
}

/**
 * Page de statistiques publiques
 */
export default async function StatsPage() {
  // Fetch les données côté serveur
  let analyticsData = null
  let rateLimitData = null
  let error = null

  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'
    const response = await fetch(`${baseUrl}/api/analytics`, {
      cache: 'no-store', // Ne pas mettre en cache pour avoir des stats à jour
    })

    if (response.ok) {
      const data = await response.json()
      analyticsData = data.analytics
      rateLimitData = data.rateLimit
    } else {
      error = 'Impossible de récupérer les statistiques'
    }
  } catch (err) {
    console.error('Erreur lors du fetch des stats:', err)
    error = 'Erreur serveur'
  }

  // Fonction helper pour obtenir l'icône par type d'événement
  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'download':
        return Download
      case 'view_presentation':
      case 'view_tutorial':
        return Eye
      default:
        return Activity
    }
  }

  // Fonction helper pour formater les labels
  const formatEventType = (eventType: string): string => {
    const labels: Record<string, string> = {
      download: 'Téléchargements',
      view_presentation: 'Vues Présentations',
      view_tutorial: 'Vues Tutoriels',
      page_view: 'Pages vues',
    }
    return labels[eventType] || eventType
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* En-tête */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold glow-text mb-2 flex items-center gap-3">
          <BarChart3 className="w-10 h-10" />
          Statistiques d'Utilisation
        </h1>
        <p className="text-muted-foreground">
          Consultez les statistiques publiques d'utilisation du site
        </p>
      </div>

      {error ? (
        <Card className="glass-card border-red-500/50">
          <CardContent className="pt-6">
            <p className="text-red-400">{error}</p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-6">
          {/* Stats globales */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="glass-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <Activity className="w-4 h-4" />
                  Total Événements
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold glow-text">
                  {analyticsData?.totalEvents || 0}
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <Download className="w-4 h-4" />
                  Téléchargements
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-cosmic-400">
                  {analyticsData?.eventsByType?.download || 0}
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <TrendingUp className="w-4 h-4" />
                  IPs Aujourd'hui
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-400">
                  {rateLimitData?.dailyNewIPs || 0}
                  <span className="text-sm text-muted-foreground ml-2">
                    / {rateLimitData?.maxDailyNewIPs || 20}
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-card">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                  <Download className="w-4 h-4" />
                  DL Aujourd'hui
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-purple-400">
                  {rateLimitData?.totalDownloadsToday || 0}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Événements par type */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-cosmic-400" />
                Événements par Type
              </CardTitle>
              <CardDescription>Répartition des différents types d'événements</CardDescription>
            </CardHeader>
            <CardContent>
              {analyticsData?.eventsByType &&
              Object.keys(analyticsData.eventsByType).length > 0 ? (
                <div className="space-y-3">
                  {Object.entries(analyticsData.eventsByType).map(([type, count]) => {
                    const Icon = getEventIcon(type)
                    const percentage =
                      analyticsData.totalEvents > 0
                        ? ((count as number) / analyticsData.totalEvents) * 100
                        : 0

                    return (
                      <div key={type} className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span className="flex items-center gap-2">
                            <Icon className="w-4 h-4 text-cosmic-400" />
                            {formatEventType(type)}
                          </span>
                          <span className="font-medium">{count as number}</span>
                        </div>
                        <div className="w-full bg-cosmic-900/30 rounded-full h-2 overflow-hidden">
                          <div
                            className="h-full cosmic-gradient rounded-full transition-all duration-500"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <p className="text-muted-foreground text-center py-8">
                  Aucune donnée disponible
                </p>
              )}
            </CardContent>
          </Card>

          {/* Évolution quotidienne */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-cosmic-400" />
                Évolution Quotidienne
              </CardTitle>
              <CardDescription>Nombre d'événements par jour (30 derniers jours)</CardDescription>
            </CardHeader>
            <CardContent>
              {analyticsData?.dailyStats && analyticsData.dailyStats.length > 0 ? (
                <div className="space-y-2">
                  {analyticsData.dailyStats.map((stat: { date: string; count: number }) => {
                    const maxCount = Math.max(
                      ...analyticsData.dailyStats.map((s: any) => s.count)
                    )
                    const percentage = maxCount > 0 ? (stat.count / maxCount) * 100 : 0

                    return (
                      <div key={stat.date} className="flex items-center gap-3">
                        <span className="text-xs text-muted-foreground w-24 flex-shrink-0">
                          {new Date(stat.date).toLocaleDateString('fr-FR', {
                            day: '2-digit',
                            month: 'short',
                          })}
                        </span>
                        <div className="flex-1 bg-cosmic-900/30 rounded-full h-6 overflow-hidden">
                          <div
                            className="h-full cosmic-gradient rounded-full transition-all duration-500 flex items-center justify-end px-2"
                            style={{ width: `${percentage}%` }}
                          >
                            {stat.count > 0 && (
                              <span className="text-xs font-medium text-white">
                                {stat.count}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <p className="text-muted-foreground text-center py-8">
                  Aucune donnée disponible
                </p>
              )}
            </CardContent>
          </Card>

          {/* Ressources les plus populaires */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="w-5 h-5 text-cosmic-400" />
                Ressources les Plus Populaires
              </CardTitle>
              <CardDescription>Top 10 des ressources les plus consultées</CardDescription>
            </CardHeader>
            <CardContent>
              {analyticsData?.topResources && analyticsData.topResources.length > 0 ? (
                <div className="space-y-3">
                  {analyticsData.topResources
                    .slice(0, 10)
                    .map(
                      (
                        resource: { resource: string; count: number; type: string },
                        index: number
                      ) => {
                        const Icon = getEventIcon(resource.type)
                        return (
                          <div
                            key={`${resource.resource}-${index}`}
                            className="flex items-center gap-3 p-3 rounded-lg bg-cosmic-900/20 hover:bg-cosmic-900/40 transition-colors"
                          >
                            <div className="flex items-center justify-center w-8 h-8 rounded-full cosmic-gradient text-white font-bold text-sm">
                              {index + 1}
                            </div>
                            <Icon className="w-4 h-4 text-cosmic-400 flex-shrink-0" />
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium truncate">{resource.resource}</p>
                              <p className="text-xs text-muted-foreground">
                                {formatEventType(resource.type)}
                              </p>
                            </div>
                            <div className="text-sm font-bold text-cosmic-400 flex-shrink-0">
                              {resource.count}
                            </div>
                          </div>
                        )
                      }
                    )}
                </div>
              ) : (
                <p className="text-muted-foreground text-center py-8">
                  Aucune donnée disponible
                </p>
              )}
            </CardContent>
          </Card>

          {/* Détails Rate Limiting */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-cosmic-400" />
                Détails Rate Limiting (Aujourd'hui)
              </CardTitle>
              <CardDescription>Téléchargements par IP (anonymisées)</CardDescription>
            </CardHeader>
            <CardContent>
              {rateLimitData?.ipDownloads && rateLimitData.ipDownloads.length > 0 ? (
                <div className="space-y-2">
                  {rateLimitData.ipDownloads.map(
                    (item: { ip: string; count: number }, index: number) => (
                      <div
                        key={`${item.ip}-${index}`}
                        className="flex items-center justify-between p-2 rounded-lg bg-cosmic-900/20"
                      >
                        <span className="text-sm font-mono text-muted-foreground">
                          {item.ip}
                        </span>
                        <span className="text-sm font-medium">{item.count} téléchargement(s)</span>
                      </div>
                    )
                  )}
                </div>
              ) : (
                <p className="text-muted-foreground text-center py-8">
                  Aucun téléchargement aujourd'hui
                </p>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
