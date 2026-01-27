import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Page Not Found</h2>
      <p className="text-gray-600 mb-4">The page you are looking for does not exist.</p>
      <Link href="/" className="text-blue-600 hover:text-blue-800 underline">
        Go back to Tasks
      </Link>
    </div>
  );
}
