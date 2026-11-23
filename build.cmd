@echo off
REM بناء ملف CSS النهائي المضغوط (Tailwind Standalone CLI)
tailwindcss.exe -c tailwind.config.js -i assets\css\input.css -o assets\css\style.css --minify
