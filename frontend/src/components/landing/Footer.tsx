export function Footer() {
  return (
    <footer className="py-8 px-6 border-t border-gray-100">
      <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-sm text-gray-500">
          &copy; {new Date().getFullYear()} ClawList. All rights reserved.
        </div>
        <div className="flex items-center gap-6 text-sm text-gray-500">
          <a href="#" className="hover:text-gray-700 transition-colors">
            Privacy
          </a>
          <a href="#" className="hover:text-gray-700 transition-colors">
            Terms
          </a>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-700 transition-colors"
          >
            GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}
