# 🚀 Quick Deployment Guide

Complete step-by-step guide to deploy your UNEP FI Citation Search app to Streamlit Cloud.

---

## 📋 Pre-deployment Checklist

Make sure you have these files in your `~/Desktop/UNEP FI/web` folder:

```
web/
├── app.py
├── citation_search_engine.py
├── requirements.txt
├── test_environment.py
├── .gitignore
├── .streamlit/
│   └── config.toml
├── Complete_References_Scopus_FULL.csv  ✅ (33MB)
└── UNEP FI Reports Title.csv            ✅ (few KB)
```

---

## 🎯 Step-by-Step Deployment (15 minutes)

### Step 1: Create GitHub Account (if you don't have one)

1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process
4. Verify your email

### Step 2: Upload Code to GitHub

Open Terminal and run these commands:

```bash
# Navigate to your project folder (note the quotes for spaces)
cd ~/Desktop/"UNEP FI"/web

# Initialize Git repository
git init

# Configure Git (replace with your info)
git config user.name "Your Name"
git config user.email "fan.su@un.org"

# Add all files
git add .

# Make first commit
git commit -m "Initial commit: UNEP FI Citation Search System"

# Create repository on GitHub:
# 1. Go to https://github.com/new
# 2. Repository name: unep-fi-citation-search
# 3. Description: "UNEP FI Report Citation Search System"
# 4. Select "Public" (so 100+ people can access)
# 5. Do NOT initialize with README
# 6. Click "Create repository"

# Link to GitHub (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/unep-fi-citation-search.git

# Push code
git branch -M main
git push -u origin main
```

**Note:** When it asks for password, use a Personal Access Token instead:
- Go to https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select "repo" scope
- Copy the token and use it as password

### Step 3: Deploy to Streamlit Cloud

1. **Register Streamlit Cloud Account**
   - Go to https://share.streamlit.io
   - Click "Sign in"
   - Choose "Continue with GitHub"
   - Authorize Streamlit to access your GitHub

2. **Create New App**
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/unep-fi-citation-search`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL (optional): customize your URL slug

3. **Deploy**
   - Click "Deploy!"
   - Wait 3-5 minutes for deployment

4. **Get Your App URL**
   Your app will be available at:
   ```
   https://YOUR_USERNAME-unep-fi-citation-search.streamlit.app
   ```

### Step 4: Share with Your Team

Send this URL to your 100+ team members:
```
https://YOUR_USERNAME-unep-fi-citation-search.streamlit.app
```

They can use it immediately - no installation needed!

---

## ✅ Verification

After deployment, test your app:

1. Open the URL in browser
2. Check if "Use pre-loaded data files" checkbox appears ✅
3. It should be checked by default ✅
4. Select a report name
5. Click "Search"
6. Verify the disclaimer appears at bottom ✅

---

## 🔄 Updating Your App

When you need to update (e.g., add more data):

```bash
cd ~/Desktop/"UNEP FI"/web

# Make your changes (edit files, update CSV, etc.)

# Commit and push
git add .
git commit -m "Update: [describe your changes]"
git push

# Streamlit Cloud will automatically redeploy (takes 2-3 minutes)
```

---

## 🐛 Troubleshooting

### Problem: Git push fails

**Solution:**
```bash
# Check your remote URL
git remote -v

# If wrong, reset it
git remote set-url origin https://github.com/YOUR_USERNAME/unep-fi-citation-search.git
```

### Problem: CSV files too large

**Solution:** Files under 100MB are fine. Your 33MB file is well within limits.

### Problem: Streamlit Cloud deployment fails

**Check these:**
1. Is `requirements.txt` in the repository?
2. Are all Python files present?
3. Check the deployment logs for specific errors

### Problem: App loads but data files not found

**Solution:** Make sure:
1. CSV files are committed to Git
2. `.gitignore` allows these specific CSV files (already configured)
3. File names exactly match:
   - `Complete_References_Scopus_FULL.csv`
   - `UNEP FI Reports Title.csv`

---

## 💡 Pro Tips

### Make CSV Filenames URL-Friendly

If you want, you can rename your files (optional):

```bash
# Rename files to remove spaces
mv "UNEP FI Reports Title.csv" "UNEP_FI_Reports_Title.csv"
mv "Complete_References_Scopus_FULL.csv" "Complete_References_Scopus_FULL.csv"

# Update in app.py:
# Change line 177 and 178 to match new names
```

### Custom Domain (Optional)

You can set up a custom domain like `citations.unepfi.org`:

1. In Streamlit Cloud app settings
2. Go to "Settings" → "Custom domain"
3. Follow the DNS configuration instructions

---

## 📞 Contact

If you encounter issues:
- **Email:** fan.su@un.org
- **Streamlit Support:** https://discuss.streamlit.io
- **GitHub Issues:** Create issue in your repository

---

## ✨ Expected Result

After deployment, users will see:

```
📚 UNEP FI Report Citation Search
================================

[Sidebar]
✅ Use pre-loaded data files (checked)

Search for reports...
[Search button]

[Results with disclaimer at bottom]
⚠️ Disclaimer:
• Numbers are approximate...
• Only includes papers indexed in Scopus...
• Contact: fan.su@un.org
```

---

**Ready to deploy? Start with Step 1!** 🚀

Good luck! The whole process should take about 15 minutes.
