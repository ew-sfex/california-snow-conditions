# California Snow Conditions - Live Data Pipeline

🏔️ **Automated data visualization pipeline that updates live snow conditions for all California ski resorts**

This project automatically scrapes snow conditions from OnTheSnow, updates a Google Sheet, and powers an interactive map every 2 hours showing all 25+ California resorts with current conditions.

**Live Map Features:**
- Interactive map with all California ski resorts
- Color-coded markers showing terrain open percentage
- Region zoom toggles (All CA, North Tahoe, South Tahoe, Mammoth, SoCal)
- Real-time snow conditions and terrain status
- Auto-refresh every 5 minutes

---

## 🚀 Quick Start

### Prerequisites

You'll need:
- Python 3.11+
- New Google account (for Google Cloud & Sheets)
- New GitHub account (for hosting)
- Mapbox token (can reuse existing or create new)

### 1. Setup Google Cloud & Sheets

**Create Google Cloud Project:**
1. Go to https://console.cloud.google.com/
2. Create new project: "California Snow Conditions"
3. Enable Google Sheets API
4. Create service account: "california-snow-updater"
5. Generate and download JSON key file

**Create Google Sheet:**
1. Create new Google Sheet: "California Ski Resort Conditions"
2. Share with service account email (Editor access)
3. Note the Spreadsheet ID from URL
4. File → Share → Publish to web → CSV
5. Copy the published CSV URL

### 2. Configure Environment

Create `.env` file:

```bash
# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=your_california_sheet_id_here
GOOGLE_CREDENTIALS='{"type":"service_account","project_id":"...","private_key":"..."}'

# Mapbox (Optional - can reuse existing token)
MAPBOX_TOKEN=your_mapbox_token_here
```

### 3. Update Map Configuration

Edit `docs/config.js`:
- Update `DATA_URL` with your California Google Sheet CSV URL

### 4. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 5. Test Locally

```bash
# Test the scraper
python combined_scraper.py

# Check that california_resorts_combined.csv was created

# Test Google Sheets upload
python google_sheets_updater.py

# Verify data appears in your Google Sheet
```

### 6. Deploy to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .
git commit -m "Initial California snow conditions setup"

# Add remote (use your new GitHub account)
git remote add origin https://github.com/YOUR_NEW_ACCOUNT/california-snow-conditions.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 7. Configure GitHub Actions

**Add Secrets:**
Go to repository Settings → Secrets and variables → Actions

Add these secrets:
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_CREDENTIALS` (full JSON)
- `MAPBOX_TOKEN`

**Enable GitHub Pages:**
1. Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/docs`
4. Save

Your map will be live at: `https://YOUR_USERNAME.github.io/california-snow-conditions/`

---

## 📊 Data Coverage

### California Resorts (25+)

**Lake Tahoe Region:**
- North: Palisades Tahoe, Northstar, Sugar Bowl, Alpine Meadows, Homewood, Diamond Peak, Boreal, Soda Springs, Tahoe Donner, Donner Ski Ranch
- South: Heavenly, Kirkwood, Sierra-at-Tahoe

**Mammoth Lakes:**
- Mammoth Mountain, June Mountain

**Southern California:**
- Bear Mountain, Snow Summit, Mountain High (East, West, North), Snow Valley

**Other:**
- Bear Valley, China Peak, Dodge Ridge, Mt. Shasta

### Data Tracked Per Resort

- **Location**: Latitude/longitude for map display
- **Snow Conditions**: Base depth, 24h/48h snowfall, surface conditions
- **Terrain Status**: Trails open/total, Lifts open/total, Percentage open
- **Operating Status**: Open, Closed, or Limited operation
- **Last Updated**: Timestamp of last data fetch

---

## 🤖 Automated Updates

GitHub Actions runs every 2 hours during ski season:
- Scrapes OnTheSnow for latest conditions
- Updates Google Sheet with new data
- Map auto-refreshes to show latest conditions

**Manual Trigger:**
- Go to Actions tab → "Update California Snow Conditions" → Run workflow

---

## 🗺️ Region Toggle Feature

The map includes region-specific zoom buttons:

- **All CA**: Full California view
- **N. Tahoe**: North Lake Tahoe resorts (Palisades, Northstar, Sugar Bowl, etc.)
- **S. Tahoe**: South Lake Tahoe resorts (Heavenly, Kirkwood, Sierra-at-Tahoe)
- **Mammoth**: Mammoth Lakes area (Mammoth Mountain, June Mountain)
- **SoCal**: Southern California resorts (Bear, Summit, Mountain High)

Click any region button to quickly zoom to that area.

---

## 📁 Project Structure

```
california-snow-conditions/
├── onthesnow_scraper.py          # Scrapes OnTheSnow California
├── combined_scraper.py            # Combines data and adds coordinates
├── google_sheets_updater.py       # Updates Google Sheet
├── run_all_updates.py             # Master orchestration script
│
├── california_resort_metadata.csv # Resort coordinates and metadata
├── requirements.txt               # Python dependencies
├── .env                          # API keys (DO NOT COMMIT)
├── .gitignore                    # Git ignore rules
│
├── docs/                         # GitHub Pages website
│   ├── index.html                # Map HTML
│   ├── map.js                    # Map logic + region toggles
│   ├── config.js                 # Configuration (bounds, data URL)
│   └── style.css                 # Styling
│
└── .github/workflows/
    └── update-snow-data.yml      # GitHub Actions automation
```

---

## 🔧 Configuration & Customization

### Adjust Update Frequency

Edit `.github/workflows/update-snow-data.yml`:

```yaml
schedule:
  - cron: '0 */2 * * *'  # Every 2 hours
  # Change to:
  - cron: '0 */4 * * *'  # Every 4 hours
  - cron: '0 6,14,22 * * *'  # 3 times daily
```

### Customize Region Bounds

Edit `docs/map.js` → `REGIONS` object to adjust zoom areas.

### Add/Remove Resorts

Edit `combined_scraper.py` → `RESORT_DATA` dictionary.

---

## 🐛 Troubleshooting

### "API key not found" error
- Check `.env` file exists in project root
- Verify credentials are properly formatted

### Data not updating
1. Check GitHub Actions logs for errors
2. Verify Google Sheets API credentials
3. Test scraper locally: `python combined_scraper.py`

### Map not loading
1. Check browser console for errors
2. Verify `DATA_URL` in `docs/config.js` is correct
3. Ensure Google Sheet is published as CSV

---

## 📚 Tech Stack

- **Python 3.11+**: Core scripting language
- **Selenium + BeautifulSoup**: Web scraping
- **Pandas**: Data processing
- **Google Sheets API**: Data storage
- **Mapbox GL JS**: Interactive mapping
- **GitHub Actions**: Automated scheduling
- **GitHub Pages**: Free hosting

---

## 🎿 Credits

Based on the Colorado Snow Conditions project architecture.

Data provided by [OnTheSnow](https://www.onthesnow.com/california/skireport.html)

---

## 📝 License

This project is open source and available for anyone to use and modify.

---

**Happy skiing! 🏔️⛷️**

