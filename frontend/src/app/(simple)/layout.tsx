import { ReactNode } from 'react';

// project imports
import SimpleLayout from 'layout/SimpleLayout';

// ================================|| SIMPLE LAYOUT ||================================ //

export default function Layout({ children }: { children: ReactNode }) {
  return <SimpleLayout>{children}</SimpleLayout>;
}
