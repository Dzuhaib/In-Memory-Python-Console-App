import Link from 'next/link';

export function CTASection() {
  return (
    <section className="py-20 px-6">
      <div className="max-w-3xl mx-auto text-center">
        <h2 className="text-3xl font-bold text-gray-900">
          Ready to take control of your tasks?
        </h2>
        <p className="mt-4 text-gray-600">
          Join ClawList today and experience task management powered by AI.
          No credit card required.
        </p>
        <div className="mt-8">
          <Link
            href="/register"
            className="inline-block bg-gray-900 text-white px-8 py-3 rounded-lg text-base font-medium hover:bg-gray-800 transition-colors shadow-lg shadow-gray-900/20"
          >
            Get Started Free
          </Link>
        </div>
      </div>
    </section>
  );
}
