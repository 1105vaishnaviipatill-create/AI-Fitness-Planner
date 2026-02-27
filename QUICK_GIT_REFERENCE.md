# 🚀 Quick Git Commands Reference

## One-Time Setup (First Upload)

```powershell
# 1. Navigate to project
cd "c:\Users\Lenovo\OneDrive\Desktop\AI_Fitness_Planner"

# 2. Initialize Git
git init

# 3. Configure user (first time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 4. Add files
git add .

# 5. Create commit
git commit -m "Initial commit: Add AI Fitness Planner project"

# 6. Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git

# 7. Set branch name
git branch -M main

# 8. Push to GitHub
git push -u origin main
```

---

## Updating Code (After Initial Upload)

```powershell
# Check changes
git status

# Add changes
git add .

# Commit
git commit -m "Update: Your change description"

# Push
git push origin main
```

---

## Useful Commands

```powershell
# See all commits
git log --oneline

# See what changed
git diff

# Undo last commit
git reset --soft HEAD~1

# Clone project elsewhere
git clone https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git

# Pull latest changes
git pull origin main

# See all branches
git branch -a

# Create new branch
git checkout -b feature-name
```

---

## File Structure on GitHub

```
AI-Fitness-Planner/
├── app.py ✅ (visible)
├── ai_chat.py ✅ (visible)
├── recommender.py ✅ (visible)
├── train_model.py ✅ (visible)
├── requirements.txt ✅ (visible)
├── README.md ✅ (visible)
├── GITHUB_UPLOAD_GUIDE.md ✅ (visible)
├── .gitignore ✅ (visible)
├── models/ ⚠️ (excluded - comment out line to include)
├── data/ ✅ (visible - CSV files included)
│   ├── user_profiles.csv
│   ├── foods.csv
│   └── workouts.csv
└── .env ❌ (NOT uploaded - protected by .gitignore)
```

---

## Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✅ | Will be uploaded |
| ❌ | Will NOT be uploaded |
| ⚠️ | Optional (configure in .gitignore) |

---

## Verification Checklist

After pushing:

```powershell
# ✓ Check status is clean
git status
# Should show: "nothing to commit, working tree clean"

# ✓ Verify remote is set
git remote -v
# Should show origin URL

# ✓ Check commit history
git log --oneline
# Should show your commits
```

Then visit: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner`

---

## Quick Troubleshooting

| Problem | Command |
|---------|---------|
| Git not found | Install from git-scm.com |
| Not a git repo | Run: `git init` |
| Auth failed | Use Personal Access Token |
| Wrong URL | `git remote set-url origin <new-url>` |
| Want to undo | `git reset --soft HEAD~1` |
| Models too big | Uncomment in .gitignore |

---

**Need help?** See GITHUB_UPLOAD_GUIDE.md for detailed instructions.
