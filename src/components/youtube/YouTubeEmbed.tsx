interface YouTubeEmbedProps {
  videoId: string
  title: string
  autoplay?: boolean
}

/**
 * Composant d'intégration YouTube
 */
export function YouTubeEmbed({ videoId, title, autoplay = false }: YouTubeEmbedProps) {
  const embedUrl = `https://www.youtube.com/embed/${videoId}${autoplay ? '?autoplay=1' : ''}`

  return (
    <div className="relative w-full aspect-video">
      <iframe
        src={embedUrl}
        title={title}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        className="absolute inset-0 w-full h-full rounded-t-xl"
      />
    </div>
  )
}
