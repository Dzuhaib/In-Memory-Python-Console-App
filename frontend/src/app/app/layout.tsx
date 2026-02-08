'use client';

import { Header } from '@/components/Header';
import { ChatWidget } from '@/components/ChatWidget';

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-gray-900">ClawList</h1>
        </div>
        {children}
      </main>
      <ChatWidget />
    </div>
  );
}
