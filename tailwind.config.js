/**
 * إعداد Tailwind — يُستخدم مع Tailwind Standalone CLI فقط (بدون npm).
 * أمر البناء:
 *   ./tailwindcss.exe -i ./assets/css/input.css -o ./assets/css/style.css --minify
 */
module.exports = {
  content: [
    './*.html',
    './**/*.html',
    './assets/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // عنابي ملكي — اللون الأساسي للبراند
        brand: {
          50:  '#fbf3f6',
          100: '#f6e4ec',
          200: '#eccad9',
          300: '#dca1bb',
          400: '#c46e94',
          500: '#a84a73',
          600: '#8c3459',
          700: '#722847',   // الأساسي (تباين مع الأبيض ≈ 9.6:1)
          800: '#5c213a',
          900: '#3f1528',
          950: '#260b17',
        },
        // ذهبي — للتمييز فقط (على الأبيض استخدم gold-700 للنصوص)
        gold: {
          50:  '#fdf9ec',
          100: '#f9efcc',
          200: '#f2dd95',
          300: '#e9c65c',
          400: '#dfb03a',   // على الخلفيات الداكنة
          500: '#c99424',
          600: '#a9741c',
          700: '#86561a',   // نص ذهبي على أبيض (AA)
          800: '#6e451c',
          900: '#5d3a1c',
        },
        whatsapp: {
          DEFAULT: '#0f7a3f', // أغمق من الأخضر الرسمي لتحقيق تباين AA مع النص الأبيض
          dark: '#0b5f31',
        },
      },
      fontFamily: {
        sans: ['"IBM Plex Sans Arabic"', 'Tahoma', 'Arial', 'sans-serif'],
      },
      maxWidth: {
        site: '80rem',
      },
    },
  },
  plugins: [],
};
