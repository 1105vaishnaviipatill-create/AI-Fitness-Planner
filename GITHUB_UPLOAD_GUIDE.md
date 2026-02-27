# GitHub Upload Guide for AI Fitness Planner

Complete step-by-step instructions to upload your project to GitHub.

---

## 📋 Prerequisites

1. **Git installed** - Download from https://git-scm.com/
2. **GitHub account** - Create free at https://github.com
3. **Your project files** - All ready in `AI_Fitness_Planner` folder

---

## 🚀 Step 1: Create Repository on GitHub

### 1.1 Go to GitHub
- Visit: https://github.com
- Sign in to your account
- Click **+** icon (top right) → Select **New repository**

### 1.2 Fill Repository Details

| Field | Value |
|-------|-------|
| Repository name | `AI-Fitness-Planner` |
| Description | `AI-powered personalized workout and diet planner with ML and OpenAI integration` |
| Visibility | Public (or Private if you prefer) |
| Initialize | **DO NOT** check "Add README", "Add .gitignore", ".gitignore" |

### 1.3 Create Repository
- Click **Create repository** button
- **COPY** the repository URL (looks like: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git`)

---

## 💻 Step 2: Initialize Git Locally

Open PowerShell and navigate to your project:

```powershell
cd "c:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner"
```

### 2.1 Initialize Git Repository
```powershell
git init
```

**Output:**
```
Initialized empty Git repository in C:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner\.git
```

### 2.2 Configure Git (First time only)
```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Example:**
```powershell
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
```

---

## 📁 Step 3: Add Files to Git

### 3.1 Check Project Status
```powershell
git status
```

**You should see all your Python files listed as "Untracked files"**

### 3.2 Add All Files (except those in .gitignore)
```powershell
git add .
```

**This adds all files EXCEPT:**
- `.env` files
- `__pycache__/`
- `.venv/` folder
- `models/` folder (if you chose to exclude)
- Other files in .gitignore

### 3.3 Verify Files Are Staged
```powershell
git status
```

**You should see green "new file" entries for:**
- app.py
- ai_chat.py
- recommender.py
- train_model.py
- requirements.txt
- .gitignore
- README.md

---

## 💾 Step 4: Create First Commit

```powershell
git commit -m "Initial commit: Add AI Fitness Planner project"
```

**Output example:**
```
[main (root-commit) abc1234] Initial commit: Add AI Fitness Planner project
 7 files changed, 1250 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 create mode 100644 ai_chat.py
 ...
```

---

## 🔗 Step 5: Connect to GitHub Repository

Replace `YOUR-USERNAME` and use the URL from Step 1.3:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git
```

**Example:**
```powershell
git remote add origin https://github.com/johndoe/AI-Fitness-Planner.git
```

### Verify Connection
```powershell
git remote -v
```

**You should see:**
```
origin  https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git (fetch)
origin  https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git (push)
```

---

## 📤 Step 6: Upload (Push) to GitHub

### 6.1 Rename Default Branch (if needed)
```powershell
git branch -M main
```

### 6.2 Push Your Code
```powershell
git push -u origin main
```

**First time you might need to authenticate:**
- GitHub will open a browser to authenticate
- Or you'll be prompted for credentials

**Success output:**
```
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (10/10), 1.25 KiB | 1.25 MiB/s
Creating branch...
To https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git
 * [new branch]      main -> main
Branch 'main' is set to track remote branch 'main' from 'origin'.
```

---

## ✅ Step 7: Verify Upload Success

### 7.1 Check on GitHub Website
1. Go to your GitHub repository: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner`
2. You should see all your files listed
3. Verify these files are visible:
   - ✅ app.py
   - ✅ ai_chat.py
   - ✅ recommender.py
   - ✅ train_model.py
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ .gitignore

### 7.2 Verify .env NOT Uploaded
- Look for `.env` file in repository
- **Should NOT see it** (because of .gitignore)

### 7.3 Check Git Status Locally
```powershell
git status
```

**Should show:**
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

## 🔄 Complete Command Summary

**Copy-paste all at once:**

```powershell
# Navigate to project
cd "c:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner"

# Initialize Git
git init

# Configure user (first time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Add AI Fitness Planner project"

# Add remote repository (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git

# Set main branch
git branch -M main

# Upload to GitHub
git push -u origin main
```

---

## 🛠️ Common Issues & Fixes

### Issue 1: "fatal: not a git repository"
**Error:**
```
fatal: not a git repository (or any of the parent directories): .git
```

**Fix:**
```powershell
git init
```

---

### Issue 2: Authentication Failed
**Error:**
```
fatal: Authentication failed for 'https://github.com/YOUR-USERNAME/...'
```

**Solution Options:**

**Option A: Personal Access Token (Recommended)**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `gist`
4. Copy the token
5. When prompted for password, paste the token instead

**Option B: SSH Key Setup**
```powershell
ssh-keygen -t ed25519 -C "your@email.com"
# Then follow prompts and add public key to GitHub
```

**Option C: GitHub Desktop (Easiest)**
- Download GitHub Desktop: https://desktop.github.com
- Sign in with your GitHub account
- Publish your repository from there

---

### Issue 3: ".gitignore not working"
**Problem:** Files in .gitignore are still being tracked

**Fix:**
```powershell
# Remove files from Git cache
git rm --cached .env

# Re-add files respecting .gitignore
git add .

# Commit
git commit -m "Remove .env from tracking"

# Push
git push origin main
```

---

### Issue 4: "Repository already exists"
**Error:**
```
fatal: destination path 'AI-Fitness-Planner' already exists
```

**Fix:**
```powershell
# If you already have .git folder, don't run git init again
# Just verify:
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git
```

---

### Issue 5: "Remote origin already exists"
**Error:**
```
fatal: remote origin already exists.
```

**Fix:**
```powershell
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git
```

---

### Issue 6: "Rejected because of large files"
**Error:**
```
fatal: The remote end hung up unexpectedly
```

**Check file sizes:**
```powershell
# Find large files
Get-ChildItem -Recurse | Sort-Object Length -Descending | Select-Object FullName, Length -First 10
```

**If models/ too large, exclude it:**
```powershell
# Edit .gitignore to uncomment:
# models/
```

---

## 📝 After Upload: Making Changes

### To Update Code (Push Updates)

```powershell
# Navigate to project
cd "c:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner"

# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Update feature: Add new workout types"

# Push to GitHub
git push origin main
```

---

## 🔐 Important Security Notes

### ✅ What IS Safe to Upload
- Python source code (.py files)
- Requirements.txt
- CSV data files
- README and documentation
- .gitignore file

### ❌ What is NOT Safe to Upload
- `.env` file with API keys ✗
- Secrets or credentials ✗
- Database passwords ✗
- Private user data ✗

**Your .gitignore prevents these automatically!**

---

## 🎯 Final Checklist

Before considering upload complete:

- [ ] GitHub repository created
- [ ] All Python files visible on GitHub
- [ ] `.env` file NOT visible on GitHub
- [ ] `models/` folder handled (excluded or included intentionally)
- [ ] README.md displays properly
- [ ] Local `git status` shows "working tree clean"
- [ ] Can see commit history on GitHub

---

## 📚 Useful Git Commands for Future

```powershell
# See commit history
git log --oneline -5

# See what will be staged
git diff

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Clone repository to another computer
git clone https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git

# Update from GitHub (if others contribute)
git pull origin main

# Create new branch for features
git checkout -b new-feature
```

---

## 🚀 You're Done!

Your project is now on GitHub! 🎉

**Share your repository link:**
```
https://github.com/YOUR-USERNAME/AI-Fitness-Planner
```

**Next steps:**
1. Add collaborators (Settings → Collaborators)
2. Enable GitHub Pages for portfolio
3. Add topics/tags for discoverability
4. Keep updating with new features!

---

## 💡 Pro Tips

1. **Add meaningful commit messages** - Helps track changes
2. **Commit frequently** - Small, focused commits are better
3. **Write good README** - First thing people see
4. **Add LICENSE** - Makes it official (Apache, MIT, GPL)
5. **Enable Issues** - Let others report bugs
6. **Add GitHub Actions** - Automate testing

---

**Questions?** Check GitHub's official guide: https://docs.github.com/en/get-started

Happy coding! 🚀
