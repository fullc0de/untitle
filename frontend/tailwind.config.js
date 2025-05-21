/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // 고요한 밤 테마 색상
        'sn': {
          // 주요 색상 계열
          'primary': {
            DEFAULT: '#4A7CFF', // 기본 로열 블루
            50: '#EEF3FF',      // 가장 밝은 버전
            100: '#D6E4FF',
            200: '#ADC8FF',
            300: '#85ACFF',
            400: '#5C90FF',
            500: '#4A7CFF',     // 기본값
            600: '#3A63CC',
            700: '#2B4A99',
            800: '#1C3266',
            900: '#0D1933',
          },
          
          // 보조 색상 계열
          'secondary': {
            DEFAULT: '#B5A9D1', // 기본 라벤더
            50: '#F8F6FB',
            100: '#EDE9F7',
            200: '#DBD3EF',
            300: '#C9BEE7',
            400: '#B5A9D1',     // 기본값
            500: '#9D8FBF',
            600: '#8575AD',
            700: '#6D5F93',
            800: '#554A79',
            900: '#3C3560',
          },
          
          // 강조 색상 계열
          'accent': {
            DEFAULT: '#FF7DB8', // 기본 비비드 핑크
            50: '#FFF0F7',
            100: '#FFE0F0',
            200: '#FFC2E1',
            300: '#FFA3D2',
            400: '#FF7DB8',     // 기본값
            500: '#FF57A5',
            600: '#FF3092',
            700: '#FF0A7F',
            800: '#DB006C',
            900: '#B70059',
          },
          
          // 성장 인디케이터 계열
          'growth': {
            DEFAULT: '#00E5B0', // 기본 밝은 민트
            50: '#E6FEF8',
            100: '#CCFDF2',
            200: '#99FBE5',
            300: '#66F9D8',
            400: '#33F7CB',
            500: '#00E5B0',     // 기본값
            600: '#00B88E',
            700: '#008A6B',
            800: '#005C47',
            900: '#002E24',
          },
          
          // 배경 및 텍스트 색상
          'bg': '#1A1D24',        // 딥 차콜 배경
          'text': {
            'light': '#FFFFFF',   // 순수 화이트 텍스트
            'mid': '#B5B9C6',     // 미드톤 그레이 텍스트
            'dark': '#131519',    // 진한 차콜 텍스트
          },
          
          // 추가 UI 요소
          'bubble': {
            'user': 'rgba(181, 169, 209, 0.25)',  // 사용자 메시지 배경
            'ai': 'rgba(74, 124, 255, 0.25)',     // AI 메시지 배경
          },
          'border': 'rgba(255, 255, 255, 0.12)',  // UI 요소 테두리
          'hover': 'rgba(255, 255, 255, 0.08)',   // UI 호버 효과
          'shadow': 'rgba(0, 0, 0, 0.5)',         // 그림자 효과
        },
      },
      fontFamily: {
        sans: ['var(--font-family)', 'sans-serif'],
        heading: ['var(--font-family)', 'sans-serif'],
        notoSansJP: ['var(--font-notoSansJP)', 'sans-serif'],
      },
      boxShadow: {
        'sn': '0 4px 12px rgba(0, 0, 0, 0.2)',
        'sn-sm': '0 2px 8px rgba(0, 0, 0, 0.15)',
        'sn-lg': '0 8px 24px rgba(0, 0, 0, 0.3)',
        'sn-button': '0 4px 12px rgba(74, 124, 255, 0.3)',
        'sn-accent': '0 4px 12px rgba(255, 125, 184, 0.3)',
        'sn-growth': '0 4px 12px rgba(0, 229, 176, 0.3)',
      },
      borderRadius: {
        'sn': '0.75rem',
        'sn-sm': '0.5rem',
        'sn-lg': '1rem',
        'sn-full': '9999px',
      }
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"],
  },
} 