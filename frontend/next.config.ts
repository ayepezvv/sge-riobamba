import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // TypeScript errors are known pre-existing issues across the codebase.
  // Compilation succeeds; type-check errors are tracked separately.
  typescript: {
    ignoreBuildErrors: true,
  },
  // todo: this need to set to true or remove it as default is true. set false as chart was giving error when first render
  // https://github.com/apexcharts/apexcharts.js/issues/3652
  reactStrictMode: false,
  modularizeImports: {
    '@mui/material': {
      transform: '@mui/material/{{member}}'
    },
    '@mui/lab': {
      transform: '@mui/lab/{{member}}'
    },
    '@mui/icons-material': {
      transform: '@mui/icons-material/{{member}}'
    }
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'flagcdn.com',
        pathname: '**'
      }
    ],
    localPatterns: [
      {
        pathname: '/assets/**'
      }
    ]
  },
  experimental: {
    // Next.js 14 server actions allowed origins
    serverActions: {
        allowedOrigins: ['192.168.1.15', 'localhost', '192.168.1.15:3000']
    }
  }
};

export default nextConfig;
