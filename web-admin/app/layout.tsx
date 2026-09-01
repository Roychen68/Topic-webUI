import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL ?? 'http://localhost:3000',
  ),
  title: 'Concentrate｜AI 管家控制中心',
  description: '不是提醒你，而是逼你專心。整合 Discord Bot 的任務排程、強制介入、效率追蹤與 AI routine 建議。',
  icons: { icon: '/favicon.svg' },
  openGraph: {
    title: 'Concentrate｜不是提醒你，而是逼你專心',
    description: 'AI 管家控制中心：主動介入分心行為，讓專注成為可追蹤的日常。',
    type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: 'Concentrate AI 管家控制中心' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Concentrate｜不是提醒你，而是逼你專心',
    description: 'AI 管家控制中心：主動介入分心行為，讓專注成為可追蹤的日常。',
    images: ['/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
