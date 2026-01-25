import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'Phase 2 Full Stack Web Application - Todo App',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        <main className="container mx-auto px-4 py-8 max-w-4xl">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Todo App</h1>
          {children}
        </main>
      </body>
    </html>
  );
}
