import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LLM Benchmark Dashboard",
  description: "Visualize and compare LLM benchmark results",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 antialiased">
        <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-14">
              <a href="/" className="text-lg font-bold text-gray-900">
                🏆 LLM Benchmark
              </a>
              <div className="flex gap-6">
                <a
                  href="/"
                  className="text-sm font-medium text-gray-600 hover:text-gray-900"
                >
                  Runs
                </a>
                <a
                  href="/compare"
                  className="text-sm font-medium text-gray-600 hover:text-gray-900"
                >
                  Compare
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
      </body>
    </html>
  );
}
