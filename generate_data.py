import csv
import random
from faker import Faker
from datetime import date, timedelta

# --- SETTINGS ---
NUM_RECORDS = 1000
OUTPUT_FILE = 'bulk_assets.csv'
# ------------------

# Initialize Faker
fake = Faker()

# Define some pools of realistic data
ASSET_TYPES_POOL = ['Laptop', 'Desktop', 'Monitor', 'Printer', 'Server', 'Phone', 'Software License', 'Projector', 'Router']
LOCATIONS_POOL = ['Building A', 'Building B', 'Data Center 1', 'Remote (Home)', 'New York Office', 'London Office', 'Storage Room']

# Define the headers. These MUST match your import-export resource fields
HEADERS = [
    'asset_name', 
    'asset_code',
    'asset_type', 
    'location', 
    'manager', 
    'is_active', 
    'start_date', 
    'end_date',
    'parent'
]

print(f"Generating {NUM_RECORDS} records for '{OUTPUT_FILE}'...")

with open(OUTPUT_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write the header row
    writer.writerow(HEADERS)
    
    # Generate and write the data rows
    for i in range(NUM_RECORDS):
        
        # 1. Create realistic start_date
        start_date = fake.date_between(start_date='-5y', end_date='today')
        
        # 2. Decide if asset is active (90% chance of True)
        is_active = random.choices([True, False], weights=[0.9, 0.1], k=1)[0]
        
        # 3. Set end_date ONLY if inactive
        end_date_str = ''
        if not is_active:
            # Ensure end_date is after start_date
            end_date = fake.date_between(start_date=start_date, end_date='today')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
        # 4. Generate asset type and name
        asset_type = random.choice(ASSET_TYPES_POOL)
        asset_name = f"{fake.company()} {asset_type} {random.randint(100, 1000)}"
        
        # 5. Create a guaranteed unique asset_code
        # Formats as CODE-00001, CODE-00002, etc.
        asset_code = f"CODE-{i+1:05d}" 

        # 6. Assemble the row
        row = [
            asset_name,
            asset_code,
            asset_type,
            random.choice(LOCATIONS_POOL),
            fake.name(),  # Random manager name
            is_active,
            start_date.strftime('%Y-%m-%d'),
            end_date_str,
            ''
        ]
        
        # Write the row to the CSV
        writer.writerow(row)

print(f"Successfully created '{OUTPUT_FILE}' with {NUM_RECORDS} records.")