import './globals.css';
import type { Metadata } from 'next';
import localFont from 'next/font/local';
import { Noto_Sans_JP } from 'next/font/google';

const pretendard = localFont({
  src: 'fonts/PretendardVariable.woff2',
  variable: '--font-pretendard',
});

const notoSansJP = Noto_Sans_JP({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
  variable: '--font-notoSansJP',
});

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
    <html lang="ko" className={`${pretendard.variable} ${notoSansJP.variable}`}>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                const locale = navigator.language.toLowerCase();
                const root = document.documentElement;
                if (locale.startsWith('ja')) {
                  root.style.setProperty('--font-family', 'var(--font-notoSansJP)');
                } else {
                  root.style.setProperty('--font-family', 'var(--font-pretendard)');
                }
              })();
            `,
          }}
        />
      </head>
      <body>
        {children}
      </body>
    </html>
  );
} 