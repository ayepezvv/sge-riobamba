import { ReactNode } from 'react';

// next
import type { Metadata } from 'next';

import './../scss/style.scss';

// project imports
import ProviderWrapper from 'store/ProviderWrapper';

export const metadata: Metadata = {
  title: 'SGE — Sistema de Gestión Empresarial · EP Riobamba',
  description: 'Sistema de Gestión Empresarial de la Empresa Pública EP Riobamba.'
};

// ==============================|| ROOT LAYOUT ||============================== //

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es" suppressHydrationWarning>
      <head></head>
      <body>
        <ProviderWrapper>{children}</ProviderWrapper>
      </body>
    </html>
  );
}
