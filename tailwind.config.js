/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./python_graph/**/*.{html,js,ts,py}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}

