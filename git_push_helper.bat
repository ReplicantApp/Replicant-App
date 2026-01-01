@echo off
echo Committing changes...
git add .
git commit -m "feat: complete app logic with backup and restore"
echo.
echo Pushing to remote...
git push
echo.
pause
