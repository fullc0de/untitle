import './globals.css';
import type { Metadata } from 'next';
import localFont from 'next/font/local';
import { Noto_Sans_JP } from 'next/font/google';
import { headers } from 'next/headers';

const pretendard = localFont({
  src: 'fonts/PretendardVariable.woff2',
  variable: '--font-pretendard',
  display: 'swap',
});

const notoSansJP = Noto_Sans_JP({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
  variable: '--font-notoSansJP',
  display: 'swap',
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
  // 미들웨어에서 설정한 언어 가져오기
  const headersList = headers();
  const locale = headersList.get('x-locale') || 'ko';

  return (
    <html lang={locale} className={`${pretendard.variable} ${notoSansJP.variable}`}>
      <body className="font-sans [&:lang(ja)]:font-notoSansJP">
        {children}
      </body>
    </html>
  );
} 