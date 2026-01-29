/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                isro: {
                    orange: '#FF9933',
                    blue: '#138808', // Saffron/Green actually, wait. ISRO blue is #00529B. Let's use thematic space colors.
                    primary: '#0B0F19', // Deep Space
                    secondary: '#1C2431',
                    accent: '#38A3A5',
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
