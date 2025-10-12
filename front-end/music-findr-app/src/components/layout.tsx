import React from "react";

interface LayoutProps {
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ title, children, footer }) => {
  return (
    <div className="min-h-screen bg-[#f7f7f8] dark:bg-[#1e1e20] text-[#202123] dark:text-gray-200 font-sans flex flex-col px-4 sm:px-6 md:px-8 transition-colors duration-300">
      <div className="w-full max-w-full flex flex-col min-h-screen">
        {/* Header with responsive spacing */}
        {title && (
          <header className="py-4 sm:py-6 transition-all duration-300">
            <h1 className="text-left text-xl sm:text-2xl md:text-3xl font-semibold text-gray-800 dark:text-gray-100">
              {title}
            </h1>
          </header>
        )}

        {/* Main Content */}
        <main className="flex-grow py-4 sm:py-6">
          <div className="h-full max-w-none transition-colors duration-300">
            {children}
          </div>
        </main>

        {/* Footer */}
        <footer className="py-4 sm:py-6 text-center text-xs sm:text-sm text-gray-400 dark:text-gray-500 transition-all duration-300">
          {footer ?? "Music Findr © 2025. All rights reserved."}
        </footer>
      </div>
    </div>
  );
};

export default Layout;
