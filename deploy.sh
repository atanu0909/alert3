#!/bin/bash
# Deployment script for pushing to GitHub

echo "=== Attendance System Deployment ==="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding files to git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Initial attendance system setup with GitHub Actions"

# Add remote repository
echo "Adding remote repository..."
git remote add origin https://github.com/atanu0909/alert3.git

# Push to main branch
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo "Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Go to https://github.com/atanu0909/alert3"
echo "2. Navigate to Settings > Secrets and variables > Actions"
echo "3. Add the following secrets:"
echo "   - DB_SERVER=1.22.45.168:19471"
echo "   - DB_NAME=etimetrackliteWEB"
echo "   - DB_USERNAME=sa"
echo "   - DB_PASSWORD=sa@123"
echo "   - EMAIL_FROM=your_email@gmail.com"
echo "   - EMAIL_PASSWORD=your_gmail_app_password"
echo "   - EMAIL_TO=aghosh09092004@gmail.com"
echo "   - SMTP_SERVER=smtp.gmail.com"
echo "   - SMTP_PORT=587"
echo "4. The system will automatically run daily at 12:15 PM UTC"
