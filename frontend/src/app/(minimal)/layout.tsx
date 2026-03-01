import { ReactNode } from 'react';

// project imports
import MinimalLayout from 'layout/MinimalLayout';

// ================================|| SIMPLE LAYOUT ||================================ //

export default function Layout({ children }: { children: ReactNode }) {
  return <MinimalLayout>{children}</MinimalLayout>;
}
