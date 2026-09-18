import pandas as pd
import os
from django.conf import settings

# Build the absolute path to the CSV file (which sits next to manage.py)
BASE_DIR = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, 'fuel-prices-for-be-assessment.csv')

def load_fuel_data():
    """Loads the fuel CSV into a Pandas DataFrame for lightning-fast lookups."""
    try:
        df = pd.read_csv(CSV_PATH)
        # Ensure the 'Retail Price' column is purely numeric
        df['Retail Price'] = pd.to_numeric(df['Retail Price'], errors='coerce')
        # Drop rows where don't have a valid price or coordinates
        df = df.dropna(subset=['Retail Price', 'City', 'State'])
        print(f"Successfully loaded {len(df)} fuel stops into memory.")
        return df
    except Exception as e:
        print(f"Warning: Could not load fuel data. Error: {e}")
        return pd.DataFrame() # Return empty dataframe if file is missing

# Load the data once when server boots up
FUEL_DF = load_fuel_data()