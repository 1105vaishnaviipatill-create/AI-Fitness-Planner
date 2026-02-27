# ✅ GitHub Upload Checklist

Complete each step before moving to the next.

---

## 📋 Pre-Upload Checklist

- [ ] **Git installed?**
  - Open PowerShell and run: `git --version`
  - Should show version number like: `git version 2.x.x`
  
- [ ] **GitHub account created?**
  - Go to https://github.com and sign up (if not already)
  - Verify you can log in

- [ ] **.gitignore created?**
  - Check that `.gitignore` file exists in project folder
  - Should NOT contain API keys or secrets

- [ ] **All Python files present?**
  - [ ] app.py
  - [ ] ai_chat.py
  - [ ] recommender.py
  - [ ] train_model.py
  - [ ] requirements.txt
  - [ ] README.md

- [ ] **Sensitive files excluded?**
  - [ ] `.env` file exists locally (will NOT be uploaded)
  - [ ] `.env` should NOT be in git (check with: `git status`)
  - [ ] No API keys in any .py files

- [ ] **Data files present?**
  - [ ] data/user_profiles.csv
  - [ ] data/foods.csv
  - [ ] data/workouts.csv

---

## 🚀 Upload Steps

### Step 1: GitHub Setup
- [ ] Went to https://github.com/new
- [ ] Created repository named: `AI-Fitness-Planner`
- [ ] Set to Public
- [ ] Did NOT check "Add README" or ".gitignore"
- [ ] Copied repository URL: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git`

### Step 2: Local Git Setup
- [ ] Opened PowerShell in project folder
- [ ] Ran: `git init`
- [ ] Ran: `git config --global user.name "Your Name"`
- [ ] Ran: `git config --global user.email "your@email.com"`
- [ ] Ran: `git add .`
- [ ] Ran: `git commit -m "Initial commit: Add AI Fitness Planner project"`

### Step 3: Connect & Push
- [ ] Ran: `git remote add origin https://github.com/YOUR-USERNAME/AI-Fitness-Planner.git`
- [ ] Ran: `git branch -M main`
- [ ] Ran: `git push -u origin main`
- [ ] Authenticated when prompted
- [ ] Saw success message with "new branch"

---

## ✅ Post-Upload Verification

### Verify Locally
- [ ] Ran: `git status` in PowerShell
- [ ] Shows: "nothing to commit, working tree clean"
- [ ] Ran: `git log --oneline`
- [ ] Shows your commit message

### Verify on GitHub Website
Go to: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner`

**Check these files ARE visible:**
- [ ] app.py ✅
- [ ] ai_chat.py ✅
- [ ] recommender.py ✅
- [ ] train_model.py ✅
- [ ] requirements.txt ✅
- [ ] README.md ✅
- [ ] .gitignore ✅
- [ ] GITHUB_UPLOAD_GUIDE.md ✅
- [ ] COPY_PASTE_COMMANDS.md ✅
- [ ] QUICK_GIT_REFERENCE.md ✅

**Check these files are HIDDEN (NOT visible):**
- [ ] .env ❌ (should NOT see this)
- [ ] __pycache__/ ❌ (should NOT see this)
- [ ] .venv/ ❌ (should NOT see this)

### Verify Files Content
- [ ] Click on `app.py` - should show your Streamlit code
- [ ] Click on `ai_chat.py` - should show refactored code
- [ ] Click on `requirements.txt` - should show dependencies
- [ ] Click on `README.md` - should display formatted nicely

---

## 📊 Final Status

| Item | Status | Notes |
|------|--------|-------|
| Repository created | ☐ | GitHub side |
| Files added locally | ☐ | Via `git add .` |
| Commit created | ☐ | Via `git commit` |
| Remote connected | ☐ | Via `git remote add` |
| Code pushed | ☐ | Via `git push` |
| GitHub page shows files | ☐ | Verify online |
| .env NOT uploaded | ☐ | Security check |
| Local status clean | ☐ | `git status` = clean |

---

## 🎯 Success Criteria

You're done when:

✅ Can see all Python files on GitHub website
✅ Cannot see `.env` file on GitHub
✅ README displays formatted nicely
✅ Local `git status` shows "working tree clean"
✅ Can share link: `https://github.com/YOUR-USERNAME/AI-Fitness-Planner`

---

## 📝 Next Steps (After Upload)

- [ ] Add GitHub topics (e.g., `streamlit`, `machine-learning`, `fitness`)
- [ ] Write GitHub bio/profile
- [ ] Add `LICENSE` file (choose from MIT, Apache, GPL)
- [ ] Enable "Issues" for bug tracking
- [ ] Create GitHub Pages (optional)
- [ ] Share repository link on social media
- [ ] Continue developing features

---

## 🆘 Troubleshooting Quick Links

If stuck, check:
- [ ] Read: COPY_PASTE_COMMANDS.md (step-by-step with examples)
- [ ] Read: GITHUB_UPLOAD_GUIDE.md (detailed explanations)
- [ ] Read: QUICK_GIT_REFERENCE.md (common commands)
- [ ] Search GitHub docs: https://docs.github.com

---

## 💬 Common Questions

**Q: Can I change the repository name later?**
A: Yes! GitHub Settings → Rename Repository

**Q: Can I make it private later?**
A: Yes! GitHub Settings → Change to Private

**Q: Do I need to push every time I code?**
A: No, only when you want to upload changes

**Q: Can I delete and restart?**
A: Yes, delete on GitHub and create new repository

**Q: How do I work with others?**
A: Settings → Collaborators → Add their GitHub username

---

## 📞 Need Help?

1. **Error messages?** → Check GITHUB_UPLOAD_GUIDE.md "Common Issues" section
2. **Don't know command?** → Check QUICK_GIT_REFERENCE.md
3. **Lost?** → Start fresh with COPY_PASTE_COMMANDS.md
4. **Still stuck?** → Try GitHub Desktop instead (easier UI)

---

**Congratulations! You've successfully uploaded your AI Fitness Planner to GitHub! 🎉**

Time to celebrate and show off your project! 🚀
