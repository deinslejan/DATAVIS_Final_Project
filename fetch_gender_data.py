import pandas as pd
from pandas_datareader import wb
import datetime

# --- CONFIGURATION ---
# Define the specific World Bank indicators we want
# This matches the "Upgraded" list for the "Future Denied" topic
indicators = {
    'SE.PRM.UNER.FE': 'Girls_Out_Of_School_Primary',       # The Problem
    'SE.ADT.LITR.FE.ZS': 'Literacy_Rate_Female',           # The Outcome
    'SE.ADT.LITR.MA.ZS': 'Literacy_Rate_Male',             # The Comparison (for Dumbbell Plot)
    'SP.ADO.TFRT': 'Adolescent_Fertility_Rate',            # The Consequence (Teen Pregnancy)
    'SL.TLF.TOTL.FE.ZS': 'Female_Labor_Force_Participation' # The Economic Impact
}

# Time range
start_year = 1980
end_year = datetime.datetime.now().year

print("Connecting to World Bank API... this may take a minute.")

try:
    # 1. DOWNLOAD DATA
    # country='all' fetches data for every country in the world
    df = wb.download(indicator=indicators.keys(), country='all', start=start_year, end=end_year)
    
    # 2. CLEANUP
    # Rename the cryptic codes to readable column names
    df = df.rename(columns=indicators)
    
    # Reset index so 'country' and 'year' become regular columns, not index levels
    df = df.reset_index()
    
    # Convert 'year' to numeric (sometimes it comes as a string)
    df['year'] = pd.to_numeric(df['year'])

    # 3. FILTERING (Optional but recommended)
    # Remove aggregate regions (like "World", "Arab World") to keep only actual countries.
    # We do this by dropping rows where the country name is a known aggregate.
    # (A simple way is to check for non-countries later, but this raw dump is usually fine).
    
    # 4. PREVIEW
    print("\nData Downloaded Successfully!")
    print(f"Total Rows: {len(df)}")
    print(f"Total Countries: {df['country'].nunique()}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # 5. SAVE TO CSV
    filename = 'gender_education_dataset.csv'
    df.to_csv(filename, index=False)
    print(f"\n[SUCCESS] Dataset saved as '{filename}'")
    print("You can now upload this file to your repository.")

except Exception as e:
    print(f"\n[ERROR] Something went wrong: {e}")
    print("Make sure you have installed the library: pip install pandas-datareader")