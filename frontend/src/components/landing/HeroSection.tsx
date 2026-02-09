import Link from 'next/link';

export function HeroSection() {
  return (
    <section className="py-24 px-6">
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 tracking-tight leading-tight">
          Manage your tasks
          <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
            with intelligence
          </span>
        </h1>
        <p className="mt-6 text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
          ClawList combines smart task management with an AI-powered chatbot
          to help you organize, prioritize, and accomplish more every day.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Link
            href="/register"
            className="bg-gray-900 text-white px-8 py-3 rounded-lg text-base font-medium hover:bg-gray-800 transition-colors shadow-lg shadow-gray-900/20"
          >
            Get Started Free
          </Link>
          <Link
            href="/login"
            className="text-gray-700 px-8 py-3 rounded-lg text-base font-medium hover:text-gray-900 transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </section>
  );
}
