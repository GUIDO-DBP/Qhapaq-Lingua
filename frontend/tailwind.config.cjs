/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        'ql-bg': '#020617',
        'ql-card': '#0b1020',
        'ql-primary': '#6366f1',
        'ql-secondary': '#ec4899',
        'ql-accent': '#22c55e'
      }
    }
  },
  plugins: []
}
