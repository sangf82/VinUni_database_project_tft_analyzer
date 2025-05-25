/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        vintage: {
          cream: '#F5E6D3',
          sand: '#E2C799',
          coffee: '#A17C6B',
          mocha: '#7C5D54',
          bronze: '#8B6F5C',
          leather: '#5C4B3F',
          wood: '#3F332C',
          bark: '#2A211C',
          shadow: '#1A1412',
          ink: '#0D0A09'
        }
      }
    },
  },
  plugins: [],
};