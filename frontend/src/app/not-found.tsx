import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <Link href="/" className="text-2xl font-bold text-gray-900 tracking-tight mb-8">
        ClawList
      </Link>
      <h2 className="text-4xl font-bold text-gray-900 mb-4">404</h2>
      <p className="text-gray-600 mb-6">The page you are looking for does not exist.</p>
      <Link
        href="/"
        className="bg-gray-900 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
      >
        Back to Home
      </Link>
    </div>
  );
}
