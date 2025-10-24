/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'img.youtube.com',
      },
      {
        protocol: 'https',
        hostname: 'i.ytimg.com',
      },
    ],
  },
  // Configuration pour servir les fichiers statiques depuis src/public
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@/public': require('path').join(__dirname, 'src/public'),
    }
    return config
  },
}

module.exports = nextConfig
