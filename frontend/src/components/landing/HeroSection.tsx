import Link from 'next/link';

export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-mesh-light">
      {/* Decorative orbs */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-200/30 rounded-full blur-3xl -translate-y-1/2 translate-x-1/4" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-violet-200/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/4" />

      <div className="relative max-w-7xl mx-auto px-6 py-24 sm:py-32 lg:py-40">
        <div className="max-w-3xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-50 border border-indigo-100 mb-8 animate-fade-in">
            <div className="w-2 h-2 bg-indigo-500 rounded-full animate-pulse" />
            <span className="text-sm font-medium text-indigo-700">AI-Powered Task Management</span>
          </div>

          {/* Heading */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 tracking-tight leading-[1.1] animate-slide-up">
            Manage tasks with
            <br />
            <span className="text-gradient">superhuman clarity</span>
          </h1>

          {/* Subheading */}
          <p className="mt-8 text-lg sm:text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed animate-slide-up delay-200" style={{ animationFillMode: 'both' }}>
            ClawList combines intelligent task management with an AI chatbot that understands
            your workflow. Prioritize, organize, and accomplish more every day.
          </p>

          {/* CTA buttons */}
          <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up delay-300" style={{ animationFillMode: 'both' }}>
            <Link
              href="/login"
              className="w-full sm:w-auto bg-gradient-to-r from-indigo-600 to-violet-600 text-white px-8 py-3.5 rounded-xl text-base font-semibold
                         shadow-xl shadow-indigo-500/25 hover:shadow-2xl hover:shadow-indigo-500/30
                         hover:from-indigo-500 hover:to-violet-500
                         active:scale-[0.98] transition-all duration-200"
            >
              Start Free Today
            </Link>
            <Link
              href="#features"
              className="w-full sm:w-auto text-gray-600 px-8 py-3.5 rounded-xl text-base font-semibold
                         border border-gray-200 hover:border-gray-300 hover:bg-gray-50
                         active:scale-[0.98] transition-all duration-200
                         flex items-center justify-center gap-2"
            >
              See Features
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" />
              </svg>
            </Link>
          </div>

          {/* Social proof */}
          <div className="mt-16 animate-slide-up delay-400" style={{ animationFillMode: 'both' }}>
            <div className="flex items-center justify-center gap-6 flex-wrap">
              <div className="flex -space-x-2">
                {['from-blue-400 to-cyan-400', 'from-violet-400 to-purple-400', 'from-rose-400 to-pink-400', 'from-amber-400 to-orange-400', 'from-emerald-400 to-teal-400'].map((gradient, i) => (
                  <div
                    key={i}
                    className={`w-8 h-8 rounded-full bg-gradient-to-br ${gradient} border-2 border-white flex items-center justify-center`}
                  >
                    <span className="text-[10px] text-white font-bold">
                      {['AK', 'SJ', 'MR', 'LP', 'CT'][i]}
                    </span>
                  </div>
                ))}
              </div>
              <div className="flex items-center gap-1.5">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 text-amber-400 fill-current" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <span className="text-sm text-gray-500 font-medium">Loved by 10,000+ users</span>
              </div>
            </div>
          </div>
        </div>

        {/* Dashboard preview mockup */}
        <div className="mt-20 max-w-5xl mx-auto animate-slide-up delay-500" style={{ animationFillMode: 'both' }}>
          <div className="relative rounded-2xl overflow-hidden border border-gray-200/80 shadow-2xl shadow-gray-900/10 bg-white">
            {/* Browser chrome */}
            <div className="flex items-center gap-2 px-4 py-3 bg-gray-50 border-b border-gray-100">
              <div className="flex gap-1.5">
                <div className="w-3 h-3 rounded-full bg-red-400" />
                <div className="w-3 h-3 rounded-full bg-amber-400" />
                <div className="w-3 h-3 rounded-full bg-emerald-400" />
              </div>
              <div className="flex-1 flex justify-center">
                <div className="px-4 py-1 bg-white rounded-lg border border-gray-200 text-xs text-gray-400 font-mono">
                  app.clawlist.com/dashboard
                </div>
              </div>
            </div>

            {/* Mockup content */}
            <div className="p-6 sm:p-8">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
                {[
                  { label: 'Total Tasks', value: '128', color: 'from-blue-500 to-indigo-500' },
                  { label: 'Completed', value: '94', color: 'from-emerald-500 to-teal-500' },
                  { label: 'In Progress', value: '27', color: 'from-amber-500 to-orange-500' },
                  { label: 'Overdue', value: '7', color: 'from-red-500 to-rose-500' },
                ].map((stat) => (
                  <div key={stat.label} className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                    <p className="text-xs text-gray-400 font-medium">{stat.label}</p>
                    <p className={`text-2xl font-bold mt-1 text-transparent bg-clip-text bg-gradient-to-r ${stat.color}`}>
                      {stat.value}
                    </p>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                {[
                  { title: 'Finalize Q4 report', priority: 'high', done: false },
                  { title: 'Review design mockups', priority: 'medium', done: true },
                  { title: 'Team standup notes', priority: 'low', done: false },
                ].map((task) => (
                  <div key={task.title} className="flex items-center gap-3 p-3 rounded-xl bg-gray-50/50 border border-gray-100">
                    <div className={`w-5 h-5 rounded-md border-2 flex items-center justify-center ${task.done ? 'bg-indigo-500 border-indigo-500' : 'border-gray-300'}`}>
                      {task.done && (
                        <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                        </svg>
                      )}
                    </div>
                    <span className={`text-sm flex-1 ${task.done ? 'text-gray-400 line-through' : 'text-gray-700 font-medium'}`}>
                      {task.title}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium priority-${task.priority}`}>
                      {task.priority}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
