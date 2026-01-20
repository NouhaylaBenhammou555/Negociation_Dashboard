#!/usr/bin/env python3
"""Extract salary records from Levels.fyi HTML tables."""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

levels_dir = Path('data/levels.fyi_pages')
all_records = []

def extract_from_table(filepath):
    """Extract salary data from MuiTable component."""
    records = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Find the table with the specific class
        table = soup.find('div', class_=re.compile('MuiTable-root'))
        
        if table:
            # Find all table rows
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                
                if len(cells) >= 3:  # Typical salary table has: Company, Title, Salary, etc.
                    row_text = [cell.get_text(strip=True) for cell in cells]
                    
                    # Look for salary values in the row
                    for cell_text in row_text:
                        # Check if this cell contains a salary ($XXX,XXX)
                        salary_match = re.search(r'\$?([\d,]+)', cell_text)
                        if salary_match:
                            try:
                                salary = int(salary_match.group(1).replace(',', ''))
                                if 40000 <= salary <= 500000:
                                    records.append({
                                        'raw_row': ' | '.join(row_text),
                                        'salary_median_cad': salary,
                                        'source': 'Levels.fyi',
                                        'country': 'Canada',
                                        'city': 'Canada'
                                    })
                                    break  # Move to next row
                            except ValueError:
                                pass
    
    return records

# Process all files
print("📊 Extracting salary records from Levels.fyi tables...\n")

file_list = sorted(os.listdir(levels_dir))
total = 0

for file in file_list:
    if file.endswith('.html'):
        filepath = levels_dir / file
        records = extract_from_table(filepath)
        print(f"✅ {file:<40} → {len(records):2d} records")
        all_records.extend(records)
        total += len(records)

print(f"\n{'='*60}")
print(f"✅ TOTAL EXTRACTED: {total} records")
print(f"   Expected: 67 (11×6 + 1)")
print(f"{'='*60}")

if all_records:
    # Save to CSV
    df = pd.DataFrame(all_records)
    output_path = Path('data/real_data/levelsfyi_67_records.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Saved: {output_path}")
    print(f"\nSample data:")
    print(df[['salary_median_cad', 'source']].head(15))
    print(f"\nSalary stats:")
    print(df['salary_median_cad'].describe())
