'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';

export function Header() {
  const { data: session, isPending } = authClient.useSession();
  const router = useRouter();

  const handleLogout = async () => {
    await authClient.signOut();
    router.push('/');
    router.refresh();
  };

  return (
    <header className="sticky top-0 z-50 glass border-b border-gray-200/50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-lg flex items-center justify-center shadow-md shadow-indigo-500/20">
            <span className="text-white text-sm font-bold">C</span>
          </div>
          <span className="text-lg font-bold text-gray-900 tracking-tight">ClawList</span>
        </Link>

        <nav className="flex items-center gap-3">
          {isPending ? (
            <div className="w-20 h-9 bg-gray-100 animate-pulse rounded-lg" />
          ) : session ? (
            <>
              <span className="text-sm text-gray-500 hidden sm:inline mr-1">
                {session.user.email}
              </span>
              <Link
                href="/app"
                className="text-sm font-medium text-gray-600 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100 transition-all duration-200"
              >
                Dashboard
              </Link>
              <button
                onClick={handleLogout}
                className="text-sm font-medium text-gray-400 hover:text-red-600 px-3 py-2 rounded-lg hover:bg-red-50 transition-all duration-200"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-sm font-medium text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg hover:bg-gray-100 transition-all duration-200"
              >
                Sign In
              </Link>
              <Link
                href="/login"
                className="text-sm font-semibold bg-gradient-to-r from-indigo-600 to-violet-600 text-white px-5 py-2.5 rounded-xl
                           shadow-lg shadow-indigo-500/25 hover:shadow-xl hover:shadow-indigo-500/30
                           hover:from-indigo-500 hover:to-violet-500
                           active:scale-[0.98] transition-all duration-200"
              >
                Get Started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
