import { createClient } from 'redis'

/**
 * Client Redis global (singleton pattern)
 */
let redisClient: ReturnType<typeof createClient> | null = null
let connectionAttempted = false
let isRedisAvailable = false

/**
 * Obtenir ou créer le client Redis
 */
export async function getRedisClient() {
  // Si on a déjà essayé et ça a échoué, ne pas réessayer
  if (connectionAttempted && !isRedisAvailable) {
    throw new Error('Redis is not available')
  }

  if (!redisClient && !connectionAttempted) {
    connectionAttempted = true

    try {
      // Vérifier que REDIS_URL est configuré
      if (!process.env.REDIS_URL) {
        console.warn('⚠️ REDIS_URL not configured - running in degraded mode')
        isRedisAvailable = false
        throw new Error('REDIS_URL not configured')
      }

      // Créer le client Redis avec options pour désactiver la reconnexion automatique
      redisClient = createClient({
        socket: {
          reconnectStrategy: false, // Pas de reconnexion automatique
        }
      })

      // Supprimer les listeners d'erreur par défaut pour éviter les logs intempestifs
      redisClient.on('error', () => {
        // Silencieux - on gère les erreurs dans le catch
      })

      // Connecter avec timeout court
      await Promise.race([
        redisClient.connect(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Redis connection timeout')), 3000)
        )
      ])

      isRedisAvailable = true
      console.log('✓ Redis connected successfully')
    } catch (error) {
      console.warn('⚠️ Redis not available - running in degraded mode:', error instanceof Error ? error.message : error)
      isRedisAvailable = false

      // Nettoyer le client échoué
      if (redisClient) {
        try {
          await redisClient.quit()
        } catch (e) {
          // Ignorer les erreurs de quit
        }
        redisClient = null
      }

      throw error
    }
  }

  if (!isRedisAvailable) {
    throw new Error('Redis is not available')
  }

  return redisClient!
}

/**
 * Fermer la connexion Redis (utile pour cleanup)
 */
export async function closeRedisClient() {
  if (redisClient) {
    await redisClient.quit()
    redisClient = null
  }
}
