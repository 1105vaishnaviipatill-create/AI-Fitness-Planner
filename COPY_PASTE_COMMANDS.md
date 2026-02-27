# 📋 Copy-Paste Commands for GitHub Upload

**Follow these steps exactly. Copy each command and paste into PowerShell.**

---

## ✅ STEP 1: Create GitHub Repository (On GitHub Website)

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name:** `AI-Fitness-Planner`
   - **Description:** `AI-powered personalized workout and diet planner with ML and OpenAI`
   - **Visibility:** Public
   - **Do NOT check:** Add README, Add .gitignore
3. Click **Create repository**
4. **COPY THE URL** (looks like: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git`)

---

## ✅ STEP 2: Open PowerShell

Press `Windows Key + X` → Select **Windows PowerShell (Admin)**

Or open VS Code terminal (you already have it open!)

---

## ✅ STEP 3: Run These Commands (Copy-Paste One at a Time)

### Command 1: Navigate to Project
```
cd "c:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner"
```

**Press Enter**

---

### Command 2: Initialize Git
```
git init
```

**Press Enter**

**Expected output:**
```
Initialized empty Git repository in C:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner\.git
```

---

### Command 3: Configure Git (First Time Only)
```
git config --global user.name "Your Full Name"
```

**Replace "Your Full Name" with your actual name, keep the quotes**

**Example:**
```
git config --global user.name "John Doe"
```

**Press Enter** (no output is normal)

---

### Command 4: Set Email
```
git config --global user.email "your.email@gmail.com"
```

**Replace email with your actual email**

**Press Enter** (no output is normal)

---

### Command 5: Check Status
```
git status
```

**Press Enter**

**You should see many "Untracked files" - that's normal!**

---

### Command 6: Add All Files
```
git add .
```

**Press Enter** (no output is normal)

---

### Command 7: Verify Files Added
```
git status
```

**Press Enter**

**You should see files in GREEN with "new file" label**

---

### Command 8: Create First Commit
```
git commit -m "Initial commit: Add AI Fitness Planner project"
```

**Press Enter**

**You should see output showing files changed, insertions added**

---

### Command 9: Add Remote Repository
```
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git
```

**⚠️ IMPORTANT:** Replace `YOUR-USERNAME` with your actual GitHub username!

**Example:**
```
git remote add origin https://github.com/johndoe/AI-Fitness-Planner.git
```

**Press Enter** (no output is normal)

---

### Command 10: Verify Remote Added
```
git remote -v
```

**Press Enter**

**You should see two lines with your repository URL**

---

### Command 11: Set Main Branch
```
git branch -M main
```

**Press Enter** (no output is normal)

---

### Command 12: Push to GitHub (UPLOAD)
```
git push -u origin main
```

**Press Enter**

**First time might ask for authentication:**
- GitHub will open a browser window
- Sign in and authorize
- Come back to PowerShell

**You should see:**
```
Enumerating objects: ...
Counting objects: ...
Creating branch...
...
[new branch]      main -> main
Branch 'main' is set to track remote branch 'main' from 'origin'.
```

---

## ✅ STEP 4: Verify Upload on GitHub

1. Go to: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner`
2. You should see all your Python files
3. Verify you see:
   - ✅ app.py
   - ✅ ai_chat.py
   - ✅ recommender.py
   - ✅ train_model.py
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ .gitignore
4. **Important:** Make sure you do NOT see `.env` file

---

## ✅ STEP 5: Final Verification (Local)

In PowerShell, run:

```
git status
```

**Should show:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

## 🎉 Success!

Your project is now on GitHub! Share the link:

```
https://github.com/YOUR-USERNAME/AI-Fitness-Planner
```

---

## 📝 For Future Updates (After Initial Upload)

Whenever you make changes:

```powershell
# 1. Check what changed
git status

# 2. Add changes
git add .

# 3. Commit with message
git commit -m "Update: Describe your changes"

# 4. Push to GitHub
git push origin main
```

---

## ❌ Common Mistakes to AVOID

| ❌ Don't | ✅ Do |
|---------|-------|
| Forget to replace `YOUR-USERNAME` | Replace with actual username |
| Upload `.env` file | It's automatically excluded by .gitignore |
| Run `git init` twice | Only run once |
| Forget `git push` step | Must push to upload |
| Use wrong repository URL | Copy from GitHub website |

---

## 🆘 If Something Goes Wrong

### Error: "fatal: not a git repository"
```
git init
```

### Error: "authentication failed"
- Use Personal Access Token instead of password
- Get token from: Settings → Developer settings → Personal access tokens

### Error: "remote origin already exists"
```
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git
```

### Error: "repository already exists and is not empty"
Just continue - you might have git already initialized

---

## 💡 Pro Tip: Use GitHub Desktop Instead

If command line is confusing, use **GitHub Desktop**:

1. Download: https://desktop.github.com
2. Sign in with GitHub account
3. File → Add Local Repository → Select your folder
4. Publish repository
5. Done! Much easier!

---

**Ready? Start with STEP 3, Command 1 in your PowerShell! 🚀**
