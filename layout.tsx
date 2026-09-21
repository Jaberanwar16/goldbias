import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Gold & Dollar Bias - Analyse Macroeconomique',
  description: "Analyse en temps reel du sentiment entre l'Or (XAUUSD) et le Dollar (DXY)",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
