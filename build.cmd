@echo off
chcp 65001 >nul
call npx -y tailwindcss@3 -c tailwind.config.js -i assets/css/input.css -o assets/css/style.css --minify
