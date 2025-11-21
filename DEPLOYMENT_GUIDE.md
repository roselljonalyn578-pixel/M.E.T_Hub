# GitHub Deployment Guide

## Step 1: Prepare Your Project

✅ Already completed:
- Created `.gitignore` file
- Created `requirements.txt` file
- Created `README.md` file

## Step 2: Initialize Git Repository

Open your terminal/command prompt in the project folder and run:

```bash
cd c:\Users\rosel\OneDrive\Desktop\M.E.T
git init
```

## Step 3: Add Files to Git

```bash
git add .
git commit -m "Initial commit: MET HUB project"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name it: `met-hub` (or any name you prefer)
5. Keep it Public or Private (your choice)
6. DO NOT initialize with README (we already have one)
7. Click "Create repository"

## Step 5: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/met-hub.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 6: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded

## Important Notes Before Deployment

⚠️ **SECURITY WARNINGS:**

1. **SECRET_KEY**: Your Django SECRET_KEY is exposed in settings.py
   - For production, use environment variables
   - Never commit real SECRET_KEY to public repositories

2. **DEBUG Mode**: Currently set to `True`
   - For production, set `DEBUG = False`

3. **Database**: Using SQLite (db.sqlite3)
   - Already excluded in .gitignore
   - For production, consider PostgreSQL or MySQL

## Next Steps for Web Deployment

After GitHub, you can deploy to:

1. **PythonAnywhere** (Free tier available)
   - Easy Django deployment
   - Good for beginners

2. **Heroku** (Free tier limited)
   - Popular platform
   - Good documentation

3. **Railway** (Free tier available)
   - Modern platform
   - Easy setup

4. **Render** (Free tier available)
   - Simple deployment
   - Good for Django

Would you like instructions for any specific platform?

## Troubleshooting

If you get errors:

1. **"git is not recognized"**: Install Git from https://git-scm.com/
2. **Authentication failed**: Use GitHub Personal Access Token instead of password
3. **Large files rejected**: Check .gitignore includes media/ and db.sqlite3

## Useful Git Commands

```bash
# Check status
git status

# Add specific file
git add filename.py

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull from GitHub
git pull
```
