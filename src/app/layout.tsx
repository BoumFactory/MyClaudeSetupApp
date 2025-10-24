import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";
import { MainNav } from "@/components/layout/MainNav";
import { Footer } from "@/components/layout/Footer";
import { MathBackground } from "@/components/background/MathBackground";
import { BackgroundAnimationProvider } from "@/contexts/BackgroundAnimationContext";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
});

export const metadata: Metadata = {
  title: {
    default: "IA & Enseignement des Mathématiques",
    template: "%s | IA & Enseignement",
  },
  description:
    "Plateforme de partage de connaissances sur l'intelligence artificielle au service des enseignants de mathématiques. Découvrez Claude Code, des présentations interactives et des ressources pédagogiques.",
  keywords: [
    "IA",
    "intelligence artificielle",
    "enseignement",
    "mathématiques",
    "Claude Code",
    "pédagogie",
    "éducation",
  ],
  authors: [{ name: "Enseignant de mathématiques" }],
  creator: "Enseignant de mathématiques",
  openGraph: {
    type: "website",
    locale: "fr_FR",
    title: "IA & Enseignement des Mathématiques",
    description:
      "Plateforme de partage de connaissances sur l'IA au service des enseignants de mathématiques",
    siteName: "IA & Enseignement",
  },
  twitter: {
    card: "summary_large_image",
    title: "IA & Enseignement des Mathématiques",
    description:
      "Plateforme de partage de connaissances sur l'IA au service des enseignants de mathématiques",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className="dark">
      <body
        className={`${inter.variable} ${spaceGrotesk.variable} font-sans antialiased`}
      >
        <BackgroundAnimationProvider>
          <div className="relative min-h-screen math-bg">
            <MathBackground />
            <div className="relative z-10">
              <MainNav />
              <main className="container mx-auto px-4 py-8">
                {children}
              </main>
              <Footer />
            </div>
          </div>
        </BackgroundAnimationProvider>
      </body>
    </html>
  );
}
