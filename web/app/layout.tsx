import { Providers } from "@/components/providers";
import { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Input Demo",
  description: "Demo with theme switching and AI input",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background transition-colors duration-300">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}