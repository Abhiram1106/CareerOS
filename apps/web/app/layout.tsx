import "./globals.css";
import type { Metadata } from "next";
import { DM_Sans, Manrope, JetBrains_Mono } from "next/font/google";
import { MotionProvider } from "../components/motion-provider";
import { ToastProvider } from "../components/ui/toast";

// Self-hosted via next/font — zero Google Fonts network round-trip
const dmSans = DM_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  style: ["normal", "italic"],
  variable: "--loaded-dm-sans",
  display: "swap",
});

const manrope = Manrope({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--loaded-manrope",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["500"],
  variable: "--loaded-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "CareerOS Student AI — Placement readiness",
  description:
    "Intel-optimized placement-readiness operating layer for Indian students. ATS-safe resumes, JD matching, and proof-linked scoring.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${dmSans.variable} ${manrope.variable} ${jetbrainsMono.variable}`}
    >
      <body>
        <div className="app-root">
          <ToastProvider>
            <MotionProvider>{children}</MotionProvider>
          </ToastProvider>
        </div>
      </body>
    </html>
  );
}
