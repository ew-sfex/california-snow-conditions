#!/usr/bin/env python3
"""
Combined California Ski Resort Scraper
Uses OnTheSnow as primary source, supplements with California Ski Country for any missing resorts
Adds coordinates from known resort locations
"""

import pandas as pd
import logging
from datetime import datetime
from onthesnow_scraper import OnTheSnowScraper

# California resort coordinates and trail counts
# Data compiled from resort websites and OnTheSnow
RESORT_DATA = {
    'Alpine Meadows': {'lat': 39.1666, 'lng': -120.2242, 'total_trails': 100, 'total_lifts': 13, 'region': 'Tahoe North'},
    'Bear Mountain': {'lat': 34.2311, 'lng': -116.9097, 'total_trails': 27, 'total_lifts': 11, 'region': 'Southern California'},
    'Bear Valley': {'lat': 38.4933, 'lng': -120.0086, 'total_trails': 67, 'total_lifts': 9, 'region': 'Northern California'},
    'Boreal Mountain': {'lat': 39.3309, 'lng': -120.3500, 'total_trails': 33, 'total_lifts': 9, 'region': 'Tahoe North'},
    'China Peak': {'lat': 37.3036, 'lng': -119.1883, 'total_trails': 45, 'total_lifts': 11, 'region': 'Central California'},
    'Diamond Peak': {'lat': 39.2528, 'lng': -119.9133, 'total_trails': 30, 'total_lifts': 7, 'region': 'Tahoe North'},
    'Dodge Ridge': {'lat': 38.1961, 'lng': -120.0347, 'total_trails': 67, 'total_lifts': 12, 'region': 'Central California'},
    'Donner Ski Ranch': {'lat': 39.3169, 'lng': -120.3419, 'total_trails': 52, 'total_lifts': 6, 'region': 'Tahoe North'},
    'Heavenly': {'lat': 38.9350, 'lng': -119.9400, 'total_trails': 97, 'total_lifts': 28, 'region': 'Tahoe South'},
    'Homewood': {'lat': 39.0838, 'lng': -120.1669, 'total_trails': 64, 'total_lifts': 7, 'region': 'Tahoe North'},
    'June Mountain': {'lat': 37.7764, 'lng': -119.0778, 'total_trails': 35, 'total_lifts': 7, 'region': 'Mammoth'},
    'Kirkwood': {'lat': 38.6853, 'lng': -120.0658, 'total_trails': 86, 'total_lifts': 15, 'region': 'Tahoe South'},
    'Mammoth Mountain': {'lat': 37.6308, 'lng': -119.0325, 'total_trails': 175, 'total_lifts': 28, 'region': 'Mammoth'},
    'Mountain High East': {'lat': 34.3803, 'lng': -117.6856, 'total_trails': 25, 'total_lifts': 6, 'region': 'Southern California'},
    'Mountain High North': {'lat': 34.4243, 'lng': -117.6784, 'total_trails': 24, 'total_lifts': 5, 'region': 'Southern California'},
    'Mountain High West': {'lat': 34.4184, 'lng': -117.7025, 'total_trails': 21, 'total_lifts': 5, 'region': 'Southern California'},
    'Mt. Shasta': {'lat': 41.3592, 'lng': -122.2097, 'total_trails': 32, 'total_lifts': 3, 'region': 'Northern California'},
    'Northstar California': {'lat': 39.2735, 'lng': -120.1211, 'total_trails': 100, 'total_lifts': 20, 'region': 'Tahoe North'},
    'Palisades Tahoe': {'lat': 39.1969, 'lng': -120.2356, 'total_trails': 200, 'total_lifts': 30, 'region': 'Tahoe North'},
    'Sierra-at-Tahoe': {'lat': 38.7951, 'lng': -120.0829, 'total_trails': 46, 'total_lifts': 14, 'region': 'Tahoe South'},
    'Snow Summit': {'lat': 34.2322, 'lng': -116.8864, 'total_trails': 31, 'total_lifts': 12, 'region': 'Southern California'},
    'Snow Valley': {'lat': 34.2411, 'lng': -117.0383, 'total_trails': 28, 'total_lifts': 13, 'region': 'Southern California'},
    'Soda Springs': {'lat': 39.3195, 'lng': -120.3917, 'total_trails': 16, 'total_lifts': 5, 'region': 'Tahoe North'},
    'Sugar Bowl': {'lat': 39.3022, 'lng': -120.3464, 'total_trails': 103, 'total_lifts': 13, 'region': 'Tahoe North'},
    'Tahoe Donner': {'lat': 39.3225, 'lng': -120.3094, 'total_trails': 17, 'total_lifts': 4, 'region': 'Tahoe North'},
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("california_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def add_resort_data(df):
    """Add latitude, longitude, trail counts, and lift counts to resorts"""
    
    def find_resort_data(name):
        """Find complete resort data by name"""
        name_clean = name.strip().lower()
        
        # Try exact match first
        if name in RESORT_DATA:
            data = RESORT_DATA[name]
            return pd.Series([data['lat'], data['lng'], data['total_trails'], data['total_lifts']])
        
        # Try partial matching
        for resort_name, data in RESORT_DATA.items():
            if resort_name.lower() in name_clean or name_clean in resort_name.lower():
                return pd.Series([data['lat'], data['lng'], data['total_trails'], data['total_lifts']])
        
        # No match found
        logger.warning(f"⚠️ No resort data found for: {name}")
        return pd.Series([None, None, None, None])
    
    # Add coordinates and trail/lift totals
    df[['latitude', 'longitude', 'total_trails_manual', 'total_lifts_manual']] = df['name'].apply(find_resort_data)
    
    # Fill in missing total_trails and total_lifts from manual data
    df['total_trails'] = df['total_trails'].fillna(df['total_trails_manual'])
    df['total_lifts'] = df['total_lifts'].fillna(df['total_lifts_manual'])
    
    # Drop the temporary manual columns
    df = df.drop(columns=['total_trails_manual', 'total_lifts_manual'], errors='ignore')
    
    # Calculate percentages
    df['trails_open_pct'] = 0.0
    df['lifts_open_pct'] = 0.0
    
    # Calculate trails open percentage
    valid_trails = (df['total_trails'].notna()) & (df['total_trails'] > 0) & (df['open_trails'].notna())
    df.loc[valid_trails, 'trails_open_pct'] = (df.loc[valid_trails, 'open_trails'] / df.loc[valid_trails, 'total_trails'] * 100).round(1)
    
    # Calculate lifts open percentage
    valid_lifts = (df['total_lifts'].notna()) & (df['total_lifts'] > 0) & (df['open_lifts'].notna())
    df.loc[valid_lifts, 'lifts_open_pct'] = (df.loc[valid_lifts, 'open_lifts'] / df.loc[valid_lifts, 'total_lifts'] * 100).round(1)
    
    # Log resorts without coordinates
    missing = df[df['latitude'].isna()]
    if len(missing) > 0:
        logger.warning(f"Missing data for {len(missing)} resorts:")
        for name in missing['name']:
            logger.warning(f"  - {name}")
    else:
        logger.info(f"✅ Added complete data to all {len(df)} resorts")
    
    return df


def add_missing_major_resorts(df):
    """Add major resorts that aren't scraped yet but should appear on the map"""
    
    # Major resorts to always include (even if closed/not scraped)
    must_include = ['Palisades Tahoe', 'Mammoth Mountain', 'Heavenly', 'Northstar California']
    
    existing_names = df['name'].str.lower().tolist()
    existing_normalized = [name.replace(' ski area', '').replace(' resort', '').replace(' mountain', '').strip() 
                          for name in existing_names]
    
    missing_resorts = []
    
    for resort_name in must_include:
        # Check if resort is already in the data (by normalized name)
        resort_normalized = resort_name.lower()
        if not any(resort_normalized in existing for existing in existing_normalized):
            # Resort is missing - add it as placeholder
            if resort_name in RESORT_DATA:
                data = RESORT_DATA[resort_name]
                missing_resorts.append({
                    'name': resort_name,
                    'status': 'Closed',
                    'new_snow_24h': 0,
                    'new_snow_48h': 0,
                    'base_depth': 0,
                    'trails_open': '0/0',
                    'lifts_open': '0/0',
                    'data_fetched_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source': 'Manual Entry',
                    'open_lifts': 0,
                    'total_lifts': data['total_lifts'],
                    'open_trails': 0,
                    'total_trails': data['total_trails'],
                    'mid_mtn_depth': 0,
                    'surface_conditions': '',
                    'name_lower': resort_name.lower(),
                    'latitude': data['lat'],
                    'longitude': data['lng'],
                    'trails_open_pct': 0.0,
                    'lifts_open_pct': 0.0,
                })
                logger.info(f"  + Added placeholder for {resort_name} ({data['total_trails']} trails)")
    
    if missing_resorts:
        missing_df = pd.DataFrame(missing_resorts)
        df = pd.concat([df, missing_df], ignore_index=True)
        logger.info(f"✅ Added {len(missing_resorts)} missing major resorts")
    else:
        logger.info("✅ All major resorts already present")
    
    return df


def combine_resort_data():
    """
    Scrape California resort data from OnTheSnow
    """
    logger.info("="*70)
    logger.info("CALIFORNIA SCRAPER - OnTheSnow")
    logger.info("="*70)
    
    all_resorts = []
    
    # 1. Get OnTheSnow data (primary source)
    logger.info("\n📊 Step 1: Scraping OnTheSnow (primary source)...")
    try:
        ots_scraper = OnTheSnowScraper(headless=True)
        ots_df = ots_scraper.scrape()
        
        if not ots_df.empty:
            logger.info(f"✅ OnTheSnow: Found {len(ots_df)} resorts")
            all_resorts.append(ots_df)
            ots_resort_names = set(ots_df['name'].str.lower())
        else:
            logger.warning("⚠️ OnTheSnow returned no data")
            ots_resort_names = set()
            
    except Exception as e:
        logger.error(f"❌ OnTheSnow scraper failed: {e}")
        ots_resort_names = set()
    
    # Note: California doesn't have a centralized resort association website like Colorado
    # OnTheSnow is the primary and only source for California
    
    # 3. Combine all data
    if not all_resorts:
        logger.error("❌ No data from any source!")
        return pd.DataFrame()
    
    combined_df = pd.concat(all_resorts, ignore_index=True)
    
    # Remove duplicate resorts with better deduplication logic
    # Handle A-Basin appearing as both "Arapahoe Basin" and "Arapahoe Basin Ski Area"
    def normalize_name(name):
        """Normalize resort names for duplicate detection"""
        name = name.lower().strip()
        # Remove common suffixes
        name = name.replace(' ski area', '').replace(' ski resort', '')
        name = name.replace(' resort', '').replace(' mountain resort', '')
        name = name.replace(' mountain', '')
        return name
    
    combined_df['name_normalized'] = combined_df['name'].apply(normalize_name)
    
    # Remove duplicates, keeping OnTheSnow version (first occurrence)
    combined_df = combined_df.drop_duplicates(subset=['name_normalized'], keep='first')
    combined_df = combined_df.drop(columns=['name_normalized'])
    
    # 4. Add coordinates, trail counts, and calculate percentages
    logger.info("\n📍 Adding resort data (coordinates, trail counts, percentages)...")
    combined_df = add_resort_data(combined_df)
    
    # 5. Add missing major resorts (not yet scraped but should be shown)
    logger.info("\n➕ Checking for missing major resorts...")
    combined_df = add_missing_major_resorts(combined_df)
    
    # Sort by name
    combined_df = combined_df.sort_values('name').reset_index(drop=True)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("FINAL COMBINED RESULTS")
    logger.info("="*70)
    logger.info(f"Total unique resorts: {len(combined_df)}")
    logger.info(f"From OnTheSnow: {len(combined_df[combined_df['source'] == 'OnTheSnow'])}")
    logger.info(f"From CSCUSA: {len(combined_df[combined_df['source'] == 'CSCUSA'])}")
    
    return combined_df


def main():
    """Test the combined scraper"""
    df = combine_resort_data()
    
    if df.empty:
        logger.error("No data collected")
        return
    
    # Save combined data
    output_file = "california_resorts_combined.csv"
    df.to_csv(output_file, index=False)
    logger.info(f"\n✅ Saved combined data to {output_file}")
    
    # Display results
    print("\n" + "="*70)
    print("ALL CALIFORNIA RESORTS")
    print("="*70)
    for idx, row in df.iterrows():
        status_emoji = "🟢" if row['status'] == 'Open' else "🔴"
        source = f"({row['source']})"
        print(f"{idx+1:2d}. {status_emoji} {row['name']:30s} {source}")
    print("="*70)
    print(f"Total: {len(df)} resorts")


if __name__ == "__main__":
    main()

