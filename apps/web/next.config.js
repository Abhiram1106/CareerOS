/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disabled in dev — Strict Mode double-invokes renders and effects which
  // doubles CPU work per page visit. Re-enable before production builds.
  reactStrictMode: false,

  experimental: {
    // Turbopack: 3-5x faster dev compilation vs webpack
    turbo: {},
  },

  // Disable x-powered-by header (tiny perf/security win)
  poweredByHeader: false,

  // Compress responses
  compress: true,
};

module.exports = nextConfig;
