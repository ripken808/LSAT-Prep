import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono, Press_Start_2P, Fredoka } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Pixel display font - headings and large stat numbers ONLY (illegible at
// small sizes). Never used for nav/buttons/badges or the reading screen.
const pixelDisplay = Press_Start_2P({
  variable: "--font-pixel-display",
  weight: "400",
  subsets: ["latin"],
});

// Legible rounded sans for chunky UI chrome - nav links, button labels,
// badge text. Carries the playful pixel-chunky identity via panels/borders/
// palette instead of an illegible font at small sizes.
const chromeSans = Fredoka({
  variable: "--font-chrome-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "LSAT Prep",
  description: "Generate, take, and grade LSAT Logical Reasoning questions",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} ${pixelDisplay.variable} ${chromeSans.variable}`}
    >
      <body>
        <nav className="app-nav">
          <Link href="/" className="app-nav-link">Practice</Link>
          <Link href="/reading-comp" className="app-nav-link">Reading Comp</Link>
          <Link href="/progress" className="app-nav-link">Progress</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
