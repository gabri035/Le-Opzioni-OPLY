import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "OPLY - Options & Pairs Trading Platform",
  description: "Advanced financial analysis platform for options strategies and pairs trading",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-50 min-h-screen">
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold text-purple-600">OPLY</h1>
              </div>
              <div className="flex items-center space-x-8">
                <Link href="/" className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">
                  Home
                </Link>
                <Link href="/pairs-trading" className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">
                  Pairs Trading
                </Link>
                <Link href="/option-chain" className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">
                  Option Chain
                </Link>
                <Link href="/strategy-builder" className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">
                  Strategy Builder
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <main>
          {children}
        </main>
      </body>
    </html>
  );
}
