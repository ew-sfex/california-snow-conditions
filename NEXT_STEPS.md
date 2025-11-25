# California Snow Conditions - Next Steps

The California snow conditions project has been **successfully set up** with all code adapted from Colorado! 🎉

## ✅ What's Been Completed

1. **Project Structure Created** - New directory with all necessary files
2. **California Resort Data** - 25 resorts with coordinates, trails, lifts, and regions
3. **Scrapers Updated** - OnTheSnow scraper configured for California
4. **Map Configuration** - California bounds, region toggles added
5. **Region Toggle Feature** - Quick zoom to Tahoe North/South, Mammoth, SoCal
6. **Documentation** - README and SETUP_GUIDE created
7. **GitHub Actions** - Workflow configured for Pacific Time zone

## 📋 What You Need to Do Next

The remaining tasks require **manual action** since they involve account creation and deployment:

### 1. Google Cloud Setup (30 minutes)

**Action Required:**
- Create new Google Cloud project
- Enable Google Sheets API
- Create service account and download JSON key
- Create new Google Sheet and share with service account

**Follow:** `SETUP_GUIDE.md` Phase 2 & 3 (steps 2.1-3.4)

### 2. Local Configuration (5 minutes)

**Action Required:**
- Create `.env` file with Google credentials
- Update `docs/config.js` with Google Sheet CSV URL

**Follow:** `SETUP_GUIDE.md` Phase 4 (steps 4.2-4.3)

### 3. Local Testing (15 minutes)

**Action Required:**
- Install Python dependencies
- Test scraper locally
- Test Google Sheets upload
- Verify map loads correctly

**Follow:** `SETUP_GUIDE.md` Phase 5 (steps 5.1-5.3)

### 4. GitHub Deployment (20 minutes)

**Action Required:**
- Create new GitHub repository
- Push code to GitHub
- Configure GitHub secrets
- Enable GitHub Pages

**Follow:** `SETUP_GUIDE.md` Phase 6 (steps 6.1-6.5)

### 5. Verify Automation (10 minutes)

**Action Required:**
- Trigger manual workflow run
- Check results in Google Sheet and live map
- Verify automatic schedule works

**Follow:** `SETUP_GUIDE.md` Phase 7 (steps 7.1-7.3)

---

## 🎯 Quick Start Checklist

Use this checklist to track your progress:

- [ ] **Google Cloud Project Created**
  - [ ] Google Sheets API enabled
  - [ ] Service account created
  - [ ] JSON key downloaded
  - [ ] Service account email copied

- [ ] **Google Sheet Created**
  - [ ] Sheet created and named
  - [ ] Shared with service account
  - [ ] Sheet ID copied
  - [ ] Published as CSV
  - [ ] CSV URL copied

- [ ] **Local Configuration**
  - [ ] `.env` file created
  - [ ] `GOOGLE_SHEETS_SPREADSHEET_ID` set
  - [ ] `GOOGLE_CREDENTIALS` set
  - [ ] `docs/config.js` DATA_URL updated

- [ ] **Local Testing**
  - [ ] Dependencies installed
  - [ ] Scraper runs successfully
  - [ ] Google Sheets uploads work
  - [ ] Map displays correctly

- [ ] **GitHub Deployment**
  - [ ] New GitHub account created
  - [ ] Repository created
  - [ ] Code pushed to GitHub
  - [ ] GitHub secrets configured
  - [ ] GitHub Pages enabled

- [ ] **Verification**
  - [ ] Manual workflow triggered
  - [ ] Data appears in Google Sheet
  - [ ] Map shows data correctly
  - [ ] Automatic schedule verified

---

## 📂 Project Files Overview

### Core Python Files
- `onthesnow_scraper.py` - Scrapes California resorts from OnTheSnow
- `combined_scraper.py` - Combines data and adds coordinates/metadata
- `google_sheets_updater.py` - Uploads data to Google Sheets
- `run_all_updates.py` - Orchestrates full update cycle

### Map Files (docs/)
- `index.html` - Map webpage with region toggles
- `map.js` - Map logic, regions, and marker rendering
- `config.js` - Configuration (needs YOUR Google Sheet URL)
- `style.css` - Styling for map and controls

### Configuration Files
- `california_resort_metadata.csv` - Resort coordinates and metadata
- `.env` - Your credentials (you need to create this)
- `requirements.txt` - Python dependencies
- `.gitignore` - Files to exclude from git

### Documentation
- `README.md` - Project overview and quick start
- `SETUP_GUIDE.md` - Detailed setup instructions
- `NEXT_STEPS.md` - This file (what to do next)

### Automation
- `.github/workflows/update-snow-data.yml` - GitHub Actions workflow

---

## 🔑 Critical Files You Need to Configure

Before the project will work, you MUST update these files with your credentials:

### 1. `.env` (CREATE THIS FILE)

Location: `/california-snow-conditions/.env`

```bash
GOOGLE_SHEETS_SPREADSHEET_ID=YOUR_SHEET_ID_HERE
GOOGLE_CREDENTIALS='YOUR_JSON_CREDENTIALS_HERE'
MAPBOX_TOKEN=YOUR_MAPBOX_TOKEN_HERE
```

### 2. `docs/config.js` (UPDATE LINE 12)

Location: `/california-snow-conditions/docs/config.js`

Change line 12 from:
```javascript
const DATA_URL = 'YOUR_CALIFORNIA_GOOGLE_SHEET_CSV_URL_HERE';
```

To:
```javascript
const DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-YOUR_ACTUAL_URL/pub?output=csv';
```

---

## 🚀 Ready to Launch?

### Option 1: Follow the Complete Guide

Open `SETUP_GUIDE.md` and follow each phase step-by-step. This is the recommended approach if this is your first time.

### Option 2: Quick Setup (Experienced Users)

If you're familiar with Google Cloud and GitHub:

1. **Google Setup (20 min):**
   - Create Google Cloud project → Enable Sheets API → Create service account
   - Create Google Sheet → Share with service account → Publish as CSV

2. **Local Setup (5 min):**
   - Create `.env` file with credentials
   - Update `docs/config.js` with CSV URL
   - Run: `pip install -r requirements.txt`

3. **Test (5 min):**
   - Run: `python combined_scraper.py`
   - Run: `python google_sheets_updater.py`
   - Open `docs/index.html` in browser

4. **Deploy (10 min):**
   - Create GitHub repo
   - Push code: `git push origin main`
   - Add GitHub secrets (3 secrets)
   - Enable GitHub Pages

5. **Verify (5 min):**
   - Trigger workflow manually
   - Check Google Sheet updated
   - Visit live map URL

---

## 💡 Tips for Success

1. **Take Your Time:** Don't rush through account setup - errors here cause issues later
2. **Save Everything:** Keep service account JSON, sheet IDs, and URLs in a secure note
3. **Test Locally First:** Make sure scraper works before deploying to GitHub
4. **Check Logs:** If something fails, check the `.log` files for details
5. **One Step at a Time:** Complete each phase before moving to the next

---

## 🆘 Need Help?

### Common Issues

**"Authentication failed"**
→ Check service account has Editor access to Google Sheet

**"Sheet not found"**
→ Verify Sheet ID in `.env` matches your Google Sheet URL

**"Map not loading data"**
→ Update `DATA_URL` in `docs/config.js` with published CSV URL

**"GitHub Actions failing"**
→ Ensure all 3 secrets are set correctly in GitHub repository settings

### Where to Look

1. **Setup Instructions:** `SETUP_GUIDE.md`
2. **Project Overview:** `README.md`
3. **Log Files:** `*.log` files in project root
4. **GitHub Actions Logs:** Actions tab in GitHub repository

---

## 🎉 When It's Working

Your California Snow Conditions map will:

- ✅ Auto-update every 2 hours with latest conditions
- ✅ Show all 25+ California resorts
- ✅ Provide region-specific zoom (Tahoe, Mammoth, SoCal)
- ✅ Display trail/lift counts and snow depths
- ✅ Work on desktop and mobile
- ✅ Be publicly accessible via GitHub Pages

**Your live map URL will be:**
`https://YOUR_GITHUB_USERNAME.github.io/california-snow-conditions/`

---

## 📞 Ready to Start?

1. Open `SETUP_GUIDE.md`
2. Start with Phase 2: Google Cloud Setup
3. Follow each step carefully
4. Check off items in the checklist above

**Good luck! 🏔️⛷️**

*Estimated total setup time: 1-2 hours*

