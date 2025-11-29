# California Snow Conditions

**Live interactive map showing real-time snow conditions for all California ski resorts**

🔗 **Live Map:** https://ew-sfex.github.io/california-snow-conditions/

---

## What It Does

Automatically scrapes snow conditions from OnTheSnow every 2 hours and displays them on an interactive map with 27+ California ski resorts.

### Features

- 🗺️ **Interactive Map** - Click any resort for detailed conditions
- 🏔️ **Region Toggles** - Quick zoom to North Tahoe, South Tahoe, Mammoth, or SoCal
- 🎨 **Visual Encoding** - Marker color shows % terrain open, size shows resort size
- 🔄 **Auto-Updates** - Fresh data every 2 hours via GitHub Actions
- 📱 **Mobile Friendly** - Works on any device
- 🆓 **Completely Free** - Open source, no API costs

### Data Tracked

For each resort:
- Current operating status (Open/Closed)
- 24-hour snowfall
- Base depth
- Trails open (e.g., 55/180)
- Lifts operating (e.g., 9/24)
- Last update timestamp

---

## California Regions

**Lake Tahoe:** Palisades Tahoe, Heavenly, Northstar, Kirkwood, Sugar Bowl, Alpine Meadows, Homewood, Sierra-at-Tahoe, and more

**Mammoth:** Mammoth Mountain, June Mountain

**Southern California:** Bear Mountain, Snow Summit, Mountain High, Snow Valley, Mt. Baldy

**Other:** Mt. Shasta, Bear Valley, China Peak, Dodge Ridge, and more

---

## How It Works

```
OnTheSnow → JSON Scraper → Google Sheets → Map (auto-refreshes)
     ↑                                              
GitHub Actions runs every 2 hours
```

1. **Scraper** fetches live data from OnTheSnow using JSON parsing
2. **Google Sheets** stores the data and publishes as CSV
3. **GitHub Pages** serves the interactive map
4. **GitHub Actions** automates updates every 2 hours

---

## Tech Stack

- **Frontend:** Mapbox GL JS, Vanilla JavaScript
- **Backend:** Python 3.11, Selenium, BeautifulSoup, Pandas
- **Data:** OnTheSnow (via JSON scraping)
- **Storage:** Google Sheets API
- **Hosting:** GitHub Pages
- **Automation:** GitHub Actions

---

## Development

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions.

**Quick local test:**
```bash
python combined_scraper.py    # Scrape data
python google_sheets_updater.py  # Upload to sheets
open docs/index.html           # View map locally
```
