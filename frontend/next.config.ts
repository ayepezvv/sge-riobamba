import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // TODO YXP-42: ignoreBuildErrors debe eliminarse antes de producción.
  // Errores pendientes (tsc --noEmit): 344 total
  //   - 235 × TS2769: props `item`/`xs`/`md` de Grid v5 incompatibles con MUI v6 (migración pendiente)
  //   - 66  × TS6133: importaciones sin usar
  //   - 43  × otros (TS2304, TS2322, TS2339, etc.)
  // Seguimiento: YXP-55 (migración Grid MUI v5→v6)
  typescript: {
    ignoreBuildErrors: true,
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
