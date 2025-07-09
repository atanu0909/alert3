# PowerShell deployment script for Windows

Write-Host "=== Attendance System Deployment ===" -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m "Initial attendance system setup with GitHub Actions"

# Add remote repository
Write-Host "Adding remote repository..." -ForegroundColor Yellow
git remote add origin https://github.com/atanu0909/alert3.git

# Push to main branch
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com/atanu0909/alert3"
Write-Host "2. Navigate to Settings > Secrets and variables > Actions"
Write-Host "3. Add the following secrets:" -ForegroundColor Yellow
Write-Host "   - DB_SERVER=1.22.45.168:19471"
Write-Host "   - DB_NAME=etimetrackliteWEB"
Write-Host "   - DB_USERNAME=sa"
Write-Host "   - DB_PASSWORD=sa@123"
Write-Host "   - EMAIL_FROM=your_email@gmail.com"
Write-Host "   - EMAIL_PASSWORD=your_gmail_app_password"
Write-Host "   - EMAIL_TO=aghosh09092004@gmail.com"
Write-Host "   - SMTP_SERVER=smtp.gmail.com"
Write-Host "   - SMTP_PORT=587"
Write-Host "4. The system will automatically run daily at 12:30 PM UTC" -ForegroundColor Green
