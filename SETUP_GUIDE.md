# California Snow Conditions - Complete Setup Guide

This guide walks you through setting up the California Snow Conditions project from scratch.

---

## Phase 1: Account Setup

### 1.1 Create New Google Account

**Why:** Separate account for California project credentials

1. Go to https://accounts.google.com/signup
2. Create new Google account (e.g., `california.snow.data@gmail.com`)
3. Complete verification
4. Save credentials securely

### 1.2 Create New GitHub Account

**Why:** Separate GitHub account for hosting California project

1. Go to https://github.com/signup
2. Create new account (e.g., `ca-snow-conditions`)
3. Verify email
4. Save credentials

---

## Phase 2: Google Cloud Setup

### 2.1 Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Sign in with your NEW Google account
3. Click "Create Project"
   - Name: `California Snow Conditions`
   - Leave organization blank
   - Click "Create"
4. Wait for project creation (30 seconds)

### 2.2 Enable Google Sheets API

1. In Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click "Google Sheets API"
4. Click "Enable"
5. Wait for activation

### 2.3 Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "+ Create Credentials" → "Service Account"
3. Service account details:
   - Name: `california-snow-updater`
   - ID: (auto-generated)
   - Description: `Automated service for updating California ski resort data`
4. Click "Create and Continue"
5. Grant access: Skip (click "Continue")
6. Done (click "Done")

### 2.4 Generate Service Account Key

1. Go to "APIs & Services" → "Credentials"
2. Find your service account in the list
3. Click on the service account name
4. Go to "Keys" tab
5. Click "Add Key" → "Create New Key"
6. Choose "JSON"
7. Click "Create"
8. JSON file will download automatically
9. **IMPORTANT:** Save this file securely - you'll need it later

### 2.5 Copy Service Account Email

1. In the service account details, copy the email (looks like: `california-snow-updater@PROJECT_ID.iam.gserviceaccount.com`)
2. Save this email - you'll need it for Google Sheets sharing

---

## Phase 3: Google Sheets Setup

### 3.1 Create New Google Sheet

1. Go to https://sheets.google.com
2. Sign in with your NEW Google account
3. Click "+ Blank" to create new sheet
4. Name it: `California Ski Resort Conditions`

### 3.2 Share Sheet with Service Account

1. Click "Share" button (top-right)
2. Paste the service account email
3. Give it "Editor" access
4. Uncheck "Notify people"
5. Click "Share"

### 3.3 Get Sheet ID

1. Look at the URL in your browser
2. URL format: `https://docs.google.com/spreadsheets/d/SHEET_ID/edit`
3. Copy the `SHEET_ID` part (long string of letters/numbers)
4. Save this ID - you'll need it

**Example:**
```
URL: https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit
Sheet ID: 1a2b3c4d5e6f7g8h9i0j
```

### 3.4 Publish Sheet as CSV

1. File → Share → Publish to web
2. "Entire Document" dropdown
3. Select "Comma-separated values (.csv)"
4. Click "Publish"
5. Confirm the warning
6. Copy the published URL (looks like: `https://docs.google.com/spreadsheets/d/e/2PACX-.../pub?output=csv`)
7. Save this URL - you'll need it for `docs/config.js`

---

## Phase 4: Local Project Setup

### 4.1 Navigate to Project Directory

```bash
cd ~/california-snow-conditions
```

### 4.2 Create .env File

Create a file named `.env` in the project root:

```bash
# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_sheet_id_from_step_3.3
GOOGLE_CREDENTIALS='paste_entire_json_from_downloaded_file_step_2.4'

# Mapbox Token (can reuse from Colorado project or create new)
MAPBOX_TOKEN=your_mapbox_token_here
```

**IMPORTANT:** 
- The `GOOGLE_CREDENTIALS` value should be the ENTIRE JSON content from the downloaded service account key file
- Wrap it in single quotes
- All on one line

**Example:**
```bash
GOOGLE_CREDENTIALS='{"type":"service_account","project_id":"california-snow-123456","private_key_id":"abc123...","private_key":"-----BEGIN PRIVATE KEY-----\nMIIE...","client_email":"california-snow-updater@california-snow-123456.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/california-snow-updater%40california-snow-123456.iam.gserviceaccount.com"}'
```

### 4.3 Update Map Configuration

Edit `docs/config.js`:

1. Find the line: `const DATA_URL = 'YOUR_CALIFORNIA_GOOGLE_SHEET_CSV_URL_HERE';`
2. Replace with your published CSV URL from Step 3.4

**Example:**
```javascript
const DATA_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/pub?output=csv';
```

### 4.4 Install Python Dependencies

```bash
# Activate virtual environment (if not already active)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

---

## Phase 5: Testing

### 5.1 Test Scraper

```bash
python combined_scraper.py
```

**Expected output:**
- "Scraping OnTheSnow..."
- "Found X resorts"
- "Saved combined data to california_resorts_combined.csv"
- Check that CSV file was created

### 5.2 Test Google Sheets Upload

```bash
python google_sheets_updater.py
```

**Expected output:**
- "Uploading data to Google Sheets..."
- "Successfully updated Google Sheet"
- Check your Google Sheet - data should appear

### 5.3 Test Map Locally

1. Open `docs/index.html` in your browser
2. Check that map loads with California bounds
3. Verify region toggle buttons work
4. Check that markers appear (if sheet has data)

---

## Phase 6: GitHub Deployment

### 6.1 Create GitHub Repository

1. Sign in to your NEW GitHub account
2. Click "+" → "New repository"
3. Repository name: `california-snow-conditions`
4. Make it **Public**
5. Do NOT initialize with README (we have our own)
6. Click "Create repository"

### 6.2 Push Code to GitHub

```bash
# Add all files
git add .
git commit -m "Initial California snow conditions setup"

# Add remote (replace YOUR_USERNAME with your new GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/california-snow-conditions.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 6.3 Configure GitHub Secrets

1. Go to repository on GitHub
2. Click "Settings" tab
3. Go to "Secrets and variables" → "Actions"
4. Click "New repository secret" for each of these:

**Secret 1: GOOGLE_SHEETS_SPREADSHEET_ID**
- Name: `GOOGLE_SHEETS_SPREADSHEET_ID`
- Value: Your sheet ID from Step 3.3

**Secret 2: GOOGLE_CREDENTIALS**
- Name: `GOOGLE_CREDENTIALS`
- Value: Entire JSON from service account key file (Step 2.4)

**Secret 3: MAPBOX_TOKEN**
- Name: `MAPBOX_TOKEN`
- Value: Your Mapbox token

### 6.4 Enable GitHub Pages

1. Go to repository "Settings"
2. Scroll to "Pages" in left sidebar
3. Source: "Deploy from a branch"
4. Branch: `main`
5. Folder: `/docs`
6. Click "Save"
7. Wait 1-2 minutes for deployment

### 6.5 Get Your Live URL

After GitHub Pages deploys:
- Your map will be live at: `https://YOUR_USERNAME.github.io/california-snow-conditions/`
- Bookmark this URL!

---

## Phase 7: Verify Automation

### 7.1 Trigger Manual Workflow Run

1. Go to "Actions" tab in GitHub
2. Click "Update California Snow Conditions" workflow
3. Click "Run workflow" dropdown
4. Click "Run workflow" button
5. Wait for workflow to complete (~3-5 minutes)

### 7.2 Check Results

1. Go to your Google Sheet - verify data updated
2. Visit your live map URL - verify new data appears
3. Check workflow logs for any errors

### 7.3 Verify Automatic Schedule

The workflow will now run automatically every 2 hours:
- 12am, 2am, 4am, 6am, 8am, 10am, 12pm, 2pm, 4pm, 6pm, 8pm, 10pm (UTC)
- Check the "Actions" tab to see scheduled runs

---

## Troubleshooting

### "Authentication failed" error

**Problem:** Google Sheets API credentials not working

**Solution:**
1. Verify service account email has Editor access to sheet
2. Check that `GOOGLE_CREDENTIALS` secret is complete JSON
3. Ensure no extra spaces or line breaks in credentials

### "Sheet not found" error

**Problem:** Wrong spreadsheet ID

**Solution:**
1. Double-check sheet ID in `.env` and GitHub secrets
2. Verify sheet exists and is accessible
3. Make sure you used the sheet ID, not the CSV publish URL

### Map not loading data

**Problem:** CSV URL not configured

**Solution:**
1. Check `docs/config.js` has correct `DATA_URL`
2. Verify Google Sheet is published as CSV (Step 3.4)
3. Test CSV URL in browser - should download CSV file

### GitHub Actions failing

**Problem:** Missing secrets or permissions

**Solution:**
1. Verify all 3 secrets are set in GitHub
2. Check Actions logs for specific error
3. Ensure service account has Editor access to sheet

---

## Next Steps

Once everything is working:

1. **Monitor Data Quality:**
   - Check that resorts are being scraped correctly
   - Verify coordinates are accurate on map
   - Adjust resort metadata if needed

2. **Customize Region Bounds:**
   - Edit `docs/map.js` → `REGIONS` object
   - Adjust bounds to fit your preferred zoom levels

3. **Share Your Map:**
   - Share the GitHub Pages URL with friends/skiers
   - Consider adding to your portfolio
   - Submit to ski forums/communities

4. **Maintenance:**
   - Check GitHub Actions logs weekly
   - Update resort data if new resorts open
   - Monitor for scraping errors (OnTheSnow may change structure)

---

## Support

If you encounter issues:

1. Check log files (`.log` files in project root)
2. Review GitHub Actions logs
3. Verify all steps in this guide were completed
4. Test each component individually (scraper, sheets, map)

---

**Congratulations! Your California Snow Conditions map is now live! 🏔️**

