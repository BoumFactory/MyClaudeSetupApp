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

      console.log('🔄 Attempting to connect to Redis...')
      console.log('📍 REDIS_URL format:', process.env.REDIS_URL?.substring(0, 20) + '...')

      // Créer le client Redis avec options pour désactiver la reconnexion automatique
      redisClient = createClient({
        socket: {
          reconnectStrategy: false, // Pas de reconnexion automatique
          connectTimeout: 10000, // 10 secondes
        }
      })

      // Logger les erreurs pour debug
      redisClient.on('error', (err) => {
        console.error('🔴 Redis connection error:', err.message)
      })

      // Connecter avec timeout
      console.log('⏳ Connecting to Redis...')
      await Promise.race([
        redisClient.connect(),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Redis connection timeout after 10s')), 10000)
        )
      ])

      isRedisAvailable = true
      console.log('✅ Redis connected successfully!')
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
