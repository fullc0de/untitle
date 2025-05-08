import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '애플리케이션',
  description: 'Next.js와 Tailwind CSS로 만든 애플리케이션',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        {children}
      </body>
    </html>
  );
} 