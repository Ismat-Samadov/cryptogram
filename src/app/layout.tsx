import type { Metadata, Viewport } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Cryptogram — Crack the Cipher',
  description:
    'A neon-styled browser puzzle game. Decrypt hidden quotes by cracking substitution ciphers. Three difficulty levels, hints, scoring, and high scores.',
  keywords: ['cryptogram', 'cipher', 'puzzle', 'word game', 'brain teaser'],
  openGraph: {
    title: 'Cryptogram — Crack the Cipher',
    description: 'Decode encrypted quotes by cracking substitution ciphers.',
    type: 'website',
  },
};

export const viewport: Viewport = {
  themeColor: '#020818',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1, // prevent zoom on input focus on iOS
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className="antialiased">{children}</body>
    </html>
  );
}
