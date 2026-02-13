import Link from 'next/link';

export function CTASection() {
  return (
    <section className="py-24 px-6 bg-mesh-light">
      <div className="max-w-4xl mx-auto text-center">
        <div className="relative">
          {/* Decorative orbs */}
          <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-96 h-96 bg-indigo-200/20 rounded-full blur-3xl" />

          <div className="relative">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight">
              Ready to supercharge{' '}
              <span className="text-gradient">your productivity?</span>
            </h2>
            <p className="mt-4 text-lg text-gray-500 max-w-2xl mx-auto leading-relaxed">
              Join thousands of professionals who use ClawList to stay organized
              and accomplish more. Free to get started, no credit card required.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/login"
                className="w-full sm:w-auto bg-gradient-to-r from-indigo-600 to-violet-600 text-white px-8 py-3.5 rounded-xl text-base font-semibold
                           shadow-xl shadow-indigo-500/25 hover:shadow-2xl hover:shadow-indigo-500/30
                           hover:from-indigo-500 hover:to-violet-500
                           active:scale-[0.98] transition-all duration-200"
              >
                Get Started Free
              </Link>
              <p className="text-sm text-gray-400">
                No credit card required
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
