import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// 지원하는 언어 목록
const SUPPORTED_LOCALES = ['ko', 'ja']
const DEFAULT_LOCALE = 'ko'

export function middleware(request: NextRequest) {
  // 브라우저의 선호 언어 가져오기
  const acceptLanguage = request.headers.get('accept-language')
  let locale = DEFAULT_LOCALE

  if (acceptLanguage) {
    // 브라우저의 선호 언어 목록에서 첫 번째 지원되는 언어 찾기
    const preferredLocale = acceptLanguage
      .split(',')
      .map(lang => lang.split(';')[0].trim().toLowerCase())
      .find(lang => SUPPORTED_LOCALES.includes(lang))

    if (preferredLocale) {
      locale = preferredLocale
    }
  }

  // 응답 헤더에 언어 설정
  const response = NextResponse.next()
  response.headers.set('x-locale', locale)
  
  return response
}

// 미들웨어가 실행될 경로 설정
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
} 