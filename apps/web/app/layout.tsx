import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CareerOS Platform",
  description: "CareerOS full-stack application",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
