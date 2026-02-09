import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ClawList — Smart Todo Management',
  description: 'AI-Powered Todo App with Natural Language Interface',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 antialiased">
        {children}
      </body>
    </html>
  );
}
