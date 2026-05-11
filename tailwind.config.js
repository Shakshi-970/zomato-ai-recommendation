/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        zomato: {
          red: '#EF4F5F',
          dark: '#1A1A1A',
          light: '#F5F5F5',
        }
      }
    },
  },
  plugins: [],
};
