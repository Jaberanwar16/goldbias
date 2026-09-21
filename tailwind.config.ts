import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        gold: '#F5B942',
        bullish: '#22C55E',
        bearish: '#EF4444',
        neutral: '#9CA3AF',
      },
    },
  },
  plugins: [],
};

export default config;
