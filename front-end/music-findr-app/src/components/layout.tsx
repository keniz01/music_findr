import React from "react";

interface LayoutProps {
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ title, children, footer }) => {
  return (
    <div className="min-h-screen flex flex-col bg-gray-100 text-gray-900">
      <header className="bg-white shadow p-4">
        <h1 className="text-2xl font-bold">{title}</h1>
      </header>
      <main className="flex-grow p-6">{children}</main>
      <footer className="bg-white border-t p-4 text-sm text-center text-gray-500">
        {footer ?? "Music Findr © 2025. All rights reserved."}
      </footer>
    </div>
  );
};

export default Layout;
