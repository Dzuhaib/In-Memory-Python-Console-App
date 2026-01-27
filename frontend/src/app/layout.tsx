import type { Metadata } from 'next';
import './globals.css';
import { ClientProviders } from '@/components/ClientProviders';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'AI-Powered Todo App with Natural Language Interface',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <ClientProviders>
          <main className="container mx-auto px-4 py-8 max-w-4xl">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
            </div>
            {children}
          </main>
        </ClientProviders>
      </body>
    </html>
  );
}
