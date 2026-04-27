import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  typescript: {
    ignoreBuildErrors: false,
  },
  // BC-05 resuelto: todos los usos de react-apexcharts ya usan dynamic({ ssr: false }),
  // que neutraliza el bug de double-mount en StrictMode.
  reactStrictMode: true,
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
