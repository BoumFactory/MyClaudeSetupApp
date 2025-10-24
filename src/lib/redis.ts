import { createClient } from 'redis'

/**
 * Client Redis global (singleton pattern)
 */
let redisClient: ReturnType<typeof createClient> | null = null

/**
 * Obtenir ou créer le client Redis
 */
export async function getRedisClient() {
  if (!redisClient) {
    // Créer le client Redis avec la connection string de l'environnement
    redisClient = createClient({
      url: process.env.REDIS_URL || process.env.KV_URL,
    })

    // Gérer les erreurs
    redisClient.on('error', (err) => {
      console.error('Redis Client Error:', err)
    })

    // Connecter
    await redisClient.connect()
  }

  return redisClient
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
