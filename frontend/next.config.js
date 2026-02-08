/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverComponentsExternalPackages: ['better-auth', '@neondatabase/serverless', 'drizzle-orm'],
  },
}

module.exports = nextConfig
