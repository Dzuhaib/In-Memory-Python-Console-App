/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    serverComponentsExternalPackages: ['better-auth', '@neondatabase/serverless'],
  },
}

module.exports = nextConfig
