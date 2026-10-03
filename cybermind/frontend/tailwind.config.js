/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#0a0f1d',
          card: '#111827',
          border: '#1f293d',
          accent: '#00f0ff',
          neon: '#00ff66',
          danger: '#ff3366',
          warning: '#ffb703',
          muted: '#94a3b8'
        }
      }
    },
  },
  plugins: [],
}
