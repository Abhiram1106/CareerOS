import "./globals.css";
import type { Metadata } from "next";
import { MotionProvider } from "../components/motion-provider";

export const metadata: Metadata = {
  title: "CareerOS Campus AI — Placement readiness",
  description:
    "Intel-optimized placement-readiness operating layer for Indian colleges. ATS-safe resumes, JD matching, and proof-linked scoring.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Manrope:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <div className="app-root">
          <MotionProvider>{children}</MotionProvider>
        </div>
      </body>
    </html>
  );
}
