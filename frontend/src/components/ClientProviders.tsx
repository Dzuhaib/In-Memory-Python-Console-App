'use client';

import { ChatWidget } from './ChatWidget';

export function ClientProviders({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
