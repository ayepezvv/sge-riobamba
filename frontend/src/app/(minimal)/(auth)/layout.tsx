import { ReactNode } from 'react';

// project imports
import MinimalLayout from 'layout/MinimalLayout';
import GuestGuard from 'utils/route-guard/GuestGuard';

// ================================|| SIMPLE LAYOUT ||================================ //

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <GuestGuard>
      <MinimalLayout>{children}</MinimalLayout>
    </GuestGuard>
  );
}
